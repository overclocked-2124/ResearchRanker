document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('grammar-file');
    
    function updateFileName(input) {
        const fileName = input.files[0] ? input.files[0].name : "No file selected";
        const fileNameDisplay = input.parentElement.querySelector('.file-name');
        fileNameDisplay.textContent = fileName;
    }

    fileInput.addEventListener('change', function() {
        updateFileName(this);
    });
});