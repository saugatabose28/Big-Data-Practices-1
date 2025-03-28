import math
import time
import sys
from rtree import index

B = 4  #Deciding on a node's maximum amount of entries

### Task 2.1: Sequential Scan Skyline Algorithm

def read_dataset(filename):  
    data = []
    with open(filename, 'r') as file:
        for line in file:  # recursively read every line in the file
            parts = line.strip().split()  # dividing the line into its constituent parts
            id = parts[0]  # The first part is the id
            x = float(parts[1])  # The x-coordinate, or cost, is the second component.
            y = float(parts[2])  # The y-coordinate, or size, is the third component.
            data.append((id, x, y))  # adding a tuple representing the point to the data list
    return data

def is_dominated(p1, p2):
    """Checks if point p1 is dominated by point p2."""
    return p1[1] >= p2[1] and p1[2] >= p2[2]  # p1 is dominated if p2 is both cheaper and larger or equal

def sequential_scan_skyline(data):
    """Identifies the skyline points using the sequential scan method."""
    skyline = []  # Creating a blank list at the beginning to hold the skyline points
    for i, p1 in enumerate(data):  # go over every dataset point in a loop
        dominated = False  # Assumeing p1 is not dominated
        for j, p2 in enumerate(data):  # go over every dataset point in a loop again
            if i != j and is_dominated(p1, p2):  # Checking if p1 is dominated by p2
                dominated = True  # If p1 is dominated, seting dominated to True
                break  # Exiting the inner loop as we found p1 is dominated
        if not dominated:  # If p1 is not dominated by any point
            skyline.append(p1)  # Including P1 in the list of skylines
    return skyline

def main_sequential_scan(filename):
    """Carries out the skyline search in a sequential scan manner while tracking execution time.."""
    data = read_dataset(filename)  # obtaining the dataset from the file
    start_time = time.time()  # Capturing the start time
    skyline = sequential_scan_skyline(data)  # Identifying the skyline points
    end_time = time.time()  # Capturing the end time
    execution_time = end_time - start_time  # Calculating the execution time
    return skyline, execution_time

### Task 2.2: BBS Skyline Algorithm with R-tree ###

class Node:
    def __init__(self):
        """Initializes a new node with default values."""
        self.child_nodes = []  # storing child nodes (used in internal nodes)
        self.data_points = []  # storing data points (used in leaf nodes)
        self.skyline_points = []  # storing skyline points
        self.parent = None  # Reference to the parent node
        self.MBR = {  # Minimum Bounding Rectangle (MBR) defining the node's boundary
            'x1': -1,
            'y1': -1,
            'x2': -1,
            'y2': -1,
        }

    def perimeter(self):
        """determines the node's MBR perimeter"""
        return (self.MBR['x2'] - self.MBR['x1']) + (self.MBR['y2'] - self.MBR['y1'])

    def is_overflow(self):
        """determines if the node's capacity is exceeded."""
        if self.is_leaf():
            return len(self.data_points) > B
        else:
            return len(self.child_nodes) > B

    def is_root(self):
        """determines if the node is the root node."""
        return self.parent is None

    def is_leaf(self):
        """determines if the node is a leaf node. """
        return len(self.child_nodes) == 0

class RTree:
    def __init__(self):
        """starts the R-tree with an empty set of data points and a root node."""
        self.root = Node()  # starts the R-tree by  adding a root node
        self.data_points = []  # List to store data points

    def insert(self, u, p):
        """adds a point, beginning at node u, to the R-tree."""
        if u.is_leaf():
            self.add_data_point(u, p)  # Adding data point to leaf node
            if u.is_overflow():
                self.handle_overflow(u)  # Managing excess if the node is larger than its capacity
        else:
            v = self.choose_subtree(u, p)  # Selecting the optimal subtree for insertion
            self.insert(v, p)  # Inserting the point into the subtree recursively
            self.update_mbr(v)  # Updating the MBR of the node

    def choose_subtree(self, u, p):
        """based on the least perimeter increase, selects the optimal subtree for insertion."""
        if u.is_leaf():
            return u
        else:
            min_increase = sys.maxsize
            best_child = None
            for child in u.child_nodes:  # going around each of the child nodes
                increase = self.peri_increase(child, p)  # Figuring out the increase in perimeter
                if min_increase > increase:
                    min_increase = increase
                    best_child = child
            return best_child

    def peri_increase(self, node, p):
        """determines how much the perimeter will grow if point p is added to the node's MBR. """
        origin_mbr = node.MBR
        x1, x2, y1, y2 = origin_mbr['x1'], origin_mbr['x2'], origin_mbr['y1'], origin_mbr['y2']
        # Finding the new perimeter when point p is added
        increase = (max([x1, x2, p['x']]) - min([x1, x2, p['x']]) +
                    max([y1, y2, p['y']]) - min([y1, y2, p['y']])) - node.perimeter()
        return increase

    def handle_overflow(self, u):
        """Handles node overflow by splitting the node and putting forward changes up the tree."""
        u1, u2 = self.split(u)  # dividing the node into two
        if u.is_root():
            new_root = Node()  # Creating a new root node
            self.add_child(new_root, u1)  # Adding the split nodes as children of the new root
            self.add_child(new_root, u2)
            self.root = new_root  # Updating the root
            self.update_mbr(new_root)  # Updating the MBR of the new root
        else:
            w = u.parent
            w.child_nodes.remove(u)  # Removing the old node from its parent
            self.add_child(w, u1)  # Adding the split nodes as children of the old node's parent
            self.add_child(w, u2)
            if w.is_overflow():
                self.handle_overflow(w)  # If necessary, recursively managing overflow

    def split(self, u):
        """divides a node in half according to how the data points or child nodes are sorted."""
        best_s1 = Node()
        best_s2 = Node()
        best_perimeter = sys.maxsize

        if u.is_leaf():
            m = len(u.data_points)
            divides = [sorted(u.data_points, key=lambda dp: dp['x']),  # Sorting points by x-coordinate
                       sorted(u.data_points, key=lambda dp: dp['y'])]  # Sorting points by y-coordinate
            for divide in divides:  # Trying split based on both x and y coordinates
                for i in range(math.ceil(0.4 * B), m - math.ceil(0.4 * B) + 1):
                    s1 = Node()
                    s1.data_points = divide[0: i]  # First half of the points
                    self.update_mbr(s1)
                    s2 = Node()
                    s2.data_points = divide[i: len(divide)]  # Second half of the points
                    self.update_mbr(s2)
                    # Choosing the split with the minimum combined perimeter
                    if best_perimeter > s1.perimeter() + s2.perimeter():
                        best_perimeter = s1.perimeter() + s2.perimeter()
                        best_s1 = s1
                        best_s2 = s2
        else:
            m = len(u.child_nodes)
            divides = [sorted(u.child_nodes, key=lambda cn: cn.MBR['x1']),  # Sorting child nodes by their MBR's x1
                       sorted(u.child_nodes, key=lambda cn: cn.MBR['x2']),  # Sorting child nodes by their MBR's x2
                       sorted(u.child_nodes, key=lambda cn: cn.MBR['y1']),  # Sorting child nodes by their MBR's y1
                       sorted(u.child_nodes, key=lambda cn: cn.MBR['y2'])]  # Sorting child nodes by their MBR's y2
            for divide in divides:  # Trying split based on each coordinate
                for i in range(math.ceil(0.4 * B), m - math.ceil(0.4 * B) + 1):
                    s1 = Node()
                    s1.child_nodes = divide[0: i]  # First half of the child nodes
                    self.update_mbr(s1)
                    s2 = Node()
                    s2.child_nodes = divide[i: len(divide)]  # Other half of the child nodes
                    self.update_mbr(s2)
                    # Choosing the split with the minimum combined perimeter
                    if best_perimeter > s1.perimeter() + s2.perimeter():
                        best_perimeter = s1.perimeter() + s2.perimeter()
                        best_s1 = s1
                        best_s2 = s2

        # Updating parent references 
        for child in best_s1.child_nodes:
            child.parent = best_s1
        for child in best_s2.child_nodes:
            child.parent = best_s2

        return best_s1, best_s2

    def add_child(self, node, child):
        """updates the parent node's MBR and adds a child node to it."""
        node.child_nodes.append(child)
        child.parent = node
        self.update_mbr(node)

    def add_data_point(self, node, data_point):
        """updates the parent node's MBR and adds a data point to it. """
        node.data_points.append(data_point)
        self.update_mbr(node)

    def update_mbr(self, node):
        """ modifies a node's MBR according to its data points or child nodes. """
        if node.is_leaf():
            x_list = [dp['x'] for dp in node.data_points]
            y_list = [dp['y'] for dp in node.data_points]
        else:
            x_list = [child.MBR['x1'] for child in node.child_nodes] + [child.MBR['x2'] for child in node.child_nodes]
            y_list = [child.MBR['y1'] for child in node.child_nodes] + [child.MBR['y2'] for child in node.child_nodes]

        node.MBR = {
            'x1': min(x_list),
            'x2': max(x_list),
            'y1': min(y_list),
            'y2': max(y_list)
        }

    def read_dataset(self, filename):
        """reads the dataset from a file and adds it to the list of data points. """
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) != 3:
                    continue
                point = {
                    'id': int(parts[0]),
                    'x': float(parts[1]),
                    'y': float(parts[2])
                }
                self.data_points.append(point)

    def build_rtree(self):
        """ Builds the R-tree by inserting all data points. """
        for point in self.data_points:
            self.insert(self.root, point)

    def rtree_skyline(self):
        """Computes the skyline using the R-tree. """
        rtree_skyline = []
        for point in self.data_points:  # recurring each data point
            dominated = False
            to_remove = []
            for skyline_point in rtree_skyline:  # Lrecurring each point in the current skyline
                if point['x'] >= skyline_point['x'] and point['y'] >= skyline_point['y']:
                    to_remove.append(skyline_point)  # If the skyline is dominated, marking it for removed
                elif point['x'] <= skyline_point['x'] and point['y'] <= skyline_point['y']:
                    dominated = True  # Marking the point as dominated
                    break
            if not dominated:
                rtree_skyline = [sp for sp in rtree_skyline if sp not in to_remove]  # Removing the dominated points
                rtree_skyline.append(point.copy())  # Adding the skyline point
        return rtree_skyline

    def bbs_skyline(self):
        """Computes the skyline using the Branch and Bound Skyline (BBS) algorithm. """
        start = time.time()  # Recording the time
        bbs_skyline = self.rtree_skyline()  # Computing the skyline using the R-tree
        bbs_time = time.time() - start  # Calculating the time taken by the algorithm
        return bbs_skyline, bbs_time

### Task 2.3: BBS with Divide-and-Conquer ###

def divide_dataset(data_points, dimension='x'):
    """Divides the dataset into two subspaces based on the median ."""
    data_points.sort(key=lambda p: p[dimension])  # Sorting data points 
    median_index = len(data_points) // 2  # Finding the median index
    return data_points[:median_index], data_points[median_index:]  # Spliting into two subspaces

def combine_skyline(skyline1, skyline2):
    """ Combines the skyline results from two subspaces using 1D dominance screening."""
    combined_skyline = skyline1.copy()  # Starting with first skyline
    for point in skyline2:  # Looping through each point in second skyline
        dominated = False
        to_remove = []
        for skyline_point in combined_skyline:  # Looping through each point in the combined skyline
            if point['x'] >= skyline_point['x'] and point['y'] >= skyline_point['y']:
                to_remove.append(skyline_point)  # Marking the skyline point for removal if dominated
            elif point['x'] <= skyline_point['x'] and point['y'] <= skyline_point['y']:
                dominated = True  # Marking the point as dominated
                break
        if not dominated:
            combined_skyline = [sp for sp in combined_skyline if sp not in to_remove]  # Removing dominated points
            combined_skyline.append(point.copy())  # Adding the new skyline point
    return combined_skyline


### Main Function ###

def main():
    dataset_filename = "city1.txt"  
    
    # Task 2.1: Sequential Scan
    skyline1, execution_time1 = main_sequential_scan(dataset_filename)  # Executing the sequential scan skyline search
    save_task_2_1_results(skyline1, execution_time1)
    
    # Task 2.2: BBS Skyline with R-tree
    rtree = RTree()
    rtree.read_dataset(dataset_filename)
    rtree.build_rtree()  # Building the R-tree from the dataset
    bbs_skyline, bbs_time = rtree.bbs_skyline()  # Computing the BBS skyline and measure the time
    save_task_2_2_results(bbs_skyline, bbs_time)

    # Task 2.3: BBS with Divide-and-Conquer
    rtree1 = RTree()
    rtree2 = RTree()
    
    rtree1.read_dataset(dataset_filename)  # Reading the dataset in rtree1
    subspace1, subspace2 = divide_dataset(rtree1.data_points)  # Dividing the dataset in two subspaces
    
    rtree1.data_points = subspace1  # Assigning the first subspace in rtree1
    rtree2.data_points = subspace2  # Assigning the second subspace in rtree2
    
    rtree1.build_rtree()  # Building R-tree for the first subspace
    rtree2.build_rtree()  # Building R-tree for the second subspace

    start_time= time.time()
    skyline1_dc, _ = rtree1.bbs_skyline()  # Computing the BBS skyline for the first subspace
    skyline2_dc, _ = rtree2.bbs_skyline()  # Computing the BBS skyline for the second subspace
    combined_skyline = combine_skyline(skyline1_dc, skyline2_dc)  # Combining  the skylines from both subspaces
    bbs_dc_time = time.time() - start_time  # Calculating the time taken for the skyline computation
    save_task_2_3_results(combined_skyline, bbs_dc_time)

def save_task_2_1_results(skyline1, execution_time1):
    with open("task2.1.txt", 'w') as file:
        file.write("Sequential Scan Skyline Points:\n")
        file.write("ID x y\n")
        for point in skyline1:
            file.write(f"{point[0]} {point[1]} {point[2]}\n")
        file.write(f"Execution Time (Sequential Scan): {execution_time1} seconds\n")

def save_task_2_2_results(bbs_skyline, bbs_time):
    with open("task2.2.txt", 'w') as file:
        file.write("BBS Skyline Points:\n")
        file.write("ID x y\n")
        for point in bbs_skyline:
            file.write(f"{point['id']} {point['x']} {point['y']}\n")
        file.write(f"BBS Skyline Computation Time: {bbs_time} seconds\n")

def save_task_2_3_results(combined_skyline, bbs_dc_time):
    with open("task2.3.txt", 'w') as file:
        sorted_skyline = sorted(combined_skyline, key=lambda x: x['id'])
        file.write("BBS Skyline Points with Divide-and-Conquer:\n")
        file.write("ID x y\n")
        for point in sorted_skyline:
            file.write(f"{point['id']} {point['x']} {point['y']}\n")
        file.write(f"Skyline Computation Time (Divide-and-Conquer): {bbs_dc_time} seconds\n")

if __name__ == "__main__":
    main()
