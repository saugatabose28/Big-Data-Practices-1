import numpy as np


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
result = {} #https://stackoverflow.com/questions/5230874/what-is-the-difference-between-and-in-python
result["p1"] = points[0]['id'] 
result["p2"] = points[1]['id']
x_length_init=abs(points[0]['x']-points[1]['x'])
y_length_init=abs(points[0]['y']-points[1]['y'])
result["distance"] = np.sqrt((x_length_init)**2+(y_length_init)**2) #the initial distance between the first pair of data points, https://pythonexamples.org/numpy-sqrt-find-square-root-of-numbers/
print('The initial distance is',result)


    
for i in range(0,n-1):
    for j in range(i+1, n): #check each pair of data points by using two for loops
        x_length=abs(points[j]['x']-points[i]['x'])
        y_length=abs(points[j]['y']-points[i]['y'])
        distance = np.sqrt((x_length)**2+(y_length)**2)
        if distance < result["distance"]: #finding the pair with the minimal distance
            result["p1"] = points[i]['id']
            result["p2"] = points[j]['id']
            result["distance"] = distance
print ('The closest pair is',result)