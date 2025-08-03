package ws_test

import (
	"testing"
	"time"

	"github.com/gorilla/websocket"
	"github.com/stretchr/testify/require"
)

func TestEndToEnd_WSConnection(t *testing.T) {
	dialer := websocket.Dialer{HandshakeTimeout: 5 * time.Second}
	conn, _, err := dialer.Dial(serverURL+"/", nil)
	require.NoError(t, err)
	defer conn.Close()
}
