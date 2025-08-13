package db

import (
	"time"

	"github.com/google/uuid"
	"github.com/lib/pq"
)

type Chat struct {
	ID        uuid.UUID `gorm:"type:uuid;default:gen_random_uuid();primaryKey"`
	Chatname  string
	UsersID   pq.StringArray `gorm:"type:uuid[];not null"`
	Messages  []Message      `gorm:"foreignKey:ChatID;references:ID"`
	CreatedAt time.Time
	UpdatedAt time.Time
}
