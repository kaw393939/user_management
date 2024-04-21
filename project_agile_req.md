# System Specifications

# **Professional Networking Event Platform**

## Initiative: Enhanced Professional Networking Platform

This initiative aims to provide a comprehensive system for students and professionals to connect through company tours, mock interviews, guest lectures, and other events, featuring robust user management, event management, notifications, and full site administration functionalities.

### Epic 1: User Management
Handles user registration, roles, and privileges, ensuring secure and role-appropriate access to the platform's features.

#### **User Story 1.1: Registration and Authentication**
- **As an** anonymous user,
- **I want to** register using my email and create a profile,
- **So that** I can access authenticated user features.
- **Acceptance Criteria:**
  - Email format is validated during registration.
  - Passwords are hashed and securely stored.
  - A confirmation email is sent post-registration.
  - Users can enter optional links to their GitHub and LinkedIn profiles at registration.
  - Users can provide a URL for their profile photo during registration.

#### **User Story 1.2: Role-Based Access Control**
- **As an** admin,
- **I want to** assign and modify user roles (authenticated, manager, admin),
- **So that** I can ensure users have appropriate permissions.
- **Acceptance Criteria:**
  - Only admins have the ability to change user roles.
  - Role changes are logged in an audit trail.

#### **User Story 1.3: Upgrade to Pro Status**
- **As a** manager,
- **I want to** upgrade professional users to pro status based on their resumes and experience,
- **So that** they can unlock additional functionalities.
- **Acceptance Criteria:**
  - Managers can view and verify linked resumes.
  - Notifications are sent to users upon being upgraded to pro status.

#### **User Story 1.4: Manage Social Media Links**
- **As an** authenticated user,
- **I want to** add or update links to my GitHub and LinkedIn profiles,
- **So that** other users can view my professional and coding experiences.
- **Acceptance Criteria:**
  - Users can edit their social media links via their profile settings.
  - URL formats for GitHub and LinkedIn are validated.

#### **User Story 1.5: Manage Profile Photo URL**
- **As an** authenticated user,
- **I want to** input a URL for my profile photo,
- **So that** I can update my profile appearance without uploading files.
- **Acceptance Criteria:**
  - Users can add or change their profile photo URL in profile settings.
  - The system checks that the URL is likely an image file (e.g., ends with .jpg, .png).

### Epic 2: Event Management
Involves the creation, approval, and participation management of events to ensure they meet organizational standards and user needs.

#### **User Story 2.1: Create Event**
- **As a** manager,
- **I want to** create and define events,
- **So that** users can register for and attend professionally enriching activities.
- **Acceptance Criteria:**
  - Events include details such as title, description, location, date, and participation requirements.
  - Events require manager approval before becoming visible to users.

#### **User Story 2.2: Register for Events**
- **As an** authenticated user,
- **I want to** easily find and register for events,
- **So that** I can benefit from networking opportunities.
- **Acceptance Criteria:**
  - Event details are accessible before registration.
  - Confirmation is sent upon successful registration.

### Epic 3: Notifications and Approvals
Handles the distribution of information and approval processes to maintain effective communication and operational efficiency.

#### **User Story 3.1: Event Approval Notifications**
- **As a** manager,
- **I want to** be alerted about new events needing approval,
- **So that** I can review them promptly.
- **Acceptance Criteria:**
  - Notifications for new event submissions are sent within 24 hours.
  - Managers have the ability to approve or reject events with feedback.

#### **User Story 3.2: General Notifications**
- **As a** user,
- **I want to** receive timely updates about events and my user status,
- **So that** I stay informed of relevant activities and any changes.
- **Acceptance Criteria:**
  - Users can customize their notification preferences.
  - Notifications are delivered both via email and on the user dashboard.

### Epic 4: Full Site Management
Provides admins with the tools to manage site-wide settings and features, ensuring the platform aligns with organizational goals and security standards.

#### **User Story 4.1: Manage Site


### Original ChatGPT4 Prompt