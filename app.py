from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(days=7)

documents_list = [
        {"id":"doc_grundbuchauszug", "name": "Grundbuch", "preis": 50, "beschreibung": "Ein Grundbuchauszug enthält Informationen über die Eigentümer und Rechte an einer Immobilie."},
        {"id":"doc_flurkarte", "name": "Flurkarte", "preis": 12.80, "beschreibung": "Eine Flurkarte zeigt die genaue Lage und Abgrenzung von Grundstücken."},
        {"id":"doc_teilungserklaerung", "name": "Teilungserklärung", "preis": 100, "beschreibung": "Die Teilungserklärung teilt das Gebäude in einzelne Eigentumseinheiten auf."},
        {"id":"doc_aufteilungsplan", "name": "Aufteilungsplan", "preis": 70, "beschreibung": "Der Aufteilungsplan zeigt die räumliche Aufteilung der Immobilie."},
        {"id":"doc_eintragungsbewilligung", "name": "Eintragungsbewilligung", "preis": 40, "beschreibung": "Die Eintragungsbewilligung ist die Zustimmung zur Eintragung von Rechten ins Grundbuch."},
        {"id":"doc_baulastenverzeichnis", "name": "Baulastenverzeichnis", "preis": 20, "beschreibung": "Das Baulastenverzeichnis enthält Informationen über öffentlich-rechtliche Verpflichtungen eines Grundstücks."},
        {"id":"doc_altlastenverzeichnis", "name": "Altlastenverzeichnis", "preis": 25, "beschreibung": "Das Altlastenverzeichnis gibt Auskunft über Boden- und Grundwasserverunreinigungen."}
    ]

# Konvertiere die Liste in ein Dictionary
documents = {doc['id']: doc for doc in documents_list}

@app.route('/')
def index():
    return redirect(url_for('produkte'))

@app.route('/produkte', methods=['GET', 'POST'])
def produkte():
    if request.method == 'POST':
        selected_documents = request.form.getlist('documents')
        session['selected_documents'] = selected_documents
        return redirect(url_for('immobiliendaten'))
    return render_template('produkte.html', documents=documents, active_page='produkte')

@app.route('/immobiliendaten', methods=['GET', 'POST'])
def immobiliendaten():
    if request.method == 'POST':
        session['immo_strasse'] = request.form['immo_strasse']
        session['immo_hausnummer'] = request.form['immo_hausnummer']
        session['immo_plz'] = request.form['immo_plz']
        session['immo_ort'] = request.form['immo_ort']
        session['buyer_is_owner'] = request.form['buyer_is_owner']
        session['eigentuemer_typ'] = request.form['eigentuemer_typ']
        session['eigentuemer_firmenname'] = request.form['eigentuemer_firmenname']
        session['eigentuemer_vorname'] = request.form['eigentuemer_vorname']
        session['eigentuemer_nachname'] = request.form['eigentuemer_nachname']
        session['eigentuemer_strasse'] = request.form['eigentuemer_strasse']
        session['eigentuemer_hausnummer'] = request.form['eigentuemer_hausnummer']
        session['eigentuemer_plz'] = request.form['eigentuemer_plz']
        session['eigentuemer_ort'] = request.form['eigentuemer_ort']
        return redirect(url_for('kundendaten'))
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
    selected_documents = session.get('selected_documents', [])
    return render_template('angaben.html', documents=documents, selected_documents=selected_documents, active_page='angaben')

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