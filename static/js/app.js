document.addEventListener('DOMContentLoaded', () => {
    // Registration form handling
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const completePassword = document.getElementById('completePassword').value;
            const firstName = document.getElementById('firstName').value;
            const lastName = document.getElementById('lastName').value;
            const surname = document.getElementById('surname').value;

            const response = await fetch('/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email, password, complete_password: completePassword, phone, first_name: firstName, last_name: lastName, surname
                })
            });

            if (response.ok) {
                alert('Registration successful');
            } else {
                const error = await response.json();
                alert(`Error: ${error.detail}`);
            }
        });
    }

    // Login form handling
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            const response = await fetch('/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    username, password
                })
            });

            if (response.ok) {
                alert('Login successful');
            } else {
                const error = await response.json();
                alert(`Error: ${error.detail}`);
            }
        });
    }

    // Change password form handling
    const changePasswordForm = document.getElementById('changePasswordForm');
    if (changePasswordForm) {
        changePasswordForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const completePassword = document.getElementById('completePassword').value;

            const response = await fetch('/change_password/', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email, password, complete_password: completePassword
                })
            });

            if (response.ok) {
                alert('Password changed successfully');
            } else {
                const error = await response.json();
                alert(`Error: ${error.detail}`);
            }
        });
    }

    // Update user form handling
    const updateUserForm = document.getElementById('updateUserForm');
    if (updateUserForm) {
        updateUserForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const firstName = document.getElementById('firstName').value;
            const lastName = document.getElementById('lastName').value;
            const surname = document.getElementById('surname').value;

            const token = document.cookie.split('access_token=')[1] || '';

            const response = await fetch('/update/', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    first_name: firstName, last_name: lastName, surname
                })
            });

            if (response.ok) {
                alert('User updated successfully');
            } else {
                const error = await response.json();
                alert(`Error: ${error.detail}`);
            }
        });
    }
});
