package main

import (
	"fmt"
	"log"
	"time"
)

type AccessReview struct {
	UserID      string
	Resource    string
	Permissions []string
	LastAccess  time.Time
	Excessive   bool
}

type AccessReviewer struct {
	reviews []AccessReview
}

func NewAccessReviewer() *AccessReviewer {
	return &AccessReviewer{
		reviews: make([]AccessReview, 0),
	}
}

func (ar *AccessReviewer) ReviewAccess() {
	log.Println("🔍 Reviewing access permissions...")
	
	ar.reviews = append(ar.reviews, AccessReview{
		UserID:      "user-123",
		Resource:    "S3 Bucket: prod-data",
		Permissions: []string{"s3:GetObject", "s3:PutObject", "s3:DeleteObject"},
		LastAccess:  time.Now().AddDate(0, -6, 0),
		Excessive:   true,
	})
	
	ar.reviews = append(ar.reviews, AccessReview{
		UserID:      "user-456",
		Resource:    "RDS Database: prod-db",
		Permissions: []string{"rds:DescribeDBInstances"},
		LastAccess:  time.Now().AddDate(0, 0, -2),
		Excessive:   false,
	})
}

func (ar *AccessReviewer) FindStaleAccess(days int) []AccessReview {
	stale := make([]AccessReview, 0)
	cutoff := time.Now().AddDate(0, 0, -days)
	
	for _, review := range ar.reviews {
		if review.LastAccess.Before(cutoff) {
			stale = append(stale, review)
		}
	}
	
	return stale
}

func (ar *AccessReviewer) FindExcessivePermissions() []AccessReview {
	excessive := make([]AccessReview, 0)
	
	for _, review := range ar.reviews {
		if review.Excessive {
			excessive = append(excessive, review)
		}
	}
	
	return excessive
}

func (ar *AccessReviewer) GenerateReport() {
	fmt.Println("\n🔐 Access Review Report")
	fmt.Println("======================")
	
	stale := ar.FindStaleAccess(90)
	excessive := ar.FindExcessivePermissions()
	
	fmt.Printf("\nStale Access (>90 days): %d\n", len(stale))
	for _, review := range stale {
		fmt.Printf("  ⚠️  %s: %s (Last access: %s)\n",
			review.UserID, review.Resource, review.LastAccess.Format("2006-01-02"))
	}
	
	fmt.Printf("\nExcessive Permissions: %d\n", len(excessive))
	for _, review := range excessive {
		fmt.Printf("  ⚠️  %s: %s\n", review.UserID, review.Resource)
		fmt.Printf("     Permissions: %v\n", review.Permissions)
	}
}

func main() {
	reviewer := NewAccessReviewer()
	reviewer.ReviewAccess()
	reviewer.GenerateReport()
}
