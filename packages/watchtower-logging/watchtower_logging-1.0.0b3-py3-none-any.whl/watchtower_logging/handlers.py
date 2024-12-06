import logging
from logging.handlers import QueueListener
import hashlib
import datetime
import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Dict, Any, Optional
from watchtower_logging import config
from watchtower_logging.version import __version__


class WatchtowerHandler(logging.Handler):

    '''
    A logging handler that sends logs to a Watchtower endpoint
    '''

    def __init__(self, 
                 beam_id: str,
                 host: str,
                 token: Optional[str] = None,
                 protocol: str = 'https', 
                 retry_count: int = config.DEFAULT_RETRY_COUNT,
                 backoff_factor: int = config.DEFAULT_BACKOFF_FACTOR,
                 use_fallback: bool = True,
                 fallback_host: Optional[str] = None,
                 debug: bool = False,
                 http_timeout: int = config.DEFAULT_HTTP_TIMEOUT) -> None:

        super().__init__()

        self.beam_id = beam_id
        self.host = host
        self.token = token
        self.protocol = protocol
        self.http_timeout = http_timeout
        self.retry_count = retry_count
        self.backoff_factor = backoff_factor

        self.use_fallback = use_fallback
        self.fallback_host = fallback_host or 'fallback.' + self.host

        # prevent infinite recursion by silencing requests and urllib3 loggers
        logging.getLogger('requests').propagate = False
        logging.getLogger('urllib3').propagate = False

        # and do the same for ourselves
        logging.getLogger(__name__).propagate = False

        self.session = self._setup_session()

    def formatTime(self, record, datefmt=None):

        ct = datetime.datetime.fromtimestamp(record.created, tz=datetime.timezone.utc)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S%z")
            s = "%s,%03d" % (t, record.msecs)
        return s

    def build_frame_info(self,
                         record: logging.LogRecord) -> Dict[str, Any]:
        
        return {
            'filename': record.pathname,
            'lineno': record.lineno,
            'function': record.funcName
        }
    
    def generate_dedup_id(self,
                        payload: dict) -> str:
    
        '''
        Method to generate a deduplication id for a log message
        '''

        data = payload.get('data', {})

        # If dedup_keys are specified, use them to filter extra data for generating the dedup ID
        if not self.dedup_keys is None and isinstance(self.dedup_keys, (list, tuple, set)):
            
            dedup_data = {k:v for k,v in payload.items() if k in self.dedup_keys and k != 'data'}
            if data:
                dedup_data['data'] = {k: v for k, v in data.items() if k in self.dedup_keys}
            
        else:
            # Otherwise, include all extra data and add the message
            dedup_data = payload

        return hashlib.md5(json.dumps(dedup_data,
                                    sort_keys=True,
                                    indent=None,
                                    separators=(',',':')).encode('utf-8')).hexdigest()

    def build_payload(self,
                      record: logging.LogRecord) -> dict:
        
        if not hasattr(record, 'asctime'):
            record.asctime = self.formatTime(record, "%Y-%m-%dT%H:%M:%S.%f%z")

        payload = {
            'asctime': record.asctime,
            'name': record.name,
            'levelname': record.levelname,
            'message': record.getMessage(),
            'dev': record.dev,
            'taskName': record.taskName,
            'execution_id': record.execution_id,
            'beam_id': self.beam_id,
            'frame__': self.build_frame_info(record)}
        
        if hasattr(record, 'env') and record.env:
            payload['env__'] = record.env

        if hasattr(record, 'levelno'):
            payload['severity'] = int(record.levelno)

        data = {k:v for k,v in record.__dict__.items() if not k in payload
                and not k in ('msg','args','levelno','pathname','filename','module','exc_info',
                              'exc_text', 'stack_info', 'lineno', 'funcName', 'created', 'msecs', 
                              'relativeCreated', 'thread', 'threadName', 'processName', 'process', 
                              'data', 'env')}

        if hasattr(record, 'data') and record.data:
            data = {**data, **record.data}
        else:
            record.data = {}

        payload['data'] = data

        dedup_id = self.generate_dedup_id(payload)
        record.dedup_id = dedup_id
        payload['dedup_id'] = dedup_id

        return payload
    
    def build_params(self,
                     record: logging.LogRecord) -> dict:
        
        return {
            'lvl': record.levelname,
            'exec_id': record.execution_id,
            'dedup': record.dedup_id,
            't': record.asctime }

    def prepareRecord(self,
                      record: logging.LogRecord) -> logging.LogRecord:
        
        record.payload = self.build_payload(record)
        record.params = self.build_params(record)

        return record

    def write_log(self,
                  log_message: str):

        print('[WatchTowerHandler] ' + log_message)

    def write_debug_log(self,
                        log_message: str):

        if self.debug:
            print('[WatchTowerHandler DEBUG] ' + log_message)
        
    def _setup_session(self) -> requests.Session:

        # Set up a requests session with retry logic
        
        session = requests.Session()
        retries = Retry(total=self.retry_count, backoff_factor=self.backoff_factor, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        return session

    def handle(self, 
               record) -> logging.LogRecord | bool:
        
        record = self.prepareRecord(record)
        return super().handle(record)

    def emit(self,
             record: logging.LogRecord) -> None:
        
        try:
            # Send the log entry to the HTTP endpoint
            self.send_log(payload=record.payload, params=record.params)
        except Exception as e:
            print(f"Failed to send log entry: {e}")

    def send_log(self, 
                 payload: Dict[str, Any],
                 params: Dict[str, Any]) -> None:

        headers = {'User-Agent': self.user_agent}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'

        try:

            response = self.session.post(self.url, json=payload, headers=headers, params=params, timeout=self.http_timeout)
            response.raise_for_status()

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:

            if self.use_fallback:
                self._send_fallback(payload, headers)
            else:
                raise e
            
        except requests.exceptions.HTTPError as e:

            if response.status_code >= 500 and self.use_fallback:
                self._send_fallback(payload, headers)
            else:
                raise e
            
    def _send_fallback(self, 
                       payload: Dict[str, Any], 
                       headers: Dict[str, str]) -> None:

        response = self.session.post(self.fallback_url, json=payload, headers=headers, timeout=self.http_timeout)
        response.raise_for_status()

    def build_endpoint(self, 
                       host: str) -> str:
        
        return f'{self.protocol}://{host}/api/beams/{self.beam_id}'
    
    @property
    def user_agent(self):
        
        return config.USER_AGENT_STR_FMT.format(version=__version__)

    @property
    def url(self) -> str:
        
        return self.build_endpoint(host=self.host)
    
    @property
    def fallback_url(self) -> str:

        return self.build_endpoint(host=self.fallback_host)
    

class CustomQueueListener(QueueListener):

    def stop(self, timeout=None):
        """
        Stop the listener.

        This asks the thread to terminate, and then waits for it to do so.
        Note that if you don't call this before your application exits, there
        may be some records still left on the queue, which won't be processed.
        """
        if self._thread:  # see gh-114706 - allow calling this more than once
            self.enqueue_sentinel()
            self._thread.join(timeout)  # Wait for the thread to finish
            self._thread = None