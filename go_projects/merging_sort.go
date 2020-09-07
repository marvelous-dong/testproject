package main

import "fmt"

func main() {
	arr01 := []int{34, 45, 3, 6, 76, 34, 46, 809, 92, 8}
	fmt.Print("排序前: ")
	fmt.Println(arr01)
	mergeSort(arr01, 0, len(arr01)-1)
	fmt.Print("排序后: ")
	fmt.Println(arr01)
}

func merge1(arr []int, low int, mid int, high int) {
	leftLen := mid - low + 1
	rightLen := high - mid
	arrLeft := make([]int, leftLen+1)
	for i := 0; i < leftLen; i++ {
		arrLeft[i] = arr[low+i]
	}
	arrLeft[leftLen] = 99999
	arrRight := make([]int, rightLen+1)

	for j := 0; j < rightLen; j++ {
		arrRight[j] = arr[mid+1+j]
	}

	arrRight[rightLen] = 99999
	i, j := 0, 0
	for k := low; k <= high; k++ {
		if arrLeft[i] <= arrRight[j] {
			arr[k] = arrLeft[i]
			i++
		} else {
			arr[k] = arrRight[j]
			j++
		}
	}
}

func mergeSort(arr [] int, low int, high int) {
	if low < high {
		mid := (low + high) / 2
		mergeSort(arr, low, mid)
		mergeSort(arr, mid+1, high)
		merge1(arr, low, mid, high)
	}
}

