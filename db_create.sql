CREATE TABLE breweries
(
    BEER TEXT,
    CATEGORY TEXT,
    ABV INTEGER,
    BREWERY TEXT
);
CREATE UNIQUE INDEX sqlite_autoindex_breweries_1 ON breweries (BEER);
CREATE TABLE products
(
    BEER TEXT,
    PRICE INTEGER,
    QUANTITY INTEGER,
    SIZE INTEGER,
    CONTAINER_TYPE TEXT,
    ID TEXT,
    TIME TEXT DEFAULT 'current_timestamp'
);
CREATE UNIQUE INDEX products_ID_uindex ON products (ID);
