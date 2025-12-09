# LPNU Schedule API

A public REST API designed to retrieve schedule data for LPNU (Lviv Polytechnic National University). This service allows developers to integrate university schedule information into their applications.

## 🌐 Public Access & Hosting

This API is publicly hosted and open for general use.

- **Base URL:** `https://lpnu-api-py6o.onrender.com`
- **Status:** ✅ Public / Open Access
- **Hosting Provider:** Render

## 📚 Documentation

The API is fully documented using OpenAPI 3.0 standards. You can access the interactive documentation and specifications via the following endpoints:

- **Interactive Documentation (ReDoc):**
  [https://lpnu-api-py6o.onrender.com/docs/](https://lpnu-api-py6o.onrender.com/docs/)

- **OpenAPI Specification (YAML):**
  [https://lpnu-api-py6o.onrender.com/openapi.yaml](https://lpnu-api-py6o.onrender.com/openapi.yaml)

- **OpenAPI Specification (JSON):**
  [https://lpnu-api-py6o.onrender.com/openapi.json](https://lpnu-api-py6o.onrender.com/openapi.json)

## 🚀 Usage

You can make GET requests to the available endpoints to fetch schedule data.

### Example Request
```bash
curl -X GET [https://lpnu-api-py6o.onrender.com/api/schedule?group=KN-101](https://lpnu-api-py6o.onrender.com/api/schedule?group=KN-101)
