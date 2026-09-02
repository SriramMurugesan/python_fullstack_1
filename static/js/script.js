let registerForm = document.getElementById("registerForm")
if (registerForm) {
    registerForm.addEventListener("submit", function (event) {
        event.preventDefault();
        console.log(event);
        let name = document.getElementById("name").value;
        let email = document.getElementById("email").value;
        let password = document.getElementById("password").value;
        let date = document.getElementById("date").value;
        let male = document.getElementById("male").checked;
        let female = document.getElementById("female").checked;
        let course = document.getElementById("course").value;
        let gender = "";
        if (male) {
            gender = "male";
        } else if (female) {
            gender = "female";
        }
        if (name == "" || email == "" || password == "" || date == "" || gender == "" || course == "") {
            alert("Please fill all the fields");
        } else {
            fetch("/api/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password,
                    dob: date,
                    gender: gender,
                    courses: course
                })
            })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    window.location.href = "/login";

                });
        }

    }
    )
}
let loginForm = document.getElementById("loginForm")
if (loginForm) {
    loginForm.addEventListener("submit", function (event) {
        event.preventDefault();
        console.log(event);
        let email = document.getElementById("loginEmail").value;
        let password = document.getElementById("loginPassword").value;
        if (email == "" || password == "") {
            alert("Please fill all the fields");
        } else {

            alert("Login successful");
        }

    })
}
