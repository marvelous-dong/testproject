package main

import "fmt"

func main() {
	final := ""
	for k:=1; k<=9; k++ {
		final += make_product(k)
	}
	fmt.Println(final)
}

func make_product(i int) string {

	final_string := ""
	for j:=1; j<=i; j++ {
		final_string += fmt.Sprintf("%v x %v = %v\t", j, i, i*j)
	}
	final_string += "\n"

	return final_string
}