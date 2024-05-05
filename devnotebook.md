# Developer Notebook:
* Composed the docker image and navigated to PGAdmin, got Postgres setup per instructions. No issues.
* Ran the Alembic migration script to load the tables/schemas in Postgres, no issues.
* Navigated to http://localhost/docs & registered a new user successfully.
    * It took me a long time to realize the admin authentication method from Homework 10 no longer worked and I burned a few days here before asking others in the Discord.
    * After this I realized that I needed to begin by registering a user when I have no authentication.
* Authenticated the user via the email being the 'user id' (I'm not proud of how long it took me to realize that the user ID was the email and not the UUID).
* Executed the Get User endpoint successfully, returned the correct data.
* Spent several days (intermitently) trying to figure out why an email was not received in MailTrap.
    * Realized that an email isn't sent for the initial admin user. (ouch)
* Registered a second user, successfully received email into MailTrap.
* Clicked the link within the email, and logged in successfully.
* Queried the users table & saw that the email_verified bool was flipped to TRUE for the user.
* 

⫸ 
⪢
⪼
⪫
