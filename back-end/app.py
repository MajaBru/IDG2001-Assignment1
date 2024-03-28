
import os
import csv
import pandas as pd
from markdown2 import markdown
from fpdf import FPDF
import tarfile
import pdfkit
from flask import Flask, request, send_from_directory
import shutil

# Create a Flask app
app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# upload csv file that needs to be processed
@app.route('./upload', methods=['POST'])
def upload_file():

            return "no file part ine the request", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400

       tar_path = os.path.join(UPLOAD_FOLDER, 'file.filename')
file.save(tar_path)
try:
    process_files(tar.path)
except Exception as e:
    return f"Eror processing file: {e}", 500

def process_files(tar_path):
    extract_path = tar_path.replace('.tar.gz', '')
    with tarfile.open(tar_path, 'r:gz') as tar:
        tar.extractall(path=extract_path)
    
    csv_path = os.path.join(extract_path, 'data.csv')
    
    return send_from_directory(directory=PROCESSED_FOLDER, path=os.path.basename(tar_path), as_attachment=True)

df = pd.read_csv(csv_path)
for index, row in df.iterrows():
    md_content = generate_markdown(row)
    pdf_path = os.path.join(PROCESSED_FOLDER, f'{row["First name"]}_{row["Last name"]}.pdf')
    pdfkit.from_string(md_content, pdf_path)

    # create a tar.gz file
    with tarfile.open(tar_path.replace(UPLOAD_FOLDER, PROCESSED_FOLDER), 'w:gz') as tar:
        for pdf in os.listdir(PROCESSED_FOLDER):
            tar.add(os.path.join(PROCESSED_FOLDER, pdf), arcname=pdf)


    shutil.rmtree(extract_path)
    for pdf in os.listdir(PROCESSED_FOLDER):
        os.remove(os.path.join(PROCESSED_FOLDER, pdf))

def generate_markdown(row):
    markdown_template = """

{{FirstName}} {{LastName}} have successfully completed the course."""
    return markdown(markdown_template.replace("{{FirstName}}", row["First name"]).replace("{{LastName}}", row["Last name"]))

    if __name__ == '__main__':
        app.run(port=5000, debug=True)    


# # make directories
# os.makedirs("PDF", exist_ok=True)
# os.makedirs("MD", exist_ok=True)
# os.makedirs("uploads", exist_ok=True)
# os.makedirs("processed", exist_ok=True)

# # paths
# UPLOADS_PATH = "./uploads"
# PDF_PATH = "./PDF"
# MD_PATH = "./MD"
# PROCESSED_PATH = "./processed"

# # files
# CSV_FILE = os.path.join(UPLOADS_PATH, "people.csv")
# MARKDOWN_TEMPLATE = os.path.join(UPLOADS_PATH, "template.md")


# # read csv file ... JUST A DUMMY FILE FOR TESTING

# def read_csv_file():
#     print("Reading CSV file...")
#     data = [] 
#     with open(CSV_FILE, 'r') as file:
#         csv_reader = csv.DictReader(file, delimiter=';')
#         for row in csv_reader:
#             data.append(row)
#     return data


# # modify the markdown template with data from the csv file
# def modify_and_write_markdown(data):
#     print("Modifying markdown template...")
#     with open(MARKDOWN_TEMPLATE, 'r') as template:
#         markdown = template.read()

#     for person in data:
#         modified_markdown = markdown.replace("{{FirstName}}", person['First name'])
#         modified_markdown = modified_markdown.replace("{{LastName}}", person['Last name'])

#         # Create a markdown file for each person
#         md_filename = f"{person['First name']}_{person['Last name']}.md"
#         md_filepath = os.path.join(MD_PATH, md_filename)
#         with open(md_filepath, 'w') as md_file:
#             md_file.write(modified_markdown)
#     print("Markdown files generated.")


# csv_data = read_csv_file()
# modify_and_write_markdown(csv_data)


# # convert MD to PDF
# def convert_to_pdf(md_file):

#     pdf = FPDF()
#     pdf.add_page()


#     # read MD file
#     with open(md_file, 'r') as md:
#         lines = md.readlines()
#         for line in lines:
#             pdf.set_font("Arial", size=12)
#             pdf.multi_cell(0, 10, line)


# # replace file extension
#     pdf_file = os.path.basename(md_file).replace(".md", ".pdf")

#     # save PDF in folder
#     pdf.output(os.path.join(PDF_PATH, pdf_file))


# # DEfine flask enpoint for file upload
# def upload_file():
#     if 'file' not in request.files:
#         return redirect(request.url)


# # loop through all MD files and convert to PDF
# for mdfile in os.listdir(MD_PATH):
#     if mdfile.endswith(".md"):
#         md_file_path = os.path.join(MD_PATH, mdfile)
#         convert_to_pdf(md_file_path)

# # PDF folder into tar.gz file

# with tarfile.open(os.path.join(PROCESSED_PATH, 'certificates.tar.gz'), "w:gz") as tar:
#     tar.add(PDF_PATH)


# """@app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# if __name__ == '__main__':
# app.run(port=5000, debug=True)"""
