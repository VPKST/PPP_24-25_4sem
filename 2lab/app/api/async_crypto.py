from fastapi import APIRouter
from app.schemas.crypto import EncodeRequest, DecodeRequest
from app.services.crypto import encode_task, decode_task

router = APIRouter()

@router.post("/async-encode")
async def async_encode(request: EncodeRequest):
    task = encode_task.delay(request.text, request.key)
    return {"task_id": task.id}

@router.post("/async-decode")
async def async_decode(request: DecodeRequest):
    task = decode_task.delay(
        request.encoded_data,
        request.key,
        request.huffman_codes,
        request.padding
    )
    return {"task_id": task.id}

@router.get("/task-result/{task_id}")
async def get_task_result(task_id: str):
    from celery.result import AsyncResult
    task = AsyncResult(task_id)
    
    if task.ready():
        if task.successful():
            return {"status": "completed", "result": task.result}
        else:
            return {"status": "error", "result": str(task.result)}
    else:
        return {"status": "processing"}
