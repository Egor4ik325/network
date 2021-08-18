// Django app static JS file (available for all apps via {% static %})

document.addEventListener('DOMContentLoaded', () => {
    bodyElement = document.querySelector('#body');
    // bodyElement.innerHTML = "Hi, I'm rendered on the client side!";
    // bodyElement.innerHTML = username;
    renderUser();

});

function renderUser() {
    const userDetailUrl = userDetailPath + '?' + new URLSearchParams({
        username: username
    });

    console.log('user detail url', userDetailUrl);

    fetch(userDetailUrl, {
        headers: {
            'content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(user => {
            bodyElement.innerHTML = user;
        })
        .catch(err => {
            console.error(err);
        });
}