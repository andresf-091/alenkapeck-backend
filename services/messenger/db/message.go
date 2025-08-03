package db

import (
	"time"

	"github.com/google/uuid"
)

type Message struct {
	ID        uuid.UUID `gorm:"type:uuid;default:gen_random_uuid();primaryKey"`
	ChatID    uuid.UUID `gorm:"type:uuid;index;not null"`
	Chat      Chat      `gorm:"constraint:OnUpdate:CASCADE,OnDelete:CASCADE;"`
	SenderID  uuid.UUID `gorm:"type:uuid;index;not null"`
	Text      string    `gorm:"type:text;not null"`
	CreatedAt time.Time
	UpdatedAt time.Time
}
