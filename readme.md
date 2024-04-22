# Final Project Introduction:
The User Management System is an open-source project developed by Professor Keith Williams for his students at NJIT. This project aims to provide a robust foundation for an event management system that bridges the gap between professionals in the software industry and college students. By facilitating company tours, guest lectures, and mock interviews, the system fosters valuable interactions and knowledge exchange between industry experts and aspiring software engineers.

[Introduction to the system features and overview of the project - please read](system_documentation.md)

[Instructor Video - Project Overview and Tips]()

[Project Setup Instructions](setup.md)

## Submission and Grading Instructions
1. Submit a 1-2 page Word document reflecting on your learnings throughout the course, particularly focusing on your experience working on the final project. Include links to the closed issues for the **5 QA issues, 10 NEW tests, and 2 Features** that you will be graded on as per the requirements below. Ensure that your project successfully deploys to DockerHub and include a link to your Docker repository in the document.

2. Demonstrate a consistent history of work on the project through your commits. **Projects with less than 10 commits will be given an automatic 0**. A significant part of your project's evaluation will be based on your use of issues, commits, and adherence to a professional development process.

3.  Significant points will be deducted for broken projects that do not deploy to Dockerhub and pass all the automated tests on GitHub actions.

## Managing the project's workload
This project requires a time management strategy.  First, you need to select a feature and plan a minimal but well thought out and well executed implementation. You should first focus on performing the QA in an area of the system that is relevant to **YOUR FEATURE** and then proceed to QA to ensure that before you implement your new feature that you understand and have verified that there are no hidden gotchas that would prevent you from implementing your new feature.  Once you have finished this, you need to write new tests for the same area of the system that your new feature would relate to, and you can write tests for the issues you find and fix from the previous step.  Once you have done the QA and added tests, you will have a more solid understanding of the system and you will proceed with developing the new feature swiftly. Don't forget to always have a working main branch deploying to docker at all times.  If you always have a working main branch, you will never be in jeopardy of receving a very disappointing grade :-) .  **You need to implement a complete documented feature; however, it is more important to make something work reliabbly and to be reasonablly complete, so it's something you you can build on or demonstrate on an interview. 

## Student Tasks and Grading Rubric:
As a student working on this project, your tasks are as follows. **Submit a document with links to all the issues you create for the bugs, tests, and new feature implementations**:

### Quality Assurance (20 Points):
- Thoroughly test the system's major functionalities and identify at **least 5** issues or bugs.
- Create GitHub issues for each identified problem, providing detailed descriptions and steps to reproduce. Resolve each of the 5 issues and merge your fixes one at a time into the main branch through pull requests.

### Test Coverage Improvement (40 Points):
- Review the existing test suite and identify gaps in test coverage.
- Create **10 additional tests** to cover edge cases, error scenarios, and important functionalities.  You should write tests that simulate the setup of the system as the admin user, then creating users, and updating the user accounts.'
- Focus on areas such as user registration, login, authorization, and database interactions. Create branches and issues for each test and merge to main with a pull request and close the issue.

#### Test Coverage Gaps:

- Missing tests for edge cases in user registration and login.
- Insufficient coverage for error handling and exception scenarios.
- Lack of tests for database transaction management.
- Missing tests for user authorization and access control.
- Insufficient coverage for email service integration.

### New Feature Implementation (40 Points):
- Choose one feature from the provided list of additional improvements.
- Create a new  for the feature using the GitFlow branching model of having a development branch that is for new development work, while you keep your main branch up-to-date with the most complete version of the project that you feel is what you want evaluated.  Keep a separation between the main branch and your feature branch, so that you always have a working project to submit from the very first day you set your project up.
- Implement the chosen features, following the project's coding practices and architecture.
- Write appropriate tests to ensure the functionality and reliability of the new features.
- Document the new features, including their usage, configuration, and any necessary migrations.
- Submit a pull request for each implemented feature, following the project's contribution guidelines.
- If you would like to submit a feature for inclusion in the open source project make an issue on my repository and send me a discord message after the semester and we can discuss using the feature and what needs done to add it to the project.  I think it's important to show that you have code being used in a project; however, I want to ensure that all the features added are done consistently and at the highest quality, so that the codebase is maintainable.  In IS690 we will be adding middleware using a distributed message broker called Apache Kafka,  I have a vision for the system and may need any new features setup in a way that will work with microservice architecture that i'm planning to implement for the event registration system.

### Select one of the following features.
1. User Profile Management
   Implement endpoints for retrieving and updating user profile information.
   Allow users to update their first name, last name, bio, profile picture URL, LinkedIn profile URL, and GitHub profile URL.
   Implement validation for the updated profile data using Pydantic schemas.
   Use SQLAlchemy's update method to update the user's profile in the database.  You need to ensure that this is for the CURRENT user ONLY by using the provided function in the [dependencies.py](app/dependencies.py) file as a dependency injection like how the has role is used on the api routes.
2. Password Reset Functionality
   Implement a password reset flow for users who forget their passwords.
   Generate a unique password reset token and send a password reset email to the user's registered email address.
   Create endpoints for requesting a password reset, validating the reset token, and setting a new password.
   Update the user's password in the database using SQLAlchemy's update method.
3. Account Deletion
   Implement an endpoint for users to delete their accounts.
   Require the user to confirm their password before proceeding with account deletion.
   Delete the user's associated data from the database using SQLAlchemy's delete method.
   Send a confirmation email to the user's registered email address upon successful account deletion.  
4. Two-Factor Authentication (2FA)
   Add support for two-factor authentication to enhance account security.
   Allow users to enable or disable 2FA for their accounts.
   Implement time-based one-time password (TOTP) or send verification codes via email or SMS.
   Create endpoints for enabling/disabling 2FA, generating and validating 2FA codes.
5. User Activity Logging
   Implement logging of user activities, such as login attempts, profile updates, and account deletions.
   Use Python's logging module to log user activities with appropriate log levels and messages.
   Store the activity logs in a separate database table or a logging service for analysis and auditing purposes.
6. Email Notification System
   Enhance the email notification system to send emails for various user-related events, such as account lockout, suspicious login attempts, and password resets.
   Use a templating engine like Jinja2 to create dynamic email templates.
   Implement a background task queue (e.g., Celery) to handle email sending asynchronously and avoid blocking the main application.
7. Integration with External Authentication Providers
   Implement integration with external authentication providers, such as Google, Facebook, or GitHub.
   Use the OAuth2 or OpenID Connect protocols to authenticate users via these external providers.
   Create endpoints for initiating the authentication flow and handling the callback from the external provider.  Use Ngrok [here](https://ngrok.com/) to make it so that you can have a public testing URL, so that you can properly handle call backs from 3rd party services.  A callback is when another system sends a message to yours and you need to receive it, so you need to have a unique URL and ngrok provides a service to route the requests to that URL to your development computer, so you don't need a public server.
   Store the user's external authentication details securely in the database.
8. User Analytics and Reporting
   Implement user analytics and reporting features to gain insights into user behavior and engagement.
   Collect data on user registration, login, and activity metrics and provide api endpoint to proxy requests to elastic search to provide at least one endpoint to retrieve data from elastic search. 
   Create endpoints that would be useful for dashboards and visualizations to display user analytics data, such as user growth, retention, and engagement metrics. Simulate fake data to populate data over time for user account creation.   Make use of the ANONYMOUS role to capture how many people come to the site but do not register and provide this information. 
   Implement endpoints for retrieving user analytics data for authorized users (e.g., administrators).
9. Command Line Management of Database for resets, installs, and use account administration and the removal of the ability to have an automtaticly created admin account during user registration.  The ability to load the database with user test data using faker to add X number of users.
   Implement a user feedback and support system to allow users to report issues, suggest improvements, or seek assistance.
   Create endpoints for submitting feedback and support requests.
   Integrate with a third-party support ticketing system or build a custom solution to manage and track user support tickets.
   Notify administrators or support staff when new feedback or support requests are received.
10. Internationalization and Localization
   Implement internationalization (I18n) and localization (L10n) support to cater to users from different regions and languages.
   Use a localization library like gettext or babel to manage translations.
   Store user language preferences in the database and allow users to change their preferred language.
   Translate user-facing messages, emails, and interface elements based on the user's preferred language.

### Grading Rubric:

#### Quality Assurance 
- Thoroughness of testing and identification of issues
- Clarity and detail of GitHub issues
- Reproducibility of identified bugs
- Identification of test coverage gaps
- Quality and effectiveness of additional tests
- Coverage of edge cases, error scenarios, and important functionalities

#### Bug Fixes and Enhancements 
- Correctness and completeness of bug fixes
- Quality and maintainability of code changes
- Appropriate testing of bug fixes and enhancements
- Adherence to the project's contribution guidelines

#### New Feature Implementation 
- Functionality and usability of implemented features
- Quality and maintainability of code
- Appropriate testing of new features
- Documentation and ease of integration with the existing codebase
- Adherence to the project's coding practices and architecture

## Conclusion
Remember, it is crucial to demonstrate a consistent and professional work ethic throughout the project. Regularly commit your work, follow the GitFlow branching model, and provide clear and concise commit messages. Active participation in code reviews and collaboration with your peers is highly encouraged.

By completing this project, you will gain valuable experience working with a real-world codebase, collaborating with others, and contributing to an open-source project. The skills and knowledge you acquire will be highly beneficial for your future career as a software engineer.

If you have any further questions or need assistance, feel free to reach out to your instructor or the project maintainers. Happy coding, and best of luck with the User Management System project!
