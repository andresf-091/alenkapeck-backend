PROTO_DIR=services/proto
PY_OUT=services/users/grpc
GO_OUT=services/messenger/grpc

PY_PROTOC=python -m grpc_tools.protoc
GO_PROTOC=protoc

proto:
	# Python
	$(PY_PROTOC) -I$(PROTO_DIR) \
		--python_out=$(PY_OUT) \
		--grpc_python_out=$(PY_OUT) \
		$(PROTO_DIR)/user/v1/user.proto

	# Go
	$(GO_PROTOC) -I$(PROTO_DIR) \
		--go_out=$(GO_OUT) --go-grpc_out=$(GO_OUT) \
		$(PROTO_DIR)/user/v1/user.proto
