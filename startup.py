from  BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import urllib
import json

cur_dir = './'

class ServerHTTP(BaseHTTPRequestHandler):
	def do_OPTIONS(self):
		self.send_response(200)
		self.send_header("Content-type","Application/json")
		self.send_header("Access-Control-Allow-Origin", "*");
		self.end_headers()
		self.wfile.write('')

	# http get request
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"

		try:
			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				f = open(cur_dir + self.path)
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return 
		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	# http post request
	def do_POST(self):
		path = self.path
		# get request path. -> http://domain:port{path} <-this path
		print path

		# fetch post body data
		# we use application/json protocol
		source = self.rfile.read(int(self.headers['content-length']))
		source = urllib.unquote(source).decode("utf-8", 'ignore')
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

		# response data to html client.
		self.send_response(200)
		self.send_header("Content-type","Application/json")
		self.send_header("Access-Control-Allow-Origin", "*");
		self.end_headers()

		# use json.dumps to format
		response = json.dumps({
			'number' : data['number'] + 100
		})
		# send
		self.wfile.write(response)

def start_server(port):
	print("listened at 8000")
	http_server = HTTPServer(('', int(port)), ServerHTTP)
	http_server.serve_forever() 


if __name__ == "__main__":
	start_server(8000)