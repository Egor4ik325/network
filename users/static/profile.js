// Django app static JS file (available for all apps via {% static %})

document.addEventListener('DOMContentLoaded', () => {
    render()
    renderTemplate();
    renderUser();
    renderUserPosts();
});

function render() {
    const bodyElement = document.querySelector('#body');
    bodyElement.innerHTML = `
    <div id="profile" class="mb-4">
    </div>
    <div id="container" class="mb-4">
    </div>
    <div id="posts">
        <h3 class="mb-3">${username} posts</h3>
    </div>
    `;
}

function renderTemplate() {
    const profileElement = document.querySelector('#profile');
    profileElement.innerHTML = `
    <h2>${username} profile</h2>
    <mark>${profileUserFollows} followers</mark>
    <button 
        class="btn btn-outline-sucess"
        onclick="followUnfollow()"
        >
        ${userIsFollowing ? 'Unfollow' : 'Follow'}
    </button>
    `;
}


function followUnfollow() {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    fetch('/nezort11/follow/', {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken }
    })
        .then(res => {
            if (res.ok) {
                if (userIsFollowing) {
                    profileUserFollows = parseInt(profileUserFollows) - 1;
                } else {
                    profileUserFollows = parseInt(profileUserFollows) + 1;
                }

                // Switch following state
                userIsFollowing = !userIsFollowing;

                renderTemplate();
            }
        })
}

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
                    <div class="btn btn-secondary btn-sm px-3" onclick="renderUserUpdateForm()">Edit</div>
                    `;
                }

                // Render webpage user template
                document.querySelector('#container').innerHTML += `
                <ul class="list-group mt-4">
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

async function fetchUserPosts() {
    const response = await fetch(`/${username}/posts/`, { headers: { 'content-type': 'application/json' } });
    const data = await response.json();
    return data;
}

async function renderUserPosts() {
    const posts = await fetchUserPosts();

    const postsRenderedHTML = posts.map(post => {
        return `
        <div class="post">
            <b>${post.fields.title}</b>
            <p>${post.fields.body}</p>
        </div>
        `;
    });

    document.querySelector('#posts').innerHTML += postsRenderedHTML.join('');
}