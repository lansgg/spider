# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import random
import re
import codecs

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]


class url_manager(object):
	"""docstring for url_manager"""
	def __init__(self):
		super(url_manager, self).__init__()
		self.new_urls = set()
		self.old_urls = set()

	def add_new_url(self,url):
		if url is None:
			return

		if url not in self.new_urls and url not in self.old_urls:
			self.new_urls.add(url)

	def add_new_urls(self,urls):
		if urls is None or len(urls) == 0:
			return

		for url in urls:
			self.add_new_url(url)

	def has_new_url(self):
		return len(self.new_urls) != 0

	def get_new_url(self):
		new_url = self.new_urls.pop()
		self.old_urls.add(new_url)
		return new_url


class html_downloader(object):
	"""docstring for html_downloader"""
	def __init__(self):
		super(html_downloader, self).__init__()

	def download(self,url):
		if url is None:
			return

		headers = {"User-Agent" : random.choice(USER_AGENTS)}
		response = requests.get(base_url,headers=headers)
		response.encoding='gb2312'
		if response.status_code != 200:
			return None

		return response.content

class html_parser(object):
	"""docstring for html_parser"""
	def __init__(self):
		super(html_parser, self).__init__()

	def __get_new_urls(self,page_url,soup):
		new_urls = set()
		links = soup.find_all('a',href=re.compile(r"http://www.gaokao.com/e/2017\d+/\S+.shtml"))
		for link in links:
			new_url = link['href']
			new_urls.add(new_url)
		return new_urls

	def __get_new_data(self,page_url,soup):
		if page_url == base_url:
			return 

		new_data = {}
		response = requests.get(page_url)
		response.encoding='gb2312'
		if response.status_code != 200:
			return

		result = response.text
		soup = BeautifulSoup(result,'html.parser')
		title = soup.find('a',href=re.compile('gaokao.com/e/\d+\S+.shtml'))
		new_data['title'] = title.get_text()
		
		content = soup.find('div',class_="main").find('p')
		new_data['content'] =  content.get_text()
		return new_data


	def parser(self,page_url,html_cont):
		if page_url is None or html_cont is None:
			return

		soup = BeautifulSoup(html_cont,'html.parser')
		new_urls = self.__get_new_urls(page_url,soup)
		new_data = self.__get_new_data(page_url,soup)
		return new_urls,new_data

class html_outputer(object):
	"""docstring for html_outputer"""
	def __init__(self):
		super(html_outputer, self).__init__()
		self.datas = []

	def collect_data(self,data):
		if data is None:
			return

		fh = codecs.open(data['title'],'a',encoding='utf-8')
		fh.write(data['content'])
		# self.datas.append(data)

	def outputer_html(self):
		fout = open('output.html','w')
		for data in self.datas:
			fout.write(data)
		

class SpiderMain(object):
	"""docstring for SpiderMain"""
	def __init__(self):
		super(SpiderMain, self).__init__()
		self.urls =	url_manager()
		self.downloader = html_downloader()
		self.outputer = html_outputer()
		self.parser = html_parser()

	def craw(self,base_url):
		count = 1
		self.urls.add_new_url(base_url)
		while self.urls.has_new_url():
			try:
				new_url = self.urls.get_new_url()
				print 'craw %d : %s' %(count,new_url)
				html_cont = self.downloader.download(new_url)
				new_urls,new_data = self.parser.parser(new_url,html_cont)
				self.urls.add_new_urls(new_urls)
				self.outputer.collect_data(new_data)

			except Exception as e:
				print 'craw failed %d %s' %(count,str(e))

			finally:
				count += 1
				if count == 100:
					break
		# self.outputer.outputer_html()


if __name__ == '__main__':

	base_url = r'http://www.gaokao.com/gkzw/gkmfzw/'
	obj_spider = SpiderMain()
	obj_spider.craw(base_url)

