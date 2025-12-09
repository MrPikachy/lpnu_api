# LPNU Schedule API

A public REST API designed to retrieve schedule data for LPNU (Lviv Polytechnic National University). This service serves as a bridge between the university website and external applications.

## 🌐 Public Access & Hosting

This API is publicly hosted and open for general use. It is deployed on Render and maintained as an open-source project.

- **Base URL:** `https://lpnu-api-py6o.onrender.com`
- **Status:** ✅ Public / Open Access
- **Documentation Endpoint:** `https://lpnu-api-py6o.onrender.com/docs/`

## 📚 Documentation

The API is fully documented using OpenAPI 3.0 standards.

- **Interactive UI (ReDoc):** [https://lpnu-api-py6o.onrender.com/docs/](https://lpnu-api-py6o.onrender.com/docs/)
- **OpenAPI Spec (JSON):** [https://lpnu-api-py6o.onrender.com/openapi.json](https://lpnu-api-py6o.onrender.com/openapi.json)

## 🚀 Usage

**Endpoint:** `/api/schedule`

**Parameters:**
- `group`: The name of the student group (e.g., `ПП-12`)

**Example Request:**
```bash

curl "[https://lpnu-api-py6o.onrender.com/api/schedule?group=KN-101](https://lpnu-api-py6o.onrender.com/api/schedule?group=ПП-12)"
