# Secure the login

## Description

NovaCorp's internal employee portal uses a simple username and password login. The development team shipped it fast - maybe too fast. Lock it down without breaking access for legitimate users.

https://defense.dalctf2026.com/

## Solution Walkthrough

It can be seen that the `username` and `password` were originally concatenated directly into the query statement, which poses a risk of SQL injection:

```js
const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
const result = await pool.query(query);
```

So switching to a parameterized query fixed the issue.

```js
const express = require('express');
const { Pool } = require('pg');

const app = express();
app.use(express.json());

const pool = new Pool({
  host: 'database',
  user: 'testuser',
  password: 'testpass',
  database: 'testdb',
  port: 5432
});

async function initDB() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      username VARCHAR(50) UNIQUE NOT NULL,
      password VARCHAR(100) NOT NULL
    )
  `);

  const adminUser = process.env.ADMIN_USERNAME;
  const adminPass = process.env.ADMIN_PASSWORD;

  await pool.query(
    `INSERT INTO users (username, password) VALUES ($1, $2) ON CONFLICT (username) DO NOTHING`,
    [adminUser, adminPass]
  );
}

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.post('/login', async (req, res) => {
  const { username, password } = req.body;

  try {
    const query = `SELECT * FROM users WHERE username = $1 AND password = $2`;
    const result = await pool.query(query, [username, password]);

    if (result.rows.length > 0) {
      res.json({ success: true, message: 'Login successful' });
    } else {
      res.status(401).json({ success: false, message: 'Invalid credentials' });
    }
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

const PORT = 3000;
app.listen(PORT, async () => {
  await initDB();
  console.log(`Server running on port ${PORT}`);
});
```

## Flag

```text
dalctf{3asy_P3asy_SQL_1nj3ction}
```
