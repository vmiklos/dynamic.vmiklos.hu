import feedparser
from email.Utils import formatdate
import re
import cgi

import sys
sys = reload(sys)
sys.setdefaultencoding("utf-8")

class Feed:
	def __init__(self):
		self.feed = feedparser.parse("http://bithumen.be/bh-rss.xml")

class Node:
	def __init__(self):
		self.title = ""
		self.description = ""
		self.link = ""
		self.pubdate = ""

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
</item>\n""" % (i.title, i.description, i.link, i.pubdate))
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
		if re.sub(r'(.*) \((.*)\)', r'\2', i.title.strip()) == "XXX":
			continue
		node.title = cgi.escape(re.sub(r'(.*) \((.*)\)', r'[\2] \1', i.title.strip()))
		node.description = cgi.escape(i.summary_detail.value)
		node.link = i.id
		node.pubdate = i.updated
		rss.items.append(node)
	return [rss.output()]
