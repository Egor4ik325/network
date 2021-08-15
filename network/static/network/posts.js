document.addEventListener('DOMContentLoaded', () => {
    const likeIcons = Array.from(document.getElementsByClassName('like-icon'));

    likeIcons.forEach(likeIcon => {
        likeIcon.addEventListener('click', event => {
            try {
                const liked = JSON.parse(likeIcon.dataset.liked);
                const postSlug = likeIcon.dataset.post;
                const csrftoken = Cookies.get('csrftoken');

                // Make like POST request (switch like state on the server)
                fetch(`/posts/${postSlug}/like/`, {
                    method: 'POST',
                    mode: 'same-origin',
                    redirect: 'follow',
                    headers: {
                        "X-CSRFToken": csrftoken
                    }
                })
                    .then(response => {
                        // Response if result of redirect
                        if (!response.redirected) {
                            if (response.ok) {
                                // The post like state was switched successfully
                                if (!liked) {
                                    likeIcon.dataset.liked = true;
                                    likeIcon.innerHTML = '<i class="bi bi-suit-heart-fill" style="color: red;"></i>';
                                    // Increment likes number
                                    const postFooter = likeIcon.parentElement;
                                    const likesElement = postFooter.querySelector('.likes');
                                    const likes = parseInt(likesElement.innerHTML);
                                    likesElement.innerHTML = likes + 1;

                                } else {
                                    likeIcon.dataset.liked = false;
                                    likeIcon.innerHTML = '<i class="bi bi-suit-heart" style="color: red;"></i>';
                                    // Decrement likes number
                                    const postFooter = likeIcon.parentElement;
                                    const likesElement = postFooter.querySelector('.likes');
                                    const likes = parseInt(likesElement.innerHTML);
                                    likesElement.innerHTML = likes - 1;
                                }
                            }
                        } else {
                            if (response.ok) {
                                // Follow redirected response url
                                const redirectUrl = response.url;
                                window.location.href = redirectUrl;
                            }
                        }
                    }).catch(error => {
                        console.error(error);
                    });
            } catch (error) {
                console.error(error);
            }
        });
    });
});