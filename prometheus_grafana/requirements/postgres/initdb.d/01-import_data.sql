-- Create temporary tables to hold CSV data
CREATE TEMP TABLE temp_vendors (
    id UUID,
    qualification CHAR(1)
);

CREATE TEMP TABLE temp_products (
    id UUID,
    name VARCHAR(255),
    price DECIMAL(10, 2),
    quantity INT,
    required_qualification CHAR(1)
);

-- Copy data from CSV files
\copy temp_vendors FROM '/data/vendors.csv' WITH (FORMAT csv, HEADER true);
\copy temp_products FROM '/data/products.csv' WITH (FORMAT csv, HEADER true);

-- Insert data into actual tables
INSERT INTO vendors SELECT * FROM temp_vendors;
INSERT INTO products SELECT * FROM temp_products;

-- Drop temporary tables
DROP TABLE temp_vendors;
DROP TABLE temp_products;
