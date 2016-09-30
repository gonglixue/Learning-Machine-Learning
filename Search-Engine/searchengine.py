class crawler:
	def __init__(self, dbname):
		pass

	def __del__(self):
		pass

	def dbcommit(self):
		pass

	#get the entry id, if the id does not exist than add it to db
	def getentryid(self, table, field, value, createnew=True):
		return None

	# 
	def addtoindex(self, url, soup):
		print('Indexing %s' % url)

	#
	def gettextonly(self, soup):
		return None

	def separatewords(self, text):
		return None

	def isindexed(self, url):
		return False

	def addlinkrel(self, urlFrom, urlTo, linkText):
		pass

	def crawl(self, pages, depth=2):
		pass

	def createindextables(self):
		pass
