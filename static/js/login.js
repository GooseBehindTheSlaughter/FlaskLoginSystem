// Search the error box and see if it has anything in it
document.addEventListener("DOMContentLoaded", function() {
    var errorMessage = document.querySelector('.flash-message p');
    if (errorMessage && errorMessage.innerText != "" ) 
    {
        alert(errorMessage.innerText); // Server supplies the error
    }
});