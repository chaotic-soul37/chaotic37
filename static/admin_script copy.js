
const socket = io.connect("http://localhost:5000");
const ADMIN_PASSWORD = "admin123"; // Change this to your desired password

function validateAdmin() {
    const enteredPassword = document.getElementById("adminPassword").value;
    if (enteredPassword === ADMIN_PASSWORD) {
        alert("logged in successfully!");
        
        document.getElementById("loginbox").classList.add("hidden");
        
        document.getElementById("adminPage").classList.remove("hidden");
        
    } else {
        alert("Incorrect Password!");
    }
}

function addProfile() {
    const profileName = document.getElementById("newProfileName").value.trim();
    if (profileName) {
        socket.emit("add_profile", { name: profileName });
        document.getElementById("newProfileName").value = "";
    }
}

function logoutAdmin() {
    window.location.href = "/";
}

document.addEventListener("DOMContentLoaded", function () {
    const passwordField = document.getElementById("adminPassword");

    // Create an eye button dynamically and insert it after the password field
    if (passwordField) {
        const toggleButton = document.createElement("button");
        toggleButton.innerHTML = "👁️"; // Eye icon
        toggleButton.classList.add("absolute", "inset-y-0", "right-3", "flex", "items-center", "bg-transparent", "border-none", "cursor-pointer", "text-gray-500");
        toggleButton.style.padding = "8px"; // Add padding for better UI

        // Wrap password input in a div for positioning
        const wrapperDiv = document.createElement("div");
        wrapperDiv.classList.add("relative", "w-full");
        passwordField.parentNode.insertBefore(wrapperDiv, passwordField);
        wrapperDiv.appendChild(passwordField);
        wrapperDiv.appendChild(toggleButton);

        // Toggle password visibility on button click
        toggleButton.addEventListener("click", function () {
            if (passwordField.type === "password") {
                passwordField.type = "text";
                toggleButton.innerHTML = "🙈"; // Closed-eye icon
            } else {
                passwordField.type = "password";
                toggleButton.innerHTML = "👁️"; // Open-eye icon
            }
        });
    }
});

