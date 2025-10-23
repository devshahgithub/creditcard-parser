from flask import Flask, render_template, request
import pdfplumber
import re

app = Flask(__name__)

def parse_statement(file):
    data = {}
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    # Simple regex patterns for demo (adjust per bank's PDF)
    data['card_variant'] = re.search(r'(Platinum|Gold|Classic|Silver)', text)
    data['last_4_digits'] = re.search(r'(\d{4})$', text)
    data['billing_cycle'] = re.search(r'Billing Cycle: (\d{2}/\d{2}/\d{4} - \d{2}/\d{2}/\d{4})', text)
    data['due_date'] = re.search(r'Payment Due Date: (\d{2}/\d{2}/\d{4})', text)
    data['total_balance'] = re.search(r'Total Balance: ₹?([\d,]+\.\d{2})', text)

    for k, v in data.items():
        data[k] = v.group(1) if v else "Not found"

    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    if not file.filename.lower().endswith('.pdf'):
        return "Only PDF files are allowed!"

    data = parse_statement(file)
    return render_template('results.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
