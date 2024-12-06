import httpx
from lapidary.runtime import HttpxMiddleware


class MediaFixer(HttpxMiddleware[str]):
    async def handle_response(self, response: httpx.Response, request: httpx.Request, _: None) -> None:
        accept_arr = request.headers.get('Accept', '').split(',')
        if accept_arr:
            accept = accept_arr[0]

            actual_type = response.headers['Content-Type']
            if actual_type != accept and actual_type in accept:
                response.headers['Content-Type'] = accept
