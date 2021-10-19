package log

import (
	"holerr/core/config"
	"log"
)

func Info(msg ...interface{}) {
	if config.IsDebug() {
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
