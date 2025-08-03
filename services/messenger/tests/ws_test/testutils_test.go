package ws_test

import (
	"gorm.io/gorm"
)

func truncateTables(db *gorm.DB) error {
	if err := db.Exec("TRUNCATE messages, chats RESTART IDENTITY CASCADE").Error; err != nil {
		return err
	}
	return nil
}
