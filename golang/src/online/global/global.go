package global

import "database/sql"

type User struct {
	ID      int     `json:"id"`
	NAME    string  `json:"name"`
	ADDRESS string  `json:"address"`
	LAT     float64 `json:"lat"`
	LNG     float64 `json:"lng"`
	LOCNAME string  `json:"locname"`
	IMG     string  `json:"img"`
	INTRO   string  `json:"intro"`
	ICON    string  `json:"icon"`
	TYPE    string  `json:"type"`
}

type TableSchema []User

var (
	Mysql *sql.DB
)

var RedisHost string = "192.168.23.130:6379"
var MySQLHost string = "192.168.23.130:3306"
var MySQLUser string = "root"
var MySQLPw string = "jiang123"
var MySQLDb string = "test_db"