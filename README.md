# PSMS Backend (Phase 2)

## Overview
This is the backend for the PSMS application, built with Django & Django REST Framework.
The **Phase 1 Foundation** has been implemented, including the custom user model, RBAC, and authentication setup.

### Phase 1 has been completed.
### Tech Lead's Phase 2 has been completed.

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

## Phase 2 Tasks (Developer)

### 1. Full Ownership of Clients
**Status**: Stub `Client` model exists in `clients/models.py`.
**Action**:
-   Implement the full `Client` model (add fields: Industry, Status, etc.).
-   Create API endpoints: `GET`, `POST`, `PATCH`, `DELETE` at `/api/v1/clients/`.

### 2. Full Ownership of Contacts
**Action**:
-   Implement `Contact` model (ForeignKey to Client).
    -   Fields: `full_name`, `email`, `phone`, `is_primary`.
-   Create API endpoints (Sub-resource or standalone) to manage contacts.

### 3. List Views & Filtering
**Action**:
-   Update `GET /api/v1/clients/`.
-   **Requirement**: Add filtering capabilities.
    -   Search by `name`.
    -   Filter by `industry`.
-   Recommended: Use `django-filter` or DRF's `SearchFilter`.
