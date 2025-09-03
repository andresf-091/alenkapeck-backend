Services:
    user:
        to run separatly:
            1. cd services/messenger
            2. uvicorn app.main:app --reload --port 8000

    messenger:
        to run separatly:
            1. cd services/messenger
            2. go mod tidy
            3. go run app/main.go