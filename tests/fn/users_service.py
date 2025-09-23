import pytest_asyncio
import subprocess
import os
from dotenv import load_dotenv
import time


@pytest_asyncio.fixture(scope="session")
async def users_service():

    load_dotenv("services/users/.env.test", override=True)
    env = os.environ.copy()

    migration_process = subprocess.run(
        ["alembic", "upgrade", "head"],
        env=env,
        cwd="services/users",
    )
    time.sleep(2)

    process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--reload", "--port", "8000"],
        env=env,
        cwd="services/users",
    )
    time.sleep(5)

    yield process
    process.terminate()
    time.sleep(2)
