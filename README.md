This project was developed with flask app.

## `Structure`

It's Transformer Toy Collection store.
It includes home,collection,login,signup,cart pages.

### `Database`

-- Toy table
CREATE TABLE toy (
id serial PRIMARY KEY,
name text NOT NULL,
image_url_1 text,
image_url_2 text,
qty integer,
price integer NOT NULL
);

-- Users table
CREATE TABLE users (
id serial PRIMARY KEY,
username text NOT NULL UNIQUE,
password_hash text NOT NULL,
address text NOT NULL
);
