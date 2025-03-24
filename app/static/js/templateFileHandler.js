document.addEventListener('DOMContentLoaded', function() {

    const userFileInput = document.getElementById('user-research-file');
    const templateFileInput = document.getElementById('reference-research-file');
    function updateFileName(input) {
        const fileName = input.files[0] ? input.files[0].name : 'No file selected';
        const fileNameDisplay = input.parentElement.querySelector('.file-name');
        fileNameDisplay.textContent = fileName;
    }
    userFileInput.addEventListener('change', function() {
        updateFileName(this);
    })
    templateFileInput.addEventListener('change', function() {
        updateFileName(this);
    })
})