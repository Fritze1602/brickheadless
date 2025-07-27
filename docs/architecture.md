# 🧠 Architecture Overview: Bricks CMS

Bricks is organized around two content types, and one core idea:
**Define content in Python → use it anywhere.**

## Core Content Types

### 1. Pages (Unstructured, JSON)

- One-off content like Home, About, Contact
- Fully flexible structure using JSONField in the database
- Defined in `content/pages.py` using `Page(...)` and field definitions
- Can contain nested fields like `Repeater`, `TextField`, `URLField`
- Rendered in frontend as blocks or sections

### 2. Collections (Structured, SQL)

- Repeatable types like Projects, Team Members, Jobs
- Defined in the same file using `Collection(...)`
- Bricks uses `sync_collections` to generate real Django models as Python code
  (in `content/generated_models.py`), based on `Collection(...)` definitions.

  We explicitly avoid runtime model generation (e.g. via `type()` or factories)
  to ensure full support for migrations, admin registration, type checking, and IDE integration.

- Full ORM support, database migrations, filters, relations, etc.

## Admin UI Strategy

Bricks ships with a modern admin interface using **Progressive Island Hydration**.

- Built in React 19 with Tailwind CSS v4
- Hydrates only interactive islands (e.g. forms, repeaters)
- Avoids full-page SPAs and JavaScript-heavy stacks

### 🔧 Developer Experience (DX)

Bricks users:

- **Do not need Node.js or npm**
- **Do not run any frontend build process**
- Admin UI is pre-built and served as static files via Django

Only the Bricks **core maintainers** build and ship the React UI inside the package.
However, Bricks is designed to allow advanced users to **extend or replace the admin UI** if needed — enabling agency branding, custom widgets, or full overrides.

This architecture delivers a modern experience with zero setup friction.

## API Layer

Bricks is API-first by design — not by extension.

- Built directly on Django REST Framework
- Page and Collection schemas automatically generate endpoints and serializers
- RESTful structure (e.g. `/api/pages/homepage/`, `/api/projects/`)
- JSON responses ready to consume in modern frontends
- No GraphQL, no custom client, no black box

### OpenAPI & TypeScript Support

- Bricks uses [`drf-spectacular`](https://github.com/tfranzel/drf-spectacular) for OpenAPI 3.0 schema generation
- You can generate fully typed client code for TypeScript frontends:
  ```bash
  npx openapi-typescript http://localhost:8000/api/schema/ -o types/api.d.ts
  ```

## Key Design Decisions

- ✅ **Pages = JSON** → flexible, composable, frontend-controlled
- ✅ **Collections = SQL** → structured, queryable, admin-listable
- ✅ **Fields are modular** → each field knows how to render/save/validate
- ✅ **No builder UI** → everything is defined in code
