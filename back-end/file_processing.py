import os
import csv
from fpdf import FPDF
import tarfile
from flask import Flask, request, render_template, redirect, url_for, send_file

app = Flask(__name__, template_folder='../front-end')

# make directories
os.makedirs("PDF", exist_ok=True)
os.makedirs("MD", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)

# paths
UPLOADS_PATH = "./uploads"
PDF_PATH = "./PDF"
MD_PATH = "./MD"
PROCESSED_PATH = "./processed"

# files
CSV_FILE = os.path.join(UPLOADS_PATH, "people.csv")
MARKDOWN_TEMPLATE = os.path.join(UPLOADS_PATH, "template.md")


# home, just renders the form page
@app.route('/')
def home():
    return render_template('upload.html')

# upload route, handles file upload and processing
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(UPLOADS_PATH, uploaded_file.filename)
            uploaded_file.save(file_path)
            process_files(file_path)
            return redirect(url_for('upload'))
            # make download link available
            return render_template('upload.html', download=True)
            
    return render_template('upload.html')

@app.route('/download')
def download():
    return send_file('processed/certificates.tar.gz', as_attachment=True)
    
def extract_gz(file_path):
    with tarfile.open(file_path, "r:gz") as tar:
        for member in tar.getmembers():
    
            member.name = os.path.basename(member.name)
            tar.extract(member, path=UPLOADS_PATH)


def process_files(file_path):
    # extract .tar.gz file
    if file_path.endswith('.tar.gz'):
        extract_gz(file_path)
        os.remove(file_path)

    # file processing logic
    csv_data = read_csv_file()
    modify_and_write_markdown(csv_data)

    for mdfile in os.listdir(MD_PATH):
        if mdfile.endswith(".md"):
            md_file_path = os.path.join(MD_PATH, mdfile)
            convert_to_pdf(md_file_path)

    # make .tar.gz file with certificates
    with tarfile.open(os.path.join(PROCESSED_PATH, 'certificates.tar.gz'), "w:gz") as tar:
        tar.add(PDF_PATH, arcname=os.path.basename(PDF_PATH))


def read_csv_file():
    print("Reading CSV file...")
    data = []
    with open(CSV_FILE, 'r') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            data.append(row)
    return data


def modify_and_write_markdown(data):
    print("Modifying markdown template...")
    with open(MARKDOWN_TEMPLATE, 'r') as template:
        markdown = template.read()

    for person in data:
        modified_markdown = markdown.replace("{{FirstName}}", person['First name'])
        modified_markdown = modified_markdown.replace("{{LastName}}", person['Last name'])

        md_filename = f"{person['First name']}_{person['Last name']}.md"
        md_filepath = os.path.join(MD_PATH, md_filename)
        with open(md_filepath, 'w') as md_file:
            md_file.write(modified_markdown)
    print("Markdown files generated.")


def convert_to_pdf(md_file):
    pdf = FPDF()
    pdf.add_page()

    with open(md_file, 'r') as md:
        lines = md.readlines()
        for line in lines:
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, line)
    pdf_file = os.path.basename(md_file).replace(".md", ".pdf")
    pdf.output(os.path.join(PDF_PATH, pdf_file))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
