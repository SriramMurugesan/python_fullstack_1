// ==========================================
// 1. REGISTER USER
// ==========================================
let registerForm = document.getElementById("registerForm");

if (registerForm) {
    registerForm.addEventListener("submit", function (event) {
        event.preventDefault();

        // Get values from form
        let name = document.getElementById("name").value;
        let email = document.getElementById("email").value;
        let password = document.getElementById("password").value;
        let dob = document.getElementById("date") ? document.getElementById("date").value : "";
        let course = document.getElementById("course") ? document.getElementById("course").value : "";

        let gender = "";
        if (document.getElementById("male") && document.getElementById("male").checked) {
            gender = "male";
        } else if (document.getElementById("female") && document.getElementById("female").checked) {
            gender = "female";
        }

        if (name === "" || email === "" || password === "") {
            alert("Please fill all fields!");
            return;
        }

        // Send data to backend
        fetch("/api/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: name,
                email: email,
                password: password,
                dob: dob,
                gender: gender,
                course: course
            })
        })
        .then(function (response) { return response.json(); })
        .then(function (data) {
            alert(data.message);
            if (data.status === "success") {
                window.location.href = "/login";
            }
        });
    });
}


// ==========================================
// 2. LOGIN USER
// ==========================================
let loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", function (event) {
        event.preventDefault();

        let email = document.getElementById("loginEmail").value;
        let password = document.getElementById("loginPassword").value;

        if (email === "" || password === "") {
            alert("Please enter email and password!");
            return;
        }

        fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email, password: password })
        })
        .then(function (response) { return response.json(); })
        .then(function (data) {
            alert(data.message);
            if (data.status === "success") {
                window.location.href = "/";
            }
        });
    });
}


// ==========================================
// 3. TO-DO LIST (READ, CREATE, UPDATE, DELETE)
// ==========================================
let todoList = document.getElementById("todoList");

// READ: Load tasks from backend
function loadTodos() {
    if (!todoList) return;

    fetch("/api/todos")
        .then(function (response) { return response.json(); })
        .then(function (data) {
            todoList.innerHTML = "";
            let todos = data.todos;

            if (todos.length === 0) {
                todoList.innerHTML = "<p>No tasks found.</p>";
                return;
            }

            for (let i = 0; i < todos.length; i++) {
                let item = todos[i];
                let li = document.createElement("li");
                li.className = "todo-item";

                let statusColorClass = item.status === "Completed" ? "status-completed" : "status-pending";

                li.innerHTML =
                    "<span>" + item.task + " <b class='status-badge " + statusColorClass + "'>" + item.status + "</b></span>" +
                    "<div class='todo-actions'>" +
                        "<button class='btn-toggle' onclick='updateTodoStatus(" + item.id + ", \"" + item.status + "\")'>Change Status</button>" +
                        "<button class='btn-delete' onclick='deleteTodoItem(" + item.id + ")'>Delete</button>" +
                    "</div>";

                todoList.appendChild(li);
            }
        });
}

// Automatically load tasks on page open
if (todoList) {
    loadTodos();
}


// CREATE: Add new task
let addTodoForm = document.getElementById("addTodoForm");

if (addTodoForm) {
    addTodoForm.addEventListener("submit", function (event) {
        event.preventDefault();

        let taskInput = document.getElementById("todoTask");
        let taskText = taskInput.value;

        if (taskText === "") {
            alert("Please enter a task!");
            return;
        }

        fetch("/api/todos", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ task: taskText })
        })
        .then(function (response) { return response.json(); })
        .then(function (data) {
            taskInput.value = "";
            loadTodos();
        });
    });
}


// UPDATE: Change status between Pending and Completed
function updateTodoStatus(id, currentStatus) {
    let newStatus = "Completed";
    if (currentStatus === "Completed") {
        newStatus = "Pending";
    }

    fetch("/api/todos/update/" + id, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus })
    })
    .then(function (response) { return response.json(); })
    .then(function (data) {
        loadTodos();
    });
}


// DELETE: Remove task
function deleteTodoItem(id) {
    fetch("/api/todos/delete/" + id, {
        method: "POST"
    })
    .then(function (response) { return response.json(); })
    .then(function (data) {
        loadTodos();
    });
}




