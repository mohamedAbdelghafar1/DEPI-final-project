CREATE TABLE Recommendations (
    user_id INT,
    product_id INT,
    score FLOAT,
    recommended_at DATETIME DEFAULT GETDATE(),
    PRIMARY KEY (user_id, product_id)
);