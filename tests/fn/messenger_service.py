import pytest_asyncio
import subprocess
import os
from dotenv import load_dotenv
import time


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
    process.terminate()
    time.sleep(2)
