#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
import os
import markdown
import codecs
import datetime
import time
from .base import *
site_config = {
	"title" : "IceHoney!",
	"url" : """http://blog.icehoey.me""",
	"post_dir": os.getcwd() + os.sep + 'posts',
}
def SingleFileHandler(file_path):
	f = codecs.open(file_path, mode='r', encoding='utf8')
	lines = []
	try:
		lines = f.readlines()
	except:
		pass
	f.close()
	
	ret = {}
	title = ''
	date = ''
	index = 1

	for line in lines[1:]:
		index += 1
		if line.find('title: ') == 0:
			title = line.replace('title: "','')[0:-2]
		if line.find('date: ') == 0:
			date = line.replace('date: ','')[0:-1]
		if line.find('---') == 0:
			break

	content = u'';
	for line in lines[index:]:
		content += line
		
	if title:
		ret['title'] = title
		ret['date'] = date
		ret['content'] = markdown.markdown(content)
		ret['name'] = file_path.split(os.sep)[-1].split('.')[0]
	return ret
class IndexHandler(BaseHandler):
    def get(self):
    	articles = []
    	post_dir =site_config["post_dir"]
    	file_list=[]
    	files=os.listdir(post_dir)
    	try:
    		p=int(self.get_argument('p','0'))	
    	except:
    		print 'Some Error Happen Line 58'
    		p=0
    	for f in files:
    		file_list.append(post_dir+os.sep+f)
    	file_list.sort(reverse=True)
    	if p>len(file_list):
    		p=0
    	for single_file in file_list[p:p+3]:
    		article=SingleFileHandler(single_file)
    		if article:
    			articles.append(article)
    	
    	if p>2:
    		prev=True
    	else:
    		prev=False
    	if p+4<=len(file_list):
    		next=True
    	else:
    		next=False
        self.render("index.html", title=site_config['title'], articles = articles,prev=prev, next=next, prevnum=p-3, nextnum=p+3)
class PostsHandler(BaseHandler):
	def get(self,id):
		post_path = site_config["post_dir"] + os.sep + id.replace('.','') + '.markdown'
		if os.path.exists(post_path):
			article = SingleFileHandler(post_path)
		else:
			self.set_status(404)
			self.render("404.html",title="404 NOT FOUND")
			return	
		self.render("article.html", title=site_config['title'], url=site_config["url"], article = article)
class RSSOutput(BaseHandler):
	def get(self):
		articles = []
		post_dir = site_config["post_dir"]
		file_list = []
		files = os.listdir(post_dir)
		for f in files:
			file_list.append(post_dir + os.sep + f)
		file_list.sort(reverse=True)
		for single_file in file_list:
			article = SingleFileHandler(single_file)
			if article: articles.append(article)
		self.set_header("Content-Type", "application/atom+xml")
		self.render("feed.xml",articles=articles)
class NotFounderHandler(BaseHandler):
	def prepare(self):
		self.set_status(404)
		self.render("404.html",title="404 NOT FOUND")
handlers = [
        (r"/", IndexHandler),
        (r"/posts/(.*)",PostsHandler),
        (r"/feed",RSSOutput),
        (r"/.*",NotFounderHandler)
        ]