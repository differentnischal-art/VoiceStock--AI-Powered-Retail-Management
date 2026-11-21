# PRD – Smart Retail Management System

## 1. Project Overview

An AI-powered retail management system designed for Samita Liquor & General Store to automate inventory management, billing, transaction tracking, and daily business reporting.

The system combines voice-based interaction, inventory automation, and computer vision to reduce manual work and improve shop management.

## 2. Problem Statement

Small retail shops often depend on manual billing and inventory tracking, leading to stock inaccuracies, billing errors, time consumption, and difficulty monitoring daily sales.

## 3. Core Features

### 3.1 Inventory Management
- Add, update, delete, and search products.
- Manage product categories, prices, and stock.
- Automatically update inventory after successful sales.
- Display low-stock alerts.

### 3.2 Voice-Based Billing
- Accept natural voice commands from the shopkeeper.
- Extract product names, quantities, and actions.
- Identify matching products from inventory.
- Display multiple options when product names are ambiguous.
- Add selected products to the billing cart.
- Calculate bills automatically.

### 3.3 Transaction Management
- Record every completed transaction.
- Maintain product-wise purchase details.
- Store transaction date, quantity, and total amount.
- Maintain transaction history.

### 3.4 Daily Business Reports
- Display total daily sales.
- Show number of transactions.
- Identify best-selling products.
- Display inventory status and low-stock products.

### 3.5 CCTV-Based Activity Analysis
- Upload sample CCTV videos for analysis.
- Use computer vision to detect people and activity around defined areas.
- Generate approximate entry and counter activity summaries.
- Compare activity estimates with transaction records.

### 3.6 Barcode Demonstration
- Support sample barcode input.
- Retrieve matching products from inventory.
- Add identified products to the billing cart.

## 4. Technology Stack

- **Frontend:** Next.js / React
- **Backend:** Python FastAPI
- **Database:** SQLite / PostgreSQL
- **AI:** Speech-to-Text, NLP / LLM
- **Computer Vision:** OpenCV and object detection models
- **ORM:** SQLAlchemy

## 5. Current Development Constraints

- No direct CCTV access; sample video uploads will be used.
- No physical barcode scanner; barcode functionality will be demonstrated using sample inputs.
- Inventory and voice-based billing are the primary development priorities.

## 6. MVP Development Priority

1. Inventory management and product dataset.
2. Billing cart and automatic stock updates.
3. Transaction history.
4. Voice-based billing and product matching.
5. Daily sales reports.
6. Barcode demonstration.
7. CCTV video analysis prototype.

## 7. Expected Outcome

A functional AI-assisted retail management platform that allows shopkeepers to manage inventory, process sales using voice commands, maintain accurate transaction records, and monitor daily business performance through automated reports.