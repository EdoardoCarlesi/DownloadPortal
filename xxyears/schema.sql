DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  code TEXT UNIQUE NOT NULL,
  code_sell BOOLEAN,
  registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS password_reset;

CREATE TABLE password_reset (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL,
  token TEXT UNIQUE NOT NULL,
  expiration TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
