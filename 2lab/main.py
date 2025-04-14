import sys
import os
import subprocess
import signal

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

def main():
    celery_cmd = [
        "celery", "-A", "app.core.celery_config.celery_app",
        "worker", "--loglevel=info", "--pool=solo"
    ]
    celery_proc = subprocess.Popen(
        celery_cmd,
        cwd=PROJECT_DIR
    )

    uvicorn_cmd = [
        "uvicorn", "app.main:app", "--host", "127.0.0.1",
        "--port", "8000", "--reload"
    ]
    uvicorn_proc = subprocess.Popen(
        uvicorn_cmd,
        cwd=PROJECT_DIR
    )

    def shutdown(signum, frame):
        celery_proc.terminate()
        uvicorn_proc.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    while True:
        pass

if __name__ == "__main__":
    main()
