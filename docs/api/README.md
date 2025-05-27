# Segecha Logistics API Documentation

## Authentication

All API endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your_token>
```

## Endpoints

### Authentication

#### POST /api/auth/login
Authenticate user and get JWT token.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

**Response:**
```json
{
    "token": "jwt_token_here",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "is_admin": false
    }
}
```

### Shipments

#### GET /api/shipments
Get list of shipments.

**Query Parameters:**
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)
- `status`: Filter by status
- `search`: Search term

**Response:**
```json
{
    "shipments": [
        {
            "id": 1,
            "tracking_number": "SEG123456",
            "status": "in_transit",
            "pickup_location": "Nairobi",
            "delivery_location": "Mombasa",
            "created_at": "2024-03-20T10:00:00Z"
        }
    ],
    "total": 100,
    "page": 1,
    "per_page": 20
}
```

#### POST /api/shipments
Create new shipment.

**Request Body:**
```json
{
    "pickup_location": "Nairobi",
    "delivery_location": "Mombasa",
    "cargo_details": {
        "weight": 100,
        "dimensions": "2x2x2",
        "type": "general"
    },
    "customer_info": {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+254700000000"
    }
}
```

### Quotes

#### POST /api/quotes
Request a shipping quote.

**Request Body:**
```json
{
    "pickup_location": "Nairobi",
    "delivery_location": "Mombasa",
    "cargo_details": {
        "weight": 100,
        "dimensions": "2x2x2",
        "type": "general"
    }
}
```

**Response:**
```json
{
    "quote_id": "Q123456",
    "estimated_cost": 5000,
    "estimated_delivery_time": "2-3 days",
    "valid_until": "2024-03-27T10:00:00Z"
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
    "error": "Invalid request data",
    "details": {
        "field": ["error message"]
    }
}
```

### 401 Unauthorized
```json
{
    "error": "Authentication required"
}
```

### 403 Forbidden
```json
{
    "error": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
    "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
    "error": "Internal server error"
}
```

## Rate Limiting

API requests are limited to:
- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

Rate limit headers are included in all responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1616238000
``` 