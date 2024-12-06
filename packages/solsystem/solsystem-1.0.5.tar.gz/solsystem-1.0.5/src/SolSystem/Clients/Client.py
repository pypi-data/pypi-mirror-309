from __future__ import annotations
import time
import json
import httpx
import asyncio
from typing import Self
from pydantic import HttpUrl
from types import TracebackType
from termcolor import cprint, colored
from SolSystem.Models.Common import Method, Response, MethodAPICost


type Seconds = float


class AsyncClient:
    _retry_curve: list[float] = [3.0, 5.0, 10.0, 30.0, 60.0]


    def __init__(
            self,
            rpc_endpoint: HttpUrl,
            global_headers: dict[str,str] | None = None,
            timeout: float = 10,
            used_api_cedits: int = 0,
            limit_api_credits: int = 500_000,
        ):
        """### Summary
        Solana Async Client.
        
        ### Parameters
        `rpc_endpoint:` URL to the RPC endpoint.

        `global_headers:` Headers to use for every subsequent request in this
        session.

        `timeout:` Default request timeout.
        
        `used_api_cedits` The number of api credits already used by your account
        
        `limit_api_credits` The maximum api credits to use. You may set this to
        the account limit, or use your own limit to prevent runaway querying. Set
        to -1 to disable the limit."""
        self.base_rpc_url = rpc_endpoint
        self.current_api_credits = used_api_cedits
        self.limit_api_credits = limit_api_credits

        self.global_headers = {"Content-Type": "application/json"}
        if global_headers is not None:
            self.global_headers = {** self.global_headers, ** global_headers}

        self.session: httpx.AsyncClient = httpx.AsyncClient(timeout = timeout)

    

    async def request[T: Response](self, method: Method[T]) -> T:        
        if self.limit_api_credits == -1:
            method_cost = MethodAPICost[method.metadata.method]
            api_credits = self.current_api_credits + method_cost
            if api_credits > self.limit_api_credits:
                raise RuntimeError("Exceed API credit usage")
            self.current_api_credits = api_credits
        
        response = None
        for sleep_time in self._retry_curve:
            response = await self.session.post(
                url = str(self.base_rpc_url),
                json = method.model_dump(),
                headers = self.global_headers,
            )
            if response.status_code == httpx.codes.TOO_MANY_REQUESTS:
                await asyncio.sleep(sleep_time)
                continue
            
            if response.status_code != httpx.codes.OK:
                raise RuntimeError(F"Request failed with: {response.text}")
            break
                
        assert response, colored("Response cannot be null.")
        if response.status_code == httpx.codes.TOO_MANY_REQUESTS:
            raise RuntimeError(
                "Exceeded acceptable retries and request still failed."
            )

        response = method.response_type(**response.json())
        if response.id != method.metadata.id:
            raise RuntimeError("Invalid id")
        return response

    
    async def __aenter__(self) -> AsyncClient:
        await self.session.__aenter__()
        return self
    

    async def __aexit__(self, _exception_type, _exception, _exception_traceback):
        await self.session.aclose()



class SyncClient:
    _retry_curve: list[float] = [3.0, 5.0, 10.0, 30.0, 60.0]


    def __init__(
            self,
            rpc_endpoint: HttpUrl,
            global_headers: dict[str,str] | None = None,
            timeout: float = 10,
            used_api_cedits: int = 0,
            limit_api_credits: int = 500_000,
        ):
        """### Summary
        Solana Async Client.
        
        ### Parameters
        `rpc_endpoint:` URL to the RPC endpoint.

        `global_headers:` Headers to use for every subsequent request in this
        session.

        `timeout:` Default request timeout.
        
        `used_api_cedits` The number of api credits already used by your account
        
        `limit_api_credits` The maximum api credits to use. You may set this to
        the account limit, or use your own limit to prevent runaway querying."""
        self.base_rpc_url = rpc_endpoint
        self.current_api_credits = used_api_cedits
        self.limit_api_credits = limit_api_credits
        
        self.global_headers = {"Content-Type": "application/json"}
        if global_headers is not None:
            self.global_headers = {** self.global_headers, ** global_headers}

        self.session: httpx.Client = httpx.Client(timeout = timeout)


    def request[T: Response](self, method: Method[T]) -> T:
        if self.limit_api_credits == -1:
            method_cost = MethodAPICost[method.metadata.method]
            api_credits = self.current_api_credits + method_cost
            if api_credits > self.limit_api_credits:
                raise RuntimeError("Exceed API credit usage")
            self.current_api_credits = api_credits

        response = None
        for sleep_time in self._retry_curve:
            response = self.session.post(
                url = str(self.base_rpc_url),
                json = method.model_dump(),
                headers = self.global_headers,
            )
            if response.status_code == httpx.codes.TOO_MANY_REQUESTS:
                time.sleep(sleep_time)
                continue
            
            if response.status_code != httpx.codes.OK:
                raise RuntimeError(F"Request failed with: {response.text}")
            break
                
        assert response, colored("Response cannot be null.")
        if response.status_code == httpx.codes.TOO_MANY_REQUESTS:
            raise RuntimeError(
                "Exceeded acceptable retries and request still failed."
            )

        try:
            response = method.response_type(**response.json())
        except Exception:
            cprint(json.dumps(response.json(), indent = 2), "light_red")
            raise

        if response.id != method.metadata.id:
            raise RuntimeError("Invalid id")
        return response


    
    def __enter__(self) -> Self:
        self.session.__enter__()
        return self
    

    def __exit__(self, 
			_exception_type: type[BaseException] | None,
			_exception: BaseException | None,
			_traceback: TracebackType | None
		) -> None:
        self.session.close()


