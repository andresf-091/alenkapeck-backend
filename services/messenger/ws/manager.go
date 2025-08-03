package ws

import (
	"context"
	"encoding/json"
	"log"
	"messenger/db"
	"sync"

	"github.com/google/uuid"
	"github.com/gorilla/websocket"
	"github.com/lib/pq"
)

type WSManager struct {
	ChatRepo    *db.ChatRepo
	MessageRepo *db.MessageRepo
	PublishFn   PublisherFunc

	userConns map[uuid.UUID][]*websocket.Conn
	mu        sync.Mutex
}

type PublisherFunc func(channel, message string)

type WSMessageInput struct {
	ChatID   uuid.UUID `json:"chat_id"`
	SenderID uuid.UUID `json:"sender_id"`
	Text     string    `json:"text"`
}

type WSMessageOutput struct {
	MessageID uuid.UUID `json:"message_id"`
	ChatID    uuid.UUID `json:"chat_id"`
	SenderID  uuid.UUID `json:"sender_id"`
	Text      string    `json:"text"`
}

type WSInitRequest struct {
	UserID  uuid.UUID `json:"user_id"`
	ChatID  uuid.UUID `json:"chat_id"`
	IsStart bool      `json:"is_start"`
}

func NewWSManager(chatRepo *db.ChatRepo, messageRepo *db.MessageRepo, pubFn PublisherFunc) *WSManager {
	return &WSManager{
		ChatRepo:    chatRepo,
		MessageRepo: messageRepo,
		PublishFn:   pubFn,
		userConns:   make(map[uuid.UUID][]*websocket.Conn),
	}
}

func (m *WSManager) addUserConn(chatID uuid.UUID, conn *websocket.Conn) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.userConns[chatID] = append(m.userConns[chatID], conn)
}

func (m *WSManager) removeUserConn(chatID uuid.UUID, conn *websocket.Conn) {
	m.mu.Lock()
	defer m.mu.Unlock()
	conns := m.userConns[chatID]
	for i, c := range conns {
		if c == conn {
			m.userConns[chatID] = append(conns[:i], conns[i+1:]...)
			break
		}
	}
	if len(m.userConns[chatID]) == 0 {
		delete(m.userConns, chatID)
	}
}

func (m *WSManager) readLoop(ctx context.Context, userID uuid.UUID, conn *websocket.Conn) {
	for {
		select {
		case <-ctx.Done():
			return
		default:
			var msg WSMessageInput
			if err := conn.ReadJSON(&msg); err != nil {
				if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway, websocket.CloseAbnormalClosure) {
					log.Println("WebSocket closed unexpectedly:", err)
					return
				}
				log.Println("read error:", err)
				return
			}

			persisted, err := m.MessageRepo.Create(ctx, &db.Message{
				ChatID:   msg.ChatID,
				SenderID: msg.SenderID,
				Text:     msg.Text,
			})
			if err != nil {
				log.Println("Failed to create message:", err)
				return
			}

			payload, _ := json.Marshal(persisted)
			m.PublishFn("chat_messages", string(payload))

			log.Printf("User %s sent message: %s\n", userID, msg.Text)
		}
	}
}

func (m *WSManager) HandleRedisMessage(channel, payload string) {
	var msg db.Message
	if err := json.Unmarshal([]byte(payload), &msg); err != nil {
		log.Println("Invalid Redis payload:", err)
		return
	}

	m.mu.Lock()
	defer m.mu.Unlock()
	for _, conn := range m.userConns[msg.ChatID] {
		wsMsg := WSMessageOutput{
			MessageID: msg.ID,
			ChatID:    msg.ChatID,
			SenderID:  msg.SenderID,
			Text:      msg.Text,
		}
		if err := conn.WriteJSON(wsMsg); err != nil {
			log.Println("Failed to write WS message:", err)
		}
	}
}

func (m *WSManager) HandleConnection(ctx context.Context, conn *websocket.Conn) {
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()
	defer conn.Close()

	go func() {
		<-ctx.Done()
		conn.Close()
	}()

	var initReq WSInitRequest
	if err := conn.ReadJSON(&initReq); err != nil {
		if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway, websocket.CloseAbnormalClosure) {
			log.Println("WebSocket closed unexpectedly:", err)
		} else {
			log.Println("Invalid init request:", err)
		}
		return
	}

	userID := initReq.UserID
	chatID := initReq.ChatID
	isStart := initReq.IsStart
	var chat *db.Chat
	if !isStart {
		var err error
		chat, err = m.ChatRepo.GetByID(ctx, chatID)
		if err != nil {
			log.Println("Failed to get chat:", err)
			return
		}

		if !contains(chat.UsersID, userID.String()) {
			log.Printf("User %s not in chat: %s", userID, chatID)
			return
		}
	} else {
		var err error
		// TODO: проверка, существует ли пользователь
		chat, err = m.ChatRepo.Create(ctx, &db.Chat{UsersID: pq.StringArray{userID.String(), (chatID).String()}})
		if err != nil {
			log.Println("Failed to create chat:", err)
			return
		}
	}

	m.addUserConn(chat.ID, conn)
	defer m.removeUserConn(chat.ID, conn)

	if err := conn.WriteJSON(map[string]string{
		"status":  "ok",
		"chat_id": chat.ID.String(),
	}); err != nil {
		log.Println("Failed to send init ACK:", err)
		return
	}

	log.Printf("User %s connected via WebSocket\n", userID)

	m.readLoop(ctx, userID, conn)
}
