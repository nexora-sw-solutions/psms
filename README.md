# PSMS Backend (Phase 1)

## Overview
This is the backend for the PSMS application, built with Django & Django REST Framework.
The **Phase 1 Foundation** has been implemented by the Tech Lead, including the custom user model, RBAC, and authentication setup.

## Getting Started

### 1. Environment Setup
The project uses `python-dotenv` to manage settings.
1.  Navigate to the backend: `cd backend`
2.  Copy the example env file:
    ```bash
    cp .env.example .env
    ```
3.  (Optional) Edit `.env` with your local settings.

### 2. Run with Docker
```bash
docker-compose up --build
```
*(Note: If docker-compose is not yet set up, build the image directly: `docker build -t psms-backend .`)*

### 3. Run Locally
1.  Create virtual env: `python -m venv .venv`
2.  Activate: `.venv\Scripts\Activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)
3.  Install: `pip install -r requirements.txt`
4.  Migrate: `python manage.py migrate`
5.  Run: `python manage.py runserver`

---

## Architecture (Phase 1)

### Core Models (`core/models.py`)
-   **User**: Custom model with UUID primary key.
-   **Organization**: Foundation for multi-tenancy.
-   **SoftDelete**: All core models inherit from `SoftDeleteModel` (supports `.delete()` and `.restore()`).

### Authentication & RBAC
-   **Auth**: JWT (SimpleJWT). Endpoints at `/api/v1/auth/`.
-   **Roles**: Defined in `User.Role` (SUPER_ADMIN, FIRM_ADMIN, MANAGER, CONSULTANT, CLIENT).
-   **Permissions**: `core/permissions.py` contains `IsFirmAdmin`, `IsManager`, etc.

---

## Next Steps (Developer Tasks)

### 1. Organization Models
**Status**: The base `Organization` model exists in `core/models.py`.
**Action**:
-   Review the existing model.
-   Add any missing fields if specified in your requirements.
-   Ensure migrations are created/applied: `python manage.py makemigrations` / `migrate`.

### 2. User Invitation (`POST /api/v1/users`)
**Action**:
-   Create a view/endpoint to invite new users.
-   **Requirement**: Only `FIRM_ADMIN` or `MANAGER` should be able to invite.
-   **Logic**: Create user -> Assign Default Password -> Send Email (mock for now).

### 3. Profile Management (`GET/PATCH /api/v1/users/{id}`)
**Action**:
-   Allow users to view/update their own profile.
-   Ensure `IsAuthenticated` and Object-level permissions (users can only edit themselves).

### 4. Unit Tests
**Action**:
-   Add tests in `core/tests.py`.
-   Cover: Organization creation, User signup/invitation flows.
