# Samita Retail Management System
## MVP Implementation Status

## 1. Project Understanding

The project is an AI-assisted retail management system for Samita Liquor & General Store.

The primary goal is to reduce manual effort in:

- Inventory management
- Billing
- Stock tracking
- Transaction recording
- Daily sales reporting
- Voice-based billing

CCTV and barcode features are planned demonstration features and were not prioritized in the first implementation.

## 2. Completed MVP Scope

The following functionality has been implemented:

1. Product database
2. Seed inventory dataset
3. Inventory search
4. Product categories
5. Product prices
6. Stock quantity tracking
7. Low-stock alerts
8. Product creation
9. Product update
10. Product deletion
11. Billing cart
12. Add products to cart
13. Update cart quantities
14. Remove products from cart
15. Automatic bill total calculation
16. Stock validation before checkout
17. Automatic stock deduction after checkout
18. Transaction storage
19. Transaction history API
20. Daily sales report
21. Best-selling product report
22. Browser-based voice billing
23. Voice product matching
24. Ambiguous product selection

## 3. Architecture

### Backend

The backend uses:

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

The backend is the source of truth for inventory and transactions.

The primary backend file is:

`app/main.py`

### Frontend

The frontend is a lightweight browser dashboard built with:

- HTML
- CSS
- Vanilla JavaScript

The frontend files are:

- `static/index.html`
- `static/styles.css`
- `static/app.js`

The frontend is intentionally simple for the MVP. It can later be migrated to React or Next.js without changing the core API contract.

### Database

SQLite is used for local development and zero-configuration setup.

The database models are:

#### Product

Stores:

- Product name
- Category
- Barcode
- Price
- Stock quantity
- Low-stock threshold

#### Transaction

Stores:

- Transaction ID
- Creation timestamp
- Total amount
- Transaction items

#### TransactionItem

Stores:

- Product ID
- Product name snapshot
- Quantity purchased
- Unit price
- Parent transaction ID

## 4. Inventory Implementation

The application creates the product tables automatically when the backend starts.

If the database is empty, the application seeds sample products such as:

- Dairy Milk Chocolate
- KitKat Chocolate
- Classic Salted Chips
- Orange Juice 1L
- Mineral Water 1L
- Premium Whisky 750ml

Inventory can be searched by:

- Product name
- Category
- Barcode

Products are flagged as low-stock when their stock is less than or equal to the configured low-stock threshold.

## 5. Billing and Checkout Flow

The billing flow is:

1. User searches or selects a product.
2. Product is added to the frontend cart.
3. User adjusts the quantity.
4. Frontend calculates the estimated total.
5. User confirms the sale.
6. Backend checks that all products exist.
7. Backend validates available stock.
8. Backend deducts the purchased quantities.
9. Backend creates a transaction.
10. Backend stores transaction items.
11. Frontend clears the cart and reloads inventory.

The backend prevents stock from becoming negative.

All billing methods use the same checkout endpoint:

`POST /api/checkout`

This keeps manual billing and voice billing consistent.

## 6. Voice-Based Billing Implementation

Voice billing is implemented using the browser Speech Recognition API.

Example command:

> Add 5 chocolates

The browser converts speech into text. The transcript is sent to:

`GET /api/voice/parse?text=...`

The backend parser extracts:

- Action
- Quantity
- Product search term

Supported command patterns currently include:

- `Add 5 chocolates`
- `Buy 2 chips`
- `Give me 3 water`
- `Remove 1 chocolate`
- `Delete 2 chips`

The voice parser does not directly modify the database.

It only returns a parsed intent and matching products.

The frontend then adds the selected product to the same billing cart used by manual product selection.

If multiple products match the voice command, the user is shown a selection list. This supports cases such as multiple chocolate products being available.

## 7. Transaction Management

Completed transactions are stored in the database.

The transaction history endpoint is:

`GET /api/transactions`

Each transaction includes:

- Transaction ID
- Date and time
- Total amount
- Purchased products
- Quantities
- Unit prices

Product names and unit prices are copied into transaction items so historical transactions remain understandable even if the product record changes later.

## 8. Daily Reports

The daily report endpoint is:

`GET /api/reports/daily`

The report provides:

- Total sales for the current day
- Number of transactions
- Best-selling products
- Low-stock products

The dashboard displays the sales total, transaction count, low-stock count, and best-selling products.

## 9. API Endpoints

### Inventory

```text
GET    /api/products
POST   /api/products
PUT    /api/products/{product_id}
DELETE /api/products/{product_id}
```

### Billing

```text
POST /api/checkout
```

### Transactions

```text
GET /api/transactions
```

### Reports

```text
GET /api/reports/daily
```

### Voice

```text
GET /api/voice/parse?text=Add%205%20chocolates
```

## 10. Verification Completed

The implementation was checked with an API smoke test.

The following was verified:

- Backend imports successfully
- Six sample products are available
- Voice parsing recognizes `Add 5 chocolates`
- Multiple matching products are returned for ambiguous terms
- Checkout succeeds with valid stock
- Stock decreases after checkout
- Daily report transaction count updates
- Python compilation succeeds
- Git whitespace validation succeeds

Example verification result:

```text
products 6
voice add 2
checkout 200 20.0
stock_sync 30 29
report 1
```

## 11. How to Run

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start the application:

```powershell
python -m uvicorn app.main:app --reload
```

Open the dashboard at:

```text
http://127.0.0.1:8000
```

The SQLite database is created automatically on first startup.

## 12. Current Limitations

The following features are not yet implemented:

- Full transaction history screen in the frontend
- Product management forms in the frontend
- Advanced natural language understanding
- Hindi or multilingual voice commands
- Cloud speech-to-text integration
- Physical barcode scanner integration
- CCTV video upload and computer vision analysis
- User authentication
- Role-based access control
- PostgreSQL deployment configuration
- Database migrations
- Automated frontend tests

The current voice implementation depends on browser support for the Speech Recognition API. The search and manual cart workflow remain available when voice recognition is unavailable.

## 13. Recommended Next Steps

The recommended development order is:

1. Add a full inventory management screen with create/edit/delete forms.
2. Add a dedicated transaction history view.
3. Improve voice command parsing for natural language variations.
4. Add Hindi and regional language support.
5. Add barcode demonstration input.
6. Add automated backend tests.
7. Add CCTV upload and analysis as a separate, non-inventory-changing module.
8. Migrate the frontend to Next.js if the project requires a larger production UI.

## 14. Files Added or Updated

```text
app/__init__.py
app/main.py
static/index.html
static/app.js
static/styles.css
requirements.txt
README.md
IMPLEMENTATION_STATUS.md
```
