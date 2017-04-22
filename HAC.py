"""
CPEG457
Carlton Brady
Assignment #2:  Bayes Rule, Text Processing and Clustering
3. Implementing the Hierarchical Agglomerative Clustering (HAC) algorithm [50
points]
Due: 4/21/2017

Notes: this is implemented in a very niave fashion, ignoring efficiency in favor of simplicity. 

**USING COMPLETE LINK SIMILARITY**
"""

def write_output(fname, to_write):
	"""Writes (appends) the parameter to_write to the file called fname"""
	fobj = open(fname, "a")
	fobj.write(to_write)
	fobj.close()

def read_sets_file(fname):
	"""Read all the coordinates from the file and place them into a list of 
	2 element lists, each element being a set of x,y coordinates.
	Returns the list of coordinates"""
	result = []
	fobj = open(fname, "r")
	#Read the coordinates one line at a time
	for line in fobj:
		i=0
		x=""
		while (i < len(line)):
			if(line[i] == "\t"):
				break
			x += line[i]
			i+=1
		j=i+1
		y=""
		while (j < len(line)):
			if(line[j] == "\n"):
				break
			y += line[j]
			j+=1
		result.append([[x,y]])
	fobj.close()
	#Change the type of the coordinates to be float
	for lst in result:
		for i, coordinate in enumerate(lst):
			#Initially, each coordinate is a singleton cluster
			coordinate[0] = float(coordinate[0])
			coordinate[1] = float(coordinate[1])
			#print(type(coordinate[0]))
	return result

def compute_distance(p1,p2):
	"""Computes the distance between 2 points that are represented
	by x and y coordinates. Returns the distance as a float."""
	return ( ((p2[0]-p1[0])**2) + ((p2[1]-p1[0])**2) )**.5

def complete_link_similarity(c1,c2):
	"""Given 2 clusters, compute the distance between the 2 farthest points
	in each cluster. A cluster is a list of x,y coordinates, i.e. [[x,y],[x1,y1]]
	Note: a smaller number means the clusters are more similar"""
	#initially, the farthest distance between any two points in each cluster is minimized
	farthest = float("-inf")
	for point1 in c1:
		for point2 in c2:
			if(compute_distance(point1,point2)>farthest):
				farthest = compute_distance(point1,point2)
	return farthest

def best_merge(all_clusters):
	"""given a list of clusters, determine which 2 have the optimal complete link similarity
	(this means the smallest distance between the 2 points that are farthest from eachother for a given cluster combo), 
	merge those 2 clusters,
	and update the list accordingly"""
	#Initially, the best merge is between 2 clusters that are infintely dissimilar
	best = float("inf")
	#best_c1 and best_c2 are the 2 clusters involved in the best merge
	best_c1 = [[]]
	best_c2 = [[]]
	#merged is the new cluster that is the result of merging the two clusters involved in the optimal merged 
	merged = []
	i = 0
	j = 0
	#Check the complete link similarity of all cluster combos
	while i < len(all_clusters):
		j = i+1
		while j < len(all_clusters):
			if((complete_link_similarity(all_clusters[i], all_clusters[j]) < best) and (all_clusters[i] != all_clusters [j])):
					best = complete_link_similarity(all_clusters[i], all_clusters[j])
					best_c1 = all_clusters[i]
					best_c2 = all_clusters[j]
					temp_i = i
					temp_j = j
			j = j + 1
		i = i + 1
	print("Complete link similarity for optimal merge: " + str(best) + "\n")
	del(all_clusters[temp_i])

	if(temp_i<temp_j):
		del(all_clusters[temp_j-1])
	else:
		del(all_clusters[temp_j])

	for point in best_c1:
		merged.append(point)
	for point in best_c2:
		merged.append(point)
	all_clusters.append(merged)
	return all_clusters

def num_points(clusters):
	"""returns the number of points in a list of clusters, where each cluster is a list of points"""
	count = 0
	for c in clusters:
		for pt in c:
			count = count+1
	return count

def write_clusters(fname, clusters):
	"""writes the list of clusters to output file fnam in the form of 3 columns: x    y    cluster number"""
	#clear the file first
	fobj = open(fname, "w")
	fobj.write("")
	fobj.close()
	i = 0
	for c in clusters:
		for pts in c:
			write_output(fname, str(pts[0]) + "\t" + str(pts[1]) + "\t" + "cluster: " + str(i+1) + "\n")
		i += 1

def main():
	sets = read_sets_file("point_sets.txt") # <--- To operate on a different file of the same format, change the parameter passed to read_sets_file
	num_clusters = len(sets)
	#Merge until there are 3 clusters left
	while num_clusters > 3:
		best_merge(sets)
		num_clusters = len(sets)
		print("Number of clusters: " + str(num_clusters))

	print("Writing clusters to HAC_output.txt")
	write_clusters("HAC_output.txt",sets)
	print("Clustering complete")

#Run it
main()