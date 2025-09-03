# Генерация Python
python -m grpc_tools.protoc `
    -Iservices/proto `
    --python_out=services/users/grpc `
    --grpc_python_out=services/users/grpc `
    services/proto/user/v1/user.proto

# Генерация Go
protoc -Iservices/proto `
    --go_out=services/messenger/grpc --go_opt=paths=source_relative `
    --go-grpc_out=services/messenger/grpc --go-grpc_opt=paths=source_relative `
    services/proto/user/v1/user.proto
