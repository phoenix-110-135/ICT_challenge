## Running the Project with Docker

### Prerequisites

Make sure the following tools are installed:

* Docker
* Docker Compose

You can verify the installation with:

```bash
docker --version
docker compose version
```

---

### 1. Clone the Repository

```bash
git clone https://github.com/phoeix-110-135/ict_challenge 
cd ict_challenge 
```

---

### 2. Configure Environment Variables

Create a `.env` file based on the provided environment configuration.

Example:

```env
SECRET_KEY=your-secret-key

DEBUG=True

DB_NAME=warehouse_routing
DB_USER=postgres
DB_PASSWORD=your-database-password
DB_HOST=db
DB_PORT=5432

BODY_ID=470510
```

> When running the application with Docker Compose, the database host must be `db`, not `localhost`, because PostgreSQL runs in a separate Docker container.

---

### 3. Start the Application

Build and start all services using:

```bash
docker compose up --build
```

This command starts:

* Django backend
* PostgreSQL database
* Frontend service
* Database initialization and migrations

To run the services in the background:

```bash
docker compose up --build -d
```

---

### 4. Apply Database Migrations

If migrations are not automatically applied during startup, run:

```bash
docker compose exec backend python manage.py migrate
```

---

### 5. Load Initial Database Data

The project includes an SQL database backup file:

```text
warehouse_routing.sql
```

To restore the database backup inside the PostgreSQL container:

```bash
docker compose exec -T db psql -U postgres -d warehouse_routing < warehouse_routing.sql
```

> The exact command may vary depending on the database credentials defined in `.env`.

---

### 6. Create a Django Superuser

To access the Django administration panel:

```bash
docker compose exec backend python manage.py createsuperuser
```

Then follow the instructions shown in the terminal.

---

## Accessing the Application

### Frontend

The registration page is the starting point of the application:

```text
http://localhost:5500/register.html
```

The user flow starts with:

```text
/register
```

The user can then:

1. Register a new account.
2. Receive and verify the OTP code.
3. Log in to the system.
4. Access authenticated APIs.

---

### Backend API

The backend API is available at:

```text
http://localhost:8000
```

---

### Swagger API Documentation

Interactive API documentation is available at:

```text
http://localhost:8000/api/docs/
```

Swagger UI can be used to:

* Explore all API endpoints.
* View request and response schemas.
* Test API endpoints.
* Review authentication requirements.
* Test warehouse APIs.
* Test inventory APIs.
* Test order APIs.
* Test routing APIs.
* Test routing policies.
* Test user authentication APIs.

The OpenAPI schema is available at:

```text
http://localhost:8000/api/schema/
```

---

### Django Admin Panel

The Django administration panel is available at:

```text
http://localhost:8000/admin/
```

After creating a superuser, the administrator can manage:

* Users
* Warehouses
* SKUs
* Warehouse inventory
* Orders
* Routing policies
* Other registered Django models

---

## Stopping the Application

To stop the running containers:

```bash
docker compose down
```

To stop the containers and remove the database volume:

```bash
docker compose down -v
```

> Warning: `docker compose down -v` removes the PostgreSQL volume and all data stored inside that volume. Use this command carefully.

---

## Useful Docker Commands

View running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs
```

View backend logs:

```bash
docker compose logs backend
```

View database logs:

```bash
docker compose logs db
```

Open a shell inside the backend container:

```bash
docker compose exec backend bash
```

Run Django management commands:

```bash
docker compose exec backend python manage.py <command>
```

Example:

```bash
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
```


## Architecture Overview

The system is designed as a modular warehouse-routing service responsible for selecting the most suitable warehouse for each e-commerce order.

The architecture separates the **decision-making algorithm** from the **business priorities** used during the decision-making process.

This separation is one of the most important architectural decisions in the project.

```text
                    ┌─────────────────────┐
                    │   E-commerce Client  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Orders Service    │
                    │   Order Management   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Routing Service    │
                    │  Decision Engine     │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌────────────┐   ┌──────────────┐
       │ Inventory  │   │ Warehouses │   │   Policies   │
       │  Service   │   │  Service   │   │ Configuration│
       └────────────┘   └────────────┘   └──────────────┘
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │  Routing Decision   │
                    │ Selected Warehouse  │
                    └─────────────────────┘
```

---

# Routing vs Policy

A key design principle of the system is the separation between:

```text
Routing Algorithm
```

and:

```text
Routing Policy
```

These two concepts have different responsibilities.

### Routing

The Routing Service is responsible for answering:

> Which warehouse should fulfill this order?

It is the actual decision-making engine.

For example:

```text
Warehouse A → Score: 0.82
Warehouse B → Score: 0.71
Warehouse C → Score: 0.63
```

The routing engine selects:

```text
Warehouse A
```

---

### Policy

The policy does not select the warehouse directly.

Instead, it defines:

> What is important when making the decision?

For example:

```text
Is minimizing cost more important than delivery speed?

Is fast delivery more important than distance?

How important is current traffic?

```

Therefore:

```text
Routing = Decision Maker

Policy = Decision Priorities
```

This separation allows the system to change business priorities without rewriting the routing algorithm.

---

# RoutingPolicy

The system contains a configurable `RoutingPolicy` model.

A policy defines the importance of different optimization criteria:

```text
cost_weight
time_weight
distance_weight
traffic_weight
```

For example:

```text
cost_weight     = 0.40
time_weight     = 0.30
distance_weight = 0.20
traffic_weight  = 0.10
```

The total weight is:

```text
0.40 + 0.30 + 0.20 + 0.10 = 1.00
```

This means:

```text
40% → Transportation Cost
30% → Estimated Delivery Time
20% → Distance
10% → Traffic
```

The policy therefore represents the business priorities of the routing system.

---

# Why Is the Policy Separate from the Routing Algorithm?

If the weights were hardcoded inside the routing algorithm:

```python
score = (
    cost * 0.40 +
    time * 0.30 +
    distance * 0.20 +
    traffic * 0.10
)
```

then changing business priorities would require changing the source code.

This is not ideal for a real logistics platform.

Instead, the system stores these values as configurable data:

```text
RoutingPolicy
│
├── cost_weight
├── time_weight
├── distance_weight
└── traffic_weight
```

The routing engine can then load the active policy dynamically.

Conceptually:

```python
policy = get_active_policy()

score = (
    normalized_cost * policy.cost_weight
    + normalized_time * policy.time_weight
    + normalized_distance * policy.distance_weight
    + normalized_traffic * policy.traffic_weight
)
```

This provides a much more flexible architecture.

---

# Policy Examples

Different business scenarios can use different policies.

## Cost-Optimized Policy

For a company primarily focused on reducing transportation costs:

```text
Cost:     0.60
Time:     0.15
Distance: 0.15
Traffic:  0.10
```

This policy prioritizes economical warehouse allocation.

---

## Fast Delivery Policy

For urgent orders:

```text
Cost:     0.15
Time:     0.55
Distance: 0.15
Traffic:  0.15
```

The system prioritizes delivery speed over transportation cost.

---

## Balanced Policy

For general-purpose order fulfillment:

```text
Cost:     0.40
Time:     0.30
Distance: 0.20
Traffic:  0.10
```

This provides a balanced trade-off between cost and delivery performance.

---

# Selected Optimization Criteria

The system currently considers four major factors.

## 1. Transportation Cost

```text
cost_weight
```

Transportation cost is one of the most important factors in logistics optimization.

For example:

```text
Warehouse A → 100,000 Tomans
Warehouse B → 300,000 Tomans
```

If both warehouses provide a similar delivery time, selecting Warehouse B would be economically inefficient.

Therefore, transportation cost is included in the decision model.

### Benefits

* Reduces operational expenses
* Improves profit margins
* Prevents economically inefficient warehouse selection
* Represents real-world logistics constraints

---

## 2. Estimated Delivery Time

```text
time_weight
```

The cheapest warehouse is not always the best warehouse.

For example:

```text
Warehouse A:
Cost = 100,000
Delivery Time = 120 minutes

Warehouse B:
Cost = 150,000
Delivery Time = 30 minutes
```

For an urgent order, Warehouse B may be the better choice despite its higher cost.

Delivery time is therefore important for:

* Customer satisfaction
* Express delivery
* SLA compliance
* Reducing delivery delays
* Supporting priority orders

---

## 3. Distance

```text
distance_weight
```

Distance is a fundamental logistics factor.

A longer distance usually results in:

```text
More fuel consumption
More delivery time
Higher operational cost
Higher transportation risk
```

However, the system does not select the nearest warehouse blindly.

The following statement is not always true:

```text
Nearest Warehouse = Best Warehouse
```

A nearby warehouse may have:

```text
High traffic
High transportation cost
Insufficient inventory
Poor delivery performance
```

Therefore, distance is treated as one component of a multi-factor optimization model.

---

## 4. Traffic

```text
traffic_weight
```

Traffic is particularly important in real-world logistics systems.

Two warehouses may have similar geographical distances from the customer:

```text
Warehouse A → Heavy Traffic
Warehouse B → Low Traffic
```

Even though the distance is similar, the actual delivery time can be significantly different.

Traffic information can therefore affect:

```text
Actual Delivery Time
Fuel Consumption
Delivery Reliability
Operational Cost
```

This is why traffic is included as an independent factor in the policy model.

---

# Normalized Scoring Model

The system should not directly combine raw values such as:

```text
Cost = 250000
Time = 45
Distance = 18.5
Traffic = 0.7
```

because these values have different scales.

Instead, the values should be normalized before calculating the final score.

Conceptually:

```text
Normalized Cost
Normalized Time
Normalized Distance
Normalized Traffic
```

are calculated first.

Then the policy weights are applied:

```text
Final Score =
    Cost Score × Cost Weight
  + Time Score × Time Weight
  + Distance Score × Distance Weight
  + Traffic Score × Traffic Weight
```

The routing service can then compare all eligible warehouses and select the warehouse with the best overall score.

---

# High-Level Decision Flow

```text
1. Receive Order
        │
        ▼
2. Extract SKU and Customer Location
        │
        ▼
3. Find Warehouses with Available Inventory
        │
        ▼
4. Load Active Routing Policy
        │
        ▼
5. Calculate Cost
        │
        ▼
6. Calculate Delivery Time
        │
        ▼
7. Calculate Distance
        │
        ▼
8. Analyze Traffic
        │
        ▼
9. Normalize All Metrics
        │
        ▼
10. Apply Policy Weights
        │
        ▼
11. Calculate Final Routing Score
        │
        ▼
12. Select Best Warehouse
        │
        ▼
13. Return Routing Decision
```

---

# Example Routing Decision

Suppose the system evaluates three warehouses:

| Warehouse   | Cost Score | Time Score | Distance Score | Traffic Score |
| ----------- | ---------: | ---------: | -------------: | ------------: |
| Warehouse A |       0.90 |       0.60 |           0.80 |          0.50 |
| Warehouse B |       0.70 |       0.95 |           0.60 |          0.90 |
| Warehouse C |       0.80 |       0.70 |           0.75 |          0.70 |

Using:

```text
Cost Weight     = 0.40
Time Weight     = 0.30
Distance Weight = 0.20
Traffic Weight  = 0.10
```

the system calculates a final score for each candidate.

The warehouse with the highest score becomes the selected fulfillment warehouse.

The final response can contain:

```json
{
  "warehouse_id": 12,
  "estimated_delivery_time": 35,
  "total_cost": 145000,
  "route_optimization_score": 0.87
}
```

---

# Architectural Advantages

This architecture provides several important advantages.

### 1. Configurability

Business priorities can change without changing the routing algorithm.

---

### 2. Maintainability

The system separates:

```text
Business Rules
```

from:

```text
Algorithmic Logic
```

This makes the code easier to maintain.

---

### 3. Extensibility

New factors can be added later:

```text
warehouse_capacity_weight
vehicle_type_weight
weather_weight
delivery_priority_weight
```

without redesigning the entire architecture.

---

### 4. Multi-Policy Support

The system can support different routing strategies:

```text
Standard Delivery
Express Delivery
Low-Cost Delivery
Emergency Delivery
Heavy Fleet Delivery
```

Each strategy can use a different `RoutingPolicy`.

---

### 5. Microservice Compatibility

Because the Routing Service only consumes:

```text
Order Data
Inventory Data
Warehouse Data
Routing Policy
```

it can be separated into an independent microservice in the future.

A possible architecture is:

```text
Order Service
       │
       ▼
Routing Service
       │
       ├── Inventory Service
       ├── Warehouse Service
       ├── Policy Service
       └── Traffic Provider
```

This design is compatible with containerized environments and future horizontal scaling.

---

# Architectural Summary

The central architectural idea of the project is:

> The routing algorithm determines **which warehouse should be selected**, while the routing policy determines **what makes a warehouse a good choice**.

This separation allows the system to adapt to different business requirements without modifying the core routing algorithm.

```text
Policy
   ↓
Defines Priorities

Routing Engine
   ↓
Evaluates Candidates

Inventory + Warehouse + Order Data
   ↓
Provides Real-Time Inputs

Final Decision
   ↓
Selected Warehouse
```

This design creates a flexible foundation for a scalable intelligent warehouse allocation system.
