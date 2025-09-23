from .user.v1 import user_pb2_grpc, user_pb2
import grpc
import uuid
from ..database import get_db
from ..models import User


class UserService(user_pb2_grpc.UserServiceServicer):
    async def GetUser(self, request, context):
        try:
            user_uuid = uuid.UUID(request.id)
        except (ValueError, TypeError) as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid user ID format: {e}")
            return user_pb2.GetUserResponse()

        async with get_db() as session:
            user = await session.get(User, user_uuid)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.GetUserResponse()

            return user_pb2.GetUserResponse(
                id=str(user.id),
                email=user.email,
                username=user.username,
                role=user.role,
            )


async def serve_grpc():
    server = grpc.aio.server()
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("127.0.0.1:50051")
    await server.start()
    print("gRPC сервер запущен на порту 50051")
    await server.wait_for_termination()
