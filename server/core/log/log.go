package log

import (
	"log"
	"holerr/core/config"
)

func Info(msg ...interface{}) {
	Config := config.Get()
	if Config.Debug {
		log.Println(msg)
	}
}

func Error(msg ...interface{}) {
	log.Println(msg)
}

func Fatal(msg ...interface{}) {
	log.Fatalln(msg)
}

func Panic(msg ...interface{}) {
	panic(msg)
}