package cache

import (
	"online/global"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"time"

	"github.com/go-redis/redis"
)

func NewClient() *redis.Client {
	client := redis.NewClient(&redis.Options{
		Addr:     global.RedisHost,
		Password: "",
		DB:       0,
	})

	pong, err := client.Ping().Result()
	if err != nil {
		panic(err)
	}

	fmt.Println(pong)
	return client
}

func RedisGetKey(c *redis.Client, key string) string {
	val, err := c.Get(key).Result()
	if err == redis.Nil {
		return ""
	} else {
		return val
	}

}

func RedisSetKey(c *redis.Client, key string, val global.TableSchema) {
	jsondata, _ := json.Marshal(val)
	err := c.Set(key, jsondata, 1*time.Hour).Err()
	if err != nil {
		panic(err)
	}
	c.Close()
}

func RedisGet(key string) string {
	c := NewClient()
	encodedKey := base64.StdEncoding.EncodeToString([]byte(key))
	result := RedisGetKey(c, encodedKey)
	return result

}

func RedisSet(key string, val global.TableSchema) {
	c := NewClient()
	encodedKey := base64.StdEncoding.EncodeToString([]byte(key))
	RedisSetKey(c, encodedKey, val)
}
