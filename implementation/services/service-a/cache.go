package main

import (
	"context"
	"encoding/json"
	"time"

	"github.com/go-redis/redis/v8"
)

type CacheClient struct {
	client *redis.Client
	ctx    context.Context
}

func NewCacheClient(addr, password string, db int) *CacheClient {
	rdb := redis.NewClient(&redis.Options{
		Addr:     addr,
		Password: password,
		DB:       db,
	})

	ctx := context.Background()
	return &CacheClient{
		client: rdb,
		ctx:    ctx,
	}
}

func (c *CacheClient) Set(key string, value interface{}, expiration time.Duration) error {
	data, err := json.Marshal(value)
	if err != nil {
		return err
	}
	return c.client.Set(c.ctx, key, data, expiration).Err()
}

func (c *CacheClient) Get(key string, dest interface{}) error {
	val, err := c.client.Get(c.ctx, key).Result()
	if err != nil {
		return err
	}
	return json.Unmarshal([]byte(val), dest)
}

func (c *CacheClient) Delete(key string) error {
	return c.client.Del(c.ctx, key).Err()
}

func (c *CacheClient) Exists(key string) (bool, error) {
	result, err := c.client.Exists(c.ctx, key).Result()
	return result > 0, err
}

func (c *CacheClient) Close() error {
	return c.client.Close()
}
