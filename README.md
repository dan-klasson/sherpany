## Code Challenge: Python/Django Developer

Build an "events" web application where users can log in, create events and RSVP on events.

* Sorted so that upcoming events are first.
* List view shows title, date and amount of participants.
* List view shows the owner of the event (as the part of the email before the "@").
* Assume there may be many 1000s of events and users.
* Any logged in user can create events.
* Logged in user can edit own events.
* Login with email and password.
* Registration with email and password.
* Out of scope: email confirmation, password reset, change password, profile editing and change email.


Install the dependencies:

    pip3 install -r requirements.txt

Run the migrations:

    python3 manage.py migrate

Start the server:

    python3 manage.py runserver

Run the tests:

    python3 manage.py test

