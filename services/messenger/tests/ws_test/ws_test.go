package ws_test

import (
	"testing"
	"time"

	"github.com/google/uuid"
	"github.com/gorilla/websocket"
	"github.com/stretchr/testify/require"
)

func TestEndToEnd_WSConnection(t *testing.T) {
	dialer := websocket.Dialer{HandshakeTimeout: 5 * time.Second}
	conn, _, err := dialer.Dial(serverURL+"/", nil)
	require.NoError(t, err)
	defer conn.Close()
}

func TestEndToEnd_WSInitChat(t *testing.T) {
	dialer := websocket.Dialer{HandshakeTimeout: 5 * time.Second}
	conn, _, err := dialer.Dial(serverURL+"/", nil)
	require.NoError(t, err)

	initRequest := map[string]any{
		"user_id":  uuid.New().String(),
		"chat_id":  uuid.New().String(),
		"is_start": true,
	}
	require.NoError(t, conn.WriteJSON(initRequest))

	var initResponse struct {
		Status string    `json:"status"`
		ChatID uuid.UUID `json:"chat_id"`
	}
	require.NoError(t, conn.ReadJSON(initResponse))

	require.Equal(t, "ok", initResponse.Status)
	require.NotEmpty(t, initResponse.ChatID)

	defer conn.Close()
}
