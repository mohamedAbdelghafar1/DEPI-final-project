CREATE TABLE Products (
    product_id NVARCHAR(50) PRIMARY KEY,
    product_name NVARCHAR(500) NOT NULL,
    category NVARCHAR(255) NOT NULL,
    price FLOAT,
    brand NVARCHAR(255) NOT NULL,
    rating FLOAT,
    reviews_count INT,
    stock_quantity INT,
    image_url NVARCHAR(MAX),
    description NVARCHAR(MAX),
    tags NVARCHAR(MAX),
    created_at DATETIME DEFAULT GETDATE()
);