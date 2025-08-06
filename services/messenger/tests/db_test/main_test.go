package db_test

import (
	"log"
	"os"
	"testing"

	"messenger/db"

	"github.com/joho/godotenv"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var (
	testDB      *gorm.DB
	chatRepo    *db.ChatRepo
	messageRepo *db.MessageRepo
)

func TestMain(m *testing.M) {
	err := godotenv.Load("../../.env.test")
	if err != nil {
		log.Fatalf("Error loading .env.test file: %v", err)
	}

	dsn := os.Getenv("DATABASE_URL")

	testDB, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatalf("Failed to connect to test database: %v", err)
	}

	err = testDB.Migrator().DropTable(&db.Chat{}, &db.Message{})
	if err != nil {
		log.Fatalf("Failed to drop table: %v", err)
	}
	err = testDB.AutoMigrate(&db.Chat{}, &db.Message{})
	if err != nil {
		log.Fatalf("Failed to migrate table: %v", err)
	}

	chatRepo = db.NewChatRepo(testDB)
	messageRepo = db.NewMessageRepo(testDB)

	err = truncateTables(testDB)
	if err != nil {
		log.Fatalf("Failed to truncate tables: %v", err)
	}

	code := m.Run()
	os.Exit(code)

	sqlDB, _ := testDB.DB()
	sqlDB.Close()
}
