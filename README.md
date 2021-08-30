# Social Network

This is another CRUD django app but it contains new Django & software development features (non-implemented in previous projects).

## Test-driven development

This project leverages some techniques of the test-driven development, meaning:

1. First you **define how your code/feature should behave** (througt required assertions)
    - It is all not implemeted yet, so it specification/requirements/test will fail.
2. And than you make code that just **satisfy your tests**.

## Features

User following:
- all users should have a foreign key to the other users that are following them.
- the number of followers should be displayed on the profile page.
- the "Follow" button should follow or unfollow depending on wheather the user is following already (color should also change)
- user should be able to follow/unfollow other users on their profile
- all following user's posts should be displayed on the page following (order: most recent).
- users shouldn't be able to follow themselfs (button disabled).
