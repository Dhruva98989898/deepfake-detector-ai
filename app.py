from flask import Flask, render_template, request

import os

from detector import extract_frames

from ai_model import analyze_frame


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route("/detect", methods=["POST"])
def detect():

    if "video" not in request.files:

        return "No video selected"

    video = request.files["video"]

    if video.filename == "":

        return "No file selected"

    filepath = os.path.join(

        app.config["UPLOAD_FOLDER"],

        video.filename

    )

    video.save(filepath)

    extracted_frames = extract_frames(
        filepath
    )

    analyzed = 0

    ai_generated = 0

    for frame in extracted_frames:

        result = analyze_frame(
            frame
        )
        print(result)
        analyzed += 1

        score = result.get("type", {}).get("ai_generated", 0)

        if score > 0.5:
         ai_generated += 1

    percentage = round((ai_generated / max(analyzed, 1)) * 100, 2)

    if percentage >= 50:
     verdict = "AI Generated Content Detected"
    elif percentage >= 20:
     verdict = "Suspicious Content"
    else:
     verdict = "Likely Authentic"

    return render_template(
    "result.html",
    filename=video.filename,
    frames=len(extracted_frames),
    verdict=verdict,
    analyzed=analyzed,
    percentage=percentage
)


if __name__ == "__main__":

    app.run(
        debug=True
    )