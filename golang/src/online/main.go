package main

import (
	"online/routers"
)

func main() {
	r := routers.InitRouter()
	r.Run(":8083")
}
