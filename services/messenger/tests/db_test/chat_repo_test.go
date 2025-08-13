package db_test

import (
	"context"
	"testing"

	"github.com/andresf-091/alenkapeck-backend/services/messenger/app/db"

	"github.com/google/uuid"
	"github.com/lib/pq"
	"github.com/stretchr/testify/assert"
)

func TestChatRepo_CRUD(t *testing.T) {
	ctx := context.Background()

	err := truncateTables(testDB)
	assert.NoError(t, err, "Failed to truncate tables")

	chat := &db.Chat{
		Chatname: "Test Chat",
		UsersID: pq.StringArray{
			uuid.New().String(),
			uuid.New().String(),
		},
	}

	chat, err = chatRepo.Create(ctx, chat)
	assert.NoError(t, err, "Chat should be created without error")

	got, err := chatRepo.GetByID(ctx, chat.ID)

	assert.NoError(t, err, "GetByID should return no error")
	assert.NotNil(t, got)
	assert.Equal(t, chat.ID, got.ID)
	assert.Equal(t, "Test Chat", got.Chatname)

	chatUpdate := &db.Chat{
		ID:       chat.ID,
		Chatname: "Updated Chat",
		UsersID: pq.StringArray{
			uuid.New().String(),
			uuid.New().String(),
		},
	}

	chatUpdate, err = chatRepo.Update(ctx, chatUpdate)
	assert.NoError(t, err, "Chat should be updated without error")

	got, err = chatRepo.GetByID(ctx, chatUpdate.ID)

	assert.NoError(t, err, "GetByID should return no error")
	assert.NotNil(t, got)
	assert.Equal(t, chat.ID, got.ID)
	assert.Equal(t, chatUpdate.ID, got.ID)
	assert.NotEqual(t, chat.Chatname, got.Chatname)
	assert.NotEqual(t, chat.UsersID, got.UsersID)
	assert.Equal(t, "Updated Chat", got.Chatname)

}
