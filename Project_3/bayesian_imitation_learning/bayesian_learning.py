import som
import kmeans

map = som.read_points("q3dm1-path1.csv")
activity_vectors = []

for i in range(len(map)-1):
    activity = map[i+1]-map[i]
    activity_vectors.append(activity.tolist())

print len(activity_vectors)

indexes, centers = kmeans.kmeans(3,activity_vectors)
print indexes
print centers







