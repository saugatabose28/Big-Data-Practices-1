import time
import math
from rtree import index



# Function to read points from a text file
def read_points(file_path):
    points = []
    # Open the file for reading
    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines from the file
        for line in lines:
            parts = line.strip().split()  # Split the line to get each variable
            id = int(parts[0])  # Extract the ID and convert to integer
            x = float(parts[1])  # Extract the x-coordinate (longitude) and convert to float
            y = float(parts[2])  # Extract the y-coordinate (latitude) and convert to float
            points.append((id, x, y))  # Append the point as a tuple (id, x, y)
    return points  

# Calculate Euclidean distance between two points
def calculate_distance(point1, point2):
    # Distance formula: sqrt((x2 - x1)^2 + (y2 - y1)^2)
    return math.sqrt((point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)




# Sequential Scan Based Method
def sequential_scan(query_points, dataset_points):
    results = []
    start_time = time.time() # Record the start time

    # Loop through each query point
    for query in query_points:
        min_distance = float('inf')  # Initialise the minimum distance
        nearest_neighbor = None # Initialise the nearest neighbor

        # Loop through each dataset point
        for point in dataset_points:
            distance = calculate_distance(query, point) #Calculate the distance between query and point
          
            # Check if the calculated distance is less than the current minimum distance
            if distance < min_distance:  
                min_distance = distance # Update the minimum distance
                nearest_neighbor = point # Update the nearest neighbor

        # Append the result as a tuple (query_id, nearest_id, nearest_x, nearest_y)
        results.append((query[0], nearest_neighbor[0], nearest_neighbor[1], nearest_neighbor[2]))

    total_time = time.time() - start_time #Calculate the total running time
    average_time = total_time / len(query_points) # Calculate the average time per query
   
    return results, total_time, average_time



#Create an R-tree from points
def create_rtree(points):
    p = index.Property() # Create an R-tree property object
    idx = index.Index(properties=p) # Create an R-tree index

    # Loop through each point to insert into the R-tree
    for point in points:
        # Insert the point into the R-tree with bounding box (x, y, x, y) and associate the point object
        idx.insert(point[0], (point[1], point[2], point[1], point[2]), obj=point)

    return idx #Return the R-tree index



# Best First (BF) Algorithm using R-tree
def best_first(query_points, rtree_index):
    results = []
    start_time = time.time()  # Record the start time

    #Loop through each query point
    for query in query_points:
        # Find the nearest neighbor using the R-tree
        nearest = list(rtree_index.nearest((query[1], query[2], query[1], query[2]), 1, objects=True))[0].object
        #Append the result as a tuple (query_id, nearest_id, nearest_x, nearest_y)
        results.append((query[0], nearest[0], nearest[1], nearest[2]))

    total_time = time.time() - start_time  # Calculate the total running time
    average_time = total_time / len(query_points) # Calculate the average time per query

    return results, total_time, average_time  




# BF with Divide-and-Conquer
def divide_dataset(dataset_points):

    # Sort the dataset points by their x-coordinate
    sorted_points = sorted(dataset_points, key=lambda point: point[1])
    mid_index = len(sorted_points) // 2  # Find the middle index to divide the dataset
    subspace1 = sorted_points[:mid_index] # First subspace containing the first half of points
    subspace2 = sorted_points[mid_index:] # Second subspace containing the second half of points

    return subspace1, subspace2  # Return the two subspaces



#Find the nearest neighbor for each query point using BF divide and conquer 
def bf_divide_and_conquer(query_points, rtree1, rtree2):
    results = []
    start_time = time.time()  # Record the start time

    #Loop through each query point
    for query in query_points:
        nearest1 = find_nearest_neighbor_rtree(query, rtree1) # Find nearest neighbor in first subspace
        nearest2 = find_nearest_neighbor_rtree(query, rtree2) # Find nearest neighbor in second subspace
        
        distance1 = calculate_distance(query, nearest1) # Calculate distance to nearest neighbor in first subspace
        distance2 = calculate_distance(query, nearest2) # Calculate distance to nearest neighbor in second subspace
        
        #Determine the closest neighbor by comparing distances
        if distance1 < distance2:
            nearest = nearest1
        else:
            nearest = nearest2
        
        #Append the result as a tuple (query_id, nearest_id, nearest_x, nearest_y)
        results.append((query[0], nearest[0], nearest[1], nearest[2]))

    total_time = time.time() - start_time  # Calculate the total running time
    average_time = total_time / len(query_points)  # Calculate the average time per query
    return results, total_time, average_time  # Return the results, total time, and average time



#Identify the nearest neighbour to a specified query point using the R-tree index
def find_nearest_neighbor_rtree(query_point, rtree_index):

    # Find the nearest neighbor using the R-tree
    nearest = list(rtree_index.nearest((query_point[1], query_point[2], query_point[1], query_point[2]), 1, objects=True))[0].object

    return nearest  # Return the nearest neighbor point




#Write results to an output file
def write_results(results, total_time, average_time, output_file, method_name):
    # Open the output file in append mode
    with open(output_file, 'a') as file:
        file.write(f"Results for {method_name}:\n") # Write the algorithm method name

        # Loop through each result
        for result in results:
            # Write the result to the file
            file.write(f"id={result[1]}, x={result[2]}, y={result[3]} for query {result[0]}\n")

        #Write the total running time and average time per query
        file.write(f"Total running time: {total_time:.6f} seconds\n")
        file.write(f"Average time per query: {average_time:.6f} seconds\n\n")



if __name__ == '__main__':
    # Paths to the input files
    query_file_path = 'query_points.txt'
    dataset_file_path = 'shop_dataset.txt'
    output_file_path = 'Nearest_Neighbor_Search.txt'

    # Read points from files
    query_points = read_points(query_file_path)
    dataset_points = read_points(dataset_file_path)

    # Clear the output file if it exists
    open(output_file_path, 'w').close()


    #Run the 3 algorithms: 

    #Sequential Scan Based Method
    results, total_time, average_time = sequential_scan(query_points, dataset_points)
    write_results(results, total_time, average_time, output_file_path, "Sequential Scan Based Method")

    #Best First (BF) Algorithm
    rtree_index = create_rtree(dataset_points)
    results, total_time, average_time = best_first(query_points, rtree_index)
    write_results(results, total_time, average_time, output_file_path, "Best First Algorithm")

    #BF with Divide-and-Conquer
    subspace1, subspace2 = divide_dataset(dataset_points)
    rtree1 = create_rtree(subspace1)
    rtree2 = create_rtree(subspace2)
    results, total_time, average_time = bf_divide_and_conquer(query_points, rtree1, rtree2)
    write_results(results, total_time, average_time, output_file_path, "BF with Divide-and-Conquer")


    #Print confirmation that the program has finished
    print(f"Results have been written to {output_file_path}")
