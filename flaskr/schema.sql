DROP TABLE IF EXISTS userAccount;
DROP TABLE IF EXISTS bankAccount;

CREATE TABLE userAccount (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  phoneNumber INTEGER,
  firstName TEXT NOT NULL,
  lastName TEXT NOT NULL
);

CREATE TABLE bankAccount (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userAccount_id INTEGER NOT NULL,
  amount DECIMAL(16,2) NOT NULL,
  FOREIGN KEY (userAccount_id) REFERENCES userAccount (id)
);