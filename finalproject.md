# Project Introduction:
The User Management System is an open-source project developed by Professor Keith Williams for his students at NJIT. This project aims to provide a robust foundation for an event management system that bridges the gap between professionals in the software industry and college students. By facilitating company tours, guest lectures, and mock interviews, the system fosters valuable interactions and knowledge exchange between industry experts and aspiring software engineers.

[Introduction to the system features and overview of the project - please read](system_documentation.md)

## Submission Instructions
1. Submit a 1-2 page Word document reflecting on your learnings throughout the course, particularly focusing on your experience working on the final project. Include links to the closed issues for the **5 QA issues, 10 NEW tests, and 2 Features** that you will be graded on as per the requirements below. Ensure that your project successfully deploys to DockerHub and include a link to your Docker repository in the document.

2. Demonstrate a consistent history of work on the project through your commits. **Projects with less than 10 commits will be given an automatic 0**. A significant part of your project's evaluation will be based on your use of issues, commits, and adherence to a professional development process.

## Student Tasks and Grading Rubric:
As a student working on this project, your tasks are as follows. **Submit a document with links to all the issues you create for the bugs, tests, and new feature implementations**:

### Quality Assurance (20%):
- Thoroughly test the system's major functionalities and identify at least 5 issues or bugs.
- Create GitHub issues for each identified problem, providing detailed descriptions and steps to reproduce. Resolve each of the 5 issues and merge your fixes one at a time into the main branch through pull requests.

### Test Coverage Improvement (40%):
- Review the existing test suite and identify gaps in test coverage.
- Create 10 additional tests to cover edge cases, error scenarios, and important functionalities.
- Focus on areas such as user registration, login, authorization, and database interactions. Create branches and issues for each test.

### New Feature Implementation (40%):
- Choose two features from the provided list of additional improvements.
- Create a new branch for each feature using the GitFlow branching model.
- Implement the chosen features, following the project's coding practices and architecture.
- Write appropriate tests to ensure the functionality and reliability of the new features.
- Document the new features, including their usage, configuration, and any necessary migrations.
- Submit a pull request for each implemented feature, following the project's contribution guidelines.

### Grading Rubric:

#### Quality Assurance - 30%
- Thoroughness of testing and identification of issues
- Clarity and detail of GitHub issues
- Reproducibility of identified bugs
- Identification of test coverage gaps
- Quality and effectiveness of additional tests
- Coverage of edge cases, error scenarios, and important functionalities

#### Bug Fixes and Enhancements - 30%
- Correctness and completeness of bug fixes
- Quality and maintainability of code changes
- Appropriate testing of bug fixes and enhancements
- Adherence to the project's contribution guidelines

#### New Feature Implementation - 40%
- Functionality and usability of implemented features
- Quality and maintainability of code
- Appropriate testing of new features
- Documentation and ease of integration with the existing codebase
- Adherence to the project's coding practices and architecture

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

## Conclusion
Remember, it is crucial to demonstrate a consistent and professional work ethic throughout the project. Regularly commit your work, follow the GitFlow branching model, and provide clear and concise commit messages. Active participation in code reviews and collaboration with your peers is highly encouraged.

By completing this project, you will gain valuable experience working with a real-world codebase, collaborating with others, and contributing to an open-source project. The skills and knowledge you acquire will be highly beneficial for your future career as a software engineer.

If you have any further questions or need assistance, feel free to reach out to your instructor or the project maintainers. Happy coding, and best of luck with the User Management System project!