from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def create_overlay(data_dict):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 9)

    # Example positions - you need to adjust them to fit your PDF fields
    x=170
    y=700
    rowMargin=18
    if 'eigentuemer_nachname' in data_dict:
        can.drawString(x, y, data_dict['eigentuemer_nachname'])
    if 'eigentuemer_vorname' in data_dict:
        can.drawString(x, y-(rowMargin*1), data_dict['eigentuemer_vorname'])
    if 'eigentuemer_strasse' in data_dict:
        can.drawString(x + 45, y-(rowMargin*3), data_dict['eigentuemer_strasse'])
    if 'eigentuemer_hausnummer' in data_dict:
        can.drawString(x + 320, y-(rowMargin*3), data_dict['eigentuemer_hausnummer'])
    if 'eigentuemer_plz' in data_dict:
        can.drawString(x + 45, y-(rowMargin*4), data_dict['eigentuemer_plz'])
    if 'eigentuemer_ort' in data_dict:
        can.drawString(x + 230, y-(rowMargin*4), data_dict['eigentuemer_ort'])
    if 'immo_strasse' in data_dict:
        can.drawString(x + 45, y-(rowMargin*10)+5, data_dict['immo_strasse'])
    if 'immo_hausnummer' in data_dict:
        can.drawString(x + 320, y-(rowMargin*10)+5, data_dict['immo_hausnummer'])
    if 'immo_plz' in data_dict:
        can.drawString(x + 45, y-(rowMargin*11)+5, data_dict['immo_plz'])
    if 'immo_ort' in data_dict:
        can.drawString(x + 230, y-(rowMargin*11)+5, data_dict['immo_ort'])
    if 'ang_grundbuch_von' in data_dict:
        can.drawString(x, y-(rowMargin*12), data_dict['ang_grundbuch_von'])
    if 'ang_band_blatt' in data_dict:
        can.drawString(x, y-(rowMargin*13), data_dict['ang_band_blatt'])
    if 'ang_gemarkung' in data_dict:
        can.drawString(x, y-(rowMargin*14), data_dict['ang_gemarkung'])
    if 'ang_flur' in data_dict:
        can.drawString(x, y-(rowMargin*15), data_dict['ang_flur'])
    
    can.save()
    packet.seek(0)
    return packet

def merge_pdfs(input_pdf_path, overlay_pdf_path, output_pdf_path):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Get the first page of the existing PDF
    page = reader.pages[0]

    # Merge the overlay on top of the existing page
    overlay = PdfReader(overlay_pdf_path).pages[0]
    page.merge_page(overlay)

    writer.add_page(page)

    # Write the final output to a new PDF
    with open(output_pdf_path, 'wb') as output_pdf:
        writer.write(output_pdf)

def create_pdf_with_data(session_data):
    input_pdf_path = './conf/Blanko_Vollmacht_Value.pdf'
    output_pdf_path = './temp/Eigentümervollmacht_Value_.pdf'
    overlay_pdf_path = './temp/overlay.pdf'

    # Map the session data to the PDF field names
    if session_data.get('eigentuemer_typ', '') == 'eigentuemer_person':
        name = session_data.get('eigentuemer_nachname', '')
        vorname = session_data.get('eigentuemer_vorname', '')
    else:
        name = session_data.get('eigentuemer_firmenname', '')
        vorname = ''
    data_dict = {
        'eigentuemer_nachname': name,
        'eigentuemer_vorname': vorname, 
        'eigentuemer_strasse': session_data.get('eigentuemer_strasse', ''),
        'eigentuemer_hausnummer': session_data.get('eigentuemer_hausnummer', ''),
        'eigentuemer_plz': session_data.get('eigentuemer_plz', ''),
        'eigentuemer_ort': session_data.get('eigentuemer_ort', ''),
        'immo_strasse': session_data.get('immo_strasse', ''),
        'immo_hausnummer': session_data.get('immo_hausnummer', ''),
        'immo_plz': session_data.get('immo_plz', ''),
        'immo_ort': session_data.get('immo_ort', ''),
        'ang_grundbuch_von': session_data.get('ang_grundbuch_von', ''),
        'ang_band_blatt': session_data.get('ang_band_blatt', ''),
        'ang_gemarkung': session_data.get('ang_gemarkung', ''),
        'ang_flur': session_data.get('ang_flur', '') + ' / ' + session_data.get('ang_flurstuecke', '')
    }

    overlay = create_overlay(data_dict)

    with open(overlay_pdf_path, 'wb') as f:
        f.write(overlay.read())

    merge_pdfs(input_pdf_path, overlay_pdf_path, output_pdf_path)

    return output_pdf_path