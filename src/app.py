import os
import csv
from fpdf import FPDF
import tarfile
from flask import Flask, request, render_template, redirect, url_for, flash
from flask import send_file

app = Flask(__name__, template_folder='../front-end')


# make directories
def create_dir(dir_name):
    dir_path = os.path.abspath(dir_name)
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


# paths
UPLOADS_PATH = create_dir("./uploads")
PDF_PATH = create_dir("./PDF")
MD_PATH = create_dir("./MD")
PROCESSED_PATH = create_dir("./processed")


# files in variables. Will define them when processing files
CSV_FILE = None
MARKDOWN_TEMPLATE = None


def get_downloaded_files():
    downloaded_files = []
    for filename in os.listdir(PROCESSED_PATH):
        downloaded_files.append(filename)
    return downloaded_files


# home, just renders the form page
@app.route('/')
def home():
    return render_template('index.html')


# upload route, handles file upload and processing
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('file')

        for uploaded_file in uploaded_files:
            if uploaded_file.filename != '':
                file_path = os.path.join(UPLOADS_PATH, uploaded_file.filename)
                uploaded_file.save(file_path)
                process_files(file_path)
            else:
                flash("invalid file type.")
                return redirect(request.url)
        # make download link available
        return redirect(url_for('upload_success', download=True))

    return render_template('index.html')


@app.route('/upload/success')
def upload_success():
    downloaded_files = get_downloaded_files()
    print("downloaded files:", downloaded_files)
    return render_template('upload_success.html',
                           downloaded_files=downloaded_files)


@app.route('/download')
def download():
    return send_file(os.path.join(PROCESSED_PATH, 'certificates.tar.gz'),
                     as_attachment=True)





def process_files(file_path):
    if file_path.endswith('.tar.gz'):
        extract_gz(file_path)
        os.remove(file_path)
        process_extracted_files()
    elif file_path.endswith('.csv'):
        global CSV_FILE
        CSV_FILE = file_path
    elif file_path.endswith('.md'):
        global MARKDOWN_TEMPLATE
        MARKDOWN_TEMPLATE = file_path

    if CSV_FILE and MARKDOWN_TEMPLATE:
        csv_data = read_csv_file()
        modify_and_write_markdown(csv_data)
        create_pdfs()
        create_tar_file()
    else:
        print("CSV file and MD template not found. Cant proceed with processing.")


def process_extracted_files(): 
    for extracted_file in os.listdir(UPLOADS_PATH):
        extracted_file_path = os.path.join(UPLOADS_PATH, extracted_file)
        if extracted_file.endswith('.csv'):
            global CSV_FILE
            CSV_FILE = extracted_file_path
        elif extracted_file.endswith('.md'):
            global MARKDOWN_TEMPLATE
            MARKDOWN_TEMPLATE = extracted_file_path


def extract_gz(file_path):
    with tarfile.open(file_path, "r:gz") as tar:
        for member in tar.getmembers():
            member.name = os.path.basename(member.name)
            tar.extract(member, path=UPLOADS_PATH)


### functions dealing with the processing 

def read_csv_file():
    print("Reading CSV file...")
    data = []
    with open(CSV_FILE, 'r') as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        for row in csv_reader:
            data.append(row)
    return data


def modify_and_write_markdown(data):
    print("Modifying markdown template...")
    with open(MARKDOWN_TEMPLATE, 'r') as template:
        markdown = template.read()
    for person in data:
        modified_markdown = markdown.replace("{{FirstName}}", person['FirstName'])
        modified_markdown = modified_markdown.replace("{{LastName}}", person['LastName'])

        md_filename = f"{person['FirstName']}_{person['LastName']}.md"
        md_filepath = os.path.join(MD_PATH, md_filename)
        with open(md_filepath, 'w') as md_file:
            md_file.write(modified_markdown)
    print("Markdown files generated.")


def convert_to_pdf(md_file): # https://py-pdf.github.io/fpdf2/Tutorial.html fpdf
    pdf = FPDF()
    pdf.add_page()

    with open(md_file, 'r') as md:
        lines = md.readlines()
        for line in lines:
            
            placeholder = line.strip().endswith('.png)') # getting the line where the images are located on the md file
            if placeholder:
                
                # find the images in uploads
                if "NTNU-logo.png" in line:
                    image_path = os.path.join(UPLOADS_PATH, "NTNU-logo.png") 
                elif "signature.png" in line:
                    image_path = os.path.join(UPLOADS_PATH, "signature.png")

                if os.path.exists(image_path):
                    pdf.image(image_path, x=pdf.get_x(), y=pdf.get_y(), w=50)
                    pdf.ln(20)
            else:
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, line)

    pdf_file = os.path.basename(md_file).replace(".md", ".pdf")
    pdf.output(os.path.join(PDF_PATH, pdf_file))

def create_pdfs():
    for mdfile in os.listdir(MD_PATH):
        if mdfile.endswith(".md"):
            md_file_path = os.path.join(MD_PATH, mdfile)
            convert_to_pdf(md_file_path)

def create_tar_file():
    with tarfile.open(os.path.join(PROCESSED_PATH, 'certificates.tar.gz'),
                      "w:gz") as tar:
        tar.add(PDF_PATH, arcname=os.path.basename(PDF_PATH))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
