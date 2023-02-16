package routers

import (
	"online/database"
	"online/global"
	"online/api/v1"

	"github.com/gin-gonic/gin"
)

func InitRouter() *gin.Engine {

	r := gin.Default()
	global.Mysql = db.InitMySQLDB()
	userv1_h := api.UserV1{}
	userv1 := r.Group("/user/v1")
	{
		userv1.GET("/all", userv1_h.GetAllData)
		userv1.GET("/id=:id", userv1_h.GetFilterId)
	}
	return r
}

