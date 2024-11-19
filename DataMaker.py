import random
from faker import Faker
import pandas as pd
import datetime

fake = Faker()

# Define data sizes
NUM_STAFF = 10
NUM_CUSTOMERS = 15
NUM_MENU_ITEMS = 10
NUM_TABLES = 8
NUM_ORDERS = 20
NUM_ORDER_DETAILS = 25
NUM_INVENTORY_ITEMS = 12
NUM_RECIPE_DETAILS = 15
NUM_SEASONAL_ITEMS = 5

# Simulate a starting point for staffID to ensure uniqueness across multiple runs
START_STAFF_ID = 1

staff = [{
    "staffID": START_STAFF_ID + i,  # Ensure staffID starts from a unique value
    "firstName": fake.first_name(),
    "lastName": fake.last_name(),
    "restaurantRole": fake.job()[:50],
    "salary": round(random.uniform(30000, 80000), 2),
    "yearsWorked": random.randint(1, 20),
    "email": fake.email(),
    "phoneNumber": str(random.randint(1000000000, 9999999999)),  # Converted to string for flexibility
    "streetNo": random.randint(1, 1000),
    "streetName": fake.street_name()[:100],
    "city": fake.city()[:50],
    "province": fake.state()[:50],
    "zip": fake.zipcode()[:10],
    "supervisor": random.choice([None] + [j for j in range(START_STAFF_ID, START_STAFF_ID + i)])  # Valid supervisor IDs only
} for i in range(NUM_STAFF)]

# Customers table
customers = [{
    "customerID": i,
    "firstName": fake.first_name(),
    "lastName": fake.last_name(),
    "phoneNumber": str(random.randint(1000000000, 9999999999)),  # Converted to string
    "email": fake.email()
} for i in range(1, NUM_CUSTOMERS + 1)]

# MenuItem table
menu_items = [{
    "itemName": f"Item_{i}",
    "category": fake.random_element(elements=('Food', 'Drink', 'Dessert')),
    "alcoholic": random.choice([True, False]),
    "calories": random.randint(100, 1500),
    "price": round(random.uniform(5, 30), 2),
    "revenue": round(random.uniform(100, 1000), 2),
    "orderOccurances": random.randint(1, 50)
} for i in range(1, NUM_MENU_ITEMS + 1)]

# MenuItemDetails table
menu_item_details = [{
    "itemName": item["itemName"],
    "allergens": fake.word()[:150],
    "dietaryRestrictions": fake.word()[:150],
    "preparation": fake.sentence()[:150]
} for item in menu_items]

# Inventory table
inventory = [{
    "itemName": f"Inventory_Item_{i}",
    "category": fake.random_element(elements=('Vegetable', 'Meat', 'Beverage')),
    "quantityInStock": random.randint(1, 100),
    "unitPrice": round(random.uniform(1, 50), 2),
    "supplier": fake.company()[:255],
    "expirationDate": fake.date()
} for i in range(1, NUM_INVENTORY_ITEMS + 1)]

# InventorySeasonal table
inventory_seasonal = [{
    "itemName": f"Inventory_Item_{i}",
    "season": fake.random_element(elements=('Winter', 'Spring', 'Summer', 'Fall'))
} for i in range(1, NUM_SEASONAL_ITEMS + 1)]

# RestaurantTable table
restaurant_tables = [{
    "tableNumber": i,
    "zone": random.randint(1, 3),
    "style": fake.random_element(elements=('Booth', 'Standard', 'Bar')),
    "tableStatus": fake.random_element(elements=('Available', 'Occupied')),
    "servedBy": random.choice([s["staffID"] for s in staff])
} for i in range(1, NUM_TABLES + 1)]

# RestaurantOrder table
orders = [{
    "orderID": i,
    "dateTime": fake.date_time_this_year(),
    "orderStatus": fake.random_element(elements=('In Progress', 'Completed', 'Cancelled')),
    "calories": random.randint(500, 2000),
    "price": round(random.uniform(10, 100), 2),
    "customerID": random.choice([c["customerID"] for c in customers]),
    "tableNumber": random.choice([t["tableNumber"] for t in restaurant_tables])
} for i in range(1, NUM_ORDERS + 1)]

# OrderAlterations table
order_alterations = [{
    "orderID": order["orderID"],
    "alterationsDetails": fake.sentence()
} for order in orders]

# OrderDetails table
order_details = [{
    "item": random.choice([m["itemName"] for m in menu_items]),
    "orderID": random.choice([o["orderID"] for o in orders]),
    "quantity": random.randint(1, 5)
} for _ in range(NUM_ORDER_DETAILS)]

# RecipeDetails table
recipe_details = [{
    "item": random.choice([m["itemName"] for m in menu_items]),
    "ingredient": random.choice([i["itemName"] for i in inventory]),
    "measurement": fake.word()[:255]
} for _ in range(NUM_RECIPE_DETAILS)]

# Function to generate SQL INSERT statements
def generate_sql_insert_statements(table_name, data):
    sql_statements = []
    for row in data:
        columns = ", ".join(row.keys())
        values = ", ".join(
            f"'{v}'" if isinstance(v, str) or isinstance(v, pd.Timestamp) else
            f"'{v}'" if isinstance(v, (datetime.date, datetime.datetime)) else
            "NULL" if v is None else
            str(v) for v in row.values()
        )
        sql_statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values});")
    return sql_statements

# Generate SQL insert statements for each table
insert_statements = {
    "Staff": generate_sql_insert_statements("Staff", staff),
    "Customer": generate_sql_insert_statements("Customer", customers),
    "MenuItem": generate_sql_insert_statements("MenuItem", menu_items),
    "MenuItemDetails": generate_sql_insert_statements("MenuItemDetails", menu_item_details),
    "Inventory": generate_sql_insert_statements("Inventory", inventory),
    "InventorySeasonal": generate_sql_insert_statements("InventorySeasonal", inventory_seasonal),
    "RestaurantTable": generate_sql_insert_statements("RestaurantTable", restaurant_tables),
    "RestaurantOrder": generate_sql_insert_statements("RestaurantOrder", orders),
    "OrderAlterations": generate_sql_insert_statements("OrderAlterations", order_alterations),
    "OrderDetails": generate_sql_insert_statements("OrderDetails", order_details),
    "RecipeDetails": generate_sql_insert_statements("RecipeDetails", recipe_details)
}

# Save SQL statements to a file
with open('insert_statements.sql', 'w') as file:
    for table, inserts in insert_statements.items():
        file.write(f"-- Inserting data into {table} table\n")
        for insert in inserts:
            file.write(insert + '\n')
