import feedparser
from email.Utils import formatdate
import re
import cgi

import sys
sys = reload(sys)
sys.setdefaultencoding("utf-8")

class Feed:
	def __init__(self):
		self.feed = feedparser.parse("http://hup.hu/node/feed")

class Node:
	def __init__(self):
		self.title = ""
		self.description = ""
		self.link = ""
		self.pubdate = ""
		self.author = ""

class Rss:
	def __init__(self, start_response, title, link, desc):
		self.start_response = start_response
		self.title = title
		self.desc = desc
		self.link = link
		self.items = []
	
	def output(self):
		ret = []
		ret.append("""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">
<channel>
<title>%s</title>
<description>%s</description>
<link>%s</link>\n""" % (self.title, self.desc, self.link))
		for i in self.items:
			ret.append("""<item>
<title>%s</title>
<description>%s</description>
<link>%s</link>
<pubDate>%s</pubDate>
<dc:creator>%s</dc:creator>
</item>\n""" % (i.title, i.description, i.link, i.pubdate, i.author))
		ret.append("</channel>\n</rss>")
		output = "".join(ret)
		status = '200 OK'
		response_headers = [('Content-type', 'application/xml'),
				('Content-Length', str(len(output)))]
		self.start_response(status, response_headers)
		return output.encode('utf-8')

def application(environ, start_response):
	feed = Feed()
	rss = Rss(start_response, feed.feed.feed.title, feed.feed.feed.links[0].href, feed.feed.feed.subtitle)

	for i in feed.feed.entries:
		node = Node()
		node.title = cgi.escape(i.title.strip())
		node.author = i.author.strip()
		if i.author == "hup":
			continue
		if node.title.endswith(" (x)"):
			continue
		# strip the feedburner ad at the end of the page
		node.description = cgi.escape(i.summary_detail.value.split('<img src="http://feed')[0])
		node.link = re.sub('/([0-9])', r'/node/\1', i.id.split(' ')[0])
		node.pubdate = i.updated
		rss.items.append(node)
	return [rss.output()]
