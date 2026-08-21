# Backend Constitution

This document defines the architectural rules and working assumptions for the `clone_kiot_viet` backend. Agents and developers should read it before changing backend code.

## 1. Project Context

`clone_kiot_viet` is a Python backend for a KiotViet-style business-management application. The backend is located in `backend/` and is built with:

- Python
- FastAPI
- SQLAlchemy
- MySQL
- Alembic
- Pydantic Settings
- `dependency_injector`
- Domain-Driven Design and layered architecture

Run the application from the `backend/` directory:

```shell
python -m uvicorn shared_kernel.infra.fastapi.main:app --port 8000 --reload
```

The project currently uses top-level imports such as `identity` and `shared_kernel`, so commands should normally be executed from `backend/`.

## 2. Architectural Style

The backend uses bounded contexts and four conceptual layers:

1. Domain
2. Application
3. Infrastructure
4. Presentation

The dependency direction is inward:

```text
Presentation -> Application -> Domain
Infrastructure -> Domain/Application contracts
```

The domain must not depend on FastAPI, SQLAlchemy, JWT libraries, password-hashing libraries, HTTP exceptions, or other infrastructure technologies.

## 3. Bounded Contexts

The `identity` package is the identity bounded context. It owns users, credentials, authentication, and identity-specific authorization concepts.

The `shared_kernel` package contains generic concepts and technical mechanisms shared by multiple bounded contexts. Do not put identity-specific behavior in `shared_kernel` merely for convenience.

Identity-specific code belongs in:

```text
backend/identity/
```

Generic technical code belongs in:

```text
backend/shared_kernel/
```

## 4. Domain Layer Rules

The domain layer contains business concepts, invariants, entities, value objects, repository protocols, and domain exceptions.

Important domain files include:

- `identity/domain/entity/user.py`
- `identity/domain/user_repository.py`
- `shared_kernel/domain/entity/entity.py`
- `shared_kernel/domain/entity/value_object.py`
- `shared_kernel/domain/entity/user_role.py`
- `shared_kernel/domain/unit_of_work.py`

The `User` is an aggregate root with these current attributes:

- `display_name`
- `username`
- `password`
- `role`
- `phone_number`
- `email`
- `date_of_birth`
- `address`
- `user_note`

`UserRole` currently contains:

- `UserRole.ADMIN`
- `UserRole.USER`

Domain protocols define contracts. For example, `UserRepository` belongs in `identity/domain`, while its SQLAlchemy implementation belongs in `identity/infra`.

Domain code must:

- remain framework-independent
- expose business behavior and contracts
- use domain exceptions rather than HTTP exceptions
- avoid persistence and transport concerns
- avoid logging configuration

## 5. Application Layer Rules

The application layer contains use cases and orchestration logic. It coordinates repositories, domain services, and Unit of Work transactions.

Application services should depend on abstractions such as:

- `UserRepository`
- `UnitOfWork`
- domain services
- authentication and token service contracts

Application services must not directly construct SQLAlchemy sessions or repositories. Those dependencies should be injected.

Application services must not raise FastAPI `HTTPException`. The presentation layer translates application/domain exceptions into HTTP responses.

For authentication, likely use cases include:

- authenticate a user using username and password
- issue an access token
- retrieve the current user from a token subject
- check whether a user has a required role

## 6. Infrastructure Layer Rules

Infrastructure contains technical implementations and adapters.

Important infrastructure areas include:

- `identity/infra/sqlalchemy_user_repository.py`
- `shared_kernel/infra/database/connection.py`
- `shared_kernel/infra/database/orm.py`
- `shared_kernel/infra/database/migrations/`
- `shared_kernel/infra/sql_alchemy_unitofwork.py`
- `shared_kernel/infra/fastapi/config.py`
- `shared_kernel/infra/fastapi/main.py`
- `shared_kernel/infra/logging.py`
- `shared_kernel/infra/container.py`

Infrastructure implementations may depend on external libraries, but those dependencies must not leak into domain interfaces.

## 7. Repository Rules

Repository interfaces belong to the bounded context that owns the aggregate:

```text
identity/domain/user_repository.py
```

Concrete implementations belong in that bounded context's infrastructure:

```text
identity/infra/sqlalchemy_user_repository.py
```

Repositories should:

- query and persist entities
- use an injected SQLAlchemy `Session`
- avoid owning the entire transaction lifecycle
- avoid calling `commit()` after every operation
- return domain entities or domain-defined results
- keep SQLAlchemy-specific code inside infrastructure

The current user repository uses SQLAlchemy queries and should be improved with precise type annotations while preserving the protocol boundary.

Python does not automatically map `UserRepository` to `SQLAlchemyUserRepository`. The mapping must be explicit through constructor injection, FastAPI dependencies, or `dependency_injector` providers.

## 8. Unit of Work Rules

The Unit of Work abstraction is:

```text
shared_kernel/domain/unit_of_work.py
```

The SQLAlchemy implementation is:

```text
shared_kernel/infra/sql_alchemy_unitofwork.py
```

The Unit of Work owns transaction decisions for a business operation. Repositories should add, update, and delete without committing.

A normal application operation should follow this shape:

```text
create session
-> create repositories using that session
-> execute use case
-> commit once if successful
-> rollback on failure
-> close session
```

Do not add commits inside repository methods unless a specific technical requirement demands it.

## 9. Database and ORM Rules

SQLAlchemy is configured in:

```text
shared_kernel/infra/database/connection.py
```

The project uses a manually configured engine and session factory. Sessions use:

- `autocommit=False`
- `autoflush=False`
- `expire_on_commit=False`

ORM mappings are imperative and are defined in:

```text
shared_kernel/infra/database/orm.py
```

The `User` domain entity is mapped to the `user` table. The `role` column is mapped through `UserRole.from_value` and SQLAlchemy `composite()`.

When adding entities or fields:

- follow the existing imperative mapping style
- update the database table mapping
- create an Alembic migration
- keep domain entities independent from SQLAlchemy
- initialize ORM mappers exactly once

Alembic migrations are under:

```text
shared_kernel/infra/database/migrations/
```

Do not silently change the schema without a migration.

## 10. Configuration and Secrets

Application settings are defined in:

```text
shared_kernel/infra/fastapi/config.py
```

Settings use Pydantic Settings and read from `.env` with the prefix:

```text
CLONE_KIOT_VIET_
```

Database URLs, JWT secrets, signing keys, and other credentials must come from environment variables. Never commit production credentials or secret keys.

Do not use the database password as a JWT secret.

## 11. Authentication and Authorization

The preferred first authorization mechanism is:

- username/password authentication
- password hashing
- JWT bearer access tokens
- role-based access control using `UserRole`
- FastAPI dependencies for authentication and role checks

Recommended flow:

```text
login request
-> identity application service
-> UserRepository lookup
-> password hash verification
-> JWT access token
-> Authorization: Bearer <token>
-> token validation dependency
-> current user lookup
-> role authorization dependency
-> protected endpoint
```

Suggested behavior:

- invalid username/password: HTTP 401
- missing bearer token: HTTP 401
- malformed, expired, or invalid token: HTTP 401
- valid token with insufficient role: HTTP 403
- valid authenticated request: execute the endpoint

Authorization boundaries:

- identity domain: identity and authorization concepts
- identity application: authentication and authorization use cases
- identity infrastructure: JWT and password-hashing adapters
- identity presentation: login endpoint and schemas
- shared infrastructure: generic bearer-token and FastAPI plumbing
- business presentations: apply authentication and role dependencies

Do not put JWT parsing or FastAPI dependencies in domain entities.

The first version should not add refresh tokens, token revocation storage, a permissions table, OAuth provider integration, or resource ownership rules unless the requirement specifically needs them.

Passwords must always be stored as secure hashes. Never log passwords, password hashes, JWT secrets, or bearer tokens.

## 12. FastAPI Rules

The FastAPI bootstrap is:

```text
shared_kernel/infra/fastapi/main.py
```

It is responsible for:

- configuring logging
- creating the application container
- creating the FastAPI application
- initializing ORM mappings
- including routers
- configuring application-level middleware and startup behavior

FastAPI routes belong in presentation modules. Routes should:

- validate request data through Pydantic schemas
- call application use cases
- use injected dependencies
- translate domain/application errors into HTTP responses
- avoid embedding business rules

Use `Depends(...)` only at the presentation/infrastructure boundary. Do not import FastAPI into domain or application business logic.

## 13. Dependency Injection Rules

The application container is:

```text
shared_kernel/infra/container.py
```

The intended dependency flow is:

```text
FastAPI route
-> application use case
-> domain repository protocol
-> SQLAlchemy repository
-> SQLAlchemy session
```

Register concrete implementations explicitly. Do not rely on Python to infer interface-to-implementation mappings.

When adding a dependency:

1. define the abstraction at the correct boundary
2. implement it in infrastructure if it is technical
3. register it in the container or FastAPI dependency layer
4. inject it into the application service
5. test the behavior through the public boundary

The current container is mostly a placeholder, so changes should be incremental and should not introduce unnecessary container complexity.

## 14. Logging Rules

Logging configuration belongs in:

```text
shared_kernel/infra/logging.py
```

The application configures logging once during FastAPI startup.

Application modules should use:

```python
import logging

logger = logging.getLogger(__name__)
```

Use logging for meaningful events:

- `DEBUG`: detailed diagnostic information
- `INFO`: normal application or business events
- `WARNING`: recoverable abnormal situations
- `ERROR`: operation failures
- `logger.exception(...)`: failures inside exception handlers when a traceback is useful

Never log:

- passwords
- password hashes
- JWT secrets
- bearer tokens
- sensitive personal data unless explicitly required and protected

Do not configure handlers inside domain modules.

## 15. Code Change Rules

Before changing code:

1. inspect the local module and its nearest callers
2. identify the owning architectural layer
3. preserve the existing abstraction boundary
4. formulate one concrete hypothesis about the change
5. make the smallest coherent edit
6. run a focused validation immediately

Prefer existing project patterns over introducing new frameworks or abstractions.

Do not perform unrelated refactors while implementing a feature.

Do not move a repository implementation into the domain layer. Move or create only the repository contract in the domain layer.

Do not add comments that merely narrate obvious code. Add comments only when they explain a non-obvious architectural or technical decision.

## 16. Testing Rules

Tests should verify real behavior rather than only mock interactions.

Authentication and authorization tests should cover:

- password hashing and verification
- successful login
- invalid credentials
- valid JWT decoding
- invalid JWT
- expired JWT
- missing bearer token
- authenticated access
- insufficient role
- repository lookup behavior
- commit and rollback behavior

Expected HTTP assertions include:

- `200` or expected success status for valid requests
- `401` for unauthenticated requests
- `403` for authenticated but unauthorized requests

Use focused tests first, then run the wider suite.

## 17. Known Incomplete Areas

The following areas may still be incomplete and must not be assumed to be finished:

- identity application services
- identity presentation routes
- authentication and authorization
- dependency-injector providers
- router inclusion
- precise repository type annotations
- full test coverage
- production-safe secret configuration
- complete session and Unit of Work integration

Check the actual files before relying on this document as evidence of implementation.

## 18. Agent Response Expectations

When working on this project, an agent should:

- explain which layer owns the requested behavior
- preserve DDD boundaries
- use the existing SQLAlchemy and FastAPI patterns
- keep domain code framework-independent
- avoid exposing secrets in logs or responses
- make focused changes
- validate changes with tests, type checks, linting, or an application startup check
- clearly distinguish existing behavior from planned behavior
- mention pre-existing failures separately from failures caused by the new change
