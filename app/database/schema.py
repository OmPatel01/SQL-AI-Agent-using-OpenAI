from app.database.connection import DatabaseConnection

def get_schema_as_text():
    """
    Get the database schema as a formatted text with detailed descriptions.
    This will be used to provide context to the LLM.
    """
    schema_text = """
    BikeStores Database Schema:
    
    Table: production_brands
    Description: Contains bicycle brand information
    Columns:
      - brand_id (INT) PRIMARY KEY: Unique identifier for each brand
      - brand_name (VARCHAR) NOT NULL: Name of the bicycle brand
    
    Table: production_categories
    Description: Contains bicycle category classifications
    Columns:
      - category_id (INT) PRIMARY KEY: Unique identifier for each category
      - category_name (VARCHAR) NOT NULL: Name of the bicycle category (e.g., Mountain, Road, etc.)
    
    Table: production_products
    Description: Contains information about bicycle products
    Columns:
      - product_id (INT) PRIMARY KEY: Unique identifier for each product
      - product_name (VARCHAR) NOT NULL: Name of the bicycle product
      - brand_id (INT) NOT NULL: Foreign key referencing brands.brand_id
      - category_id (INT) NOT NULL: Foreign key referencing categories.category_id
      - model_year (SMALLINT) NOT NULL: Year the product model was introduced
      - list_price (DECIMAL) NOT NULL: Standard list price of the product
    Foreign Keys:
      - brand_id references production.brands(brand_id)
      - category_id references production.categories(category_id)
    
    Table: sales_customers
    Description: Contains customer information
    Columns:
      - customer_id (INT) PRIMARY KEY: Unique identifier for each customer
      - first_name (VARCHAR) NOT NULL: Customer's first name
      - last_name (VARCHAR) NOT NULL: Customer's last name
      - phone (VARCHAR): Customer's phone number
      - email (VARCHAR) NOT NULL: Customer's email address
      - street (VARCHAR): Customer's street address
      - city (VARCHAR): Customer's city
      - state (VARCHAR): Customer's state
      - zip_code (VARCHAR): Customer's zip code
    
    Table: sales_stores
    Description: Contains store location information
    Columns:
      - store_id (INT) PRIMARY KEY: Unique identifier for each store
      - store_name (VARCHAR) NOT NULL: Name of the store
      - phone (VARCHAR): Store's phone number
      - email (VARCHAR): Store's email address
      - street (VARCHAR): Store's street address
      - city (VARCHAR): Store's city
      - state (VARCHAR): Store's state
      - zip_code (VARCHAR): Store's zip code
    
    Table: sales_staffs
    Description: Contains staff information for each store
    Columns:
      - staff_id (INT) PRIMARY KEY: Unique identifier for each staff member
      - first_name (VARCHAR) NOT NULL: Staff's first name
      - last_name (VARCHAR) NOT NULL: Staff's last name
      - email (VARCHAR) NOT NULL: Staff's email address
      - phone (VARCHAR): Staff's phone number
      - active (TINYINT) NOT NULL: Flag indicating if staff is active (1) or not (0)
      - store_id (INT) NOT NULL: Foreign key referencing stores.store_id
      - manager_id (INT): Foreign key referencing staffs.staff_id for manager
    Foreign Keys:
      - store_id references sales.stores(store_id)
      - manager_id references sales.staffs(staff_id)
    
    Table: sales_orders
    Description: Contains customer order information
    Columns:
      - order_id (INT) PRIMARY KEY: Unique identifier for each order
      - customer_id (INT): Foreign key referencing customers.customer_id
      - order_status (TINYINT) NOT NULL: Order status: 1=Pending, 2=Processing, 3=Rejected, 4=Completed
      - order_date (DATE) NOT NULL: Date the order was placed
      - required_date (DATE) NOT NULL: Date the customer requested the order to be delivered
      - shipped_date (DATE): Date the order was shipped (NULL if not shipped yet)
      - store_id (INT) NOT NULL: Foreign key referencing stores.store_id where order was placed
      - staff_id (INT) NOT NULL: Foreign key referencing staffs.staff_id who made the sale
    Foreign Keys:
      - customer_id references sales.customers(customer_id)
      - store_id references sales.stores(store_id)
      - staff_id references sales.staffs(staff_id)
    
    Table: sales_order_items
    Description: Contains line items for each order
    Columns:
      - order_id (INT): Part of composite primary key, foreign key referencing orders.order_id
      - item_id (INT): Part of composite primary key, represents the line number in the order
      - product_id (INT) NOT NULL: Foreign key referencing products.product_id
      - quantity (INT) NOT NULL: Quantity of the product ordered
      - list_price (DECIMAL) NOT NULL: Price of the product at the time of order
      - discount (DECIMAL) NOT NULL: Discount applied to the product (percentage)
    Primary Key: (order_id, item_id)
    Foreign Keys:
      - order_id references sales.orders(order_id)
      - product_id references production.products(product_id)
    
    Table: production_stocks
    Description: Contains inventory information
    Columns:
      - store_id (INT): Part of composite primary key, foreign key referencing stores.store_id
      - product_id (INT): Part of composite primary key, foreign key referencing products.product_id
      - quantity (INT): Current quantity in stock at the specified store
    Primary Key: (store_id, product_id)
    Foreign Keys:
      - store_id references sales.stores(store_id)
      - product_id references production.products(product_id)
    
    Common Relationships:
    - Customers make Orders
    - Orders contain Order Items
    - Order Items reference Products
    - Products belong to Brands and Categories
    - Stores have Staff members
    - Stores maintain Stock of Products
    """
    
    return schema_text