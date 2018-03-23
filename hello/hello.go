package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Println("Hello!")
	fmt.Println("Your os is:", runtime.GOOS)
	fmt.Println("Your arch is:", runtime.GOARCH)
}
