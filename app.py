from flask import Flask, render_template, request, jsonify
from ai_engine import generate_sentence, evaluate_speech
import speech_recognition as sr

app = Flask(__name__)

current_sentence = generate_sentence()


# microphone listening
def listen_from_mic():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except:
        return ""


@app.route("/")
def home():
    return render_template("index.html", sentence=current_sentence)


# MAIN microphone route
@app.route("/listen", methods=["GET"])
def listen():
    global current_sentence

    spoken_text = listen_from_mic()

    result = evaluate_speech(current_sentence, spoken_text)

    return jsonify({
        "spoken": spoken_text,
        "accuracy": result["accuracy"],
        "fluency": result["fluency"],
        "feedback": result["feedback"],
        "wrong_words": result["wrong_words"],
        "level": result["level"],
        "retry": result["retry"]
    })
@app.route("/next", methods=["GET"])
def next_sentence():
    global current_sentence

    current_sentence = generate_sentence()

    return jsonify({
        "sentence": current_sentence
    })


# optional old route (keep but fixed)
@app.route("/evaluate", methods=["POST"])
def evaluate():
    global current_sentence

    data = request.json
    spoken_text = data["spoken"]

    result = evaluate_speech(current_sentence, spoken_text)

    current_sentence = generate_sentence()

    return jsonify({
        "spoken": spoken_text,
        "accuracy": result["accuracy"],
        "fluency": result["fluency"],
        "feedback": result["feedback"],
        "wrong_words": result["wrong_words"],
        "level": result["level"],
        "retry": result["retry"],
        "next_sentence": current_sentence
    })


if __name__ == "__main__":
    app.run(debug=True)