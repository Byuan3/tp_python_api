import io
import json

from http.server import BaseHTTPRequestHandler
import cgi


class RequestHandler(BaseHTTPRequestHandler):
    image_data = None
    pipeline = []
    agents_pipeline = {}
    agents = {}

    def do_POST(self):
        # Camera stream API
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
                        self.wfile.write(b'Success Stream Post Request')
                    return
        # Object connection API
        if self.path == '/objects':
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
            print(ctype)
            if ctype == 'application/json':
                # Get the content length from the request headers
                content_length = int(self.headers['Content-Length'])

                # Read the request body and parse it as JSON
                body = self.rfile.read(content_length)
                data = json.loads(body)

                if 'id' in data:
                    print(data)
                    object_id = data['id']
                    object_name = data['name']
                    # Process the request data
                    RequestHandler.agents[object_name] = data

                    # Set response
                    if object_id in RequestHandler.agents_pipeline and len(
                            RequestHandler.agents_pipeline[object_id]) != 0:
                        
                        # Create a JSON response
                        response_data = RequestHandler.agents_pipeline[object_id][0]
                        response_data['msg'] = 'Success Object {0} Post Request'.format(object_id)

                        # Encode the response data as JSON
                        response_body = json.dumps(response_data).encode('utf-8')

                        # Set the Content-Type header to application/json
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()

                        # Send the JSON response
                        self.wfile.write(response_body)
                        RequestHandler.agents_pipeline[object_id].pop(0)
                    else:
                        RequestHandler.agents_pipeline[object_id] = []

                        # Set the Content-Type header to application/json
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()

                        # Send the JSON response
                        res = {'msg': 'Success Object {0} Post Request'.format(object_id)}
                        self.wfile.write(json.dumps(res).encode('utf-8'))
                    return
        # Commands update API
        elif self.path == '/commands':
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
            if ctype == 'application/json':
                # Get the length of the incoming request body
                content_length = int(self.headers['Content-Length'])

                # Read the request body and parse it as JSON
                body = self.rfile.read(content_length)
                data = json.loads(body)

                if 'id' in data:
                    # Process the JSON data as desired
                    object_id = data['id']
                    if object_id in RequestHandler.agents_pipeline:
                        RequestHandler.agents_pipeline[object_id].append(data)
                        # Send a response
                        self.send_response(200)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(b'Received PUT request with JSON\n')
                        self.wfile.write(bytes('Object id: {0}'.format(object_id), encoding='utf-8'))
                        return
        # Bad Request
        self.send_response(400)
        self.end_headers()

    def do_GET(self):
        # Camera image GET API
        if self.path == '/display':
            if RequestHandler.image_data:
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(RequestHandler.image_data)
            return
        # Agents GET API
        elif self.path == '/agents':
            if RequestHandler.agents:
                # Create a JSON response
                response_data = RequestHandler.agents

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
