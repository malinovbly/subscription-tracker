RESTful API for tracking and analyzing all your subscriptions.

The main routes include:

user:
- POST /register (create user)
- DELETE /delete-user/by-name

subs:
- POST /subs (add new subscription to your list)
- GET /subs (get all subscriptions)
- DELETE /subs (delete all subscriptions)
- GET /subs/by-name/{sub_name}
- DELETE /subs/by-name/{sub_name}
- GET /subs/by-category/{category} (get all subscriptions by category)
- GET /subs/next-payment (get info about your next payment)
- GET /subs/monthly-amount (get a monthly subscription amount)
