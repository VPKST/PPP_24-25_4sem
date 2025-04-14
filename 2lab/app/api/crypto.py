from fastapi import APIRouter
from app.schemas.crypto import EncodeRequest, EncodeResponse, DecodeRequest, DecodeResponse
from app.services.crypto import huffman_encode, huffman_decode, xor_encrypt, xor_decrypt
import base64

router = APIRouter()

@router.post("/encode", response_model=EncodeResponse)
async def encode(data: EncodeRequest):
    huff_data, codes, padding = huffman_encode(data.text)
    encrypted_data = xor_encrypt(huff_data, data.key)
    encoded_base64 = base64.b64encode(encrypted_data).decode()
    return EncodeResponse(
        encoded_data=encoded_base64,
        key=data.key,
        huffman_codes=codes,
        padding=padding
    )

@router.post("/decode", response_model=DecodeResponse)
async def decode(data: DecodeRequest):
    encrypted_data = base64.b64decode(data.encoded_data)
    decrypted_data = xor_decrypt(encrypted_data, data.key)
    decoded_text = huffman_decode(decrypted_data, data.huffman_codes, data.padding)
    return DecodeResponse(decoded_text=decoded_text)
