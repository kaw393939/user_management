## Event Manager Company: Software QA Analyst/Developer Onboarding Assignment - REST API Testing and Quality Assurance with Alembic Migrations

Welcome aboard Event Manager Company! As a newly hired Software QA Analyst/Developer, you are embarking on an exciting journey to contribute to our project aimed at developing a secure, robust REST API that supports JWT token-based OAuth2 authentication. This API is the backbone of our user management system and will eventually expand to include features for event management and registration.

### The Importance of This Assignment

This project is designed to immerse you in a realistic software development environment, focusing on API development, automated testing, and collaborative problem-solving using Git. It offers hands-on experience with REST API development and emphasizes the critical role of quality assurance in software projects.

As a Software QA Analyst/Developer, you play a pivotal role in ensuring the reliability, security, and performance of our software. This assignment will challenge you to apply your skills in testing, debugging, and collaborating with a team to deliver high-quality software. **Your work will directly impact the success of our project and the satisfaction of our users.**

### Learning Objectives: A Deep Dive

1. **Familiarize with REST API functionality and structure**:
  REST (Representational State Transfer) is an architectural style for designing networked applications. In this assignment, you'll gain hands-on experience working with a REST API, understanding its endpoints, request/response formats, and authentication mechanisms.

2. **Implement and refine documentation**:
  Clear and comprehensive documentation is essential for effective collaboration and maintaining software quality. In this assignment, you'll learn to critically analyze and improve existing documentation based on issues identified in the instructor videos. *You'll understand the importance of keeping documentation up-to-date and ensuring that it accurately reflects the current state of the software.*

3. **Engage in manual and automated testing**:
  Testing is a cornerstone of quality assurance, and it will be a significant part of your role. In this assignment, you'll develop a keen eye for potential issues and edge cases. You'll write comprehensive test cases and leverage automated testing tools like [pytest](https://docs.pytest.org/) to push the project's test coverage towards 90%. You'll learn about different types of testing, such as unit testing, integration testing, and end-to-end testing, and understand their roles in ensuring software quality.

4. **Explore and debug issues**:
  Debugging is an essential skill for any developer. In this assignment, you'll dive deep into the codebase to investigate and resolve issues related to user profile updates and OAuth token generation. *You'll learn how to use debugging tools, interpret error messages, and trace the flow of execution to identify the root cause of problems.* You'll also learn how to write clean, maintainable code that is easier to debug and understand.

5. **Collaborate effectively**:
  Effective collaboration is key to success in modern software development. In this assignment, you'll experience the power of collaboration using Git for version control and GitHub for code reviews and issue tracking. **You'll learn to work with issues, branches, create pull requests, and merge code.** You'll understand the importance of clear communication, constructive feedback, and teamwork in delivering high-quality software.

### Setup and Preliminary Steps: Getting Started

1. **Fork the Project Repository**:
  To begin, you'll fork the [project repository](https://github.com/yourusername/event_manager) to your own GitHub account. This creates a copy of the repository under your account, allowing you to work on the project independently. *Forking is a common practice in open-source development, as it allows developers to contribute to a project without affecting the original codebase.*

2. **Clone the Forked Repository**:
  After forking, you'll clone the repository to your local machine using the `git clone` command. Cloning creates a local copy of the repository on your computer, enabling you to make changes and run the project locally.

3. **Verify the Project Setup**:
  Following the steps in the instructor video, you'll set up the project using [Docker](https://www.docker.com/). Docker is a platform that allows you to package an application with all its dependencies into a standardized unit called a container. By using Docker, you ensure that the project runs consistently across different environments. *You'll verify that you can access the API documentation at `http://localhost/docs` and the database using [PGAdmin](https://www.pgadmin.org/) at `http://localhost:5050`.*

### Testing and Database Management: Ensuring Quality

1. **Explore the API**:
  Using the Swagger UI at `http://localhost/docs`, you'll familiarize yourself with the API endpoints, request/response formats, and authentication mechanisms. Swagger UI provides an interactive interface to explore and test the API endpoints, making it easier to understand how the API works and what data it expects and returns.

2. **Run Tests**:
  You'll execute the provided test suite using pytest, a popular testing framework for Python. Running tests ensures that the existing functionality of the API is working as expected. **Note that running tests will drop the database tables, so you may need to manually drop the Alembic version table using PGAdmin and re-run migrations to ensure a clean state.**

3. **Increase Test Coverage**:
  To enhance the reliability of the API, you'll aim to increase the project's test coverage to 90%. Test coverage measures the percentage of code that is executed during testing. *By writing additional tests for various scenarios and edge cases, you'll ensure that the API handles different situations correctly and provide confidence in its behavior.*

### Collaborative Development Using Git: Working as a Team

1. **Enable Issue Tracking**:
  You'll enable GitHub issues in your repository settings. [GitHub Issues](https://guides.github.com/features/issues/) is a powerful tool for tracking bugs, enhancements, and other tasks related to the project. *It allows you to create, assign, and prioritize issues, facilitating effective collaboration among team members.*

2. **Create Branches**:
  For each issue or task you work on, you'll create a new branch with a descriptive name using the `git checkout -b` command. Branching allows you to work on different features or fixes independently without affecting the main codebase. **It enables parallel development and helps maintain a stable main branch.**

3. **Pull Requests and Code Reviews**:
  When you have completed work on an issue, you'll create a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) to merge your changes into the main branch. Pull requests provide an opportunity for code review, where your team members can examine your changes, provide feedback, and suggest improvements. *Code reviews help maintain code quality, catch potential issues, and promote knowledge sharing among the team.*

### Specific Issues to Address: Diving into the Details

In this assignment, you'll identify, document, and resolve five specific issues related to:

1. **Username validation**:
  You'll investigate and resolve any issues related to username validation. This may involve handling special characters, enforcing length constraints, or ensuring uniqueness. *Proper username validation is essential to maintain data integrity and prevent potential security vulnerabilities.*

2. **Password validation**:
  Ensuring the security of user passwords is crucial. You'll validate that password validation follows security best practices, such as enforcing minimum length, requiring complexity (e.g., a mix of uppercase, lowercase, numbers, and special characters), and properly hashing passwords before storing them in the database. **Robust password validation protects user accounts and mitigates the risk of unauthorized access.**

3. **Profile field edge cases**:
  You'll test and handle various scenarios related to updating profile fields. This may include updating the bio and profile picture URL simultaneously or individually. You'll consider different combinations of fields being updated and ensure that the API handles these cases gracefully. *Edge case testing helps uncover potential issues and ensures a smooth user experience.*

Additionally, you'll resolve a sixth issue demonstrated in the instructor video. These issues will test various combinations and scenarios to simulate real-world usage and potential edge cases. **By addressing these specific issues, you'll gain experience in identifying and resolving common challenges in API development.**

### Submission Requirements: Showcasing Your Work

To complete this assignment, you'll submit the following:

1. **GitHub Repository Link**:
  Ensure that your repository is well-organized and includes:
  - Links to five closed issues, each with accompanying test code and necessary application code modifications.
  - Each issue should be well-documented, explaining the problem, the steps taken to resolve it, and the outcome. *Proper documentation helps others understand your work and facilitates future maintenance.*
  - All issues should be merged into the main branch, following the Git workflow and best practices.

2. **Updated README**:
  Replace the existing README with:
  - Links to the closed issues, providing easy access to your work.
  - Link to project image deployed to dockerhub.
  - A 2-3 paragraph reflection on what you learned from this assignment, focusing on both technical skills and collaborative processes. Reflect on the challenges you faced, the solutions you implemented, and the insights you gained. **This reflection helps solidify your learning and provides valuable feedback for improving the assignment in the future.**

## Grading Rubric 
| Criteria                                                                                                                | Points |
|-------------------------------------------------------------------------------------------------------------------------|--------|
| Resolved 5 issues related to username validation, password validation, and profile field edge cases                      | 30     |
| Resolved the issue demonstrated in the instructor video                                                                 | 20     |
| Increased test coverage to 90% by writing comprehensive test cases                                                      | 20     |
| Followed collaborative development practices using Git and GitHub (branching, pull requests, code reviews)              | 15     |
| Submitted a well-organized GitHub repository with clear documentation, links to closed issues, and a reflective summary | 15     |
| **Total**                                                                                                               | **100**|
### Resources and Documentation: Supporting Your Learning

- **Instructor Videos and Important Links**:
 - [Introduction to REST API with Postgres](https://youtu.be/dgMCSND2FQw) - This video provides an overview of the REST API you'll be working with, including its structure, endpoints, and interaction with the PostgreSQL database.
 - [Assignment Instructions](https://youtu.be/TFblm7QrF6o) - Detailed instructions on your tasks, guiding you through the assignment step by step.
 - API Documentation: `http://localhost/docs` - The Swagger UI documentation for the API, providing information on endpoints, request/response formats, and authentication.
 - Database Management: `http://localhost:5050` - The PGAdmin interface for managing the PostgreSQL database, allowing you to view and manipulate the database tables.

- **Code Documentation**:
 The project codebase includes docstrings and comments explaining various concepts and functionalities. Take the time to read through the code and understand how different components work together. *Pay attention to the structure of the code, the naming conventions used, and the purpose of each function or class.* Understanding the existing codebase will help you write code that is consistent and integrates well with the project.

- **Additional Resources**:
 - [SQLAlchemy Library](https://www.sqlalchemy.org/) - SQLAlchemy is a powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python. It provides a set of tools for interacting with databases, including query building, database schema management, and data serialization. *Familiarize yourself with SQLAlchemy's documentation to understand how it is used in the project for database operations.*
 - [Pydantic Documentation](https://docs.pydantic.dev/latest/) - Pydantic is a data validation and settings management library for Python. It allows you to define data models with type annotations and provides automatic validation, serialization, and deserialization. **Consult the Pydantic documentation to understand how it is used in the project for request/response validation and serialization.**
 - [FastAPI Framework](https://fastapi.tiangolo.com/) - FastAPI is a modern, fast (high-performance) Python web framework for building APIs. It leverages Python's type hints and provides automatic API documentation, request/response validation, and easy integration with other libraries. *Explore the FastAPI documentation to gain a deeper understanding of its features and how it is used in the project.*
 - [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/index.html) - Alembic is a lightweight database migration tool for usage with SQLAlchemy. It allows you to define and manage database schema changes over time, ensuring that the database structure remains consistent across different environments. **Refer to the Alembic documentation to learn how to create and apply database migrations in the project.**

These resources will provide you with a solid foundation to understand the tools, technologies, and concepts used in the project. *Don't hesitate to explore them further and consult the documentation whenever you encounter challenges or need clarification.*

### Conclusion: Embracing the Learning Journey

This assignment is designed to challenge you, help you grow as a developer, and prepare you for the real-world responsibilities of a Software QA Analyst/Developer. By working on realistic issues, collaborating with your team, and focusing on testing and quality assurance, you'll gain valuable experience that will serve you throughout your career.

**Remember, the goal is not just to complete the assignment but to embrace the learning journey.** Take the time to understand the codebase, ask questions, and explore new concepts. Engage with your team members, seek feedback, and learn from their experiences. *Your dedication, curiosity, and willingness to learn will be the key to your success in this role.*

We are excited to have you on board and look forward to seeing your contributions to the project. Your fresh perspective and skills will undoubtedly make a positive impact on our team and the quality of our software.

If you have any questions or need assistance, don't hesitate to reach out to your mentor or team lead. We are here to support you and ensure that you have a rewarding and enriching experience.

Once again, welcome to the Event Manager Company! Let's embark on this exciting journey together and create something remarkable.

Happy coding and happy learning!