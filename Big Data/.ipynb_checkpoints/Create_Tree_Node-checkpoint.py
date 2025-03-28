
import math #https://docs.python.org/3/library/math.html


def main(): #https://www.guru99.com/learn-python-main-function-with-examples-understand-main.html
    points = []
    n=0
    with open("dataset_test_v2.txt", 'r') as dataset: #https://www.w3schools.com/python/ref_file_readlines.asp
        for data in dataset.readlines():
            data = data.split() #https://www.w3schools.com/python/ref_string_split.asp
            points.append({ #https://www.w3schools.com/python/ref_list_append.asp
                'id': int(data[0]),
                'x': int(data[1]),
                'y': int(data[2])
                   })
            print ("id=",(points[n]['id']), "x=", (points[n]['x']), "y=", (points[n]['y']))
        #https://stackoverflow.com/questions/17153779/how-can-i-print-variable-and-string-on-same-line-in-python
            n=n+1

    # build R-Tree
    rtree = RTree()
    print("build R-Tree: ")
    
    for point in points:
        rtree.insert(rtree.root, point)
    print (rtree.root.MBR)

# load data from query file -- Think about how to do it based on the above data structure of loading points.

class Node(object): #node class
    def __init__(self): #https://www.w3schools.com/python/python_classes.asp
        self.id = 0
        # for internal nodes
        self.child_nodes = [] #save all the child nodes if it has
        # for leaf nodes
        self.data_points = [] #save the data points included in a node
        self.parent = None # initial value of parent
        self.MBR = { 
            'x1': -1,   #initial value of MBR
            'y1': -1,
            'x2': -1,
            'y2': -1,
        }


class RTree(object):
    def __init__(self):
        self.root = Node()
    def insert(self, u, p):
        self.add_data_point(u, p)
        self.update_mbr(u)


    def add_data_point(self, node, data_point): #add data point into an MBR
        node.data_points.append(data_point)


    def update_mbr(self, node):
        x_list = []
        y_list = []
        x_list = [point['x'] for point in node.data_points]
        y_list = [point['y'] for point in node.data_points]
        
        new_mbr = {
            'x1': min(x_list),
            'x2': max(x_list),
            'y1': min(y_list),
            'y2': max(y_list)
        }
        node.MBR = new_mbr




if __name__ == '__main__': #call the main function. https://www.guru99.com/learn-python-main-function-with-examples-understand-main.html
    main()

