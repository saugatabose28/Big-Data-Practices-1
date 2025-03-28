import numpy as np #https://pythonexamples.org/numpy-sqrt-find-square-root-of-numbers/


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

def finding_closest_pair(points): #the function to find the closest pair in the given data points
    k=len(points)
    result = {}
    result["p1"] = points[0]['id']
    result["p2"] = points[1]['id']
    x_length_init=abs(points[0]['x']-points[1]['x'])
    y_length_init=abs(points[0]['y']-points[1]['y'])
    result["distance"] = np.sqrt((x_length_init)**2+(y_length_init)**2)
    #print('The initial distance is',result)
    
    for i in range(0,k-1):
        for j in range(i+1, k):
            x_length=abs(points[j]['x']-points[i]['x'])
            y_length=abs(points[j]['y']-points[i]['y'])
            distance = np.sqrt((x_length)**2+(y_length)**2) #https://pythonexamples.org/numpy-sqrt-find-square-root-of-numbers/
            if distance < result["distance"]:
                result["p1"] = points[i]['id']
                result["p2"] = points[j]['id']
                result["distance"] = distance
    return (result)
    #print ('The closest pair is',result)

def myFunc(e): 
  return e['x']

points.sort(key=myFunc) #https://www.w3schools.com/python/ref_list_sort.asp

divide_line_x=(points[n-1]['x']+points[0]['x'])/2 #the middle cordinate in X dimension for dividing the data space
print('divide_line_x',divide_line_x)
print('\nThe new order of points\n')

for i in range(0,n):
    print ("id=",(points[i]['id']), "x=", (points[i]['x']), "y=", (points[i]['y']))

points_left=[]
for l in range(0,int(n/2)): #the data points included in the left part
    points_left.append({ #https://www.w3schools.com/python/ref_list_append.asp
            'id': int(points[l]['id']),
            'x': int(points[l]['x']),
            'y': int(points[l]['y'])
                   })
print('The left part contains',points_left)

points_right=[]
for r in range(int(n/2),n): # the data points included in the right part
    points_right.append({ #https://www.w3schools.com/python/ref_list_append.asp
            'id': int(points[r]['id']),
            'x': int(points[r]['x']),
            'y': int(points[r]['y'])
                   })
print('The right part contains',points_right)

result_left = finding_closest_pair(points_left) #calculate the pair based on the left part
result_right=finding_closest_pair(points_right) #calculate the pair based on the right part

print('The answer from the left part is', result_left)
print('The answer from the right part is', result_right)

min_distance=min(result_left["distance"], result_right["distance"]) #the minimal distance between the distances delivered based on the left and right parts
print('min_distance',min_distance)
def finding_subset_for_crossing_pairs(points,divide_line,mindistance): #finding the candidate to be used in the further crossing pair processing
    result=[]
    m=len(points)
    print('m',m)
    print('mindistance',mindistance)
    print('divide_line',divide_line)
    for i in range(0,m):
        if abs(points[i]['x']-divide_line)<=mindistance:
            print(abs(points[i]['x']-divide_line))
            result.append({ #https://www.w3schools.com/python/ref_list_append.asp
            'id': int(points[i]['id']),
            'x': int(points[i]['x']),
            'y': int(points[i]['y'])
                   })
    return (result)
            
def finding_the_crossing_pair(subset_left,subset_right,mindistance): #if the subset of the left part and the right part are not empty, we calculate the crossing distance
    result={}
    len_left=len(subset_left)
    len_right=len(subset_right)
    for i in range(0,len_left):
        for j in range (0,len_right):
            x_length=abs(subset_left[j]['x']-subset_right[i]['x'])
            y_length=abs(subset_left[j]['y']-subset_right[j]['y'])
            distance = np.sqrt((x_length)**2+(y_length)**2)
            if distance < mindistance: #if the crossing distance is less than the delived minimal distance
                result["p1"] = subset_left[i]['id']
                result["p2"] = subset_right[j]['id']
                result["distance"] = distance
    return (result)

cross_left=finding_subset_for_crossing_pairs(points_left,divide_line_x,min_distance) #save the subset from the left part
cross_right=finding_subset_for_crossing_pairs(points_right,divide_line_x,min_distance) #save the subset from the right part

print('The left subset for crossing pair',cross_left)
print('The right subset for crossing pair',cross_right)


if cross_left==[] or cross_right==[]: #if there is no candidate in the left or right sub-space
    if result_left["distance"]<=result_right["distance"]:
        print('The final answer of the closest pair is',result_left)
    else:
        print('The final answer of the closest pair is',result_right)
else:
    final_pair=finding_the_crossing_pair(cross_left,cross_right,min_distance) #if we have the candidates, check the crossing pairs


