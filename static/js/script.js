// ==========================================
// 1. REGISTER FORM HANDLING (SIMPLE JAVASCRIPT)
// ==========================================
let registerForm = document.getElementById("registerForm");

if (registerForm) {
    registerForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Stop form from refreshing the page

        // Read all values from form input fields
        let name = document.getElementById("name").value;
        let email = document.getElementById("email").value;
        let password = document.getElementById("password").value;
        let dob = document.getElementById("date") ? document.getElementById("date").value : "";

        // Read selected gender from radio buttons
        let gender = "";
        let maleRadio = document.getElementById("male");
        let femaleRadio = document.getElementById("female");
        if (maleRadio && maleRadio.checked) {
            gender = "male";
        } else if (femaleRadio && femaleRadio.checked) {
            gender = "female";
        }

        // Read selected course from dropdown
        let course = document.getElementById("course") ? document.getElementById("course").value : "";

        // Check if required fields are empty
        if (name === "" || email === "" || password === "") {
            alert("Please fill in all required fields!");
            return;
        }

        // Send all form data to Flask server using fetch API
        fetch("/api/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                email: email,
                password: password,
                dob: dob,
                gender: gender,
                course: course
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Show pop-up message from Flask
            if (data.status === "success") {
                window.location.href = "/login"; // Redirect student to Login Page
            }
        })
        .catch(error => {
            console.error("Error during registration:", error);
        });
    });
}


// ==========================================
// 2. LOGIN FORM HANDLING (SIMPLE JAVASCRIPT)
// ==========================================
let loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Stop form from refreshing the page

        // Read values from form input fields
        let email = document.getElementById("loginEmail").value;
        let password = document.getElementById("loginPassword").value;

        // Check if any field is empty
        if (email === "" || password === "") {
            alert("Please fill in all fields!");
            return;
        }

        // Send data to Flask server using fetch API
        fetch("/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Show pop-up message from Flask
            if (data.status === "success") {
                window.location.href = "/"; // Redirect student to Home Page after successful login
            }
        })
        .catch(error => {
            console.error("Error during login:", error);
        });
    });
}


