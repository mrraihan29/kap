document.addEventListener('DOMContentLoaded', function () {
    const usernameElement = document.getElementById('username');
    const popup = document.getElementById('popup');
    const closePopup = document.getElementById('closePopup');
    
    if (usernameElement) {
        usernameElement.onclick = function() {
            popup.classList.add('active');
        };
    }

    if (closePopup) {
        closePopup.onclick = function() {
            popup.classList.remove('active');
        };
    }
});
