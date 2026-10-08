# Auto Repair Shop API v1

A well-structured, scalable REST API built with Python's `http.server` (no frameworks) and **Durus** as the object-oriented database.

## Project Structure

```
api/v1/
├── main.py                    # Entry point — starts the HTTP server
├── requirements.txt           # Python dependencies
├── core/
│   ├── config.py              # Server & database configuration
│   ├── headers.py             # Default HTTP response headers (CORS)
│   ├── request.py             # HTTP request parser (method, path, body)
│   ├── response.py            # HTTP JSON response builder
│   └── router.py              # URL pattern matching & dispatching
├── controllers/
│   ├── base_controller.py     # Generic CRUD controller (inherited by all)
│   ├── car_controller.py
│   ├── motorcycle_controller.py
│   ├── mechanic_controller.py
│   ├── part_controller.py
│   ├── service_order_controller.py
│   ├── user_controller.py
│   └── auth_controller.py     # Login & registration
├── models/
│   ├── vehicle.py             # Vehicle (base), Car, Motorcycle
│   ├── mechanic.py
│   ├── part.py
│   ├── service_order.py
│   └── user.py                # User with hashed password
├── validators/
│   ├── base_validator.py      # Shared validation helpers
│   ├── car_validator.py
│   ├── motorcycle_validator.py
│   ├── mechanic_validator.py
│   ├── part_validator.py
│   ├── service_order_validator.py
│   └── user_validator.py
└── database/
    ├── connection.py          # Durus singleton connection manager
    ├── repository.py          # Generic CRUD repository (base class)
    └── repositories/
        ├── car_repository.py
        ├── motorcycle_repository.py
        ├── mechanic_repository.py
        ├── part_repository.py
        ├── service_order_repository.py
        └── user_repository.py
```

## Requirements

- Python 3.8+
- Durus 4.3

## Installation

```bash
# From the project root
pip install -r api/v1/requirements.txt
```

## Running the Server

```bash
# From the project root
python -m api.v1.main
```

The server starts on `http://localhost:8000` by default. You can override this with environment variables:

```bash
API_HOST=127.0.0.1 API_PORT=9000 python -m api.v1.main
```

The database file is stored at `data/api.durus` (configurable via `DB_PATH` env var).

## API Endpoints

All endpoints are prefixed with `/api/v1`.

### Cars

| Method | Endpoint           | Description       |
|--------|--------------------|--------------------|
| GET    | `/api/v1/cars`     | List all cars      |
| GET    | `/api/v1/cars/{id}`| Get a car by ID    |
| POST   | `/api/v1/cars`     | Create a new car   |
| PUT    | `/api/v1/cars/{id}`| Update a car       |
| DELETE | `/api/v1/cars/{id}`| Delete a car       |

**POST/PUT body:**
```json
{
  "plate": "ABC-123",
  "make": "Toyota",
  "model": "Corolla",
  "year": 2020,
  "door_count": 4
}
```

### Motorcycles

| Method | Endpoint                  | Description             |
|--------|---------------------------|--------------------------|
| GET    | `/api/v1/motorcycles`     | List all motorcycles     |
| GET    | `/api/v1/motorcycles/{id}`| Get a motorcycle by ID   |
| POST   | `/api/v1/motorcycles`     | Create a new motorcycle  |
| PUT    | `/api/v1/motorcycles/{id}`| Update a motorcycle      |
| DELETE | `/api/v1/motorcycles/{id}`| Delete a motorcycle      |

**POST/PUT body:**
```json
{
  "plate": "XYZ-987",
  "make": "Honda",
  "model": "CBR 600",
  "year": 2022,
  "engine_displacement_cc": 600
}
```

### Mechanics

| Method | Endpoint                | Description            |
|--------|-------------------------|-------------------------|
| GET    | `/api/v1/mechanics`     | List all mechanics      |
| GET    | `/api/v1/mechanics/{id}`| Get a mechanic by ID    |
| POST   | `/api/v1/mechanics`     | Create a new mechanic   |
| PUT    | `/api/v1/mechanics/{id}`| Update a mechanic       |
| DELETE | `/api/v1/mechanics/{id}`| Delete a mechanic       |

**POST/PUT body:**
```json
{
  "name": "John Smith",
  "specialty": "Engine"
}
```

### Parts

| Method | Endpoint             | Description        |
|--------|----------------------|---------------------|
| GET    | `/api/v1/parts`      | List all parts      |
| GET    | `/api/v1/parts/{id}` | Get a part by ID    |
| POST   | `/api/v1/parts`      | Create a new part   |
| PUT    | `/api/v1/parts/{id}` | Update a part       |
| DELETE | `/api/v1/parts/{id}` | Delete a part       |

**POST/PUT body:**
```json
{
  "name": "Oil filter",
  "price": 180.00
}
```

### Service Orders

| Method | Endpoint              | Description             |
|--------|-----------------------|--------------------------|
| GET    | `/api/v1/orders`      | List all orders          |
| GET    | `/api/v1/orders/{id}` | Get an order by ID       |
| POST   | `/api/v1/orders`      | Create a new order       |
| PUT    | `/api/v1/orders/{id}` | Update an order          |
| DELETE | `/api/v1/orders/{id}` | Delete an order          |

**POST/PUT body:**
```json
{
  "order_number": "SO-0001",
  "vehicle_type": "car",
  "vehicle_id": 1,
  "mechanic_id": 1,
  "part_ids": [1, 2],
  "description": "Brake service and oil change",
  "status": "open",
  "labor_cost": 500.00
}
```

> **Note:** `vehicle_type` must be `"car"` or `"motorcycle"`. The `part_ids` field is optional. References to vehicle, mechanic, and parts are stored as direct object references in Durus (not as IDs).

### Users

| Method | Endpoint              | Description         |
|--------|-----------------------|----------------------|
| GET    | `/api/v1/users`       | List all users       |
| GET    | `/api/v1/users/{id}`  | Get a user by ID     |
| POST   | `/api/v1/users`       | Create a new user    |
| PUT    | `/api/v1/users/{id}`  | Update a user        |
| DELETE | `/api/v1/users/{id}` | Delete a user        |

### Authentication

| Method | Endpoint                | Description          |
|--------|-------------------------|----------------------|
| POST   | `/api/v1/auth/register` | Register a new user  |
| POST   | `/api/v1/auth/login`    | Login with credentials |

**Register body:**
```json
{
  "username": "admin",
  "password": "secret123",
  "role": "admin"
}
```

**Login body:**
```json
{
  "username": "admin",
  "password": "secret123"
}
```

## Database (Durus Object-Oriented DB)

### How it works

Durus stores Python objects directly to disk. Every model class inherits from `durus.persistent.Persistent`, and objects are organized into named collections (`PersistentDict`) inside the database root.

- **No ORM needed** — objects are stored as-is with all their attributes.
- **Direct references** — `ServiceOrder.vehicle` points to the actual `Vehicle` object, not an ID.
- **Automatic persistence** — any `Persistent` object reachable from the root is saved on `commit()`.
- **Transactions** — every write calls `connection.commit()` explicitly.

### Data file

The database is a single file (default: `data/api.durus`). Delete it to start fresh.

### Inspecting data

You can interact with the database directly from a Python shell:

```python
from api.v1.database.connection import DatabaseConnection

DatabaseConnection.initialize("data/api.durus")
db = DatabaseConnection.get_instance()

# List all collections
print(list(db.root.keys()))

# Browse cars
for car_id, car in db.root["cars"].items():
    print(car_id, car.to_dict())

db.close()
```

## How to Add a New Entity

Follow these steps to add a new entity (e.g. `Supplier`):

### 1. Create the model

Create `api/v1/models/supplier.py`:

```python
from durus.persistent import Persistent

class Supplier(Persistent):
    def __init__(self, name="", phone=""):
        self.name = name
        self.phone = phone

    def to_dict(self) -> dict:
        return {"name": self.name, "phone": self.phone}
```

### 2. Register the collection

Open `api/v1/database/connection.py` and add `"suppliers"` to the `COLLECTIONS` list:

```python
COLLECTIONS = [
    "cars",
    "motorcycles",
    # ... existing collections ...
    "suppliers",   # <-- add here
]
```

### 3. Create the repository

Create `api/v1/database/repositories/supplier_repository.py`:

```python
from api.v1.database.repository import BaseRepository

class SupplierRepository(BaseRepository):
    collection_name = "suppliers"
```

### 4. Create the validator

Create `api/v1/validators/supplier_validator.py`:

```python
from api.v1.validators.base_validator import BaseValidator

class SupplierValidator(BaseValidator):
    REQUIRED_FIELDS = ["name", "phone"]

    @classmethod
    def validate_create(cls, data: dict) -> list:
        return cls.require_fields(data, cls.REQUIRED_FIELDS)
```

### 5. Create the controller

Create `api/v1/controllers/supplier_controller.py`:

```python
from api.v1.controllers.base_controller import BaseController
from api.v1.database.repositories.supplier_repository import SupplierRepository
from api.v1.validators.supplier_validator import SupplierValidator
from api.v1.models.supplier import Supplier

class SupplierController(BaseController):
    repository_class = SupplierRepository
    validator_class = SupplierValidator
    model_class = Supplier
    entity_name = "Supplier"
    _model_fields = ["name", "phone"]
```

### 6. Register the routes

Open `api/v1/main.py`, import the controller, and add routes inside `register_routes()`:

```python
from api.v1.controllers.supplier_controller import SupplierController

# Inside register_routes():
supplier = SupplierController()
router.add_route("GET", "/suppliers", supplier.list_all)
router.add_route("GET", "/suppliers/{id}", supplier.get_one)
router.add_route("POST", "/suppliers", supplier.create)
router.add_route("PUT", "/suppliers/{id}", supplier.update)
router.add_route("DELETE", "/suppliers/{id}", supplier.delete)
```

That's it — 6 small files and you have a fully functional CRUD resource with validation.

## Response Format

All responses follow a consistent JSON structure:

**Success:**
```json
{
  "status": "success",
  "message": "Success",
  "data": { ... }
}
```

**Error:**
```json
{
  "status": "error",
  "message": "Bad request",
  "errors": ["Field 'name' is required."]
}
```

## License

MIT
