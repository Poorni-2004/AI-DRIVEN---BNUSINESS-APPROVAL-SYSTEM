from flask import Flask, request, render_template, redirect, url_for
import pytesseract
from PIL import Image
import os
import re
import cv2
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Path to Tesseract-OCR on Windows (Update if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Aadhaar and PAN validation using regex
def verify_aadhaar(text):
    return re.search(r'\b\d{4}\s\d{4}\s\d{4}\b', text) is not None

def verify_pan(text):
    return re.search(r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b', text) is not None

# Preprocess image to improve OCR results
def preprocess_image(filepath):
    img = cv2.imread(filepath)
    
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply binary thresholding to enhance the text
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # Optional: Apply noise removal (Denoising)
    thresh = cv2.fastNlMeansDenoising(thresh, None, 30, 7, 21)
    
    # Save the processed image for debugging (optional)
    processed_filepath = filepath.replace(".jpg", "_processed.jpg")
    cv2.imwrite(processed_filepath, thresh)

    return thresh

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    results = []
    valid_documents = {'aadhaar': False, 'pan': False}

    for key in request.files:
        file = request.files[key]
        if file.filename != '':
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            try:
                # Preprocess the image
                processed_image = preprocess_image(filepath)

                # Perform OCR on the preprocessed image
                text = pytesseract.image_to_string(processed_image)
                text = text.strip()

                # Check for Aadhaar or PAN card validity
                if "aadhaar" in file.filename.lower():
                    valid = verify_aadhaar(text)
                    if valid:
                        results.append(f"Aadhaar Card: ✅ Valid")
                        valid_documents['aadhaar'] = True
                        # Generate certificate for valid Aadhaar
                        generate_certificate(file.filename, 'Aadhaar')
                    else:
                        results.append(f"Aadhaar Card: ❌ Invalid")
                
                elif "pan" in file.filename.lower():
                    valid = verify_pan(text)
                    if valid:
                        results.append(f"PAN Card: ✅ Valid")
                        valid_documents['pan'] = True
                        # Generate certificate for valid PAN
                        generate_certificate(file.filename, 'PAN')
                    else:
                        results.append(f"PAN Card: ❌ Invalid")
                
                else:
                    results.append(f"{file.filename}: Uploaded and OCR done.")

            except Exception as e:
                results.append(f"Error processing {file.filename}: {str(e)}")

    # Check if both Aadhaar and PAN are valid, if so, show the payment button
    if valid_documents['aadhaar'] and valid_documents['pan']:
        return render_template('payment_page.html', results=results)
    
    # If one or both documents are invalid, show the results page with a message
    return render_template('results.html', results=results)

def generate_certificate(filename, doc_type):
    # Function to generate certificate for valid document
    certificate_path = os.path.join(UPLOAD_FOLDER, f"{doc_type}_Certificate_{filename}.pdf")
    # Logic to generate PDF certificate (for simplicity, we can use a placeholder for now)
    with open(certificate_path, 'w') as cert_file:
        cert_file.write(f"Certificate for {doc_type} Verification\nFile: {filename}\nStatus: Valid\n")
    return certificate_path

@app.route('/payment')
def payment():
    # Payment page logic (dummy page for now)
    return render_template('payment_page.html')

if __name__ == '__main__':
    app.run(debug=True)
