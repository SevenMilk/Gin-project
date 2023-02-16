package api

import (
	"encoding/json"
	"fmt"
	"online/app/v1/models/cache"
	"online/app/v1/models/maindb"
	"online/global"
	"reflect"

	"github.com/gin-gonic/gin"
)

type UserV1 struct{}

func (UserV1) GetAllData(c *gin.Context) {
	users := maindb.GetAllDataFromMysql()
	if users == nil {
		c.JSON(200, gin.H{"error": 1, "msg": "Failed"})
	} else {
		c.JSON(200, gin.H{"error": 0, "msg": "Success", "data": users})
	}
}

func (UserV1) GetFilterId(c *gin.Context) {
	urls := "http://" + c.Request.Host + c.Request.URL.Path
	response := cache.RedisGet(urls)
	if response != "" {
		var DataResult []global.User
		json.Unmarshal([]byte(response), &DataResult)
		c.JSON(200, gin.H{"Error": 0, "Msg": "Success from cache", "data": DataResult})
	} else {
		id := c.Param("id")
		users := maindb.GetDataFromMysqlFilterId(id)
		if users == nil {
			c.JSON(200, gin.H{"Error": 1, "Msg": "Failed"})
		} else {
			c.JSON(200, gin.H{"Error": 0, "Msg": "Success from db", "data": users})
			fmt.Printf("users: %s\n", reflect.TypeOf(users))
			cache.RedisSet(urls, users)
		}
	}
}
