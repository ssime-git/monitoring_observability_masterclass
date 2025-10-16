TRUNCATE vendors CASCADE;
TRUNCATE products CASCADE;

-- Create a function to import vendors with default qualification
CREATE OR REPLACE FUNCTION import_vendors() RETURNS void AS $$
DECLARE
    vendor_id UUID;
BEGIN
    FOR vendor_id IN 
        SELECT DISTINCT CAST(TRIM(BOTH '"' FROM split_part(line, ',', 1)) AS UUID)
        FROM (SELECT unnest(string_to_array(pg_read_file('/data/vendors.csv'), E'\n')) AS line) AS lines
        WHERE line != 'id,qualification'  -- Skip header
        AND line != ''  -- Skip empty lines
        AND TRIM(BOTH '"' FROM split_part(line, ',', 1)) != ''  -- Skip empty IDs
    LOOP
        INSERT INTO vendors (id, qualification) VALUES (vendor_id, 'C');
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Import vendors
SELECT import_vendors();

-- Import products
COPY products(id, name, price, quantity, required_qualification)
FROM '/data/products.csv'
WITH (FORMAT csv, HEADER true);
