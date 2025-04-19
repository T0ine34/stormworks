from flask import Flask, request
import socketio
import os
import eventlet
import eventlet.wsgi
import time
import psutil
import sys
import datetime as dt

from gamuLogger import Logger, LEVELS
Logger.showProcessName()
Logger.setLevel("stdout", LEVELS.DEBUG)


from .utils import getMIMEType, getFileName, splitchars
from .globals import CONFIG
from .layout import Layout
from .elements import Component
from .elements.utils import Types, Mode


ALLOWED_KEYS = [t+str(i) for t in ["b", "n"] for i in range(1,33)]
APP_PATH =  CONFIG["app"]["path"]
NODE_MODULES_PATH = CONFIG["node_modules"]


class Server:
    def __init__(self):
        self.BUTTON_STATE = {}
        
        self._start_time = time.time()
        
        layouts = os.listdir(f"{CONFIG['resources']}/layouts")
        if not layouts:
            raise FileNotFoundError("No layouts found in resources/layouts")
        
        for layout in layouts:
            layoutName = '.'.join(layout.split(".")[:-1])
            layout = self.__loadLayout(layoutName)
            os.makedirs(f"{CONFIG['app.path']}/../layouts", exist_ok=True)
            with open(f"{CONFIG['app.path']}/../layouts/{layoutName}.html", "w") as f:
                f.write(layout.html(CONFIG['resources'] + "/layout.template.html"))
            Logger.debug(f"Loaded layout: {layoutName} (saved to {os.path.normpath(f'{CONFIG["app.path"]}/../layouts/{layoutName}.html)')}")
        
        self.sio = socketio.Server(cors_allowed_origins='*')
        self.app = Flask(__name__)
        self.server = socketio.WSGIApp(self.sio, self.app)
        
        self._worker_pool = eventlet.GreenPool(20)
        self._sock = eventlet.listen((CONFIG["api"]["host"], CONFIG["api"]["port"]))
        
        self.__defineEvents()
        self.__defineRoutes()
        
    def setDefaultState(self, e : Component, name):
        if e.mode == Mode.WRITE:
            if e.type == Types.BOOLEAN:
                self.BUTTON_STATE[name][f"b{e.channel}"] = False
            elif e.type == Types.NUMBER:
                self.BUTTON_STATE[name][f"n{e.channel}"] = float(e.value)
        if e.hasChildren:
            for c in e.children:
                self.setDefaultState(c, name)
        
    def __loadLayout(self, name : str) -> Layout:
        if not os.path.exists(CONFIG['resources'] + f"/layouts/{name}.xml"):
            raise FileNotFoundError(f"Layout not found: {name}")
        layout = Layout.fromXml(CONFIG['resources'] + f"/layouts/{name}.xml") # type: ignore
        self.BUTTON_STATE[name] = {}
        for e in layout.elements:
            self.setDefaultState(e, name)
            
        return layout


    def __defineEvents(self):
        @self.sio.event
        def connect(sid, environ):
            Logger.info(f'connect {sid}')


        @self.sio.event
        def disconnect(sid):
            Logger.info(f'disconnect {sid}')


        @self.sio.event
        def button(sid, data):
            Logger.debug(f"button {data}")
            try:
                if data['id'].startswith("b"):
                    self.BUTTON_STATE[data['layout']][data['id']] = data['state']
                elif data['id'].startswith("n"):
                    self.BUTTON_STATE[data['layout']][data['id']] = float(data['state'])
            except KeyError as e:
                Logger.error(f"Invalid data format: {data} : {e.__class__.__name__}: {e}")
                return
            


    def __defineRoutes(self):
        @self.app.route('/game/<path:path>', methods=['GET'])
        def _game(path):
            data = ""
            for k, v in self.BUTTON_STATE[path].items():
                data += f"{splitchars(k, '.')}={v}\n"

            self.sio.emit("data", {k: v for k, v in request.args.items() if k in ALLOWED_KEYS})
                
            return data, 200, {"Content-Type": "text/plain"}

        @self.app.route('/init', methods=['GET'])
        def _init():
            Logger.debug(f"GET /init")
            Logger.debug(self.BUTTON_STATE)
            key = request.args.get("key")
            if key is None:
                return "Invalid key", 400, {"Content-Type": "text/plain"}
            data = []
            for k, v in self.BUTTON_STATE[key].items():
                data.append(f"{k}={v}")
            return '\n'.join(data), 200, {"Content-Type": "text/plain"}
        
        
        @self.app.route('/app/node_modules/<path:path>', methods=['GET'])
        def _node_modules(path):
            Logger.debug(f"GET /app/node_modules/{path}")
            try:
                filepath = getFileName(f"{NODE_MODULES_PATH}/{path}")
                return open(filepath, "rb").read(), 200, {"Content-Type": getMIMEType(filepath)}
            except FileNotFoundError:
                Logger.warning(f"File not found: {NODE_MODULES_PATH}/{path}")
                return "Not Found", 404, {"Content-Type": "text/plain"}
            except Exception as e:
                Logger.error(f"Error: {e}")
                return str(e), 500, {"Content-Type": "text/plain"}

        @self.app.route('/app/<path:path>', methods=['GET'])
        def _app(path):
            Logger.debug(f"GET /app/{path}")
            try:
                filepath = getFileName(f"{APP_PATH}/{path}")
                return open(filepath, "rb").read(), 200, {"Content-Type": getMIMEType(filepath)}
            except FileNotFoundError:
                try:
                    if path.endswith(".html"):
                        path = '.'.join(path.split(".")[:-1])
                        with open(f"{CONFIG['app.path']}/../layouts/{path}.html", "r") as f:
                            layout = f.read()
                        return layout, 200, {"Content-Type": "text/html"}
                    return "Not Found", 404, {"Content-Type": "text/plain"}
                except KeyError:
                    Logger.warning(f"File not found: {APP_PATH}/{path}")
                    return "Not Found", 404, {"Content-Type": "text/plain"}
            except Exception as e:
                Logger.error(f"Error: {e}")
                return str(e), 500, {"Content-Type": "text/plain"}

        @self.app.route('/app', methods=['GET'])
        def _app_index():
            Logger.debug(f"GET /app")
            return "Redirecting...", 302, {"Location": "/app/index.html"}
            
            
        @self.app.route('/debug', methods=['GET'])
        def _debug():
            # return a simple html page that fetch /debug/data every 0.5s
            with open(f"{CONFIG['resources']}/debug.html", "r") as f:
                return f.read(), 200, {"Content-Type": "text/html"}
            
            
        @self.app.route('/debug/data', methods=['GET'])
        def _debug_data():
            return {"mem": self.getMemUsage(), "cpu": self.getCpuUsage(), "uptime": self.getUptime(), "state" : self.BUTTON_STATE}, 200, {"Content-Type": "application/json"}

    def getMemUsage(self):
        process = psutil.Process()
        return f"{process.memory_info().rss / 1024 / 1024:.2f} MB"
    
    def getCpuUsage(self):
        return f"{psutil.cpu_percent()}%"
    
    def getUptime(self):
        return str(dt.timedelta(seconds=time.time() - self._start_time))
       

    def start(self):
        Logger.info(f"Starting server on {CONFIG['api']['host']}:{CONFIG['api']['port']}")
        eventlet.wsgi.server(self._sock, self.server, log_output=False)
        
    def stop(self):
        Logger.info("Stopping server")
        self._worker_pool.resize(0)
        self._sock.close()
        self._worker_pool.waitall()
        time.sleep(1)
        Logger.info("Server stopped")

    def restart(self):
        time.sleep(0.1)
        self.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)