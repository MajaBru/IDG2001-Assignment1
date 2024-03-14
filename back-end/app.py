from flask import Flask, request, send_file
import tempfile
import shutil
import os
import tarfile
import csv
import markdown2pdf

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_files():
    # Check if the POST request has the file part
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    
    # Save uploaded tar.gz file to a temporary directory
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, file.filename)
    file.save(file_path)

    # Call the process_files function to process the uploaded file
    process_files(temp_dir, file_path)

    # Create a new tar.gz file with processed PDFs
    output_file = os.path.join(temp_dir, 'output.tar.gz')
    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(os.path.join(temp_dir, "PDF"), arcname=os.path.basename("PDF"))

    # Send the processed tar.gz file for download
    return send_file(output_file, as_attachment=True)

def process_files(temp_dir, input_tar):
    # Load CSV file
    with open(os.path.join(temp_dir, "data.csv"), "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Load Markdown template
            with open(os.path.join(temp_dir, "template.md"), "r") as md_file:
                template = md_file.read()
            
            # Replace placeholders with values from CSV
            processed_md = template.replace("{name}", row["name"])
            # Save processed Markdown
            with open(os.path.join(temp_dir, "MD", f"{row['name']}.md"), "w") as processed_md_file:
                processed_md_file.write(processed_md)

            # Convert Markdown to PDF
            markdown2pdf.markdown2pdf(os.path.join(temp_dir, "MD", f"{row['name']}.md"), os.path.join(temp_dir, "PDF", f"{row['name']}.pdf"))

if __name__ == "__main__":
    app.run(debug=True)
