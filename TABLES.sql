
CREATE TABLE Staff (
    staffID INT UNIQUE NOT NULL PRIMARY KEY,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    restaurantRole VARCHAR(50),
    salary DECIMAL(10, 2),
    yearsWorked INT,
    email VARCHAR(100),
    phoneNumber BIGINT,
    streetNo INT,
    streetName VARCHAR(100),
    city VARCHAR(50),
    province VARCHAR(50),
    zip VARCHAR(10),
    supervisor INT,
   FOREIGN KEY (supervisor) REFERENCES Staff(staffID)
);

CREATE TABLE Customer (
   customerID INT UNIQUE NOT NULL PRIMARY KEY,
   firstName VARCHAR(50),
   lastName VARCHAR(50),
   phoneNumber BIGINT,
   email VARCHAR(100)
);
 
-- Create RestaurantTable table with servedBy as foreign key
-- servedBy is a reference to the staff serving the table
CREATE TABLE RestaurantTable (
    tableNumber INT UNIQUE NOT NULL PRIMARY KEY,
    zone INT NOT NULL,
    style VARCHAR(30) NOT NULL,
    tableStatus VARCHAR(30),
    servedBy INT,
    FOREIGN KEY (servedBy) REFERENCES Staff(staffID)
);
 
-- Create RestaurantOrder relation (used to be called just “order”)
-- order, hence price, needs to be derived from the sum of price of all menuitems in that order (stored in orderDetails with orderID of this order)
-- along with calories, needs to be a sum of all calories in every item ordered
CREATE TABLE RestaurantOrder (
    orderID INT UNIQUE NOT NULL PRIMARY KEY,
    dateTime DATETIME,
    orderStatus VARCHAR(50),
    calories INT,
    price DECIMAL(10, 2),
    customerID INT,
    tableNumber INT,
    FOREIGN KEY (customerID) REFERENCES Customer(customerID),
    FOREIGN KEY (tableNumber) REFERENCES RestaurantTable(tableNumber)
);

-- Referencing RestaurantOrder instead of Order (renamed)
CREATE TABLE OrderAlterations (
    orderID INT UNIQUE PRIMARY KEY,
    alterationsDetails TINYTEXT,
    FOREIGN KEY (orderID) REFERENCES RestaurantOrder(orderID)
);

CREATE TABLE MenuItem (
    itemName VARCHAR(30) UNIQUE NOT NULL PRIMARY KEY,
    category VARCHAR(20),
    alcoholic BOOLEAN,
    calories INT,
    price DEC(8,2),
    revenue DEC(8,2),
    orderOccurances INT
);

-- Menu item subclass made into {mandatory and}
CREATE TABLE MenuItemDetails (
    itemName VARCHAR(30) UNIQUE NOT NULL PRIMARY KEY,
    allergens VARCHAR(150),
    dietaryRestrictions VARCHAR(150),
    preparation VARCHAR(150),
    FOREIGN KEY (itemName) REFERENCES MenuItem(itemName) ON DELETE CASCADE
);

CREATE TABLE Inventory (
    itemName VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,
    category VARCHAR(50),
    quantityInStock INT,
    unitPrice DEC (8, 2),
    supplier TEXT,
    expirationDate VARCHAR(50)
);
 
-- Foreign key referencing MenuItem(name)
-- Foreign key referencing RestaurantOrder(orderID)
CREATE TABLE OrderDetails (
    item VARCHAR(255) NOT NULL, 
    orderID INT NOT NULL, 
    quantity INT,
    PRIMARY KEY (item, orderID),
    FOREIGN KEY (orderID) REFERENCES RestaurantOrder(orderID),
    FOREIGN KEY (item) REFERENCES MenuItem(itemName)
);

-- Foreign key referencing MenuItem(name)
-- Foreign key referencing Inventory(itemName)
CREATE TABLE RecipeDetails (
    item VARCHAR(255) NOT NULL, 
    ingredient VARCHAR(255) NOT NULL, 
    measurement VARCHAR(255),
    PRIMARY KEY (item, ingredient),
    FOREIGN KEY (item) REFERENCES MenuItem(itemName),
    FOREIGN KEY (ingredient) REFERENCES Inventory(itemName)
);

-- InventorySeasonal subclass of Inventory
CREATE TABLE InventorySeasonal (
    itemName VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,
    season VARCHAR(50),
    FOREIGN KEY (itemName) REFERENCES Inventory(itemName)
);
