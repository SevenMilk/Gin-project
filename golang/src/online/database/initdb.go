package db

import (
	"database/sql"
	"fmt"
	"time"
	"online/global"

	_ "github.com/go-sql-driver/mysql"
)

func InitMySQLDB() *sql.DB {
	dsn := fmt.Sprintf("%s:%s@(%s)/%s?charset=%s&parseTime=true&loc=Local",
		global.MySQLUser, global.MySQLPw, global.MySQLHost, global.MySQLDb, "utf8")

	if conn, err := sql.Open("mysql", dsn); err != nil {
		panic(err.Error())
	} else {
		conn.SetConnMaxLifetime(7 * time.Second)
		conn.SetMaxOpenConns(10)
		conn.SetMaxIdleConns(10)
		return conn
	}
}
