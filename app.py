from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(days=7)

@app.route('/')
def index():
    return redirect(url_for('produkte'))

@app.route('/produkte')
def produkte():
    documents = [
        {"name": "Grundbuch", "preis": 50, "beschreibung": "Ein Grundbuchauszug enthält Informationen über die Eigentümer und Rechte an einer Immobilie."},
        {"name": "Flurkarte", "preis": 30, "beschreibung": "Eine Flurkarte zeigt die genaue Lage und Abgrenzung von Grundstücken."},
        {"name": "Teilungserklärung", "preis": 100, "beschreibung": "Die Teilungserklärung teilt das Gebäude in einzelne Eigentumseinheiten auf."},
        {"name": "Aufteilungsplan", "preis": 70, "beschreibung": "Der Aufteilungsplan zeigt die räumliche Aufteilung der Immobilie."},
        {"name": "Eintragungsbewilligung", "preis": 40, "beschreibung": "Die Eintragungsbewilligung ist die Zustimmung zur Eintragung von Rechten ins Grundbuch."},
        {"name": "Baulastenverzeichnis", "preis": 20, "beschreibung": "Das Baulastenverzeichnis enthält Informationen über öffentlich-rechtliche Verpflichtungen eines Grundstücks."},
        {"name": "Altlastenverzeichnis", "preis": 25, "beschreibung": "Das Altlastenverzeichnis gibt Auskunft über Boden- und Grundwasserverunreinigungen."}
    ]
    return render_template('produkte.html', documents=documents, active_page='produkte')

@app.route('/immobiliendaten')
def immobiliendaten():
    return render_template('immobiliendaten.html', active_page='immobiliendaten')

@app.route('/kundendaten', methods=['GET', 'POST'])
def kundendaten():
    if request.method == 'POST':
        session['anrede'] = request.form['anrede']
        session['vorname'] = request.form['vorname']
        session['nachname'] = request.form['nachname']
        session['email'] = request.form['email']
        session['telefonnummer'] = request.form['telefonnummer']
        session['strasse'] = request.form['strasse']
        session['hausnummer'] = request.form['hausnummer']
        session['plz'] = request.form['plz']
        session['ort'] = request.form['ort']
        return redirect(url_for('angaben'))
    return render_template('kundendaten.html', session=session, active_page='kundendaten')

@app.route('/angaben')
def angaben():
    return render_template('angaben.html', active_page='angaben')

@app.route('/eigentuemervollmacht')
def eigentuemervollmacht():
    return render_template('eigentuemervollmacht.html', active_page='eigentuemervollmacht')

@app.route('/zusammenfassung')
def zusammenfassung():
    return render_template('zusammenfassung.html', active_page='zusammenfassung')

@app.route('/bezahlung')
def bezahlung():
    return render_template('bezahlung.html', active_page='bezahlung')

@app.route('/bestaetigung')
def bestaetigung():
    return render_template('bestaetigung.html', active_page='bestaetigung')

if __name__ == '__main__':
    app.run(debug=True)