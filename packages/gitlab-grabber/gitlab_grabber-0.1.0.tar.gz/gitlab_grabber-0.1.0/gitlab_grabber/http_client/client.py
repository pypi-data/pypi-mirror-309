import ssl
import aiohttp
from typing import Dict, Any
from gitlab_grabber.logger import Logging
from gitlab_grabber.cli import GitlabConfig
from dataclasses import dataclass

logger = Logging(__name__)


@dataclass
class HTTPClient:
    """HTTP Client."""

    gitlab: GitlabConfig

    async def send_request(
        self,
        request_type: str,
        url: str,
        headers: Dict[str, str] = None,
        **extra_params: Any,
    ) -> aiohttp.ClientResponse | None:
        """Send request with retries."""
        timeout = aiohttp.ClientTimeout(total=self.gitlab.timeout)
        if self.gitlab.skip_verify:
            connector = aiohttp.TCPConnector(ssl=False)
        else:
            ssl_context = ssl.create_default_context()
            if self.gitlab.crt_path:
                ssl_context.load_verify_locations(cafile=self.gitlab.crt_path)
            connector = aiohttp.TCPConnector(ssl=ssl_context)

        async with aiohttp.ClientSession(
            headers=headers,
            timeout=timeout,
            connector=connector,
        ) as session:
            return await self._retry_request(
                session=session,
                request_type=request_type,
                url=url,
                **extra_params,
            )

    async def _retry_request(
        self,
        session: aiohttp.ClientSession,
        request_type: str,
        url: str,
        max_retries: int = 5,
        **extra_params: Any,
    ) -> aiohttp.ClientResponse | None:
        """Retries http request."""
        for attempt in range(max_retries):
            try:
                response = await self._make_request(
                    session=session,
                    request_type=request_type,
                    url=url,
                    **extra_params,
                )
                if response is not None and 200 <= response.status < 300:
                    return response
                else:
                    logger.error(
                        "Request error on %s. HTTP status: %s. Attempted %s from %s.",
                        url,
                        response.status if response else "Empty response",
                        attempt + 1,
                        max_retries,
                    )
            except aiohttp.ClientError as err:
                logger.error(
                    "Failed to execute a request for %s. Attempted %s from %s. Error: %s",
                    url,
                    attempt + 1,
                    max_retries,
                    err,
                )
        logger.error(
            "Failed to execute request for %s after %s attempts",
            url,
            max_retries,
        )
        return None

    @staticmethod
    async def _make_request(
        session: aiohttp.ClientSession,
        request_type: str,
        url: str,
        **extra_params: Any,
    ) -> aiohttp.ClientResponse | None:
        """Make http request."""
        method = {
            "GET": session.get,
            "POST": session.post,
            "PUT": session.put,
            "PATCH": session.patch,
        }.get(request_type.upper())

        if not method:
            logger.error("Unsupported request type: %s", request_type)
            return None

        request_params = {
            "url": url,
            "json": extra_params.get("json"),
            "data": extra_params.get("data"),
            "params": extra_params.get("params"),
        }
        request_params = {
            key: value for key, value in request_params.items() if value is not None
        }

        response = await method(**request_params)
        return response
