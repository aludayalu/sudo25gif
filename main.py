import flask, gif, json, os

app = flask.Flask(__name__)

@app.get("/play_gif")
def play_gif():
    payload = json.loads(flask.request.args["payload"])
    gif.play_gif({"frames_played": 0, "number_of_frames": len(payload["frames"]), "frames": payload["frames"], "current_frame": 0, "apply_shader_transformer": "14"})

    if os.path.exists("flag.txt"):
        content = open("flag.txt").read()
        os.remove("flag.txt")

        return content
    
    return ":)"