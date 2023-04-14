import io
import json
import cgi

from typing import Dict, List, Optional
from http.server import BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
    cam_image: Optional[bytes] = None
    stream_pipeline: List[Dict[str, str]] = []
    commands_pipeline: Dict[str, List[Dict[str, str]]] = {}
    agents: Dict[str, Dict[str, str]] = {}

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
                    RequestHandler.cam_image = img_file.getvalue()
                    if msg is not None:
                        print(msg[0])
                    # Set response
                    if len(RequestHandler.stream_pipeline) != 0:
                        # Create a JSON response
                        response_data = RequestHandler.stream_pipeline[0]

                        # Encode the response data as JSON
                        response_body = json.dumps(response_data).encode('utf-8')

                        # Set the Content-Type header to application/json
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()

                        # Send the JSON response
                        self.wfile.write(response_body)
                        RequestHandler.stream_pipeline.pop(0)
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
                try:
                    data = json.loads(body)

                    if 'id' in data:
                        print(data)
                        object_id = data['id']
                        object_name = data['name']
                        # Process the request data
                        RequestHandler.agents[object_name] = data

                        # Set response
                        if object_id in RequestHandler.commands_pipeline and RequestHandler.commands_pipeline[object_id]:

                            # Create a JSON response
                            response_data = RequestHandler.commands_pipeline[object_id][0]
                            response_data['msg'] = 'Success Object {0} Post Request'.format(object_id)

                            # Encode the response data as JSON
                            response_body = json.dumps(response_data).encode('utf-8')

                            # Set the Content-Type header to application/json
                            self.send_response(200)
                            self.send_header('Content-Type', 'application/json')
                            self.end_headers()

                            # Send the JSON response
                            self.wfile.write(response_body)
                            RequestHandler.commands_pipeline[object_id].pop(0)
                        else:
                            RequestHandler.commands_pipeline[object_id] = []

                            # Set the Content-Type header to application/json
                            self.send_response(200)
                            self.send_header('Content-Type', 'application/json')
                            self.end_headers()

                            # Send the JSON response
                            res = {'msg': 'Success Object {0} Post Request'.format(object_id)}
                            self.wfile.write(json.dumps(res).encode('utf-8'))
                        return

                except json.JSONDecodeError:
                    return {'status': 'error', 'message': 'Invalid JSON format in request body'}

        # Commands update API
        elif self.path == '/commands':
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
            if ctype == 'application/json':
                # Get the length of the incoming request body
                content_length = int(self.headers['Content-Length'])

                # Read the request body and parse it as JSON
                body = self.rfile.read(content_length)
                try:
                    data = json.loads(body)

                    if 'id' in data:
                        # Process the JSON data as desired
                        object_id = data['id']
                        if object_id in RequestHandler.commands_pipeline:
                            RequestHandler.commands_pipeline[object_id].append(data)
                            # Send a response
                            self.send_response(200)
                            self.send_header('Content-type', 'text/plain')
                            self.end_headers()
                            self.wfile.write(b'Received PUT request with JSON\n')
                            self.wfile.write(bytes('Object id: {0}'.format(object_id), encoding='utf-8'))
                            return

                except json.JSONDecodeError:
                    return {'status': 'error', 'message': 'Invalid JSON format in request body'}
        # Bad Request
        self.send_response(400)
        self.end_headers()

    def do_GET(self):
        # Camera image GET API
        if self.path == '/display':
            if RequestHandler.cam_image:
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(RequestHandler.cam_image)
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
