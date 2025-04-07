import socket
import threading
import os
import json
import tempfile
import logging
from pydub import AudioSegment

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AUDIO_DIR = os.path.join(BASE_DIR, 'audio_files')
METADATA_FILE = os.path.join(BASE_DIR, 'metadata.json')

SERVER_HOST = 'localhost'
SERVER_PORT = 65432


def create_metadata():
    audio_files = []
    for file in os.listdir(AUDIO_DIR):
        if file.endswith('.mp3'):
            audio = AudioSegment.from_mp3(os.path.join(AUDIO_DIR, file))
            audio_files.append({
                'name': file,
                'duration_sec': len(audio) / 1000,
                'format': 'mp3'
            })
    with open(METADATA_FILE, 'w') as f:
        json.dump(audio_files, f, indent=4)
    logging.info('metadata файл создан.')


def handle_client(conn, addr):
    logging.info(f'Соединен c {addr}')
    try:
        request = conn.recv(1024).decode()
        if request == 'Список':
            with open(METADATA_FILE, 'r') as f:
                conn.send(f.read().encode())
        elif request.startswith('Отрезок аудиодорожки,'):
            _, file_name, start, end = request.split(',')
            start, end = int(float(start) * 1000), int(float(end) * 1000)
            audio = AudioSegment.from_mp3(os.path.join(AUDIO_DIR, file_name))
            audio_slice = audio[start:end]
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                audio_slice.export(tmp_file.name, format='mp3')
                with open(tmp_file.name, 'rb') as f:
                    conn.sendall(f.read())
            os.unlink(tmp_file.name)
    except Exception as e:
        logging.error(f'Ошибка: {e}')
    finally:
        conn.close()


def start_server():
    create_metadata()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen()
        logging.info(f'Сервер запускается в {SERVER_HOST}:{SERVER_PORT}')
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()


def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        action = input("Введите 'Список' или 'Отрезок аудиодорожки': ")
        if action == 'Список':
            s.send(action.encode())
            data = s.recv(4096).decode()
            print("Аудио файлы:", data)
        elif action == 'Отрезок аудиодорожки':
            file_name = input('Имя файла: ')
            start = input('Начальное время (сек): ')
            end = input('Конечное время (сек): ')
            request = f'Отрезок аудиодорожки,{file_name},{start},{end}'
            s.send(request.encode())
            with open('received_audio.mp3', 'wb') as f:
                while True:
                    data = s.recv(4096)
                    if not data:
                        break
                    f.write(data)
            logging.info('Аудио файл создан.')


def main():
    role = input("Запуск от имени (сервер/клиент): ")
    if role == 'сервер':
        start_server()
    elif role == 'клиент':
        client()


if __name__ == "__main__":
    main()
