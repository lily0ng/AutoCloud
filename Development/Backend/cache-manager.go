package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"time"

	"github.com/go-redis/redis/v8"
)

// CacheManager handles Redis caching operations
type CacheManager struct {
	client *redis.Client
	ctx    context.Context
}

// CacheConfig holds Redis configuration
type CacheConfig struct {
	Host     string
	Port     int
	Password string
	DB       int
}

// NewCacheManager creates a new cache manager instance
func NewCacheManager(config CacheConfig) (*CacheManager, error) {
	client := redis.NewClient(&redis.Options{
		Addr:         fmt.Sprintf("%s:%d", config.Host, config.Port),
		Password:     config.Password,
		DB:           config.DB,
		DialTimeout:  5 * time.Second,
		ReadTimeout:  3 * time.Second,
		WriteTimeout: 3 * time.Second,
		PoolSize:     10,
		MinIdleConns: 5,
	})

	ctx := context.Background()

	// Test connection
	if err := client.Ping(ctx).Err(); err != nil {
		return nil, fmt.Errorf("failed to connect to Redis: %w", err)
	}

	return &CacheManager{
		client: client,
		ctx:    ctx,
	}, nil
}

// Set stores a value in cache with expiration
func (cm *CacheManager) Set(key string, value interface{}, expiration time.Duration) error {
	data, err := json.Marshal(value)
	if err != nil {
		return fmt.Errorf("failed to marshal value: %w", err)
	}

	return cm.client.Set(cm.ctx, key, data, expiration).Err()
}

// Get retrieves a value from cache
func (cm *CacheManager) Get(key string, dest interface{}) error {
	data, err := cm.client.Get(cm.ctx, key).Bytes()
	if err != nil {
		if err == redis.Nil {
			return fmt.Errorf("key not found: %s", key)
		}
		return err
	}

	return json.Unmarshal(data, dest)
}

// Delete removes a key from cache
func (cm *CacheManager) Delete(keys ...string) error {
	return cm.client.Del(cm.ctx, keys...).Err()
}

// Exists checks if a key exists
func (cm *CacheManager) Exists(keys ...string) (bool, error) {
	count, err := cm.client.Exists(cm.ctx, keys...).Result()
	return count > 0, err
}

// Expire sets expiration on a key
func (cm *CacheManager) Expire(key string, expiration time.Duration) error {
	return cm.client.Expire(cm.ctx, key, expiration).Err()
}

// Increment increments a numeric value
func (cm *CacheManager) Increment(key string) (int64, error) {
	return cm.client.Incr(cm.ctx, key).Result()
}

// Decrement decrements a numeric value
func (cm *CacheManager) Decrement(key string) (int64, error) {
	return cm.client.Decr(cm.ctx, key).Result()
}

// Hash operations
func (cm *CacheManager) HSet(key, field string, value interface{}) error {
	data, err := json.Marshal(value)
	if err != nil {
		return err
	}
	return cm.client.HSet(cm.ctx, key, field, data).Err()
}

func (cm *CacheManager) HGet(key, field string, dest interface{}) error {
	data, err := cm.client.HGet(cm.ctx, key, field).Bytes()
	if err != nil {
		return err
	}
	return json.Unmarshal(data, dest)
}

func (cm *CacheManager) HGetAll(key string) (map[string]string, error) {
	return cm.client.HGetAll(cm.ctx, key).Result()
}

func (cm *CacheManager) HDel(key string, fields ...string) error {
	return cm.client.HDel(cm.ctx, key, fields...).Err()
}

// List operations
func (cm *CacheManager) LPush(key string, values ...interface{}) error {
	return cm.client.LPush(cm.ctx, key, values...).Err()
}

func (cm *CacheManager) RPush(key string, values ...interface{}) error {
	return cm.client.RPush(cm.ctx, key, values...).Err()
}

func (cm *CacheManager) LPop(key string) (string, error) {
	return cm.client.LPop(cm.ctx, key).Result()
}

func (cm *CacheManager) RPop(key string) (string, error) {
	return cm.client.RPop(cm.ctx, key).Result()
}

func (cm *CacheManager) LRange(key string, start, stop int64) ([]string, error) {
	return cm.client.LRange(cm.ctx, key, start, stop).Result()
}

// Set operations
func (cm *CacheManager) SAdd(key string, members ...interface{}) error {
	return cm.client.SAdd(cm.ctx, key, members...).Err()
}

func (cm *CacheManager) SMembers(key string) ([]string, error) {
	return cm.client.SMembers(cm.ctx, key).Result()
}

func (cm *CacheManager) SIsMember(key string, member interface{}) (bool, error) {
	return cm.client.SIsMember(cm.ctx, key, member).Result()
}

func (cm *CacheManager) SRem(key string, members ...interface{}) error {
	return cm.client.SRem(cm.ctx, key, members...).Err()
}

// Sorted Set operations
func (cm *CacheManager) ZAdd(key string, members ...*redis.Z) error {
	return cm.client.ZAdd(cm.ctx, key, members...).Err()
}

func (cm *CacheManager) ZRange(key string, start, stop int64) ([]string, error) {
	return cm.client.ZRange(cm.ctx, key, start, stop).Result()
}

func (cm *CacheManager) ZRangeByScore(key string, min, max string) ([]string, error) {
	return cm.client.ZRangeByScore(cm.ctx, key, &redis.ZRangeBy{
		Min: min,
		Max: max,
	}).Result()
}

// Pub/Sub operations
func (cm *CacheManager) Publish(channel string, message interface{}) error {
	data, err := json.Marshal(message)
	if err != nil {
		return err
	}
	return cm.client.Publish(cm.ctx, channel, data).Err()
}

func (cm *CacheManager) Subscribe(channels ...string) *redis.PubSub {
	return cm.client.Subscribe(cm.ctx, channels...)
}

// Flush all keys (use with caution)
func (cm *CacheManager) FlushAll() error {
	return cm.client.FlushAll(cm.ctx).Err()
}

// FlushDB flushes current database
func (cm *CacheManager) FlushDB() error {
	return cm.client.FlushDB(cm.ctx).Err()
}

// GetTTL returns time to live for a key
func (cm *CacheManager) GetTTL(key string) (time.Duration, error) {
	return cm.client.TTL(cm.ctx, key).Result()
}

// Keys returns all keys matching pattern
func (cm *CacheManager) Keys(pattern string) ([]string, error) {
	return cm.client.Keys(cm.ctx, pattern).Result()
}

// Close closes the Redis connection
func (cm *CacheManager) Close() error {
	return cm.client.Close()
}

// Ping checks Redis connection
func (cm *CacheManager) Ping() error {
	return cm.client.Ping(cm.ctx).Err()
}

func main() {
	config := CacheConfig{
		Host:     "localhost",
		Port:     6379,
		Password: "",
		DB:       0,
	}

	cache, err := NewCacheManager(config)
	if err != nil {
		log.Fatal(err)
	}
	defer cache.Close()

	// Example usage
	type User struct {
		ID   string
		Name string
	}

	user := User{ID: "1", Name: "John Doe"}
	
	// Set with 1 hour expiration
	if err := cache.Set("user:1", user, time.Hour); err != nil {
		log.Fatal(err)
	}

	// Get from cache
	var cachedUser User
	if err := cache.Get("user:1", &cachedUser); err != nil {
		log.Fatal(err)
	}

	log.Printf("Cached user: %+v\n", cachedUser)
}
