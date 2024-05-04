from fastapi import Request
from fastapi.responses import StreamingResponse

from src.error.error_handler import handle_errors
from src.main.adapters.request_adapter import request_adapter
from src.main.composers.file_download_composer import file_download_composer


async def file_download(request: Request):
    try:
        http_response = await request_adapter(
            request, file_download_composer()
        )
    except Exception as exc:
        http_response = handle_errors(exc)
    return StreamingResponse(
        iter([http_response.body]),
        media_type='image/jpeg',
        headers={'Content-Disposition': 'attachment; filename=atleta-avatar'},
    )
