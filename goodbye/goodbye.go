package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Printf("Your runtime is: %s\nGoodbye!\n", runtime.GOOS)
}
