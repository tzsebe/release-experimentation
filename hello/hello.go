package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Printf("Hello, your runtime is: %s\n", runtime.GOOS)
}
