## Services

### Users

**To run separately:**
```bash
cd services/users
uvicorn app.main:app --reload --port 8000
```

**To run tests:**
```bash
cd services/users
pytest tests/ -s -v
```

---

### Messenger

**To run separately:**
```bash
cd services/messenger
go mod tidy
go run app/main.go
```

**To run tests:**
```bash
cd services/messenger
go test ./...
```

---

## Userflow tests

### Users

After setup, go to [http://localhost:8000/graphql](http://localhost:8000/graphql)

- **Create a user:**
    ```graphql
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

- **Get a user:**
    ```graphql
    query {
      user(userId: "USER_ID") {
        id
        email
        username
        role
      }
    }
    ```

- **Update a user:**
    ```graphql
    mutation {
      updateUser(userId: "USER_ID", input: {email: "test2@gmail.com", username: "testuser2"}) {
        id
        email
        username
        role
      }
    }
    ```

- **Delete a user:**
    ```graphql
    mutation {
      deleteUser(userId: "USER_ID") {
        id
        email
        username
        role
      }
    }
    ```

---

### Messenger

After setup, use any WebSocket client to connect to:

```
ws://localhost:8080/ws
```
        