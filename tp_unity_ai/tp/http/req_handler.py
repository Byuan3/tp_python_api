import io
import json

from http.server import BaseHTTPRequestHandler
import cgi


class RequestHandler(BaseHTTPRequestHandler):

    image_data = None
    pipeline = []
    env_json = None

    def do_POST(self):
        if self.path == '/stream':
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
            if ctype == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                fields = cgi.parse_multipart(self.rfile, pdict)
                img = fields.get('image')
                msg = fields.get('msg')
                if img is not None:
                    img_file = io.BytesIO(img[0])
                    RequestHandler.image_data = img_file.getvalue()
                    if msg is not None:
                        print(msg[0])
                    # Set response
                    if len(RequestHandler.pipeline) != 0:
                        # Create a JSON response
                        response_data = RequestHandler.pipeline[0]

                        # Encode the response data as JSON
                        response_body = json.dumps(response_data).encode('utf-8')

                        # Set the Content-Type header to application/json
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()

                        # Send the JSON response
                        self.wfile.write(response_body)
                        RequestHandler.pipeline.pop(0)
                    else:
                        self.send_response(200)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(b'Success')
                    return
        # Bad Request
        self.send_response(400)
        self.end_headers()

    def do_PUT(self):
        if self.path == '/data':
            # Get the length of the incoming request body
            content_length = int(self.headers['Content-Length'])

            # Read the request body and parse it as JSON
            body = self.rfile.read(content_length)
            data = json.loads(body)

            # Process the JSON data as desired
            RequestHandler.pipeline.append(data)

            # Send a response
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Received PUT request with JSON body')
            return
        # Bad Request
        self.send_response(400)
        self.end_headers()

    def do_GET(self):
        if self.path == '/display':
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(RequestHandler.image_data)
            return
        elif self.path == '/env':
            if len(RequestHandler.pipeline) != 0:
                # Create a JSON response
                response_data = RequestHandler.env_json

                # Encode the response data as JSON
                response_body = json.dumps(response_data).encode('utf-8')

                # Set the Content-Type header to application/json
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()

                # Send the JSON response
                self.wfile.write(response_body)
            return
        # Bad Request
        self.send_response(400)
        self.end_headers()


        