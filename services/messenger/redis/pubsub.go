package redis

import (
	"context"
	"log"

	"github.com/redis/go-redis/v9"
)

var ctx = context.Background()
var rdb *redis.Client

// InitRedis устанавливает соединение с Redis
func InitRedis() {
	rdb = redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
		DB:   0,
	})

	if err := rdb.Ping(ctx).Err(); err != nil {
		log.Fatalf("Failed to connect to Redis: %v", err)
	}
	log.Println("Connected to Redis")
}

// Publish отправляет сообщение в указанный канал
func Publish(channel, message string) {
	if err := rdb.Publish(ctx, channel, message).Err(); err != nil {
		log.Println("Redis publish error:", err)
	}
}

// Subscribe подписывается на каналы и вызывает callback для каждого сообщения
func Subscribe(callback func(channel, payload string), channels ...string) {
	pubsub := rdb.Subscribe(ctx, channels...)
	ch := pubsub.Channel()

	for msg := range ch {
		callback(msg.Channel, msg.Payload)
	}
}
