# 🚧 Bricks CMS (TRIPPLE BETA)

**A headless, developer-first CMS built on Django.**
Write your content schema once – get a working API and admin UI.
No SaaS, no builder UI, just Python and clarity.

---

## ✨ What is Bricks?

Bricks is an early-stage, code-first CMS that combines the flexibility of JSON-based pages with the power of SQL-backed collections – all defined in plain Python.

Built for developers who:

- are tired of clicking through interfaces (Strapi, Directus),
- don’t want to give up SQL just to use Payload,
- want to **own their backend**, not rent it.

---

## 🧱 Core Concepts

### Pages

- Represent unique content like "Homepage", "About", etc.
- Defined with flexible fields (`TextField`, `Repeater`, etc.)
- Stored as structured JSON
- Ideal for block-based rendering in your frontend

### Collections

- Represent structured content types like "Projects", "Jobs", "Team"
- Backed by generated Django models and real SQL tables
- Support filtering, querying, relations, and admin lists

```python
homepage = Page(
    "Homepage",
    slug="homepage",
    fields=[
        TextField("Claim", "claim"),
        Repeater("CTAs", "ctas", fields=[
            TextField("Label", "label"),
            URLField("Link", "url"),
        ])
    ]
)

projects = Collection(
    label="Projects",
    singular_label="Project",
    slug="projects",
    fields=[
        TextField("Title", "title"),
        TextField("Description", "description"),
        URLField("URL", "url"),
    ]
)
```

## 🏗️ Current Status: TRIPPLE BETA

> Bricks is in an early experimental phase.
> Only basic field types are implemented.
> The `sync_collections` system generates database tables from your content schema.
> The `Repeater` field is a work in progress.
> The admin UI for editing content is just starting to take shape.

But: **The core ideas are working – and evolving fast.**
