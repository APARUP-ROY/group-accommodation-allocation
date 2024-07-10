import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import pandas as pd
from io import StringIO, BytesIO
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allocate_rooms(group_data, hostel_data):
    # Logic to allocate rooms based on group and hostel data
    # Implement your allocation logic here
    allocation_results = "Sample allocation results"  # Replace with actual allocation logic
    return allocation_results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'group_file' not in request.files or 'hostel_file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    group_file = request.files['group_file']
    hostel_file = request.files['hostel_file']

    if group_file.filename == '' or hostel_file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if group_file and allowed_file(group_file.filename) and hostel_file and allowed_file(hostel_file.filename):
        group_filename = secure_filename(group_file.filename)
        hostel_filename = secure_filename(hostel_file.filename)

        group_file.save(os.path.join(app.config['UPLOAD_FOLDER'], group_filename))
        hostel_file.save(os.path.join(app.config['UPLOAD_FOLDER'], hostel_filename))

        # Load CSV data into pandas DataFrames
        group_data = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], group_filename))
        hostel_data = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], hostel_filename))

        # Perform room allocation
        allocation_results = allocate_rooms(group_data, hostel_data)

        return render_template('results.html', tables=[allocation_results.to_html(classes='data')])

    else:
        flash('Allowed file types are csv')
        return redirect(request.url)

@app.route('/download')
def download_file():
    # Generate a CSV file to download (placeholder)
    data = {'Group ID': [101, 102, 103],
            'Hostel Name': ['Boys Hostel A', 'Girls Hostel B', 'Boys Hostel A'],
            'Room Number': [101, 202, 102]}
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)

    # Return the CSV file as an attachment for download
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=allocation_results.csv"})

if __name__ == '__main__':
    app.run(debug=True)
