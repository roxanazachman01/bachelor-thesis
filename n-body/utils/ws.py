import json

from utils.csv import CsvUtils


class WebsocketMessage:
    @staticmethod
    def get(json_string):
        json_obj = json.loads(json_string)
        position = json_obj["position"]
        masses = json_obj["masses"]
        colors = json_obj["colors"]
        if colors is not None and masses is not None:
            return {'type': 0, 'colors': colors, 'masses': masses}
        return {'type': 1, 'position': position}

    @staticmethod
    def create(algo="", path="", dt=0.005, processor='CPU'):
        content = [] if len(path) == 0 else CsvUtils.read_data(path).tolist()
        data = {
            "algo": algo,
            "content": content,
            "dt": dt,
            "processor": processor
        }
        return json.dumps(data)

    @staticmethod
    def stop():
        data = {
            "active": False,
            "algo": "",
            "path": "",
            "dt": 0,
            "dim": 0,
            "processor": ""
        }
        return json.dumps(data)
