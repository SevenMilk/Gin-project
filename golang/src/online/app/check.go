package check

import (
	"net/http"
	"online/app/v1/middleware"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
)

func HealthCheck(c *gin.Context) {
	c.String(http.StatusOK, "Health Check")
	middleware.Logger().WithFields(logrus.Fields{
		"name": "ericjiang",
	}).Info("Health Check", "Info")
}
