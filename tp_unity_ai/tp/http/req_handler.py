import io

import cv2
from http.server import BaseHTTPRequestHandler
import cgi

import numpy as np


class RequestHandler(BaseHTTPRequestHandler):

    image_data = None
    data_pipeline = []

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
                    nparr = np.frombuffer(img_file.getvalue(), np.uint8)
                    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    # Process the image and msg as needed
                    cv2.imshow("Received Image", img)
                    cv2.waitKey(1)
                    if msg is not None:
                        print(msg[0])
                    # Set response
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
            # Set response
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Success PUT')
            return
        # Bad Request
        self.send_response(400)
        self.end_headers()

    def do_GET(self):
        if self.path == '/display':
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            print(RequestHandler.image_data)
            self.wfile.write(RequestHandler.image_data)
            return
        # Bad Request
        self.send_response(400)
        self.end_headers()


        