package ws

import "github.com/google/uuid"

type WSMessageInput struct {
	ChatID uuid.UUID `json:"chat_id"`
	UserID uuid.UUID `json:"user_id"`
	Text   string    `json:"text"`
}

type WSMessageOutput struct {
	MessageID uuid.UUID `json:"message_id"`
	ChatID    uuid.UUID `json:"chat_id"`
	UserID    uuid.UUID `json:"user_id"`
	Text      string    `json:"text"`
}

type WSInitRequest struct {
	UserID  uuid.UUID `json:"user_id"`
	ChatID  uuid.UUID `json:"chat_id"`
	IsStart bool      `json:"is_start"`
}

type WSInitResponse struct {
	Status string    `json:"status"`
	ChatID uuid.UUID `json:"chat_id"`
}
