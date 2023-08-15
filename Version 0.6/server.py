import http.server
from threading import Thread, current_thread
from sys import stderr
from functools import partial
from os.path import abspath


def ServeDirectoryWithHTTP(directory="."):
    port = 2001
    hostname = "127.0.0.1"
    
    directory = abspath(directory)
    handler = partial(_SimpleRequestHandler, directory=directory)
    httpd = http.server.HTTPServer((hostname, 0), handler, False)
    httpd.timeout = 0.5
    httpd.allow_reuse_address = True

    _xprint("server about to bind to port %d on hostname '%s'" % (port, hostname))
    httpd.server_bind()

    address = "http://%s:%d" % (httpd.server_name, httpd.server_port)
    address = "http://%s:%d" % ("localhost", httpd.server_port)

    _xprint("server about to listen on:", address)
    httpd.server_activate()

    def serve_forever(httpd):
        with httpd: 
            _xprint("server about to serve files from directory (infinite request loop):", directory)
            httpd.serve_forever()
            _xprint("server left infinite request loop")

    thread = Thread(target=serve_forever, args=(httpd, ))
    thread.setDaemon(True)
    thread.start()

    return httpd, address


def _xprint(*args, **kwargs):
    
    print("[", current_thread().name, "]",
          " ".join(map(str, args)), **kwargs, file=stderr)


class _SimpleRequestHandler(http.server.SimpleHTTPRequestHandler):
   

    def log_message(self, format, *args):
        stderr.write("[ " + current_thread().name + " ] ")
        http.server.SimpleHTTPRequestHandler.log_message(self, format, *args)


if __name__ == "__main__":
    from doctest import testmod
    testmod(verbose=True)