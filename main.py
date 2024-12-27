# start_uvicorn.py

import subprocess


def run_uvicorn():
    subprocess.run(
        [
            "uvicorn",
            "--factory",
            "app.configurations.app:create_app",
            "--reload",
            "--port",
            "3000",
        ]
    )


if __name__ == "__main__":
    run_uvicorn()
