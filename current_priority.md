# Current Development Priorities
## Smart Retail Management System – Samita Liquor & General Store

## 1. Current Objective

Develop a functional retail management prototype focusing primarily on inventory management and voice-based billing, supported by transaction tracking and automated daily reports.

CCTV and barcode functionalities will initially use demonstration inputs.

## 2. Development Priority

### P0 – Core Foundation (Highest Priority)

**1. Inventory Management**
- Create product database and sample inventory dataset.
- Add, edit, delete, and search products.
- Manage categories, prices, and stock quantities.
- Implement low-stock alerts.

**2. Billing & Inventory Synchronization**
- Create a billing cart.
- Add, remove, and update product quantities.
- Calculate total bill automatically.
- Validate stock before checkout.
- Automatically deduct inventory after successful transactions.

**3. Transaction Management**
- Store completed transactions.
- Maintain product-wise purchase details.
- Display transaction history.

### P1 – Main AI Features

**4. Voice-Based Billing**
- Implement microphone input and speech-to-text.
- Extract product names, quantities, and user actions.
- Match voice commands with inventory products.
- Handle ambiguous commands.

Example: "Add 5 chocolates."

If multiple chocolates exist, display matching products with their prices and available stock for selection.

- Integrate voice commands with the existing billing cart.
- Support adding, removing, and updating cart items through voice.

**5. Daily Reports**
- Total daily sales.
- Number of transactions.
- Best-selling products.
- Inventory status.
- Low-stock alerts.

### P2 – Demonstration Features

**6. Barcode Integration**
- Implement sample barcode input.
- Retrieve matching products from inventory.
- Add identified products to the billing cart.

**7. CCTV / Computer Vision**
- Support sample video uploads.
- Detect people and activity in defined regions.
- Demonstrate entry and counter activity analysis.
- Display approximate activity summaries.
- Compare activity estimates with transaction records.

Note: CCTV analysis must not automatically modify inventory.

## 3. Implementation Sequence

1. Product database and sample dataset.
2. Inventory CRUD operations.
3. Billing cart and calculations.
4. Checkout and automatic stock updates.
5. Transaction history.
6. Voice recognition and command extraction.
7. Product matching and ambiguity resolution.
8. Daily reports and dashboard.
9. Barcode demonstration.
10. CCTV video analysis.

## 4. Important Development Rules

- Backend must be the source of truth for inventory and transactions.
- Voice AI must not directly modify the database.
- All billing methods must use the same cart and checkout logic.
- Stock must never become negative.
- Transactions and inventory updates must remain consistent.
- Avoid unnecessary AI complexity before core functionality works.

## 5. Current Milestone – Definition of Done

The first major milestone is achieved when:

1. Products are available in inventory.
2. Shopkeeper can say "Add 5 chocolates."
3. System displays matching products.
4. Shopkeeper selects the correct product.
5. Selected products appear in the billing cart.
6. System calculates the bill.
7. Shopkeeper confirms the transaction.
8. Inventory updates automatically.
9. Transaction appears in history.
10. Daily sales report reflects the transaction.

## 6. Immediate Focus

**Start with inventory management and the product dataset.**

Do not prioritize CCTV, barcode hardware, or advanced AI models until inventory, billing, and transaction management work reliably.

keep my core feature with ai based voice recognition