package grpc

import (
	"context"
	"google.golang.org/grpc"
	"github.com/andresf-091/alenkapeck-backend/services/messenger/grpc/user/v1"
)

type UserClient struct {
	client user.UserServiceClient
}

func NewUserClient(address string) (*UserClient, error) {
	conn, err := grpc.Dial(address, grpc.WithInsecure())
	if err != nil {
		return nil, err
	}

	return &UserClient{
		client: user.NewUserServiceClient(conn),
	}, nil
}

func (c *UserClient) GetUser(ctx context.Context, userID string) (*user.GetUserResponse, error) {
	return c.client.GetUser(ctx, &user.GetUserRequest{Id: userID})
}