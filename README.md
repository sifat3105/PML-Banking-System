# Password Change Page - PML Bank PLC

## Overview
Secure password change functionality for PML Bank's digital banking system. This page allows users to update their password while enforcing strong password requirements.

## Features
- Current password verification
- New password validation
- Password confirmation matching
- Visual feedback for form errors
- Success message display
- Responsive design

## Technical Details
- **Template**: `password_change.html`
- **Dependencies**:
  - Django's built-in password change view
  - CSRF protection
  - Form validation
- **Styling**: Self-contained CSS (no external dependencies)

## Implementation Notes
1. Extends the base template (`base.html`)
2. Uses Django's default password change form
3. Includes client-side validation cues
4. Displays password requirements
5. Shows success messages after password change

## Security
- All passwords are transmitted securely
- Server-side validation enforced
- Session protection
- CSRF tokens included

## Screenshot
![Password Change Page](screenshots/password-change.png)
