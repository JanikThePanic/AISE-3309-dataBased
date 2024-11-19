import random
from faker import Faker
import pandas as pd
import datetime

fake = Faker()

# Define data sizes
# Adjust these numbers to control the size of each table
NUM_STAFF = 1000
NUM_CUSTOMERS = 1000
NUM_MENU_ITEMS = 1000
NUM_TABLES = 1000
NUM_ORDERS = 1000
NUM_ORDER_DETAILS = 1000
NUM_INVENTORY_ITEMS = 1000
NUM_RECIPE_DETAILS = 1000
NUM_SEASONAL_ITEMS = 1000

# Simulate a starting point for staffID to ensure uniqueness across multiple runs
START_STAFF_ID = 1

# Predefined list of restaurant-specific roles to ensure valid values for 'restaurantRole'
RESTAURANT_ROLES = [
    "Chef", "Sous Chef", "Line Cook", "Prep Cook", "Dishwasher",
    "Server", "Waiter", "Waitress", "Host", "Hostess", "Bartender",
    "Barback", "Sommelier", "Restaurant Manager", "Shift Manager",
    "Pastry Chef", "Barista", "Busser", "Expeditor", "Food Runner"
]

# Generate data for the Staff table
staff = [{
    "staffID": START_STAFF_ID + i,  # Unique identifier for staff
    "firstName": fake.first_name(),  # Random first name
    "lastName": fake.last_name(),  # Random last name
    "restaurantRole": random.choice(RESTAURANT_ROLES),  # Restricted to restaurant-specific roles
    "salary": round(random.uniform(30000, 80000), 2),  # Random salary between 30k and 80k
    "yearsWorked": random.randint(1, 20),  # Random years worked (1 to 20 years)
    "email": fake.email(),  # Random email
    "phoneNumber": str(random.randint(1000000000, 9999999999)),  # Random 10-digit phone number
    "streetNo": random.randint(1, 1000),  # Random street number
    "streetName": fake.street_name()[:100],  # Random street name (truncated to 100 chars)
    "city": fake.city()[:50],  # Random city name (truncated to 50 chars)
    "province": fake.state()[:50],  # Random state name (truncated to 50 chars)
    "zip": fake.zipcode()[:10],  # Random ZIP code (truncated to 10 chars)
    "supervisor": random.choice([None] + [j for j in range(START_STAFF_ID, START_STAFF_ID + i)])  # Supervisor ID
} for i in range(NUM_STAFF)]

# Generate data for the Customers table
customers = [{
    "customerID": i,  # Unique identifier for customers
    "firstName": fake.first_name(),  # Random first name
    "lastName": fake.last_name(),  # Random last name
    "phoneNumber": str(random.randint(1000000000, 9999999999)),  # Random 10-digit phone number
    "email": fake.email()  # Random email
} for i in range(1, NUM_CUSTOMERS + 1)]

# Generate data for the MenuItem table
menu_items = [{
    "itemName": f"Item_{i}",  # Unique item name
    "category": fake.random_element(elements=('Food', 'Drink', 'Dessert')),  # Random category
    "alcoholic": random.choice([True, False]),  # Random boolean for alcoholic items
    "calories": random.randint(100, 1500),  # Random calorie count (100 to 1500)
    "price": round(random.uniform(5, 30), 2),  # Random price (5 to 30)
    "revenue": round(random.uniform(100, 1000), 2),  # Random revenue (100 to 1000)
    "orderOccurances": random.randint(1, 50)  # Random order occurrences
} for i in range(1, NUM_MENU_ITEMS + 1)]

# Generate data for the MenuItemDetails table
menu_item_details = [{
    "itemName": item["itemName"],  # Matches the itemName from MenuItem table
    "allergens": fake.word()[:150],  # Random word for allergens (truncated to 150 chars)
    "dietaryRestrictions": fake.word()[:150],  # Random word for dietary restrictions
    "preparation": fake.sentence()[:150]  # Random sentence for preparation details
} for item in menu_items]

# Generate data for the Inventory table
inventory = [{
    "itemName": f"Inventory_Item_{i}",  # Unique inventory item name
    "category": fake.random_element(elements=('Vegetable', 'Meat', 'Beverage')),  # Random category
    "quantityInStock": random.randint(1, 100),  # Random quantity in stock (1 to 100)
    "unitPrice": round(random.uniform(1, 50), 2),  # Random unit price (1 to 50)
    "supplier": fake.company()[:255],  # Random supplier name (truncated to 255 chars)
    "expirationDate": fake.date()  # Random expiration date
} for i in range(1, NUM_INVENTORY_ITEMS + 1)]

# Generate data for the InventorySeasonal table
inventory_seasonal = [{
    "itemName": f"Inventory_Item_{i}",  # Matches itemName from Inventory table
    "season": fake.random_element(elements=('Winter', 'Spring', 'Summer', 'Fall'))  # Random season
} for i in range(1, NUM_SEASONAL_ITEMS + 1)]

# Generate data for the RestaurantTable table
restaurant_tables = [{
    "tableNumber": i,  # Unique table number
    "zone": random.randint(1, 3),  # Random zone (1 to 3)
    "style": fake.random_element(elements=('Booth', 'Standard', 'Bar')),  # Random style
    "tableStatus": fake.random_element(elements=('Available', 'Occupied')),  # Random status
    "servedBy": random.choice([s["staffID"] for s in staff])  # Random staff ID serving the table
} for i in range(1, NUM_TABLES + 1)]

# Generate data for the RestaurantOrder table
orders = [{
    "orderID": i,  # Unique order ID
    "dateTime": fake.date_time_this_year(),  # Random datetime within the current year
    "orderStatus": fake.random_element(elements=('In Progress', 'Completed', 'Cancelled')),  # Random status
    "calories": random.randint(500, 2000),  # Random calorie count (500 to 2000)
    "price": round(random.uniform(10, 100), 2),  # Random price (10 to 100)
    "customerID": random.choice([c["customerID"] for c in customers]),  # Random customer ID
    "tableNumber": random.choice([t["tableNumber"] for t in restaurant_tables])  # Random table number
} for i in range(1, NUM_ORDERS + 1)]

# Generate unique data for the OrderDetails table
unique_order_details = set()
while len(unique_order_details) < NUM_ORDER_DETAILS:
    item = random.choice([m["itemName"] for m in menu_items])
    orderID = random.choice([o["orderID"] for o in orders])
    unique_order_details.add((item, orderID))

order_details = [{
    "item": item,  # Unique combination of item and orderID
    "orderID": orderID,
    "quantity": random.randint(1, 5)  # Random quantity (1 to 5)
} for item, orderID in unique_order_details]

# Generate unique data for the RecipeDetails table
unique_recipe_details = set()
while len(unique_recipe_details) < NUM_RECIPE_DETAILS:
    item = random.choice([m["itemName"] for m in menu_items])
    ingredient = random.choice([i["itemName"] for i in inventory])
    unique_recipe_details.add((item, ingredient))

recipe_details = [{
    "item": item,  # Unique combination of item and ingredient
    "ingredient": ingredient,
    "measurement": fake.word()[:255]  # Random word for measurement details
} for item, ingredient in unique_recipe_details]

# Function to generate SQL INSERT statements
def generate_sql_insert_statements(table_name, data):
    sql_statements = []
    for row in data:
        columns = ", ".join(row.keys())
        values = ", ".join(
            f"'{v.replace('\'', '\'\'')}'" if isinstance(v, str) else  # Escape single quotes in strings
            f"'{v}'" if isinstance(v, (datetime.date, datetime.datetime)) else
            "NULL" if v is None else
            str(v)
            for v in row.values()
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
    "OrderDetails": generate_sql_insert_statements("OrderDetails", order_details),
    "RecipeDetails": generate_sql_insert_statements("RecipeDetails", recipe_details)
}

# Save SQL statements to a file
with open('insert_statements.sql', 'w') as file:
    for table, inserts in insert_statements.items():
        file.write(f"-- Inserting data into {table} table\n")
        for insert in inserts:
            file.write(insert + '\n')
