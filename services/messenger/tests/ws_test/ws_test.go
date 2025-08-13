package ws_test

import (
	"testing"
	"time"

	"github.com/andresf-091/alenkapeck-backend/services/messenger/app/ws"

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

	require.NoError(t, conn.WriteJSON(ws.WSInitRequest{
		UserID:  uuid.New(),
		ChatID:  uuid.New(),
		IsStart: true,
	}))

	var initResponse ws.WSInitResponse
	require.NoError(t, conn.ReadJSON(&initResponse))

	require.Equal(t, "ok", initResponse.Status)
	require.NotEmpty(t, initResponse.ChatID)

	defer conn.Close()
}
