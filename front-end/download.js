document.querySelector("#upload-form").addEventListener('submit', function(e) {
    e.preventDefault();

    // Create a new FormData instance
    let formData = new FormData();

    // Get the files from the input field
    let files = document.querySelector('#file').files;

    // Append each file to the FormData instance
    for (let i = 0; i < files.length; i++) {
        formData.append('file', files[i]);
    }

    // Send the files to the server
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        // After successful upload, show the download link
        document.querySelector('#download-link').style.display = 'block';
    })
    .catch(error => {
        console.error('Error uploading file:', error);
    });
});