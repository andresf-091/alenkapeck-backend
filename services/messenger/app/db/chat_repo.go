package db

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type ChatRepo struct {
	DB *gorm.DB
}

func NewChatRepo(db *gorm.DB) *ChatRepo {
	return &ChatRepo{DB: db}
}

func (r *ChatRepo) GetByID(ctx context.Context, id uuid.UUID) (*Chat, error) {
	var c Chat
	if err := r.DB.WithContext(ctx).Preload("Messages").First(&c, id).Error; err != nil {
		return nil, err
	}
	return &c, nil
}

func (r *ChatRepo) Create(ctx context.Context, c *Chat) (*Chat, error) {
	if err := r.DB.WithContext(ctx).Preload("Messages").Create(c).Error; err != nil {
		return nil, err
	}
	return c, nil
}

func (r *ChatRepo) Update(ctx context.Context, c *Chat) (*Chat, error) {
	if err := r.DB.WithContext(ctx).Preload("Messages").Save(c).Error; err != nil {
		return nil, err
	}
	return c, nil
}

func (r *ChatRepo) Delete(ctx context.Context, id uuid.UUID) error {
	return r.DB.WithContext(ctx).Preload("Messages").Delete(&Chat{}, id).Error
}
