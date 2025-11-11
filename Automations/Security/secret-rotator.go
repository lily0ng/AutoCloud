package main

import (
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"log"
	"time"
)

type Secret struct {
	ID          string
	Name        string
	Value       string
	CreatedAt   time.Time
	RotatedAt   time.Time
	RotationAge int
}

type SecretRotator struct {
	secrets map[string]*Secret
}

func NewSecretRotator() *SecretRotator {
	return &SecretRotator{
		secrets: make(map[string]*Secret),
	}
}

func (sr *SecretRotator) AddSecret(name string, rotationAge int) {
	secret := &Secret{
		ID:          fmt.Sprintf("secret-%d", len(sr.secrets)+1),
		Name:        name,
		Value:       sr.generateSecret(),
		CreatedAt:   time.Now(),
		RotatedAt:   time.Now(),
		RotationAge: rotationAge,
	}
	
	sr.secrets[secret.ID] = secret
	log.Printf("🔑 Secret added: %s", name)
}

func (sr *SecretRotator) RotateSecret(secretID string) error {
	secret, exists := sr.secrets[secretID]
	if !exists {
		return fmt.Errorf("secret not found: %s", secretID)
	}
	
	oldValue := secret.Value
	secret.Value = sr.generateSecret()
	secret.RotatedAt = time.Now()
	
	log.Printf("🔄 Secret rotated: %s", secret.Name)
	log.Printf("   Old: %s...", oldValue[:8])
	log.Printf("   New: %s...", secret.Value[:8])
	
	return nil
}

func (sr *SecretRotator) CheckRotationNeeded() []string {
	needsRotation := make([]string, 0)
	
	for id, secret := range sr.secrets {
		daysSinceRotation := int(time.Since(secret.RotatedAt).Hours() / 24)
		
		if daysSinceRotation >= secret.RotationAge {
			needsRotation = append(needsRotation, id)
		}
	}
	
	return needsRotation
}

func (sr *SecretRotator) AutoRotate() {
	log.Println("🔄 Running automatic secret rotation...")
	
	needsRotation := sr.CheckRotationNeeded()
	
	for _, secretID := range needsRotation {
		if err := sr.RotateSecret(secretID); err != nil {
			log.Printf("❌ Failed to rotate %s: %v", secretID, err)
		}
	}
	
	log.Printf("✅ Rotated %d secrets", len(needsRotation))
}

func (sr *SecretRotator) generateSecret() string {
	b := make([]byte, 32)
	rand.Read(b)
	return base64.StdEncoding.EncodeToString(b)
}

func (sr *SecretRotator) ListSecrets() {
	fmt.Println("\n🔑 Secrets Inventory")
	fmt.Println("===================")
	
	for _, secret := range sr.secrets {
		daysSinceRotation := int(time.Since(secret.RotatedAt).Hours() / 24)
		status := "✅"
		if daysSinceRotation >= secret.RotationAge {
			status = "⚠️"
		}
		
		fmt.Printf("%s %s (Rotated %d days ago, Max age: %d days)\n",
			status, secret.Name, daysSinceRotation, secret.RotationAge)
	}
}

func main() {
	rotator := NewSecretRotator()
	
	rotator.AddSecret("database-password", 90)
	rotator.AddSecret("api-key", 30)
	rotator.AddSecret("jwt-secret", 180)
	
	rotator.ListSecrets()
	rotator.AutoRotate()
}
