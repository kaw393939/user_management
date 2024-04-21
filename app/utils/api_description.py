def getDescription():
    description = """
Application Overview:

This application is a robust user management system designed to facilitate the administration of user credentials and profiles in a secure and efficient manner. It leverages the capabilities of FastAPI to provide a high-performance, scalable API that adheres to the best practices of modern web service development.

Key Features:

- User Authentication: Implements OAuth2 with Password Flow to ensure secure access to the API. Users are required to authenticate using a JWT (JSON Web Token) which provides a secure and efficient means of user identification and authorization.

- CRUD Operations: Offers comprehensive endpoints for creating, reading, updating, and deleting user information. This includes management of user details such as email, passwords, and personal profiles.

- Role-Based Access Control: Enforces different access levels using a role-based mechanism that restricts certain operations to users with appropriate privileges. Supported roles include Admin, Manager, and regular Users, each with different permissions.

- Email Integration: Integrates with email services for account verification and notifications, enhancing the registration and password recovery processes.

- HATEOAS (Hypermedia as the Engine of Application State): Each response from the API includes hypermedia links to guide the client to other relevant endpoints based on the context of the current interaction, promoting discoverability and ease of navigation within the API.

- Secure Password Handling: Implements best practices for password security, including hashing and salting techniques, to ensure that user credentials are stored securely.

- Error Handling: Provides clear and informative error responses that help clients properly handle issues such as authentication failures, access violations, and data conflicts.

Security Features:

The application incorporates several security measures to protect data and ensure the integrity and confidentiality of user information:

- Data Encryption: Uses advanced encryption standards to secure sensitive data in transit and at rest.
- Input Validation: Employs rigorous validation checks to prevent SQL injection, XSS, and other common security threats.
- Rate Limiting: Protects against brute-force attacks by limiting the number of requests a user can make to the API within a given timeframe.

User Experience:

Designed with a focus on user experience, the API provides detailed documentation, descriptive error messages, and consistent interface patterns that make it intuitive and straightforward for developers to integrate with their applications.

This API is ideal for businesses and developers looking for a reliable and secure way to manage user authentication and authorization in their applications. It is particularly suited to environments where security and data privacy are paramount.
"""
    return description