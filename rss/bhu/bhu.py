import feedparser
from email.Utils import formatdate
import re
from mod_python import apache
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
	def __init__(self, req, title, link, desc):
		self.req = req
		self.title = title
		self.desc = desc
		self.link = link
		self.items = []
	
	def output(self):
		self.req.content_type = 'application/xml'
		self.req.write("""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">
<channel>
<title>%s</title>
<description>%s</description>
<link>%s</link>\n""" % (self.title, self.desc, self.link))
		for i in self.items:
			self.req.write("""<item>
<title>%s</title>
<description>%s</description>
<link>%s</link>
<pubDate>%s</pubDate>
</item>\n""" % (i.title, i.description, i.link, i.pubdate))
		self.req.write("</channel>\n</rss>")
		return apache.OK

def handler(req):
	feed = Feed()
	rss = Rss(req, feed.feed.feed.title, feed.feed.feed.links[0].href, feed.feed.feed.subtitle)

	for i in feed.feed.entries:
		node = Node()
		if re.sub(r'(.*) \((.*)\)', r'\2', i.title.strip()) == "XXX":
			continue
		node.title = cgi.escape(re.sub(r'(.*) \((.*)\)', r'[\2] \1', i.title.strip()))
		node.description = cgi.escape(i.summary_detail.value)
		node.link = i.id
		node.pubdate = i.updated
		rss.items.append(node)
	return rss.output()
