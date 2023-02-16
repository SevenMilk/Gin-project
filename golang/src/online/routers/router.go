package routers

import (
	check "online/app"
	api "online/app/v1"
	"online/app/v1/middleware"
	db "online/database"
	"online/global"

	"github.com/gin-gonic/gin"
)

func InitRouter() *gin.Engine {
	r := gin.Default()
	r.Use(middleware.LoggerToFile())
	global.Mysql = db.InitMySQLDB()
	userv1_h := api.UserV1{}
	userv1 := r.Group("/user/v1")
	{
		userv1.GET("/all", userv1_h.GetAllData)
		userv1.GET("/id=:id", userv1_h.GetFilterId)
	}
	r.GET("/hc", check.HealthCheck)
	return r
}
