from flask import Flask, render_template, redirect, url_for, request, session, send_file
from datetime import timedelta
import pandas as pd
import os
from pdf_filler import create_pdf_with_data

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(days=7)

# Laden der Dokumente aus der CSV-Datei
documents_df = pd.read_csv('./conf/documentdefinition.csv')
documents_list = documents_df.to_dict(orient='records')
documents = {doc['id']: doc for doc in documents_list}

# Laden der Felddefintion
fields_df = pd.read_csv('./conf/felddefinition.csv')

def storeSessionData(session, request):
    for key in request.form.keys():
        #print(f"{key} = {request.form.get(key)}")
        session[key] = request.form.get(key)

@app.route('/')
def index():
    session.clear()
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
        storeSessionData(session, request)
        return redirect(url_for('kundendaten'))
    return render_template('immobiliendaten.html', active_page='immobiliendaten')

@app.route('/kundendaten', methods=['GET', 'POST'])
def kundendaten():
    if request.method == 'POST':
        storeSessionData(session, request)
        return redirect(url_for('angaben'))
    return render_template('kundendaten.html', session=session, active_page='kundendaten')

@app.route('/angaben', methods=['GET', 'POST'])
def angaben():
    if request.method == 'POST':
        storeSessionData(session, request)
        return redirect(url_for('eigentuemervollmacht'))

    selected_documents = session.get('selected_documents', [])
    
    # Erstellung einer Liste von Feldern, die für die ausgewählten Unterlagen erforderlich sind
    fields_to_show = set()
    for doc_id in selected_documents:
        if doc_id in fields_df.columns:
            required_fields = fields_df.index[fields_df[doc_id] == 'x'].tolist()
            fields_to_show.update(required_fields)
    
    return render_template('angaben.html', documents=documents, selected_documents=selected_documents, fields_df=fields_df, fields_to_show=fields_to_show, active_page='angaben')

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

@app.route('/download_vollmacht')
def download_vollmacht():
    pdf_path = create_pdf_with_data(session)
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)