import json


class WebsocketMessage:
    @staticmethod
    def get(json_string):
        json_obj = json.loads(json_string)
        position = json_obj["position"]
        velocity = json_obj["velocity"]
        masses = json_obj["masses"]
        colors = json_obj["colors"]
        if colors is not None and masses is not None:
            return {'type': 0, 'colors': colors, 'masses': masses}
        return {'type': 1, 'position': position, 'velocity': velocity}

    @staticmethod
    def create(algo="", path="", dt=0.005, dim=3, processor='CPU'):
        data = {
            "active": True,
            "algo": algo,
            "path": path,
            "dt": dt,
            "dim": dim,
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
