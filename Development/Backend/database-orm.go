package main

import (
	"database/sql"
	"fmt"
	"log"
	"time"

	_ "github.com/lib/pq"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

// Database configuration
type DBConfig struct {
	Host     string
	Port     int
	User     string
	Password string
	DBName   string
	SSLMode  string
}

// Models
type Model struct {
	ID        uint           `gorm:"primaryKey" json:"id"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `gorm:"index" json:"-"`
}

type User struct {
	Model
	Email    string `gorm:"uniqueIndex;not null" json:"email"`
	Name     string `gorm:"not null" json:"name"`
	Password string `gorm:"not null" json:"-"`
	Posts    []Post `gorm:"foreignKey:UserID" json:"posts,omitempty"`
}

type Post struct {
	Model
	Title   string `gorm:"not null" json:"title"`
	Content string `gorm:"type:text" json:"content"`
	UserID  uint   `gorm:"not null" json:"user_id"`
	User    User   `gorm:"foreignKey:UserID" json:"user,omitempty"`
}

// Database manager
type Database struct {
	DB *gorm.DB
}

// NewDatabase creates a new database connection
func NewDatabase(config DBConfig) (*Database, error) {
	dsn := fmt.Sprintf(
		"host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
		config.Host, config.Port, config.User, config.Password, config.DBName, config.SSLMode,
	)

	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Info),
		NowFunc: func() time.Time {
			return time.Now().UTC()
		},
	})

	if err != nil {
		return nil, fmt.Errorf("failed to connect to database: %w", err)
	}

	sqlDB, err := db.DB()
	if err != nil {
		return nil, err
	}

	// Connection pool settings
	sqlDB.SetMaxIdleConns(10)
	sqlDB.SetMaxOpenConns(100)
	sqlDB.SetConnMaxLifetime(time.Hour)

	return &Database{DB: db}, nil
}

// AutoMigrate runs database migrations
func (d *Database) AutoMigrate() error {
	return d.DB.AutoMigrate(&User{}, &Post{})
}

// User operations
func (d *Database) CreateUser(user *User) error {
	return d.DB.Create(user).Error
}

func (d *Database) GetUserByID(id uint) (*User, error) {
	var user User
	err := d.DB.Preload("Posts").First(&user, id).Error
	return &user, err
}

func (d *Database) GetUserByEmail(email string) (*User, error) {
	var user User
	err := d.DB.Where("email = ?", email).First(&user).Error
	return &user, err
}

func (d *Database) UpdateUser(user *User) error {
	return d.DB.Save(user).Error
}

func (d *Database) DeleteUser(id uint) error {
	return d.DB.Delete(&User{}, id).Error
}

func (d *Database) ListUsers(limit, offset int) ([]User, error) {
	var users []User
	err := d.DB.Limit(limit).Offset(offset).Find(&users).Error
	return users, err
}

// Post operations
func (d *Database) CreatePost(post *Post) error {
	return d.DB.Create(post).Error
}

func (d *Database) GetPostByID(id uint) (*Post, error) {
	var post Post
	err := d.DB.Preload("User").First(&post, id).Error
	return &post, err
}

func (d *Database) UpdatePost(post *Post) error {
	return d.DB.Save(post).Error
}

func (d *Database) DeletePost(id uint) error {
	return d.DB.Delete(&Post{}, id).Error
}

func (d *Database) ListPosts(limit, offset int) ([]Post, error) {
	var posts []Post
	err := d.DB.Preload("User").Limit(limit).Offset(offset).Find(&posts).Error
	return posts, err
}

func (d *Database) GetPostsByUserID(userID uint) ([]Post, error) {
	var posts []Post
	err := d.DB.Where("user_id = ?", userID).Find(&posts).Error
	return posts, err
}

// Transaction support
func (d *Database) Transaction(fn func(*gorm.DB) error) error {
	return d.DB.Transaction(fn)
}

// Raw SQL support
func (d *Database) RawQuery(query string, args ...interface{}) (*sql.Rows, error) {
	sqlDB, err := d.DB.DB()
	if err != nil {
		return nil, err
	}
	return sqlDB.Query(query, args...)
}

// Health check
func (d *Database) Ping() error {
	sqlDB, err := d.DB.DB()
	if err != nil {
		return err
	}
	return sqlDB.Ping()
}

// Close database connection
func (d *Database) Close() error {
	sqlDB, err := d.DB.DB()
	if err != nil {
		return err
	}
	return sqlDB.Close()
}

func main() {
	config := DBConfig{
		Host:     "localhost",
		Port:     5432,
		User:     "postgres",
		Password: "password",
		DBName:   "myapp",
		SSLMode:  "disable",
	}

	db, err := NewDatabase(config)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Run migrations
	if err := db.AutoMigrate(); err != nil {
		log.Fatal(err)
	}

	log.Println("Database connected and migrated successfully")
}
