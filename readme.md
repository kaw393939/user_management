**ISSUE-1**:
- Emails were being dispatched before the user was successfully added to the database.
- I have added the code:
# https://github.com/HemanjaliK/user_management/commit/f9134c3b6f37e81f75025217d3dd74631c92feb3
- Test cases:
# https://github.com/HemanjaliK/user_management/commit/f9134c3b6f37e81f75025217d3dd74631c92feb3

**ISSUE-2**
- A success response was mistakenly given when attempting to update an email to one that already exists. The system now checks for existing emails by retrieving data based on the email address; if found, it throws an error.
- I have added the code:
# https://github.com/HemanjaliK/user_management/commit/4fa40db037260a3487949b5db45e24d71da2c762
- Test cases:
# https://github.com/HemanjaliK/user_management/commit/ddbebf278b26eb77acd0a23ade4089d561355b3e

**ISSUE-3**
- Although the values are correctly mapped to the response object, the GitHub URL and LinkedIn URL are returning null in the create user response.
- have added the code:
# app/routers/user_routes.py:
        github_profile_url = created_user.github_profile_url,
        linkedin_profile_url = created_user.linkedin_profile_url,
- Test cases:
# https://github.com/HemanjaliK/user_management/commit/1240f98bb7f5b335ad25d5bd4e5855b3464ab020

**ISSUE-4**
- When deleting values, empty strings were not accepted in the fields. In order to determine whether the incoming field is empty, a validator has been added. If it is, the value is set to null.
- have added the code:
# app/schemas/user_schemas.py:
- @validator('linkedin_profile_url', 'profile_picture_url', 'github_profile_url', pre=True, always=True)
    def empty_string_to_none(cls, v):
        v = v.strip() if isinstance(v, str) else v
        return None if v == "" else v
- Test case:
# https://github.com/HemanjaliK/user_management/commit/7245fa1e8a9ea2740d7b23f538dd5a13a739314c

**ISSUE-5**
- The report indicates a vulnerability in the libc-bin package, specifically CVE-2024-33599, which is a high severity vulnerability related to a stack-based buffer overflow in the netgroup cache. The installed version is 2.36-9+deb12u6, and the fixed version is 2.36-9+deb12u7.
# https://github.com/HemanjaliK/user_management/blob/23-dev/Dockerfile

**FEATURE**
- Feature 9, User Profile Management, requires the creation of two endpoints, and I have chosen it. Users can update their own profile fields using the first endpoint, and managers and administrators can change users' statuses to "professional" using the second. Users receive an email notification upon updating their professional status, letting them know they have been promoted.
# https://github.com/HemanjaliK/user_management/tree/29-feature

**DOCKER-LINK**
# https://hub.docker.com/repository/docker/hemanjalik/user_management/general