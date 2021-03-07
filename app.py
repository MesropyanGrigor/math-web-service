import logging
import datetime
import re
import os

from http.server import HTTPServer, BaseHTTPRequestHandler

import simple_math as math

class Service(BaseHTTPRequestHandler):
    """Math Service class"""
    def __init__(self, request, client_address, server):
        """Contstructor"""
        super().__init__(request, client_address, server)

    def setup(self):
        """setup method before hadnling actualy request"""
        super().setup()
        self.fn2func ={'fib' : math.fibonacci_s,
                       'fac': math.factorial_s,
                       'ack': math.ackermann}
        self.__init__logging()

    def __init__logging(self):
        """Initializing LOGGER"""
        self.LOGGER = logging.getLogger(__name__)
        fhandler = logging.FileHandler(f"monitor.log", mode='a')
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        fhandler.setFormatter(formatter)
        self.LOGGER.handlers = [fhandler] 
        self.LOGGER.setLevel(logging.DEBUG)

    def duration(self, func, *in_val):
        """Function wraper for logging function name and runtime """
        start_tm = datetime.datetime.now()
        val = func(*in_val)
        end_tm = datetime.datetime.now()
        #minutes, secs = divmod((end_tm - start_tm).seconds, 60)
        #self.LOGGER.info(f"{func.__name__}({*in_val}): {minutes} minutes {secs} seconds")
        #minutes, secs = divmod((end_tm - start_tm).seconds, 60)
        extent =  end_tm - start_tm
        self.LOGGER.info(f"{func.__name__}({in_val}):{extent.seconds}.{extent.microseconds} seconds")
        return val

    def _get_data(self):
        """Receiving data"""
        self.send_response(200)
        self.send_header('Content-type','text/json') # TODO
        #reads the length of the Headers
        length = int(self.headers['Content-Length'])
        #reads the contents of the request
        content = self.rfile.read(length)
        temp = str(content).strip('b\'')
        self.end_headers()
        return temp

    def do_GET(self):
        data = self._get_data()
        match_obj = re.match(r"(\w+)\(([\d, -]+)\)", data)
        func_name = match_obj.group(1)
        vals = tuple(match_obj.group(2).split(','))
        self.wfile.write(str(self.read(func_name, *vals)).encode())

    def read(self, func_name, val1, val2=None):
        if not val2:
            vals = (int(val1),)
        else:
            vals = int(val1), int(val2)
        return self.do(self.command, func_name, *vals)

    def do(self, request_type, func_name, *vals):
        if self.validate_request(request_type, func_name, *vals):
            try:
                val = self.duration(self.fn2func[func_name], *vals)
                return self.send(200, val)
            except RecursionError:
                val = "maximum recursion depth exceeded in comparison"
                self.error(val)

    def send(self, status, val):
        self.send_response(status)
        print(val)
        return val

    def error(self, msg):
        """Sending error message and putting reponse status as 404"""
        self.wfile.write(msg.encode())
        self.send_response(404)

    def validate_request(self, request_type, func_name, *vals):
        """Validationg request """
        if request_type not in ['GET', 'POST']:# can be extended, currently GET only supportted
            self.LOGGER.error(f"Not valid request: {request_type}")
            self.error(f"Not valid request: {request_type}")
            return False
        if func_name not in ['fib', 'fac', 'ack']:
            self.LOGGER.error(f"Not valid name: {func_name}")
            self.error(f"Not valid name: {func_name}")
            return False
        for val in vals:
            if int(val) < 0:
                self.LOGGER.error(f"Negative value is not accepted: {val}")
                self.error(f"Negative value is not accepted: {val}")
                return False
            if val != int(val):
                self.LOGGER.error(f"Not integer type: {val}")
                self.error(f"Not integer type: {val}")
                return False
        if func_name in ['fib', 'fac'] and len(vals) != 1 or func_name == 'ack' and len(vals) != 2:
            self.LOGGER.error(f"Not valid values {vals} for {func_name} function")
            self.error(f"Not valid values {vals} for {func_name} function")
            return False
        return True

if __name__ == '__main__':
    port = os.environ.get('PORT', 8888)
    server = HTTPServer(('127.0.0.1', port), Service)
    print("Starting server")
    server.serve_forever()
