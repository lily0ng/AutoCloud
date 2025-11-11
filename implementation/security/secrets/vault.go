package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"errors"
	"io"
	"sync"
)

type SecretVault struct {
	secrets map[string]string
	key     []byte
	mu      sync.RWMutex
}

func NewSecretVault(key []byte) (*SecretVault, error) {
	if len(key) != 32 {
		return nil, errors.New("key must be 32 bytes")
	}
	return &SecretVault{
		secrets: make(map[string]string),
		key:     key,
	}, nil
}

func (v *SecretVault) encrypt(plaintext string) (string, error) {
	block, err := aes.NewCipher(v.key)
	if err != nil {
		return "", err
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return "", err
	}

	nonce := make([]byte, gcm.NonceSize())
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		return "", err
	}

	ciphertext := gcm.Seal(nonce, nonce, []byte(plaintext), nil)
	return base64.StdEncoding.EncodeToString(ciphertext), nil
}

func (v *SecretVault) decrypt(ciphertext string) (string, error) {
	data, err := base64.StdEncoding.DecodeString(ciphertext)
	if err != nil {
		return "", err
	}

	block, err := aes.NewCipher(v.key)
	if err != nil {
		return "", err
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return "", err
	}

	nonceSize := gcm.NonceSize()
	if len(data) < nonceSize {
		return "", errors.New("ciphertext too short")
	}

	nonce, ciphertext := data[:nonceSize], data[nonceSize:]
	plaintext, err := gcm.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		return "", err
	}

	return string(plaintext), nil
}

func (v *SecretVault) Set(key, value string) error {
	v.mu.Lock()
	defer v.mu.Unlock()

	encrypted, err := v.encrypt(value)
	if err != nil {
		return err
	}

	v.secrets[key] = encrypted
	return nil
}

func (v *SecretVault) Get(key string) (string, error) {
	v.mu.RLock()
	defer v.mu.RUnlock()

	encrypted, exists := v.secrets[key]
	if !exists {
		return "", errors.New("secret not found")
	}

	return v.decrypt(encrypted)
}

func (v *SecretVault) Delete(key string) {
	v.mu.Lock()
	defer v.mu.Unlock()
	delete(v.secrets, key)
}
