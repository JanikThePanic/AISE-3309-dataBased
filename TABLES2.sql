-- Staff table
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

-- Customer table
CREATE TABLE Customer (
    customerID INT UNIQUE NOT NULL PRIMARY KEY,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    phoneNumber BIGINT,
    email VARCHAR(100)
);

-- RestaurantTable table
CREATE TABLE RestaurantTable (
    tableNumber INT UNIQUE NOT NULL PRIMARY KEY,
    zone INT NOT NULL,
    style VARCHAR(30) NOT NULL,
    tableStatus VARCHAR(30),
    servedBy INT,
    FOREIGN KEY (servedBy) REFERENCES Staff(staffID)
);

-- RestaurantOrder table
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

-- OrderAlterations table
CREATE TABLE OrderAlterations (
    orderID INT UNIQUE PRIMARY KEY,
    alterationsDetails TINYTEXT,
    FOREIGN KEY (orderID) REFERENCES RestaurantOrder(orderID)
);

-- MenuItem table
CREATE TABLE MenuItem (
    itemName VARCHAR(30) UNIQUE NOT NULL PRIMARY KEY,
    category VARCHAR(20),
    alcoholic BOOLEAN,
    calories INT,
    price DEC(8,2),
    revenue DEC(8,2),
    orderOccurances INT
);

-- MenuItemDetails table
CREATE TABLE MenuItemDetails (
    itemName VARCHAR(30) UNIQUE NOT NULL PRIMARY KEY,
    allergens VARCHAR(150),
    dietaryRestrictions VARCHAR(150),
    preparation VARCHAR(150),
    FOREIGN KEY (itemName) REFERENCES MenuItem(itemName) ON DELETE CASCADE
);

-- Inventory table
CREATE TABLE Inventory (
    itemName VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,
    category VARCHAR(50),
    quantityInStock INT,
    unitPrice DEC (8, 2),
    supplier TEXT,
    expirationDate VARCHAR(50)
);

-- OrderDetails table
CREATE TABLE OrderDetails (
    item VARCHAR(255) NOT NULL, 
    orderID INT NOT NULL, 
    quantity INT,
    PRIMARY KEY (item, orderID),
    FOREIGN KEY (orderID) REFERENCES RestaurantOrder(orderID),
    FOREIGN KEY (item) REFERENCES MenuItem(itemName)
);

-- RecipeDetails table
CREATE TABLE RecipeDetails (
    item VARCHAR(255) NOT NULL, 
    ingredient VARCHAR(255) NOT NULL, 
    measurement VARCHAR(255),
    PRIMARY KEY (item, ingredient),
    FOREIGN KEY (item) REFERENCES MenuItem(itemName),
    FOREIGN KEY (ingredient) REFERENCES Inventory(itemName)
);

-- InventorySeasonal table
CREATE TABLE InventorySeasonal (
    itemName VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,
    season VARCHAR(50),
    FOREIGN KEY (itemName) REFERENCES Inventory(itemName)
);

-- Reservation table
CREATE TABLE Reservation (
    reservationID INT UNIQUE NOT NULL PRIMARY KEY,
    dateTime DATETIME NOT NULL,
    reservationStatus VARCHAR(50) NOT NULL,
    numberOfGuests INT NOT NULL,
    customerID INT NOT NULL,
    FOREIGN KEY (customerID) REFERENCES Customer(customerID)
);

-- ReservationRequests table
CREATE TABLE ReservationRequests (
    reservationID INT NOT NULL,
    specialRequest VARCHAR(255), -- Changed TEXT to VARCHAR(255)
    PRIMARY KEY (reservationID, specialRequest),
    FOREIGN KEY (reservationID) REFERENCES Reservation(reservationID) ON DELETE CASCADE
);

-- Review table
CREATE TABLE Review (
    reviewID INT UNIQUE NOT NULL PRIMARY KEY,
    dateTime DATETIME NOT NULL,
    comment TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    customerID INT NOT NULL,
    FOREIGN KEY (customerID) REFERENCES Customer(customerID)
);
