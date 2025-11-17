function displaySuccessMessage(message) {
    const successMessage = document.getElementById('success-modal');
    console.log("cette fonction a été appelée avec ", message);
    document.getElementById('success-modal-txt').textContent = message;
    successMessage.style.display = 'flex';
}

function displayErrorMessage(message) {
    const successMessage = document.getElementById('error-modal');
    console.log("cette fonction a été appelée avec ", message);
    document.getElementById('error-modal-txt').textContent = message;
    successMessage.style.display = 'flex';
}