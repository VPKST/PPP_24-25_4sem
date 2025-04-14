from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.crypto import (
    huffman_encode, xor_encrypt, xor_decrypt, huffman_decode
)
import base64
import json

router = APIRouter()

@router.websocket("/ws/crypto")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            request = json.loads(data)

            action = request.get("action")
            text = request.get("text")
            key = request.get("key")

            if action == "encode":
                huff_data, codes, padding = huffman_encode(text)
                encrypted_data = xor_encrypt(huff_data, key)
                encoded_base64 = base64.b64encode(encrypted_data).decode()

                response = {
                    "encoded_data": encoded_base64,
                    "key": key,
                    "huffman_codes": codes,
                    "padding": padding
                }

            elif action == "decode":
                encrypted_data = base64.b64decode(request.get("encoded_data"))
                decrypted_data = xor_decrypt(encrypted_data, key)
                decoded_text = huffman_decode(
                    decrypted_data,
                    request.get("huffman_codes"),
                    request.get("padding")
                )

                response = {
                    "decoded_text": decoded_text
                }

            else:
                response = {"error": "Invalid action"}

            await websocket.send_text(json.dumps(response))

    except WebSocketDisconnect:
        print("Клиент отключился")
