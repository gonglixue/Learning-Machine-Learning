from math import sqrt
from PIL import Image,ImageDraw
def readfile(filename):
	data = open(filename)
	lines = [line for line in data]

	#first row is word
	colnames = lines[0].split('\t')[1:]
	rownames=[]
	data = []
	for line in lines[1:]:
		p = line.split('\t')
		rownames.append(p[0])
		# the rest is the actual data
		data.append([float(x) for x in p[1:]])
	return rownames, colnames, data

def pearson(v1,v2):
	sum1 = sum(v1)
	sum2 = sum(v2)

	sum1Sq = sum([pow(v,2) for v in v1])
	sum2Sq = sum([pow(v,2) for v in v2])

	pSum = sum([v1[i]*v2[i] for i in range(len(v1))])

	#calculate r
	num = pSum - (sum1*sum2 / len(v1))
	den = sqrt((sum1Sq - pow(sum1,2)/len(v1)) * (sum2Sq - pow(sum2,2)/len(v1)))
	if den==0:
		return 0
	else:
		return 1.0 - num/den

class bicluster:
	def __init__(self, vec, left=None, right=None, distance=0.0, ID=None):
		self.left = left
		self.right = right
		self.vec = vec
		self.ID = ID
		self.distance = distance


def hcluster(rows, distance=pearson):
	distances={}
	currentclusterid = -1

	# initially, all clusters are rows in data set
	clust = [bicluster(rows[i], ID=i) for i in range(len(rows))]

	while len(clust)>1:
		lowestpair=(0,1) # point out the first pair to calculate a initial distance
		closest = distance(clust[0].vec, clust[1].vec)

		#traverse every pair to find one pair with the minimum distance
		for i in range(len(clust)):
			for j in range(i+1, len(clust)):
				if (clust[i].ID, clust[j].ID) not in distances:
					distances[(clust[i].ID, clust[j].ID)] = distance(clust[i].vec, clust[j].vec)

				d = distances[(clust[i].ID, clust[j].ID)]
				if d < closest:
					closest = d
					lowestpair = (i,j)

		# calculate the average of the lowestpair
		mergevec = [
		(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i])/2.0
		for i in range(len(clust[0].vec))
		]

		# set up a new clust
		newcluster = bicluster(mergevec, left=clust[lowestpair[0]], right=clust[lowestpair[1]], distance=closest, ID=currentclusterid)

		currentclusterid -= 1
		del clust[lowestpair[1]]
		del clust[lowestpair[0]]
		clust.append(newcluster)

	return clust[0]

def printclust(clust, labels=None, n=0):
	for i in range(n):
		print(' ',end='')
	if clust.ID < 0:
		print('-')
	else:
		if labels==None:
			print(clust.ID)
		else:
			print(labels[clust.ID])

	if clust.left!=None:
		printclust(clust.left, labels=labels, n=n+1)
	if clust.right!=None:
		printclust(clust.right, labels=labels, n=n+1)

def getheight(clust):
	if clust.left==None and clust.right==None:
		return 1
	else:
		return getheight(clust.left) + getheight(clust.right)

def getdepth(clust):
	if clust.left==None and clust.right==None:
		return 0
	else:
		return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance

def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
	h = getheight(clust) * 20
	w = 1200
	depth = getdepth(clust)

	scaling = float(w-150)/depth

	img = Image.new('RGB',(w,h),(255,255,255))
	draw=ImageDraw.Draw(img)

	draw.line((0,h/2,10,h/2), fill=(255,0,0))
	drawnode(draw,clust,10,(h/2),scaling,labels)
	img.save(jpeg,'JPEG')

def drawnode(draw, clust, x,y, scaling, labels):
	if clust.ID<0:
		h1 = getheight(clust.left)*20
		h2 = getheight(clust.right)*20
		top = y-(h1+h2)/2
		bottom=y+(h1+h2)/2
		# length of line
		ll = clust.distance*scaling
		draw.line((x,top+h1/2,x,bottom-h2/2), fill=(255,0,0))
		draw.line((x,top+h1/2,x+ll,top+h1/2), fill=(255,0,0))
		draw.line((x,bottom-h2/2,x+ll,bottom-h2/2), fill=(255,0,0))

		drawnode(draw, clust.left, x+ll, top+h1/2, scaling, labels)
		drawnode(draw, clust.right, x+ll, bottom-h2/2, scaling,labels)
	else:
		draw.text((x+5,y-7), labels[clust.ID], (0,0,0))

if __name__ == '__main__':
	articlenames, words, data = readfile('articledata.txt')
	clust = hcluster(data)
	printclust(clust,labels=articlenames)
	drawdendrogram(clust,articlenames,jpeg='articleclust.jpg')
