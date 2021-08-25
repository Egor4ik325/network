// Django app static JS file (available for all apps via {% static %})

document.addEventListener('DOMContentLoaded', () => {
    const bodyElement = document.querySelector('#body');

    bodyElement.innerHTML = `
    <h2>${username} profile</h2>
    <div id="container">
    </div>
    `;

    renderUser();
});

function renderLoading() {
    document.querySelector('#container').innerHTML = `
    <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
    </div>
    `;
}

// Fetch and render user data
function renderUser() {
    renderLoading();

    const userDetailUrl = userDetailPath + '?' + new URLSearchParams({
        username: username
    });

    fetch(userDetailUrl, {
        headers: {
            'content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(users => {
            const user = JSON.parse(users)[0];
            const fullName = (user.fields.first_name || user.fields.last_name ? user.fields.first_name + ' ' + user.fields.last_name : 'No');
            const date = user.fields.date_joined.split('T')[0];
            const time = user.fields.date_joined.split('T')[1].split('.')[0];

            fetch('/get_session_username/').then(res => res.json()).then(data => {

                document.querySelector('#container').innerHTML = '';

                if (username === data.username) {
                    document.querySelector('#container').innerHTML = `
                    <div class="btn btn-secondary btn-sm px-3 mb-4" onclick="renderUserUpdateForm()">Edit</div>
                    `;
                }

                // Render webpage user template
                document.querySelector('#container').innerHTML += `
                <ul class="list-group">
                    <li class="list-group-item">Full name: ${fullName}</li>
                    <li class="list-group-item">Email: ${user.fields.email}</li>
                    <li class="list-group-item">Joined: in ${date} at ${time}</li>
                </ul>
                `;
            })
        })
        .catch(err => {
            console.error(err);
        });
}

function renderUserUpdateForm() {
    renderLoading();

    fetch(userUpdatePath, {
        headers: {
            // Request HTML response
            'content-type': 'text/html'
        }
    })
        .then(res => res.text())
        .then((updateFormHTML) => {
            // Render HTML form
            document.querySelector('#container').innerHTML = `
            <div class="btn btn-secondary btn-sm px-3 mb-4" onclick="renderUser()">View</div>
            ${updateFormHTML}
            `;

            // Stylize rendered HTML form using JavaScript
            inputs = document.querySelectorAll('#container > form input')
            inputs.forEach(input => {
                input.className += ' form-control';
            });

            document.querySelectorAll('#container > form label').forEach(label => {
                label.className += ' form-label';
            });

            document.querySelector('#container form input[type=submit]').className += ' btn btn-primary';

            document.querySelectorAll('#container form .helptext').forEach(helptext => {
                helptext.innerHTML = helptext.innerHTML.small()
                helptext.className += ' text-muted';
            });
        })
}