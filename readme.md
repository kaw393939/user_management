# Final Project Introduction:
The User Management System is an open-source project developed by Professor Keith Williams for his students at NJIT. This project aims to provide a robust foundation for an event management system that bridges the gap between professionals in the software industry and college students. By facilitating company tours, guest lectures, and mock interviews, the system fosters valuable interactions and knowledge exchange between industry experts and aspiring software engineers.

[Introduction to the system features and overview of the project - please read](system_documentation.md)

[Instructor Video - Project Overview and Tips]()

[Project Setup Instructions](setup.md)

## Submission and Grading Instructions
1. Submit a 1-2 page Word document reflecting on your learnings throughout the course, particularly focusing on your experience working on the final project. Include links to the closed issues for the **5 QA issues, 10 NEW tests, and 2 Features** that you will be graded on as per the requirements below. Ensure that your project successfully deploys to DockerHub and include a link to your Docker repository in the document.

2. Demonstrate a consistent history of work on the project through your commits. **Projects with less than 10 commits will be given an automatic 0**. A significant part of your project's evaluation will be based on your use of issues, commits, and adherence to a professional development process.

3.  Significant points will be deducted for broken projects that do not deploy to Dockerhub and pass all the automated tests on GitHub actions.

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
- Choose two features from the provided list of additional improvements.
- Create a new branch for each feature using the GitFlow branching model.
- Implement the chosen features, following the project's coding practices and architecture.
- Write appropriate tests to ensure the functionality and reliability of the new features.
- Document the new features, including their usage, configuration, and any necessary migrations.
- Submit a pull request for each implemented feature, following the project's contribution guidelines.

### Enhancements and Additions
1. User Profile Management
   Implement endpoints for retrieving and updating user profile information.
   Allow users to update their first name, last name, bio, profile picture URL, LinkedIn profile URL, and GitHub profile URL.
   Implement validation for the updated profile data using Pydantic schemas.
   Use SQLAlchemy's update method to update the user's profile in the database.
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
   Track user registration, login, and activity metrics using a data analytics platform or a custom solution.
   Create dashboards and visualizations to display user analytics data, such as user growth, retention, and engagement metrics.
   Implement endpoints for retrieving user analytics data for authorized users (e.g., administrators).
9. User Feedback and Support
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
