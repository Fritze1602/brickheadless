
# 🚀 BrickHeadless

**Python-Based Headless First CMS**

_"Schreib dein Content-Schema einmal – erhalte automatisch eine Admin-UI und eine API. Kein Click-Builder, kein SaaS."_

---

## **Zielsetzung**

- **API-First CMS für Agentur-Projekte**
- **Code-First Content-Schema (YAML oder Python DSL)**
- **Automatisierte Admin-UI mit Django Forms + Tailwind**
- **REST-API mit OpenAPI Doku (drf-spectacular)**
- **Medienverwaltung mit Alt-Text & Renditions**
- **Repeater-Felder, Link-Objekte, Zahl, Text, Media**
- **Frontend komplett frei (Next.js, Nuxt, etc.)**

---

## **Stack**

| Layer | Tool |
|--------|------|
| **Backend** | Django + DRF + drf-spectacular |
| **Schema** | YAML oder Python DSL |
| **Admin-UI** | Django Forms + Tailwind |
| **API-Doku & Typings** | OpenAPI 3.0 + `npx openapi-typescript` |
| **Frontend** | Beliebig (Next.js etc.) |

---

## **Phasen**

### **Phase 0: Setup (Woche 1)**

- Virtuelle Umgebung anlegen
- Django-Projekt & App erstellen
- DRF & drf-spectacular installieren
- Media-Handling konfigurieren

---

### **Phase 1: Schema-System (Woche 2–3)**

- `schema.yaml` pro Projekt schreiben
- Parser bauen → Modelle, Forms, API daraus generieren
- Repeater, Link-Objekte, Media definieren

---

### **Phase 2: Admin-UI (Woche 4–5)**

- Django Forms dynamisch aus Schema
- Tailwind für Styles
- Mediathek mit Alt-Text & Uploads
- Repeater als JSONField mit UI

---

### **Phase 3: API + Docs (Woche 6)**

- DRF ViewSets dynamisch aus Schema
- OpenAPI Docs mit drf-spectacular
- Typings generieren für Frontend

---

### **Phase 4: Frontend-Anbindung (optional ab Woche 7)**

- Next.js / Astro als Headless-Frontend anbinden
- ISR / SSG Caching

---

### **Phase 5: Deployment & Doku (Woche 8)**

- VPS-Deployment (Gunicorn + Nginx/Caddy)
- Dockerfile (optional)
- README + Self-Hosting Guide

---

## **Core-Features**

- **1 Datei = Content-Schema**
- **Admin-UI aus Schema**
- **REST-API mit OpenAPI Docs**
- **Media + Alt-Text + Renditions**
- **Repeater & Link-Felder**
- **On-Premise, kein SaaS, kein Click-Builder**

---

## **Nächste Schritte**

1. **Venv anlegen & Django Projekt starten**
2. **Schema-Parser bauen**
3. **Admin-Forms & API-Generator entwickeln**
4. **Frontend anbinden (optional)**

---

## **Philosophie**

- **Build for use, not for fame**
- **"Carbon Fields für Headless-APIs"**
- **Produktivität > Over-Engineering**
