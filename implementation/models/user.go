package models

import (
	"time"
)

type User struct {
	ID        int64     `json:"id" db:"id"`
	Username  string    `json:"username" db:"username"`
	Email     string    `json:"email" db:"email"`
	Password  string    `json:"-" db:"password_hash"`
	Role      string    `json:"role" db:"role"`
	Active    bool      `json:"active" db:"active"`
	CreatedAt time.Time `json:"created_at" db:"created_at"`
	UpdatedAt time.Time `json:"updated_at" db:"updated_at"`
}

type UserRepository interface {
	Create(user *User) error
	GetByID(id int64) (*User, error)
	GetByUsername(username string) (*User, error)
	GetByEmail(email string) (*User, error)
	Update(user *User) error
	Delete(id int64) error
	List(limit, offset int) ([]*User, error)
}

func (u *User) Validate() error {
	if u.Username == "" {
		return ErrInvalidUsername
	}
	if u.Email == "" {
		return ErrInvalidEmail
	}
	if len(u.Password) < 8 {
		return ErrInvalidPassword
	}
	return nil
}

func (u *User) IsAdmin() bool {
	return u.Role == "admin"
}

var (
	ErrInvalidUsername = NewError("invalid username")
	ErrInvalidEmail    = NewError("invalid email")
	ErrInvalidPassword = NewError("invalid password")
	ErrUserNotFound    = NewError("user not found")
)

type Error struct {
	Message string
}

func NewError(msg string) *Error {
	return &Error{Message: msg}
}

func (e *Error) Error() string {
	return e.Message
}
