\c suppliers

CREATE TABLE vendors (
    id UUID PRIMARY KEY,
    qualification CHAR(1) NOT NULL
);

CREATE TABLE products (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    required_qualification CHAR(1)
);

CREATE TABLE transactions (
    id UUID,
    product_id UUID REFERENCES products(id),
    vendor_id UUID REFERENCES vendors(id),
    action VARCHAR(50) NOT NULL,
    quantity INT NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id, product_id)
);
