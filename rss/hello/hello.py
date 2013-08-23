def application(environ, start_response):
	status = '200 OK'
	output = 'Hello World!'

	response_headers = [('Content-type', 'application/xml')]
	start_response(status, response_headers)

	return [output]
