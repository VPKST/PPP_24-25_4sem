from app.core.celery_config import celery_app
import heapq
import base64
from collections import Counter
from typing import Dict

class Node:
    def __init__(self, freq, char, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    freq = Counter(text)
    heap = [Node(f, c) for c, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        heapq.heappush(heap, Node(left.freq + right.freq, None, left, right))

    return heap[0]

def generate_codes(node, prefix='', codebook=None):
    if codebook is None:
        codebook = {}

    if node.char:
        codebook[node.char] = prefix
    else:
        generate_codes(node.left, prefix + '0', codebook)
        generate_codes(node.right, prefix + '1', codebook)

    return codebook

def huffman_encode(text):
    tree = build_huffman_tree(text)
    codes = generate_codes(tree)
    encoded = ''.join(codes[c] for c in text)
    padding = 8 - len(encoded) % 8
    encoded += '0' * padding
    byte_array = bytearray(int(encoded[i:i+8], 2) for i in range(0, len(encoded), 8))
    return byte_array, codes, padding

def huffman_decode(byte_array, codes, padding):
    reversed_codes = {v: k for k, v in codes.items()}
    encoded = ''.join(f'{byte:08b}' for byte in byte_array)
    encoded = encoded[:-padding]

    current_code = ''
    decoded_text = ''
    for bit in encoded:
        current_code += bit
        if current_code in reversed_codes:
            decoded_text += reversed_codes[current_code]
            current_code = ''

    return decoded_text

def xor_encrypt(data: bytes, key: str) -> bytes:
    key_bytes = key.encode()
    return bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data))

xor_decrypt = xor_encrypt

from app.core.celery_config import celery_app

import logging

logger = logging.getLogger(__name__)

@celery_app.task
def encode_task(text, key):
    try:
        logger.info(f"Starting encoding for text: {text[:10]}...")
        huff_data, codes, padding = huffman_encode(text)
        encrypted_data = xor_encrypt(huff_data, key)
        encoded_base64 = base64.b64encode(encrypted_data).decode()
        logger.info("Encoding completed successfully")
        return {
            "encoded_data": encoded_base64,
            "key": key,
            "huffman_codes": codes,
            "padding": padding
        }
    except Exception as e:
        logger.error(f"Encoding failed: {str(e)}", exc_info=True)
        raise

@celery_app.task
def decode_task(encoded_data, key, huffman_codes, padding):
    try:
        encrypted_data = base64.b64decode(encoded_data)
        decrypted_data = xor_decrypt(encrypted_data, key)
        decoded_text = huffman_decode(decrypted_data, huffman_codes, padding)
        return {"decoded_text": decoded_text}
    except Exception as e:
        logger.error(f"Decoding error: {str(e)}", exc_info=True)
        raise
