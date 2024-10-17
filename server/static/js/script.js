// Handle theme switch
const themeSwitch = document.getElementById('themeSwitch');
const body = document.body;
const formInputs = document.querySelectorAll('input');
const labels = document.querySelectorAll('label');

themeSwitch.addEventListener('change', () => {
    if (themeSwitch.checked) {
        body.classList.add('dark-mode');
        formInputs.forEach(input => input.classList.add('dark-mode'));
        labels.forEach(label => label.classList.add('dark-mode'));
    } else {
        body.classList.remove('dark-mode');
        formInputs.forEach(input => input.classList.remove('dark-mode'));
        labels.forEach(label => label.classList.remove('dark-mode'));
    }
});

// Handle image preview for multiple uploads
const fileInput = document.getElementById('images');
const previewContainer = document.getElementById('preview');

fileInput.addEventListener('change', () => {
    // Clear previous previews
    previewContainer.innerHTML = '';

    const files = fileInput.files;
    if (files.length > 0) {
        Array.from(files).forEach(file => {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.classList.add('preview-image');
                previewContainer.appendChild(img);
            };
            reader.readAsDataURL(file);
        });
    }
});

// Handle form submission
const form = document.getElementById('userForm');
const messageDiv = document.getElementById('message');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('name', document.getElementById('name').value);
    formData.append('email', document.getElementById('email').value);
    formData.append('age', document.getElementById('age').value);

    const files = document.getElementById('images').files;
    Array.from(files).forEach(file => {
        formData.append('files', file);
    });

    try {
        const response = await fetch('/add-user/', {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            messageDiv.innerHTML = `<p class="success">User added successfully with ID: ${result.user_id}</p>`;
            form.reset();
            previewContainer.innerHTML = '';  // Clear the preview on success
        } else {
            messageDiv.innerHTML = `<p class="error">${result.detail || 'Something went wrong!'}</p>`;
        }
    } catch (error) {
        messageDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
});
