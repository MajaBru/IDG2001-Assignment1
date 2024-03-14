import tarfile
import os
import csv
import markdown2pdf

def process_files(input_tar, output_tar):
    # Create output directories if not exists
    os.makedirs("MD", exist_ok=True)
    os.makedirs("PDF", exist_ok=True)

    # Extract tar.gz file
    with tarfile.open(input_tar, "r:gz") as tar:
        tar.extractall("temp")

    # Load CSV file
    with open("temp/data.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Load Markdown template
            with open("temp/template.md", "r") as md_file:
                template = md_file.read()
            
            # Replace placeholders with values from CSV
            processed_md = template.replace("{name}", row["name"])
            # Save processed Markdown
            with open(f"MD/{row['name']}.md", "w") as processed_md_file:
                processed_md_file.write(processed_md)

            # Convert Markdown to PDF
            markdown2pdf.markdown2pdf(f"MD/{row['name']}.md", f"PDF/{row['name']}.pdf")

    # Create new tar.gz file with processed PDFs
    with tarfile.open(output_tar, "w:gz") as tar:
        tar.add("PDF", arcname=os.path.basename("PDF"))

if __name__ == "__main__":
    process_files("input.tar.gz", "output.tar.gz")
