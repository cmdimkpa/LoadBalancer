# Load Balancer: Port 'FIFO' -- 3436

from flask import Flask,request
from flask_cors import CORS
import requests as http
import json

app = Flask(__name__)
CORS(app)

global FIFOQueue, nodeList, endpointMap, jobCounter

jobCounter = 0

class Queue:
    # A FIFO Queue Implementation
    def __init__(self):
        self.queue = []
    def add(self,obj):
        self.queue.insert(0,obj)
    def next(self):
        if self.queue!=[]:
            return self.queue.pop()

FIFOQueue = Queue()

nodeList = [
    "http://api.click-meter.com:7737",
    "http://ceres.media:7737",
    "http://ceres-ai.com:7737"
]

endpointMap = {
    "hello":"/rigo-remote/list-dbs"
}

class RequestObject:
    def __init__(self,route,method,data):
        self.route = route;
        self.method = method;
        self.data = data;
    update = __init__
    def export(self):
        return {"route":self.route,"method":self.method,"data":self.data}

def a404page():
    return '<div style="background-color: rgb(255, 255, 255); font-family: "Lucida Grande", "Segoe UI", "Apple SD Gothic Neo", "Malgun Gothic", "Lucida Sans Unicode", Helvetica, Arial, sans-serif; font-size: 0.9em; overflow-x: hidden; overflow-y: auto; margin: 0px !important; padding: 5px 20px 26px !important;padding: 20px;padding: 20px; color: rgb(34, 34, 34); font-size: 15px; font-family: "Roboto Condensed", Tauri, "Lucida Grande", "Lucida Sans Unicode", "Lucida Sans", AppleSDGothicNeo-Medium, "Segoe UI", "Malgun Gothic", Verdana, Tahoma, sans-serif; background-color: rgb(255, 255, 255); -webkit-font-smoothing: antialiased; background-position: initial initial; background-repeat: initial initial;"><p style="margin: 1em 0px; word-wrap: break-word;"><img src="http://ceres-ai.com:6765/static/404.jpg" alt="404" style="max-width: 100%;"></p></div>'

def JobProcessor(RO):
    global jobCounter
    if RO != None:
        # run scheduler (Round-Robin)
        jobCounter+=1
        turn = jobCounter%len(nodeList)
        node = nodeList[turn]
        # prepare job details
        url = node+RO.route;
        method = RO.method;
        data = json.dumps(RO.data);
        # execute job
        if method.lower() == "get":
            # process GET request
            return http.get(url).content
        elif method.lower() == "post":
            # process POST request
            return http.post(url,data).content
        elif method.lower() == "put":
            # process PUT request
            return http.put(url,data).content
        elif method.lower() == "delete":
            # process DELETE request
            return http.delete(url).content
        else:
            # unsupported
            return "Error: Method [%s] is not supported." % method.upper()

# catch-all route
@app.route('/<path:endpoint>', methods=["GET","POST","PUT","DELETE"])
def catch_all(endpoint):
    global FIFOQueue
    # handle request based on endpointMap
    if endpoint not in endpointMap:
        return a404page()
    else:
        # get request route
        call_route = endpointMap[endpoint]
        # get request method
        call_method = request.method;
        # get request data
        try:
            call_data = request.get_json(force=True)
        except:
            call_data = {}
        # encode as request object
        ro = RequestObject(
            route=call_route,
            method=call_method,
            data=call_data
        )
        # Queue request object
        FIFOQueue.add(ro)
        # demand-based execution: process next job on queue
        return JobProcessor(FIFOQueue.next())

if __name__ == "__main__":
    app.run(port=3436)
