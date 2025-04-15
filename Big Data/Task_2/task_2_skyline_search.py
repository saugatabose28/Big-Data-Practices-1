import sys
import math
import time

# Initialize B value for rtree
B = 4

def read_file(filename):
    points = [] # Define list of points to store point data
    with open(filename, 'r') as dataset: # Open file to read

        # Iterate over every line in the file
        for data in dataset.readlines():
            data = data.split()  # Split the line into components

            # Define point as a dictionary with 'id', 'x' and 'y' keys
            point = {
                'id': int(data[0]),
                'x': float(data[1]),
                'y': float(data[2])
            }
            points.append(point) # Add point to the points list
    return points

def sequential_search(data):
    start = time.time() # Start timing the function
    skyline = [] # Skyline List to contain points that are not dominated
    n = len(data) # Determine the number of points in the dataset

    # Iterate over all points in the data
    for i in range(n):
        current_point = data[i] # Current point being considered for the skyline
        dominated = False # Flag to check if the current point is dominated by any other point

        # Compare current point with all other points to check for dominance
        for j in range(n):
            other_point = data[j] # Point against which the current point is compared
            # Check if the current point is dominated by the other point
            if i!=j and current_point['x'] >= other_point['x'] and current_point['y'] >= other_point['y']:
                dominated = True
                break # Exit the inner loop if current point is found to be dominated

        # If not dominated by any other points, add to skyline
        if not dominated:
            skyline.append(data[i])

    end = time.time()  # End timing the function
    exec_time = end - start  # Calculate the execution time
    return skyline, exec_time  # Return both the results and the execution times

def dominated_by_skyline(q, skylines):
    is_dominate = False # Flag to check if the current node(MBR)/point is dominated by any skylines
    n = len(skylines) # Determine the number of skylines

    # In case that check object is a node, using x1, y1 of MBR to check if it is dominated by any skyline or not
    if  q['type'] == "node":
        node = q['obj']
        for skyline in skylines:
            if node.MBR['x1'] >= skyline['x'] and node.MBR['y1'] >= skyline['y']:
                is_dominate = True
                break

    # In case that check object is a point, using x, y of the point to check if it is dominated by any skyline or not
    elif  q['type'] == "point":
        point = q['obj']
        for skyline in skylines:
            if point['x'] >= skyline['x'] and point['y'] >= skyline['y']:
                is_dominate = True
                break

    return is_dominate

def construct_rtree(data):
    rtree = RTree()
    print("Building the R-Tree: Please wait...\n")
    for point in data:
        rtree.insert(rtree.root, point)
    print("Done with building RTree")
    return rtree

def bbs_skyline(data):

    # Start constructing rtree from input data (points)
    rtree = construct_rtree(data)
    start = time.time() # Start time of processing branch and bound (after done constructing rtree)

    # Initialize H list, skyline list, root node, min_dist
    H = []
    skyline = []
    rootnode = rtree.root
    min_dist = math.sqrt((rootnode.MBR['x1']**2) + (rootnode.MBR['y1']**2))

    # Append root node to H list as a dict object
    H.append({'type': "node", 'obj': rtree.root, 'min_dist': min_dist})

    # Loop until H list is empty
    while len(H)> 0:
        q = H.pop(0)  # Pop the first element after sorting

        # If current element is a point that is not dominated by any skylines, add the point to skyline list
        if q['type'] == "point" and (len(skyline) == 0 or not dominated_by_skyline(q, skyline)):
            skyline.append(q['obj'])
        
        # If current element is a point that is not dominated by any skylines
        elif q['type'] == "node" and not dominated_by_skyline(q, skyline):
            current_node = q['obj']

            # If it is a leaf node, add all points to H list
            if current_node.is_leaf():
                for point in current_node.data_points:
                    min_dist = math.sqrt(point['x']**2 + point['y']**2) # Calculate min_dist
                    H.append({'type': "point", 'obj': point, 'min_dist': min_dist})

            # If it is not a leaf node, add all child nodes to H list
            else:
                for child in current_node.child_nodes:
                    min_dist = math.sqrt((child.MBR['x1']**2) + (child.MBR['y1']**2)) # Calculate min_dist
                    H.append({'type': "node", 'obj': child, 'min_dist': min_dist})

            # Sort H list by min_dist
            H = sorted(H, key=lambda x: x['min_dist'])

    exec_time = time.time() - start # Calculate the execution time for searching skylines with branch and bound
    return skyline, exec_time # Return both skylines and the execution time

def myFunc(e):
  # return value in key 'x' of dictionary
  return e['x']

def bbs_skyline_with_divide_and_conquer(data):

    start = time.time() # start time of divide-and-conquer part

    n = len(data) # Determine the number of data
    data.sort(key=myFunc) # Sort by x

    midpoint = n // 2  # Calculate the midpoint using integer division

    points_left = data[:midpoint]  # First half of the list
    points_right = data[midpoint:]  # Assign leftover data (which are on the right side of divide line) to right group

    end = time.time() # end of divide-and-conquer part
    exec_time_divide_and_conquer = end - start # execution time of divide-and-conquer part

    skyline_left,exec_time_left = bbs_skyline(points_left) # find skyline of left group by branch and bound
    skyline_right,exec_time_right= bbs_skyline(points_right) # find skyline of right group by branch and bound

    start = time.time() # start time of sequential search part combining left and right side

    # Combine results from both left and right side, and find final skyline with 1D screening method
    skyline_combine = skyline_left + skyline_right

    # Sort results from both side by x ascendingly, if x are equal, then sort by y asc
    skyline_combine.sort(key=lambda point: (point['x'], point['y']))

    # Define a list to store final skylines
    skyline_final = []

    # Start with the highest possible y
    min_y = 999999999999

    # Find final skylines with 1D screening method
    for point in skyline_combine: # Loop over sorted the list of combined results from left and right side
        # If any point has smaller 'y' than min_y, add that point to skyline and replaced min_y with the point's 'y'
        if point['y'] < min_y: 
            skyline_final.append(point)
            min_y = point['y']


    end = time.time() # end of sequential search part combining left and right side

    # Calculate final exectution time
    # included used in side division, search time of both sides and time used in 1d screening
    # not included time used in constructing rtree
    final_exec_time = end - start + exec_time_divide_and_conquer + exec_time_left + exec_time_right

    return skyline_final, final_exec_time # Return both final skylines and the execution time

def write_output(title, results, exec_time, filename):
    # Write output to file
    with open(filename, 'a') as file:
        file.write(f"{title}\n")
        for point in results:
            triplet = f"{point['id']} {point['x']} {point['y']}\n"
            file.write(triplet)
        file.write(f"execution time: {exec_time}\n\n")


class Node(object): #node class
    def __init__(self):
        self.id = 0
        # for internal nodes
        self.child_nodes = []
        # for leaf nodes
        self.data_points = []
        self.parent = None
        self.MBR = {
            'x1': -1,
            'y1': -1,
            'x2': -1,
            'y2': -1,
        }
    def perimeter(self):
        # only calculate the half perimeter here
        return (self.MBR['x2'] - self.MBR['x1']) + (self.MBR['y2'] - self.MBR['y1'])

    def is_overflow(self):
        if self.is_leaf():
            if self.data_points.__len__() > B: #Checking overflows of data points, B is the upper bound.
                return True
            else:
                return False
        else:
            if self.child_nodes.__len__() > B: #Checking overflows of child nodes, B is the upper bound.
                return True
            else:
                return False

    def is_root(self):
        if self.parent is None:
            return True
        else:
            return False

    def is_leaf(self):
        if self.child_nodes.__len__() == 0:
            return True
        else:
            return False

class RTree(object): #R tree class
    def __init__(self):
        self.root = Node() #Create a root

    def query(self, node, query): #run to answer the query
        num = 0
        if node.is_leaf(): #check if a data point is included in a leaf node
            for point in node.data_points:
                if self.is_covered(point, query):
                    num = num + 1
            return num
        else:
            for child in node.child_nodes: #If it is an MBR, check all the child nodes to see whether there is an interaction
                if self.is_intersect(child, query): #If there is an interaction, keep continue to check the child nodes in the next layer till the leaf nodes
                    num = num + self.query(child, query)
            return num
        

    def is_covered(self, point, query):
        x1, x2, y1, y2 = query['x1'], query['x2'], query['y1'], query['y2']
        if x1 <= point['x'] <= x2 and y1 <= point['y'] <= y2:
            return True
        else:
            return False    

    def is_intersect(self, node, query):
        # if two mbrs are intersected, then:
        center1_x = (node.MBR['x2'] + node.MBR['x1']) / 2
        center1_y = (node.MBR['y2'] + node.MBR['y1']) / 2
        length1 = node.MBR['x2'] - node.MBR['x1']
        width1 = node.MBR['y2'] - node.MBR['y1']
        
        center2_x = (query['x2'] + query['x1']) / 2
        center2_y = (query['y2'] + query['y1']) / 2
        length2 = query['x2'] - query['x1']
        width2 = query['y2'] - query['y1'] 

        if (abs(center1_x - center2_x) <= length1 / 2 + length2 / 2) and (abs(center1_y - center2_y) <= width1 / 2 + width2 / 2):  #we check the absolute value
            return True
        else:
            return False                    


    def insert(self, u, p): # insert p(data point) to u (MBR)
        if u.is_leaf(): 
            self.add_data_point(u, p) #add the data point and update the corresponding MBR
            if u.is_overflow():
                self.handle_overflow(u) #handel overflow for leaf nodes
        else:
            v = self.choose_subtree(u, p) #choose a subtree to insert the data point to miminize the perimeter sum
            self.insert(v, p) #keep continue to check the next layer recursively
            self.update_mbr(v) #update the MBR for inserting the data point

    def choose_subtree(self, u, p): 
        if u.is_leaf(): #find the leaf and insert the data point
            return u
        else:
            min_increase = sys.maxsize #set an initial value
            best_child = None
            for child in u.child_nodes: #check each child to find the best node to insert the point 
                if min_increase > self.peri_increase(child, p):
                    min_increase = self.peri_increase(child, p)
                    best_child = child
            return best_child

    def peri_increase(self, node, p): # calculate the increase of the perimeter after inserting the new data point
        # new perimeter - original perimeter = increase of perimeter
        origin_mbr = node.MBR
        x1, x2, y1, y2 = origin_mbr['x1'], origin_mbr['x2'], origin_mbr['y1'], origin_mbr['y2']
        increase = (max([x1, x2, p['x']]) - min([x1, x2, p['x']]) +
                    max([y1, y2, p['y']]) - min([y1, y2, p['y']])) - node.perimeter()
        return increase


    def handle_overflow(self, u):
        u1, u2 = self.split(u) #u1 u2 are the two splits returned by the function "split"
        # if u is root, create a new root with s1 and s2 as its' children
        if u.is_root():
            new_root = Node()
            self.add_child(new_root, u1)
            self.add_child(new_root, u2)
            self.root = new_root
            self.update_mbr(new_root)
        # if u is not root, delete u, and set s1 and s2 as u's parent's new children
        else:
            w = u.parent
            # copy the information of s1 into u
            w.child_nodes.remove(u)
            self.add_child(w, u1) #link the two splits and update the corresponding MBR
            self.add_child(w, u2)
            if w.is_overflow(): #check the parent node recursively
                self.handle_overflow(w)
            
    def split(self, u):
        # split u into s1 and s2
        best_s1 = Node()
        best_s2 = Node()
        best_perimeter = sys.maxsize
        # u is a leaf node
        if u.is_leaf():
            m = u.data_points.__len__()
            # create two different kinds of divides
            divides = [sorted(u.data_points, key=lambda data_point: data_point['x']),
                       sorted(u.data_points, key=lambda data_point: data_point['y'])] #sorting the points based on X dimension and Y dimension
            for divide in divides:
                for i in range(math.ceil(0.4 * B), m - math.ceil(0.4 * B) + 1): #check the combinations to find a near-optimal one
                    s1 = Node()
                    s1.data_points = divide[0: i]
                    self.update_mbr(s1)
                    s2 = Node()
                    s2.data_points = divide[i: divide.__len__()]
                    self.update_mbr(s2)
                    if best_perimeter > s1.perimeter() + s2.perimeter(): 
                        best_perimeter = s1.perimeter() + s2.perimeter()
                        best_s1 = s1
                        best_s2 = s2

        # u is an internal node
        else:
            # create four different kinds of divides
            m = u.child_nodes.__len__()
            divides = [sorted(u.child_nodes, key=lambda child_node: child_node.MBR['x1']), #sorting based on MBRs
                       sorted(u.child_nodes, key=lambda child_node: child_node.MBR['x2']),
                       sorted(u.child_nodes, key=lambda child_node: child_node.MBR['y1']),
                       sorted(u.child_nodes, key=lambda child_node: child_node.MBR['y2'])]
            for divide in divides:
                for i in range(math.ceil(0.4 * B), m - math.ceil(0.4 * B) + 1): #check the combinations
                    s1 = Node()
                    s1.child_nodes = divide[0: i]
                    self.update_mbr(s1)
                    s2 = Node()
                    s2.child_nodes = divide[i: divide.__len__()]
                    self.update_mbr(s2)
                    if best_perimeter > s1.perimeter() + s2.perimeter():
                        best_perimeter = s1.perimeter() + s2.perimeter()
                        best_s1 = s1
                        best_s2 = s2

        for child in best_s1.child_nodes:
            child.parent = best_s1
        for child in best_s2.child_nodes:
            child.parent = best_s2

        return best_s1, best_s2


    def add_child(self, node, child):
        node.child_nodes.append(child) #add child nodes to the current parent (node) and update the MBRs. It is used in handeling overflows
        child.parent = node
        if child.MBR['x1'] < node.MBR['x1']:
            node.MBR['x1'] = child.MBR['x1']
        if child.MBR['x2'] > node.MBR['x2']:
            node.MBR['x2'] = child.MBR['x2']
        if child.MBR['y1'] < node.MBR['y1']:
            node.MBR['y1'] = child.MBR['y1']
        if child.MBR['y2'] > node.MBR['y2']:
            node.MBR['y2'] = child.MBR['y2']
    # return the child whose MBR requires the minimum increase in perimeter to cover p

    def add_data_point(self, node, data_point): #add data points and update the the MBRS
        node.data_points.append(data_point)
        if data_point['x'] < node.MBR['x1']:
            node.MBR['x1'] = data_point['x']
        if data_point['x'] > node.MBR['x2']:
            node.MBR['x2'] = data_point['x']
        if data_point['y'] < node.MBR['y1']:
            node.MBR['y1'] = data_point['y']
        if data_point['y'] > node.MBR['y2']:
            node.MBR['y2'] = data_point['y']

    def update_mbr(self, node): #update MBRs when forming a new MBR. It is used in checking the combinations and update the root
        x_list = []
        y_list = []
        if node.is_leaf():
            x_list = [point['x'] for point in node.data_points]
            y_list = [point['y'] for point in node.data_points]
        else:
            x_list = [child.MBR['x1'] for child in node.child_nodes] + [child.MBR['x2'] for child in node.child_nodes]
            y_list = [child.MBR['y1'] for child in node.child_nodes] + [child.MBR['y2'] for child in node.child_nodes]
        new_mbr = {
            'x1': min(x_list),
            'x2': max(x_list),
            'y1': min(y_list),
            'y2': max(y_list)
        }
        node.MBR = new_mbr

if __name__ == '__main__':
    
    filename = "datasets/city1.txt"
    data_points = read_file(filename)
    # task 2.1 skyline search with sequential scan based
    skyline_sq, exec_time_sq = sequential_search(data_points)
    write_output("Result From Sequantial Scan Based Method", skyline_sq, exec_time_sq, "task_2_skyline_result.txt")

    # task 2.2 skyline search with branch and bound algorithm
    skyline_bbs, exec_time_bbs = bbs_skyline(data_points)
    write_output("Result From Branch And Bound Algorithm", skyline_bbs, exec_time_bbs, "task_2_skyline_result.txt")

    # task 2.3 skyline search with divide-and-conquer
    skyline_bbs_with_dc, exec_time_bbs_with_dc = bbs_skyline_with_divide_and_conquer(data_points)
    write_output("Result From BBS With Divide and Conquer", skyline_bbs_with_dc, exec_time_bbs_with_dc, "task_2_skyline_result.txt")