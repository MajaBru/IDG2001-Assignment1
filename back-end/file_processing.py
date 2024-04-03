import os
import csv
from fpdf import FPDF
import tarfile
from flask import Flask, request, render_template, redirect
from flask import send_from_directory

app = Flask(__name__, template_folder='../front-end')

app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOADS_PATH'] = "./uploads"
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'md', 'pdf', 'tar.gz'}


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files.getlist('file')
        for uploaded_file in uploaded_file:
            if uploaded_file.filename != '':
                file_path = os.path.join(UPLOADS_PATH, uploaded_file.filename)
                uploaded_file.save(file_path)
        return 'Files uploaded successfully'
    return render_template('upload.html')


# flask route
def process_csv(file_path):
    # Add your code here to process the CSV file
    return "processed_file.pdf"


# paths
UPLOADS_PATH = "./uploads"
PDF_PATH = "./PDF"
MD_PATH = "./MD"
PROCESSED_PATH = "./processed"


# make directories
os.makedirs("PDF", exist_ok=True)
os.makedirs("MD", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)


# files
CSV_FILE = os.path.join(UPLOADS_PATH, "people.csv")
MARKDOWN_TEMPLATE = os.path.join(UPLOADS_PATH, "template.md")


# read csv file ... JUST A DUMMY FILE FOR TESTING
def read_csv_file():
    print("Reading CSV file...")
    data = [] 
    with open(CSV_FILE, 'r') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            data.append(row)
    return data


# modify the markdown template with data from the csv file
def modify_and_write_markdown(data):
    print("Modifying markdown template...")
    with open(MARKDOWN_TEMPLATE, 'r') as template:
        markdown = template.read()

    for person in data:
        modified_markdown = markdown.replace("{{FirstName}}", person
                                             ['First name'])
        modified_markdown = modified_markdown.replace("{{LastName}}", 
                                                      person['Last name'])

        # Create a markdown file for each person
        md_filename = f"{person['First name']}_{person['Last name']}.md"
        md_filepath = os.path.join(MD_PATH, md_filename)
        with open(md_filepath, 'w') as md_file:
            md_file.write(modified_markdown)
    print("Markdown files generated.")


csv_data = read_csv_file()
modify_and_write_markdown(csv_data)


# convert MD to PDF
def convert_to_pdf(md_file):

    pdf = FPDF()
    pdf.add_page()

    # read MD file
    with open(md_file, 'r') as md:
        lines = md.readlines()
        for line in lines:
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, line)
    # replace file extension
    pdf_file = os.path.basename(md_file).replace(".md", ".pdf")

    # save PDF in folder
    pdf.output(os.path.join(PDF_PATH, pdf_file))


# loop through all MD files and convert to PDF
for mdfile in os.listdir(MD_PATH):
    if mdfile.endswith(".md"):
        md_file_path = os.path.join(MD_PATH, mdfile)
        convert_to_pdf(md_file_path)

# PDF folder into tar.gz file

with tarfile.open(
    os.path.join(PROCESSED_PATH, 'certificates.tar.gz'), "w:gz"
) as tar:
    tar.add(PDF_PATH)


def uploaded_file():
    if 'file' not in request.files:
        return redirect(request.url)


@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(app.config['PDF_PATH'],
                               filename, as_attachment=True)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
