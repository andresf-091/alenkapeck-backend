package main

import (
	"log"
	"net/http"

	"messenger/db"
	"messenger/redis"
	"messenger/ws"

	"github.com/joho/godotenv"
)

func init() {
	godotenv.Load()
}

func main() {
	db.CreateDatabaseIfNotExists()
	db.InitDB()
	redis.InitRedis()

	chatRepo := db.NewChatRepo(db.DB)
	messageRepo := db.NewMessageRepo(db.DB)

	wsManager := ws.NewWSManager(chatRepo, messageRepo, redis.Publish)

	go func() {
		// передаём callback, который каждый полученный из Redis payload разошлёт в WS
		redis.Subscribe(wsManager.HandleRedisMessage, "chat_messages")
	}()

	http.HandleFunc("/ws", ws.NewWebSocketHandler(wsManager))
	log.Println("Server listening on ws://localhost:8080/ws")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
