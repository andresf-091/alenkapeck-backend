import pytest_asyncio
import subprocess
import os
from dotenv import load_dotenv
import time
import psutil


@pytest_asyncio.fixture(scope="session")
async def messenger_service():

    load_dotenv("services/messenger/.env.test", override=True)
    env = os.environ.copy()

    process = subprocess.Popen(
        ["go", "run", "app/main.go"],
        env=env,
        cwd="services/messenger",
    )
    time.sleep(5)

    yield process

    parent = psutil.Process(process.pid)
    for child in parent.children(recursive=True):
        child.kill()
    parent.kill()
