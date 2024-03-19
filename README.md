# scheduler
App that allows for providers to schedule appointment slots, and clients to book a given slot. Written in Flask, with SQLAlchemy for ORM and Marshmallow for serilaization and validation.

### Restful endpoints
- `/appointments` (POST, GET)
    * allows for providers to submit when they are available 
    * allows for clients to request times

- `/appointments/<int:appointment_id>` (GET)
    * allows for specifics of an appointment to be retrieved

- `/appointments/<int:appointment_id>/book` (PUT)
    * allows for an appointment to be booked

- `/appointments/<int:appointment_id>/confirm` (PUT)
    * allows for a booked appointment to be confirmed

- `/users` (POST)
    * creates a new user

- `/users/<int:user_id>` (POST)
    * gets more information about a user

### Future expansions

- request appointments within a certain time frame
- provider/client relationships, ability to book "first appointment" or "return appointment"
- removal of sqlite database to ensure statelessness and scalability 
- refactoring of endpoints to use common helper functions and expressions 
- extensive unit testing to ensure proper functinality 
- better security and password handling