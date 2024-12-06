import json
import os
import re
import signal
import threading
import traceback
import types

import jsonpickle
from flask import Flask, request
from robot.errors import HandlerExecutionFailed
from robot.libraries.BuiltIn import BuiltIn

TAB = re.compile('  +|\t')
port = int(os.getenv('ROBOT_RESTBRIDGE_PORT', 8882))

class ResultObject:
    payload = None
    variables = {}
    status = None

    def __init__(self, payload, varis, status):
        self.payload = payload
        self.variables = types.SimpleNamespace()
        self.variables.data = varis
        self.status = status



class RobotframeworkRestBridgeKeywords:

    def __init__(self):
        pass

    app = None

    def accept_keywords(self):
        app = Flask(__name__)
        app.add_url_rule("/", "execute_keyword", self.execute_keyword, methods=['POST'])
        app.add_url_rule("/robot/exit", "exit_process", self.exit_process, methods=['GET'])
        app.add_url_rule("/robot/available", "return_available", self.return_available, methods=['GET'])
        app.run(host="0.0.0.0", port=port)

    def execute_keyword(self):
        try:
            json_body = request.data.decode('utf-8')
            BuiltIn().run_keyword("Log to Console", "change")
            BuiltIn().run_keyword("Log to Console", json_body)
            data = json.loads(json_body)
            command = data['command']
            parsed = TAB.split(command)
            result_from_keyword = BuiltIn().run_keyword(parsed[0], *parsed[1:])
            context = BuiltIn()._get_context()
            # with the following statement we can start the debugger
            # import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            result = ResultObject(result_from_keyword, context.variables.as_dict(), "OK")
            return jsonpickle.encode(result)
        except HandlerExecutionFailed as e:
            result = ResultObject(e.message, None, e.status)
            BuiltIn().run_keyword("Log to Console", jsonpickle.encode(result))
            return jsonpickle.encode(result), 400
        except Exception as e:
            result = ResultObject(traceback.format_exc(), None, "FATAL")
            return jsonpickle.encode(result), 500

    def exit_process(self):
        try:
            self.set_timeout(self.kill_flask, 1)
        except Exception as e:
            return "Success"

    def set_timeout(self, callback, delay):
        timer = threading.Timer(delay, callback)
        timer.start()

    def kill_flask(self):
        os.kill(os.getpid(), signal.SIGINT)

    def return_available(self):
        return "Success"