# Quick sort in Python


# Function to partition the array on the basis of pivot element
def partition(array, low, high):

    # Select the pivot element
    pivot = array[high]
    i = low

    # Put the elements smaller than pivot on the left and greater 
    #than pivot on the right of pivot
    for j in range(low, high): # check the element one by one
        if array[j] <= pivot: #compare the current element with the pivot, if we find a smaller value
            (array[i], array[j]) = (array[j], array[i]) #we switch the current element with the current order (start from 1)
            i=i+1 #

    (array[i], array[high]) = (array[high], array[i]) #move the current pivot into the middle, and set a new pivot

    return i #the position to divide an array


def quickSort(array, low, high):
    if low < high: # if low == high, we stop at the current pivot, and the array cannot be further split.

        # Select pivot position and put all the elements smaller 
        # than pivot on left and greater than pivot on right
        pi = partition(array, low, high)

        print(array,"\n")

        # Sort the elements on the left of pivot
        quickSort(array, low, pi - 1)

        # Sort the elements on the right of pivot
        quickSort(array, pi + 1, high)


data = [8, 7, 2, 1, 0, 9, 6]
# in the first run,
# 8>6, did nothing
# 7>6, did nothing
# 2<6, switch the first element 8 (array[i]) with 2 (array [j]), [2,7,8,1,0,9,6] (i=i+1, i.e., i==2)
# 1<6, switch 7 with 1, [2,1,8,7,0,9,6]
# 0<6, switch 8 with 0, [2,1,0,7,8,9,6]
# 9>6, did nothing
# (array[i], array[high]) = (array[high], array[i]), [2,1,0,6,8,9,7], pi=3 (start from 0)
# keep continue a new round of quickSort for (low, pi-1) [2,1,0], and (pi+1, high) [8,9,7] till low == high


size = len(data)
quickSort(data, 0, size - 1)
print('Sorted Array in Ascending Order:')
print(data)