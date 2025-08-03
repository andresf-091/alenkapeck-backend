package db

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type MessageRepo struct {
	DB *gorm.DB
}

func NewMessageRepo(db *gorm.DB) *MessageRepo {
	return &MessageRepo{DB: db}
}

func (r *MessageRepo) GetByID(ctx context.Context, id uuid.UUID) (*Message, error) {
	var m Message
	if err := r.DB.WithContext(ctx).Preload("Chat").First(&m, id).Error; err != nil {
		return nil, err
	}
	return &m, nil
}

func (r *MessageRepo) Create(ctx context.Context, m *Message) (*Message, error) {
	if err := r.DB.WithContext(ctx).Preload("Chat").Create(m).Error; err != nil {
		return nil, err
	}
	return m, nil
}

func (r *MessageRepo) Update(ctx context.Context, m *Message) (*Message, error) {
	if err := r.DB.WithContext(ctx).Preload("Chat").Save(m).Error; err != nil {
		return nil, err
	}
	return m, nil
}

func (r *MessageRepo) Delete(ctx context.Context, id uuid.UUID) error {
	return r.DB.WithContext(ctx).Preload("Chat").Delete(&Message{}, id).Error
}
