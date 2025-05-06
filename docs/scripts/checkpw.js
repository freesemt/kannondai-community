// Include the CryptoJS library

function checkPassword(correctHash, showHash, redirectUrl, hashMemoryName) {
    var storedHash = localStorage.getItem(hashMemoryName);
    if (showHash) {
        alert("Stored hash: " + storedHash);
    }
    
    if (storedHash === correctHash) {
        document.getElementById('protected-content').style.display = 'block';
        return;
    }

    // Show the custom password prompt
    document.getElementById('password-prompt-modal').style.display = 'block';

    // Store the parameters for use in the submitPassword function
    window.correctHash = correctHash;
    window.showHash = showHash;
    window.redirectUrl = redirectUrl;
    window.hashMemoryName = hashMemoryName;

    // Add this script to handle 'Enter' key press
    const inputField = document.getElementById('password-input');
    const submitButton = document.getElementById('submit-button');

    inputField.addEventListener('keydown', function(event) {
      if (event.key === 'Enter') {
        event.preventDefault(); // Prevent the default form submission
        submitButton.click(); // Trigger the button click
      }
    });
}

function submitPassword() {
    var password = document.getElementById('password-input').value;
    document.getElementById('password-prompt-modal').style.display = 'none';

    if (password === null || password === "") {
        alert("Password is required!");
        window.location.href = window.redirectUrl; // Redirect to the specified page
        return;
    }

    var hash = CryptoJS.SHA256(password).toString();
    if (window.showHash) {
        alert("The hashed password is: " + hash);
    }
    if (hash === window.correctHash) {
        localStorage.setItem(window.hashMemoryName, hash);
        document.getElementById('protected-content').style.display = 'block';
    } else {
        alert("Incorrect password!");
        window.location.href = window.redirectUrl; // Redirect to the specified page
    }
}