import random
from faker import Faker
import pandas as pd
import datetime

fake = Faker()

# Define data sizes
NUM_STAFF = 10
NUM_CUSTOMERS = 10
NUM_MENU_ITEMS = 10
NUM_TABLES = 10
NUM_ORDERS = 10
NUM_ORDER_DETAILS = 10
NUM_INVENTORY_ITEMS = 10
NUM_RECIPE_DETAILS = 10
NUM_SEASONAL_ITEMS = 10

# Simulate a starting point for staffID to ensure uniqueness across multiple runs
START_STAFF_ID = 1

# Predefined list of restaurant-specific roles
RESTAURANT_ROLES = [
    "Chef", "Sous Chef", "Line Cook", "Prep Cook", "Dishwasher",
    "Server", "Waiter", "Waitress", "Host", "Hostess", "Bartender",
    "Barback", "Sommelier", "Restaurant Manager", "Shift Manager",
    "Pastry Chef", "Barista", "Busser", "Expeditor", "Food Runner"
]

# Staff table
staff = [{
    "staffID": START_STAFF_ID + i,
    "firstName": fake.first_name(),
    "lastName": fake.last_name(),
    "restaurantRole": random.choice(RESTAURANT_ROLES),  # Restrict roles to predefined list
    "salary": round(random.uniform(30000, 80000), 2),
    "yearsWorked": random.randint(1, 20),
    "email": fake.email(),
    "phoneNumber": str(random.randint(1000000000, 9999999999)),
    "streetNo": random.randint(1, 1000),
    "streetName": fake.street_name()[:100],
    "city": fake.city()[:50],
    "province": fake.state()[:50],
    "zip": fake.zipcode()[:10],
    "supervisor": random.choice([None] + [j for j in range(START_STAFF_ID, START_STAFF_ID + i)])
} for i in range(NUM_STAFF)]


# Customers table
customers = [{
    "customerID": i,
    "firstName": fake.first_name(),
    "lastName": fake.last_name(),
    "phoneNumber": str(random.randint(1000000000, 9999999999)),
    "email": fake.email()
} for i in range(1, NUM_CUSTOMERS + 1)]

# MenuItem table with # Predefined lists for realistic item names based on category
FOOD_ITEMS = [
    "Margherita Pizza", "Cheeseburger", "Caesar Salad", "Spaghetti Carbonara",
    "Grilled Salmon", "Chicken Alfredo", "Beef Tacos", "Vegan Buddha Bowl",
    "Sushi Platter", "BBQ Ribs",
    "Pulled Pork Sandwich", "Pad Thai", "Eggplant Parmesan", "Stuffed Bell Peppers",
    "Shrimp Scampi", "Veggie Burger", "Chicken Parmesan", "Lamb Gyro",
    "Pho Noodle Soup", "Ramen Bowl", "Greek Salad", "Avocado Toast",
    "Fish and Chips", "Steak Frites", "Caprese Salad", "Clam Chowder",
    "Fried Chicken", "Falafel Wrap", "Chili Con Carne", "Miso Soup",
    "Pasta Primavera", "Shakshuka", "Beef Wellington", "Seafood Paella",
    "Vegetable Stir Fry", "Roast Duck", "Pork Schnitzel", "Curry Chicken",
    "Stuffed Cabbage Rolls", "Shepherd's Pie"
]


DRINK_ITEMS = [
    "Coca-Cola", "Orange Juice", "Mojito", "Espresso", "Green Tea",
    "Lemonade", "Margarita", "Latte", "Smoothie", "Iced Coffee",
    "Americano", "Matcha Latte", "Bloody Mary", "Piña Colada", "Hot Chocolate",
    "Milkshake", "Chai Tea", "Cold Brew", "Gin and Tonic", "Whiskey Sour",
    "Rum Punch", "Sangria", "Peach Iced Tea", "Sparkling Water", "Arnold Palmer",
    "Strawberry Lemonade", "Berry Smoothie", "Black Coffee", "Caramel Macchiato",
    "Pineapple Juice", "Tonic Water", "Energy Drink", "Coconut Water",
    "Hot Apple Cider", "Herbal Tea", "Craft Beer", "Red Wine", "White Wine",
    "Vodka Martini", "Mint Julep", "Berry Iced Tea"
]


DESSERT_ITEMS = [
    "Chocolate Cake", "Apple Pie", "Cheesecake", "Tiramisu", "Ice Cream Sundae",
    "Brownies", "Creme Brulee", "Pavlova", "Churros", "Panna Cotta",
    "Macarons", "Lemon Tart", "Carrot Cake", "Banoffee Pie", "Baklava",
    "Peach Cobbler", "Chocolate Mousse", "Rice Pudding", "Black Forest Cake",
    "Cupcakes", "Sticky Toffee Pudding", "Eclairs", "Profiteroles", "Fruit Tart",
    "Cannoli", "Red Velvet Cake", "Coconut Macaroons", "Almond Biscotti",
    "Pumpkin Pie", "Key Lime Pie", "Doughnuts", "Strawberry Shortcake",
    "Chocolate Fondue", "Soufflé", "Mango Sorbet", "Turtle Cheesecake",
    "Raspberry Coulis", "Lava Cake", "Honey Cake", "Angel Food Cake"
]


# Update MenuItem table generation
menu_items = [({
    "itemName": random.choice(
        FOOD_ITEMS if category == 'Food' else
        DRINK_ITEMS if category == 'Drink' else
        DESSERT_ITEMS
    ),
    "category": category,
    "alcoholic": category == 'Drink' and random.choice([True, False]),
    "calories": random.randint(100, 1500),
    "price": round(random.uniform(5, 30), 2),
    "revenue": round(random.uniform(100, 1000), 2),
    "orderOccurances": random.randint(1, 50)
}) for i, category in enumerate(
    [fake.random_element(elements=('Food', 'Drink', 'Dessert')) for _ in range(NUM_MENU_ITEMS)]
)]


# MenuItemDetails table
menu_item_details = [{
    "itemName": item["itemName"],
    "allergens": fake.word()[:150],
    "dietaryRestrictions": fake.word()[:150],
    "preparation": fake.sentence()[:150]
} for item in menu_items]

# Inventory table with restricted expiration date
inventory = [{
    "itemName": f"Inventory_Item_{i}",
    "category": fake.random_element(elements=('Vegetable', 'Meat', 'Beverage')),
    "quantityInStock": random.randint(1, 100),
    "unitPrice": round(random.uniform(1, 50), 2),
    "supplier": fake.company()[:255],
    "expirationDate": (datetime.date.today() + datetime.timedelta(days=random.randint(1, 90))).isoformat()  # Restrict to 3 months
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

# Ensure unique combinations of item and orderID for OrderDetails
unique_order_details = set()
while len(unique_order_details) < NUM_ORDER_DETAILS:
    item = random.choice([m["itemName"] for m in menu_items])
    orderID = random.choice([o["orderID"] for o in orders])
    unique_order_details.add((item, orderID))

order_details = [{
    "item": item,
    "orderID": orderID,
    "quantity": random.randint(1, 5)
} for item, orderID in unique_order_details]

# Ensure unique combinations of item and ingredient for RecipeDetails
unique_recipe_details = set()
while len(unique_recipe_details) < NUM_RECIPE_DETAILS:
    item = random.choice([m["itemName"] for m in menu_items])
    ingredient = random.choice([i["itemName"] for i in inventory])
    unique_recipe_details.add((item, ingredient))

recipe_details = [{
    "item": item,
    "ingredient": ingredient,
    "measurement": fake.word()[:255]
} for item, ingredient in unique_recipe_details]

# Function to generate SQL INSERT statements
def generate_sql_insert_statements(table_name, data):
    sql_statements = []
    for row in data:
        columns = ", ".join(row.keys())
        values = ", ".join(
            f"'{v.replace('\'', '\'\'')}'" if isinstance(v, str) else
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
