package ws_test

import (
	"log"
	"messenger/db"
	"messenger/ws"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"

	"github.com/gorilla/websocket"
	"github.com/joho/godotenv"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var (
	testDB      *gorm.DB
	chatRepo    *db.ChatRepo
	messageRepo *db.MessageRepo
	wsManager   *ws.WSManager
	serverURL   string
)

func TestMain(m *testing.M) {
	if err := godotenv.Load("../../.env.test"); err != nil {
		log.Fatalf("Failed to load .env.test file: %v", err)
	}

	dsn := os.Getenv("DATABASE_URL")
	var err error
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

	called := make(chan string, 1)
	fakePublish := func(ch, msg string) {
		called <- msg
	}

	chatRepo = db.NewChatRepo(testDB)
	messageRepo = db.NewMessageRepo(testDB)
	wsManager = ws.NewWSManager(chatRepo, messageRepo, fakePublish)

	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		upgrader := websocket.Upgrader{CheckOrigin: func(r *http.Request) bool { return true }}
		conn, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			log.Printf("upgrade error: %v", err)
			return
		}
		wsManager.HandleConnection(r.Context(), conn)
	}))
	defer server.Close()
	serverURL = "ws" + server.URL[len("http"):]

	err = truncateTables(testDB)
	if err != nil {
		log.Fatalf("Failed to truncate tables: %v", err)
	}

	sqlDB, _ := testDB.DB()
	sqlDB.Close()

	os.Exit(m.Run())
}
