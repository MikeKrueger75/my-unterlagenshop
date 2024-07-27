from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    documents = [
        "Grundbuch",
        "Flurkarte",
        "Teilungserklärung",
        "Aufteilungsplan",
        "Eintragungsbewilligung",
        "Baulastenverzeichnis",
        "Altlastenverzeichnis"
    ]
    return render_template('produkte.html', documents=documents)

if __name__ == '__main__':
    app.run(debug=True)