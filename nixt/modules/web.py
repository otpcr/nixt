# This file is placed in the Public Domain.
# pylint: disable=C0103,C0115,C0116,C0209,C0301,R0903,W0105,E0402


"rest"


import base64
import os
import sys
import time


from http.server  import HTTPServer, BaseHTTPRequestHandler


from ..clients import Default
from ..objects import Object
from ..persist import Workdir, types
from ..runtime import later, launch


DEBUG = False


"init"


def init():
    try:
        rest = HTTP((Config.hostname, int(Config.port)), HTTPHandler)
    except OSError as ex:
        later(ex)
        rest = None
    if rest is not None:
        rest.start()
    return rest


"exceptions"


class WebError(Exception):

    pass


"config"


class Config(Default):

    hostname = "localhost"
    port     = 10102


"rest"


class HTTP(HTTPServer, Object):

    allow_reuse_address = True
    daemon_thread = True

    def __init__(self, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        Object.__init__(self)
        self.host = args[0]
        self._last = time.time()
        self._starttime = time.time()
        self._status = "start"

    def exit(self):
        self._status = ""
        time.sleep(0.2)
        self.shutdown()

    def start(self):
        self._status = "ok"
        launch(self.serve_forever)

    def request(self):
        self._last = time.time()

    def error(self, _request, _addr):
        exctype, excvalue, _trb = sys.exc_info()
        exc = exctype(excvalue)
        later(exc)


class HTTPHandler(BaseHTTPRequestHandler):

    def setup(self):
        BaseHTTPRequestHandler.setup(self)
        self._ip = self.client_address[0]
        self._size = 0

    def raw(self, data):
        self.wfile.write(data)

    def send(self, txt):
        self.wfile.write(bytes(txt, encoding="utf-8"))
        self.wfile.flush()

    def write_header(self, htype='text/plain', size=None):
        self.send_response(200)
        #self.send_header('Content-type', '%s; charset=%s ' % (htype, "utf-8"))
        self.send_header('Content-type', '%s;')
        if size is not None:
            self.send_header('Content-length', size)
        self.send_header('Server', "1")
        self.end_headers()

    def do_GET(self):
        if DEBUG:
            return
        if "favicon" in self.path:
            return
        if self.path == "/":
             self.path = "/index.html"
        self.path = "html" + os.sep + self.path
        if not os.path.exists(self.path):
            self.write_header("text/html")
            self.send_response(404)
            self.end_headers()
            return
        if "_images" in self.path:
            try:
                with open(self.path, "rb") as file:
                    img = file.read()
                    file.close()
                ext = self.path[-3]
                self.write_header(f"image/{ext}", len(img))
                self.raw(img)
            except (TypeError, FileNotFoundError, IsADirectoryError) as ex:
                self.send_response(404)
                later(ex)
                self.end_headers()
            return
        try:
            with open(self.path, "r", encoding="utf-8", errors="ignore") as file:
                txt = file.read()
                file.close()
            self.write_header("text/html")
            self.send(html(txt))
        except (TypeError, FileNotFoundError, IsADirectoryError) as ex:
            self.send_response(404)
            later(ex)
            self.end_headers()

    def log(self, code):
        pass


"utilities"


def html(txt):
    return """<!doctype html>
<html>
   %s
</html>
""" % txt


def image(file):
 size = len(file)
 return f"""Content-Type: image/gif\r\n
Content-Length: [{size}]\r\n
\r\n
"""
