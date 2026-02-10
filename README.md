**Authentication(hybrid) Module Documentation**
Overview
This system implements a hybrid authentication model combining:
- JWT tokens for stateless authentication and role-based access control.
- HttpOnly cookies for secure storage of tokens in browser environments.
- CSRF protection to mitigate cross-site request forgery attacks.
It is designed to support both browser-based clients and API consumers.

Components
Tokens
- Access Token
- Short-lived (minutes).
- Contains user ID (sub), role ID (role_id),"type": "access" client_type:"browser|app" and remember_me(optional,bool).
- Used for authenticating API requests.
- Refresh Token
- Long-lived (days/weeks).
- Contains user ID (sub), "type": "refresh",client_type:"browser|app".
- Used to obtain new access tokens when expired.
- CSRF Token
- Random string stored in a cookie and returned in the response body.
- Must be sent in the X-CSRF-Token header for non-GET requests.

Endpoints
POST /auth/v1/login (Browser Flow)
Authenticates a user and issues tokens.
Request Body
{
  "email": "user@example.com",
  "password": "secret",
  "remember_me": true
}


Response
{
  "csrf": "random_csrf_token",
  "token": {
    "expires_in": 3600,
    "expires_at": "2026-02-07 00:00 UTC",
    "r_expires_in": 604800,
    "r_expires_at": "2026-02-14 00:00 UTC"
  },
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role_id": 1
  }
}
Cookies Set
- access_token (HttpOnly, Secure)
- refresh_token (HttpOnly, Secure)
- csrf_token
Headers Used
- Content-type : application/json

POST /auth/v1/app/login (App Flow)
Authenticates a mobile or API client and issues tokens.
Request Body
{
  "email": "user@example.com",
  "password": "secret",
  "remember_me": true
}

Response
{
  "token": {
    "access_token": "jwt_access_token",
    "refresh_token": "jwt_refresh_token",
    "expires_in": 3600,
    "expires_at": "2026-02-07 00:00 UTC",
    "r_expires_in": 604800,
    "r_expires_at": "2026-02-14 00:00 UTC"
  },
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role_id": 1
  }
}
Cookies Set
- NONE!
Headers Used
- Content-type : application/json
- Authorization: Bearer <access_token>
- No CSRF required.
- Tokens are returned in the response body, not cookies.

POST /auth/v1/refresh
Issues a new access token using the refresh token.
Behavior
- If remember_me is true → rotates refresh token.
- If remember_me is false → reuses existing refresh token and original expiry.
- If Client==app response token will include(access_token,refresh_token)
Response
{
  "csrf": "new_csrf_token",
  "token": {
    "expires_in": 3600,
    "expires_at": "2026-02-07 01:00 UTC",
    "r_expires_in": 604800,
    "r_expires_at": "2026-02-14 00:00 UTC"
  },
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role_id": 1
  }
}

  
POST /auth/v1/logout
Clears all authentication cookies.
Response
{
  "detail": "Successfully logged out"
}


Middleware & Dependencies
**auth_user(web)**
- Reads access_token from cookies.
- Validates CSRF token for non-GET requests.
- Decodes JWT and loads user from DB.
- Raises 401 if invalid/expired, 404 if user not found.
check_roles
- Ensures the authenticated user has one of the allowed roles.
- Raises 403 if unauthorized.
**auth_user(app)**
- Reads Bearer access_token from header(Authorization)
**check_roles**
- Ensures the authenticated user has one of the allowed roles.
- Raises 403 if unauthorized.

Security Features
**web**
- HttpOnly cookies: Prevent JavaScript access to tokens().
- Secure flag: Ensures cookies are sent only over HTTPS.
- CSRF protection: Requires X-CSRF-Token header to match cookie.
- Token typing: Access vs. refresh tokens are distinguished by "type" claim.('refresh','access')
 
- Short-lived access tokens: Limits exposure if compromised.a
- Refresh token rotation: Optional, based on remember_me.
- Flow separation: Browser tokens must be in cookies with CSRF enforced; app tokens must be in headers with CSRF forbidden.
- Mixed-source rejection: Requests carrying both cookie and header tokens are denied.


Flow Diagram
**Login(web)**
- User submits credentials.
- Server issues:
- Access token (HttpOnly=true, Secure=true, type="access")
- Refresh token (HttpOnly=true, Secure=true, type="refresh")
- CSRF token (HttpOnly=false, Secure=true)
- Tokens stored in HttpOnly cookies (except CSRF, which is readable for header injection).
- Authenticated Request
- Browser automatically sends cookies.
- Server validates:
- Access token (client_type="browser")
- CSRF header matches CSRF cookie.
**app**
- App clients send Bearer header only, with client_type="app", CSRF forbidden.
- Refresh
- Access token expires.
- Client calls /refresh.
- Server validates refresh token (type="refresh", client_type bound to flow).
- New access token issued.
- Refresh token rotated if remember_me is set.
- Logout
- Server clears cookies (access_token, refresh_token, csrf_token).
- Client session invalidated.


**Authentication Module Test coverage**
Combined Coverage(test\auth)
Together, these two files validate:
- Token issuance: Access vs. refresh tokens, CSRF token, cookie handling.
- Flow separation: Browser vs. app clients, with strict source binding.
- CSRF enforcement: Required for browser, forbidden for app.
- Token rotation: Refresh rotation logic tied to remember_me.
- Session lifecycle: Login → authenticated requests → refresh → logout.

Edge cases
- test_login_fails_with_invalid_user → invalid credentials rejected (401).
- test_auth_route_with_refresh_token → refresh token used on protected route rejected (401).
- Other misuse scenarios: wrong client type, missing cookies, both cookie + header present, app request with CSRF.


This documentation should serve as a reference for developers integrating or maintaining the system.

