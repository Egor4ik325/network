# Webapp testing in Django

## How to test (assert working)?

1. Write new. Test new. (Write old. Test old. Write new. Test old on new. )
2. Test new. Write new. Test on new.

- assert your code
- assert code you aren't sure
- test what you would test manually (clone process)

## Server-side code

Assert working API for the web interface.

## Client-side code

Assert client-side code is valid (assert code you write):
(**Assert interface with the back-end is valid!**)

- Assert HTML markup (HTML DOM)
    - assert `<form>`
    - assert `<a>`
- Assert Jinja template engine
    - assert `{% url %}`
    - assert `{% for %}`
- Assert JavaScript logic/intereacitvity
    - assert `<button>`
