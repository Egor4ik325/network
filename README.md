# Social Network

This is another CRUD django app but it contains new Django & software development features (non-implemented in previous projects).

## Test-driven development

This project leverages some techniques of the test-driven development, meaning:

1. First you **define how your code/feature should behave** (througt required assertions)
    - It is all not implemeted yet, so it specification/requirements/test will fail.
2. And than you make code that just **satisfy your tests**.

## Features

- Posts:
    - new post
    - all posts
    - edit post
    - posts pagination
- profile page
- user following
- like/unlike post

### Software development features

1. server-side/client-side/continuous testing
2. webapp isolation (containerization)

- Testing:
    - manual testing
    - server-side (API) testing (django.test)
    - client-side (UI) testing (selenium)
- CI/CD software developmnet best practicies:
    - GitHub Actions
    - GitHub project development
- Deployment/release:
    - Docker project container
    - Deploy project in production

### Web framework features

- built-in class-based generic views
- slug model field

### Following

- all users should have a foreign key to the other users that are following them.
- the number of followers should be displayed on the profile page.
- the "Follow" button should follow or unfollow depending on wheather the user is following already (color should also change)
- user should be able to follow/unfollow other users on their profile
- all following user's posts should be displayed on the page following (order: most recent).
- users shouldn't be able to follow themselfs (button disabled).

## Feature test coverage

What features have test suites?

- [x] Post CRUD views
- [x] Post CRUD templates
- [x] Posts + Users
- [x] Post like
- [ ] User profile
- [ ] User posts
- [ ] User following
- [ ] Post pagination