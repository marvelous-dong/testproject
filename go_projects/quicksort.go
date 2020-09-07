package main

import (
	"fmt"
	"math/rand"
)

func main() {
	lis := []int{}

	for i:=0; i<10; i++ {
		lis = append(lis, rand.Intn(100))
	}

	fmt.Println("origin: ", lis)
	fmt.Println("after: ", quicksort(lis))
}

func quicksort(collection []int) []int {
	length := len(collection)
	if length < 2 {
		return collection
	}

	pivot := collection[0]
	pivot_list := []int{pivot}
	greater := []int{}
	lesser := []int{}
	for _, e := range collection[1:] {
		if e <= pivot {
			lesser = append(lesser, e)
		} else {
			greater = append(greater, e)
		}
	}

	return append(append(quicksort(lesser), pivot_list...), quicksort(greater)...)
}
