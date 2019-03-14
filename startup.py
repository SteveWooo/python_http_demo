from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import json
from os import path
from urllib.parse import urlparse

curdir = './'
sep = '/'
# MIME-TYPE
mimedic = [
	('.html', 'text/html'),
	('.htm', 'text/html'),
	('.js', 'application/javascript'),
	('.css', 'text/css'),
	('.json', 'application/json'),
	('.png', 'image/png'),
	('.jpg', 'image/jpeg'),
	('.gif', 'image/gif'),
	('.txt', 'text/plain'),
	('.avi', 'video/x-msvideo'),
]

class ServerHTTP(BaseHTTPRequestHandler):
	# http get request
	def do_GET(self):
		sendReply = False
		querypath = urlparse(self.path)
		filepath, query = querypath.path, querypath.query

		if filepath.endswith('/'):
			filepath += 'static/index.html'
		filename, fileext = path.splitext(filepath)
		for e in mimedic:
			if e[0] == fileext:
				mimetype = e[1]
				sendReply = True

		if sendReply == True:
			try:
				with open(path.realpath(curdir + sep + filepath),'rb') as f:
					content = f.read()
					self.send_response(200)
					self.send_header('Content-type',mimetype)
					self.end_headers()
					self.wfile.write(content)
			except IOError:
				self.send_error('File Not Found: ')

	# http post request
	def do_POST(self):
		path = self.path
		# get request path. -> http://domain:port{path} <-this path
		print(path)

		# fetch post body data
		# we use application/json protocol
		mpath,margs=urllib.parse.splitquery(self.path)
		source = self.rfile.read(int(self.headers['content-length']))
		data = json.loads(source)

		######
		#
		#
		#
		#
		######
		# this data is what we need :), signal from html client
		print(data)
		print(data['number'])
		if(path == '/add_1'):
			data['number'] += 100

		if(path == '/add_2'):
			data['number'] += 200

		# response data to html client.
		self.send_response(200)
		self.send_header("Content-type","Application/json")
		self.send_header("Access-Control-Allow-Origin", "*");
		self.end_headers()

		# use json.dumps to format
		# response = json.dumps({
		# 	'number' : data['number']
		# }).encode()
		# send
		self.wfile.write(json.dumps({
			'number' : data['number']
		}).encode())

def start_server(port):
	print("listened at ", port)
	http_server = HTTPServer(('', int(port)), ServerHTTP)
	http_server.serve_forever() 


if __name__ == "__main__":
	start_server(8000)