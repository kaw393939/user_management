
## Project Setup and Commands:

1. Fork this repository to your own account.

2. Clone the project repository to your local machine.

3. Create a local .env file with your [MailTrap](https://mailtrap.io/) SMTP settings. Mailtrap allows you to view emails when you test the site manually. When running pytest, the system uses a Mock to simulate sending emails but doesn't actually send them.

4. Alembic and Pytest:
  - When you run Pytest, it deletes the user table but doesn't remove the Alembic table. This can cause Alembic to get out of sync.
  - To resolve this, drop the Alembic table and run the migration (`docker compose exec fastapi alembic upgrade head`) when you want to manually test the site through `http://localhost/docs`.
  - If you change the database schema, delete the Alembic migration, the Alembic table, and the users table. Then, regenerate the migration using the command: `docker compose exec fastapi alembic revision --autogenerate -m 'initial migration'`.
  - Since there is no real user data currently, you don't need to worry about database upgrades, but Alembic is still required to install the database tables.

5. Run the project:
  - `docker compose up --build`
  - Set up PGAdmin at `localhost:5050` (see docker compose for login details)
  - View logs for the app: `docker compose logs fastapi -f`
  - Run tests: `docker compose exec fastapi pytest`

6. Set up the project with DockerHub deployment as in previous assignments for email testing. Enable issues in settings, create the production environment, and configure your DockerHub username and token. You don't need to add MailTrap, but if you want to, you can add the values to the production environment's variables.
