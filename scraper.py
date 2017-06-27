from lxml import html
import requests
from bs4 import BeautifulSoup
import unicodedata
import json


# page = requests.get('http://www.hearthpwn.com/forums/hearthstone-general/general-discussion/28947-group-therapy-need-to-blow-off-steam-mega-salty?page=1850')
# tree = html.fromstring(page.content)
# comments = tree.xpath('//li[@itemtype="http://schema.org/Comment"]')

# a = 3
# for com in comments:
# 	lst1 = com.xpath('./div[@id="forum-post-body-38783"]')
# 	print(lst1)

# 	# if (len(lst1) != 0):
# 	# 	a = lst1
# 	# 	break

# b = lst1[0].xpath('./p')

# for e in b:
# 	print(e.text)


# url = raw_input('http://www.hearthpwn.com/forums/hearthstone-general/general-discussion/28947-group-therapy-need-to-blow-off-steam-mega-salty?page=1850')

class Comment:
    def __init__(self, comment, commentId, commentDate):
    	self.comment = comment
    	self.commentId = commentId
    	self.commentDate = commentDate

    def __repr__(self):
    	return "Id: " + self.commentId + " Date: " + self.commentDate + " Comment: " + self.comment 	

def parseComment(comment):
	normalized = unicodedata.normalize("NFKD", comment)
	stripped = normalized.replace("\n", " ").replace(","," ").replace(".", " ").strip()
	stripped = ''.join(e for e in stripped if e.isalnum() or e.isspace())
	return stripped

def saveToFile(filename, comments):
	json_string = json.dumps([com.__dict__ for com in comments])
	with open(filename, 'a') as outfile:
		json.dump(json_string, outfile)

def loadFromFile(fileName):
	with open(fileName) as json_data:
		json_string = json.load(json_data)

	objectList = json.loads(json_string)
	for i in range(len(objectList)):
		item = objectList[i]
		objectList[i] = Comment(item['comment'], item['commentId'], item['commentDate'])
	return objectList

def scrape(i):
	r  = requests.get('http://www.hearthpwn.com/forums/hearthstone-general/general-discussion/28947-group-therapy-need-to-blow-off-steam-mega-salty?page=' + str(i))
	data = r.text
	soup = BeautifulSoup(data, "lxml")

	commentList = soup.find_all('li', itemtype="http://schema.org/Comment")
	comments = []

	for elem in commentList:
		comment = elem.find_all('div', class_="j-comment-body forum-post-body u-typography-format text")[0]
		quotes = comment.find_all('blockquote')
		for quote in quotes:
			quote.decompose()
		comment = comment.get_text()
		comment = parseComment(comment)
		commentNumber = elem.find_all('a', class_="j-comment-link")[0].get_text().replace('#','')
		commentDate = elem.find_all('abbr', class_="tip standard-date standard-datetime")[0].get("data-epoch")
		comments.append(Comment(comment, commentNumber, commentDate))

	# for comment in comments:
	# 	print((comment.comment))
	# 	print('\n')

	return comments

def analyze(comments):
	words = {}
	for comment in comments:
		wordList = [word.lower() for word in comment.comment.split()]
		for w in wordList:
			if (w in words):
				words[w] = words[w] + 1
			else:
				words[w] = 1
	return words

def sortComments(comments):
	analyzed = analyze(comments)
	tup = sorted(analyzed.items(), key=lambda x: x[1])
	tup.reverse()
	return tup

def download():
	for i in range(1000, 1800):
		comments = scrape(i)
		saveToFile("comments/" + str(i) + ".json", comments)

def reload():
	totalComments = []
	for i in range(1800, 1850):
		comments = loadFromFile("comments/" + str(i) + ".json")
		totalComments.extend(comments)
	return totalComments



