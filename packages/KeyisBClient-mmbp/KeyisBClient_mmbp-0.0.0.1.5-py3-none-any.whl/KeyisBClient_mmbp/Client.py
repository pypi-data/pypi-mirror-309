





import os
import httpx
from KeyisBLogging import logging
from KeyisBClient import Exceptions
from KeyisBClient.models import Request, Response

class Client:
    def __init__(self):
        self.protocols = {
            'mmbp': {'versions': ['0.0.0.0.1']},
            'mmbps': {'versions': ['0.0.0.0.1']}
        }
        crt_path = os.path.join(os.path.dirname(__file__), 'gw_certs', 'v0.0.1.crt')
        self.__httpAsyncClient = httpx.AsyncClient(verify=crt_path, follow_redirects=True)
        self.__httpClient = httpx.Client(verify=crt_path, follow_redirects=True)
        

    async def requestAsync(self, request: Request) -> Response:
        if request.dnsObject.host() is None:
            logging.debug("No DNS record found")
            raise Exceptions.DNS.InvalidDNSError()
        
        request.url.hostname = request.dnsObject.host() # type: ignore
        request.url.scheme = request.dnsObject.protocolInfo()['connection_protocol']

        try:
            response = await self.__httpAsyncClient.request(
                method=request.method,
                url=request.url.getUrl(),
                content=request.content,
                data=request.data,
                files=request.files,
                json=request.json,
                params=request.params,
                headers=request.headers,
                cookies=request.cookies,
                auth=request.auth,
                follow_redirects=request.follow_redirects,
                timeout=request.timeout,
                extensions=request.extensions
            )
            return Response(
                    status_code=response.status_code,
                    headers=response.headers,
                    content=response.content,
                    text=response.text,
                    json=response.json(),
                    stream=response.aiter_bytes(),
                    request=request,
                    extensions=response.extensions,
                    history=None,
                    default_encoding=response.encoding or "utf-8"
                )
        except httpx.TimeoutException:
            logging.debug("HTTPS request timed out")
            raise Exceptions.ServerTimeoutError()
        except httpx.ConnectError:
            logging.debug("Failed to connect to server")
            raise Exceptions.ErrorConnection()
        except httpx.HTTPStatusError as e:
            logging.debug(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise Exceptions.InvalidServerResponseError(message=f"Некорректный ответ от сервера: {e.response.status_code}")
        except httpx.RequestError as e:
            logging.debug(f"HTTPS request failed: {e}")
            raise Exceptions.UnexpectedError(message=f"Неожиданная ошибка запроса HTTPS: {str(e)}")

    def requestSync(self, request: Request) -> Response:
        if request.dnsObject.host() is None:
            logging.debug("No DNS record found")
            raise Exceptions.DNS.InvalidDNSError()
        
        request.url.hostname = request.dnsObject.host() # type: ignore
        request.url.scheme = request.dnsObject.protocolInfo()['connection_protocol']

        try:
            
            response = self.__httpClient.request(
                method=request.method,
                url=request.url.getUrl(),
                content=request.content,
                data=request.data,
                files=request.files,
                json=request.json,
                params=request.params,
                headers=request.headers,
                cookies=request.cookies,
                auth=request.auth,
                follow_redirects=request.follow_redirects,
                timeout=request.timeout,
                extensions=request.extensions
            )
            return Response(
                status_code=response.status_code,
                headers=response.headers,
                content=response.content,
                text=response.text,
                json=response.json(),
                stream=response.aiter_bytes(),
                request=request,
                extensions=response.extensions,
                history=None,
                default_encoding=response.encoding or "utf-8"
            )
        except httpx.TimeoutException:
            logging.debug("HTTPS request timed out")
            raise Exceptions.ServerTimeoutError()
        except httpx.ConnectError:
            logging.debug("Failed to connect to server")
            raise Exceptions.ErrorConnection()
        except httpx.HTTPStatusError as e:
            logging.debug(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise Exceptions.InvalidServerResponseError(message=f"Некорректный ответ от сервера: {e.response.status_code}")
        except httpx.RequestError as e:
            logging.debug(f"HTTPS request failed: {e}")
            raise Exceptions.UnexpectedError(message=f"Неожиданная ошибка запроса HTTPS: {str(e)}")