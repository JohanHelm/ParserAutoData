from loguru import logger
from requests import Session
from requests.models import Response

from .params import RequestManagerParams
from .retry import RetryManager


class RequestsDownloader:
    def __init__(
        self, params: RequestManagerParams, retry_manager=RetryManager()
    ) -> None:
        self._session = Session()
        self._session.headers.update(params.headers)
        self._retry_manager: RetryManager = retry_manager
        self._retry_error = self._retry_manager.retry_error
        logger.info("init RequestsDownloader")

    def unsafe_get(self, url, params: RequestManagerParams) -> Response:
        responce: Response = self._session.get(url, timeout=params.timeout)
        return responce

    def safe_get(self, url, params: RequestManagerParams) -> Response | None:
        logger.info(f"Try get {url}")
        try:
            for attempt in self._retry_manager.make_retry():
                with attempt:
                    resp: Response = self.unsafe_get(url, params)
                    return resp
        except self._retry_error:
            logger.warning(f"out of retries with request to {url}")
