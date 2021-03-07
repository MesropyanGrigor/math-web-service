
class Server:

    def __init__(self, host='127.0.0.1', port=8000):
        """Contstructor"""
        self._host = host
        self._port = port
        self.fn2func ={'fib' : math.fibonacci_s,
                       'fac': math.factorial_s,
                       'ack': math.ackermann}
        self._app = Flask(__name__)
        self._add_routes()
        self.__init__logging()


    def __init__logging(self):
        """Initializing LOGGER"""
        self.LOGGER = logging.getLogger(__name__)
        #logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
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
        self.LOGGER.info(f"{func.__name__}({in_val}): {(end_tm-start_tm).seconds} seconds")
        return val

    def read(self, func_name, val1, val2=None):
        if not val2:
            vals = (int(val1),)
        else:
            vals = int(val1), int(val2)
        return self.do("GET", func_name, *vals)

    def do(self, request_type, func_name, *vals):
        if self.validate_request(request_type, func_name, *vals):
            val = self.duration(self.fn2func[func_name], *vals)
            #return self._response(200, val)
            return val

    def _response(self, status, val):
        #return Response(json.dump([val]), status=status)
        return str(val), status

    def validate_request(self, request_type, func_name, *vals):
        if request_type not in ['GET', 'POST']:# can be extended
            self.LOGGER.error(f"Not valid request: {request_type}")
            return False
        if func_name not in ['fib', 'fac', 'ack']:
            self.LOGGER.error(f"Not valid name: {func_name}")
            return False
        for val in vals:
            if val != int(val):
                self.LOGGER.error(f"Not integer type: {val}")
                return False
        if func_name in ['fib', 'fac'] and len(vals) != 1 or func_name == 'ack' and len(vals) != 2:
            self.LOGGER.error(f"Not valid values {vals} for {func_name} function")
            return False
        return True

    def run(self):
        self._app.run(host=self._host, port=self._port)

    def _add_routes(self):
        self._app.add_url_rule('/<func_name>/<val1>/<val2>', endpoint='fib', view_func=self.read)
        self._app.add_url_rule('/<func_name>/<val1>', endpoint='func', view_func=self.read)

