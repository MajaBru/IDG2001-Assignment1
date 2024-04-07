# IDG2001 - Assignment 1 - Group 4

## Description
It is a file processing web service, which allows user to upload files, which will be processed, and return a processed file (.tar.gz).

## Local setup
1. Clone this repository.
2. Open in preferred code editor, and in terminal install dependencies by running "pip install -r requirements.txt".
3. Change dir to "src" directory and run "python app.py".
4. Open the app in the browser by following the localhost link.

## Deployment using Railway
We deployed this service with Railway here: [https://web-file-processor.up.railway.app](https://web-file-processor.up.railway.app)

## How to use:
1. On start page, choose your files for upload (either .tar.gz file or individual files). Should be these files: .csv, .md, NTNU-logo.png, signature.png. They can be found in the "Dummy" folder under /src.
2. Click "Upload"
3. Wait for processing and to be redirected
4. If successful, you will arrive at a new page saying "Upload was successful".
5. Click "Download file" to download the new processed .tar.gz file containing all PDFs.
