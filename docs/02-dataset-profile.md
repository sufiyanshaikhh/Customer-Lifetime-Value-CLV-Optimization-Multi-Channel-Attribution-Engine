Deliverables:
    Acquire data from heterogeneous operational systems.
    Design a normalized relational database with enforced referential integrity.
    Build an integrated Customer 360 analytical database.
    Create a reusable data pipeline for downstream analytics and machine learning.

Business entities (Normalized operational schema):
    Master Data:
    Customers - Stores information about each customer.
    Purpose - Demographics and acquisition details
    Products - Demonstrates each and every product in each purchase.
    Purpose - Category and product performance
    Core Transaction Tables:
    Orders - Demonstrates each and every purchase made.
    Purpose - Revenue, purchase history, CLV
    Order Details - Demonstrates total no of products in each purchases.
    Purpose - Product-level analysis
    Customer Interaction Tables:
    Marketing Touchpoints - Every interaction with the customer before actual conversion.
    Purpose - Attribution modeling
    Website Sessions - Represents browsing sessions before purchases, specific for attributions.
    Purpose - Customer journey analysis
    Email campaign - Tracks customer interactions with email campaigns.
    Purpose - Retention and remarketing analysis
    Refunds, Customer support - Tracks returned orders, specific for predicting customers likely to churn.

Data Acquistion from Operational systems:
    CRM → Customer information
    ERP → Orders and inventory
    Product catalog → Product metadata
    Marketing platforms → Campaign and advertising data
    Web analytics → User sessions and traffic
    Email platform → Engagement metrics

Data Integration:
    Customers
    │
    ├─────────────── customer_id ───────────────┐
    │                                           │
Orders                                Marketing Touchpoints
    │                                           │
order_id                                   customer_id
    │                                           │
Order Items                               Website Sessions
    │                                           │
product_id                                 Email Events
    │
Products

customer_id serves as a primary business key to correlate between different tables

Customer 360 view:
                  Customer Dataset
                         │
                         │
                    customer_id
                         │
 ┌──────────────┬────────┴────────┬──────────────┐
 │              │                 │              │
Orders      Marketing       Website        Email Events
Dataset      Dataset        Sessions         Dataset
 │              │                 │              │
 └──────────────┴────────┬────────┴──────────────┘
                         │
                    Customer Journey
                         │
                         ▼
               Unified Analytics Database
                         │
      ┌──────────────────┼─────────────────┐
      │                  │                 │
 CLV Prediction   Attribution Model   Customer Segmentation

 Dataset Stack:
    Source - Olist E-commerce, Purpose - Customers, Orders, Products, Payments, Reviews
    Source - Olist Marketing Funnel, Purpose - Lead acquisition and sales funnel
    Source - Google Analytics Sample / GA4-style sessions, Purpose - Website sessions and traffic sources
    Source - Synthetic Email Campaign Dataset, Purpose - Email opens, clicks, conversions
    Source - Synthetic Digital Ads Dataset, Purpose - Campaign spend, impressions, CTR, CPC