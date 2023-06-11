import json


class WebsocketMessage:
    @staticmethod
    def get(json_string):
        json_obj = json.loads(json_string)
        return json_obj['algo'], json_obj['content'], json_obj['dt'], json_obj['processor']

    @staticmethod
    def create(position=None, velocity=None, masses=None, colors=None):
        data = {
            "position": None if position is None else position.tolist(),
            "velocity": None if velocity is None else velocity.tolist(),
            "masses": None if masses is None else masses.tolist(),
            "colors": colors
        }
        return json.dumps(data)
