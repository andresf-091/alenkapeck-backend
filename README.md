Services:
    users:
        to run separatly:
            1. cd services/users
            2. uvicorn app.main:app --reload --port 8000
        to run tests:
            1. cd services/users
            2. pytest tests/ -s -v

    messenger:
        to run separatly:
            1. cd services/messenger
            2. go mod tidy
            3. go run app/main.go
        to run tests:
            1. cd services/messenger
            2. go test ./...

Userflow tests:
    users:
        after setup go to http://localhost:8000/graphql
        run the following mutation to create a user:
        ```
        mutation {
        createUser(
            input: {email: "test1@gmail.com", username: "testuser1", password: "testpassword"}
        ) {
            id
            email
            username
            role
        }
        }
        ```
        run the following mutation to get a user:
        ```
        query {
            user(userId: "USER_ID") {
                id
                email
                username
                role
            }
        }
        ```
        run the following mutation to update a user:
        ```
        mutation {
            updateUser(userId: "USER_ID", input: {email: "test2@gmail.com", username: "testuser2"}) {
                id
                email
                username
                role
            }
        }
        ```
        run the following mutation to delete a user:
        ```
        mutation {
            deleteUser(userId: "USER_ID") {
                id
                email
                username
                role
            }
        }
        ```
    
    messenger: