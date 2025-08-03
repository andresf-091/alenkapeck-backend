package db

import (
	"database/sql"
	"fmt"
	"log"
	"os"

	_ "github.com/lib/pq"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB

// InitDB инициализирует соединение с Postgres и делает миграции
func InitDB() {
	dsn := os.Getenv("DATABASE_URL")

	var err error
	DB, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatalf("failed to connect to database: %v", err)
	}

	// Автоматическая миграция схемы
	if err := DB.AutoMigrate(&Chat{}, &Message{}); err != nil {
		log.Fatalf("auto migrate error: %v", err)
	}
	log.Println("Database initialized")
}

func CreateDatabaseIfNotExists() {
	dsn := fmt.Sprintf(
		"postgresql://%s:%s@%s:%s/%s?sslmode=disable",
		os.Getenv("POSTGRES_USER"),
		os.Getenv("POSTGRES_PASSWORD"),
		os.Getenv("POSTGRES_HOST"),
		os.Getenv("POSTGRES_PORT"),
		"postgres",
	)
	POSTGRES_DB := os.Getenv("POSTGRES_DB")

	db, err := sql.Open("postgres", dsn)
	if err != nil {
		log.Fatalf("Ошибка подключения к PostgreSQL: %v", err)
	}
	defer db.Close()

	// Проверяем, существует ли БД
	var exists bool
	query := `SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname = $1)`
	err = db.QueryRow(query, POSTGRES_DB).Scan(&exists)
	if err != nil {
		log.Fatalf("Ошибка при проверке существования базы данных: %v", err)
	}

	if !exists {
		_, err = db.Exec(fmt.Sprintf("CREATE DATABASE %s", POSTGRES_DB))
		if err != nil {
			log.Fatalf("Ошибка при создании базы данных: %v", err)
		}
		log.Printf("База данных %s успешно создана", POSTGRES_DB)
	} else {
		log.Printf("База данных %s уже существует", POSTGRES_DB)
	}
}
