package db_test

import (
	"context"
	"testing"

	"messenger/db"

	"github.com/google/uuid"
	"github.com/lib/pq"
	"github.com/stretchr/testify/assert"
)

func TestMessageRepo_CRUD(t *testing.T) {
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

	message := &db.Message{
		ChatID: chat.ID,
		UserID: uuid.New(),
		Text:   "Test message",
	}

	message, err = messageRepo.Create(ctx, message)
	assert.NoError(t, err, "Message should be created without error")

	got, err := messageRepo.GetByID(ctx, message.ID)

	assert.NoError(t, err, "GetByID should return no error")
	assert.NotNil(t, got)
	assert.Equal(t, message.ID, got.ID)
	assert.Equal(t, message.Text, got.Text)
	assert.Equal(t, chat.ID, got.Chat.ID)

	messageUpdate := &db.Message{
		ID:     message.ID,
		ChatID: chat.ID,
		UserID: uuid.New(),
		Text:   "Updated message",
	}

	messageUpdate, err = messageRepo.Update(ctx, messageUpdate)
	assert.NoError(t, err, "Message should be updated without error")

	got, err = messageRepo.GetByID(ctx, messageUpdate.ID)

	assert.NoError(t, err, "GetByID should return no error")
	assert.NotNil(t, got)
	assert.Equal(t, message.ID, got.ID)
	assert.Equal(t, messageUpdate.ID, got.ID)
	assert.NotEqual(t, message.Text, got.Text)
	assert.Equal(t, messageUpdate.Text, got.Text)
	assert.Equal(t, chat.ID, got.Chat.ID)

	err = messageRepo.Delete(ctx, messageUpdate.ID)
	assert.NoError(t, err, "Message should be deleted without error")

	_, err = messageRepo.GetByID(ctx, messageUpdate.ID)
	assert.Error(t, err, "GetByID should return error")
}
