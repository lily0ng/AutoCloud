package models

import (
	"encoding/json"
	"time"
)

type Transaction struct {
	ID        int64           `json:"id" db:"id"`
	UserID    int64           `json:"user_id" db:"user_id"`
	Type      string          `json:"type" db:"transaction_type"`
	Amount    float64         `json:"amount" db:"amount"`
	Status    string          `json:"status" db:"status"`
	Metadata  json.RawMessage `json:"metadata" db:"metadata"`
	CreatedAt time.Time       `json:"created_at" db:"created_at"`
}

type TransactionRepository interface {
	Create(tx *Transaction) error
	GetByID(id int64) (*Transaction, error)
	GetByUserID(userID int64, limit, offset int) ([]*Transaction, error)
	UpdateStatus(id int64, status string) error
	Delete(id int64) error
	GetByStatus(status string) ([]*Transaction, error)
}

const (
	StatusPending   = "pending"
	StatusProcessed = "processed"
	StatusFailed    = "failed"
	StatusCancelled = "cancelled"
)

func (t *Transaction) Validate() error {
	if t.UserID == 0 {
		return NewError("invalid user ID")
	}
	if t.Amount <= 0 {
		return NewError("invalid amount")
	}
	if t.Type == "" {
		return NewError("invalid transaction type")
	}
	return nil
}

func (t *Transaction) IsPending() bool {
	return t.Status == StatusPending
}

func (t *Transaction) IsCompleted() bool {
	return t.Status == StatusProcessed
}
