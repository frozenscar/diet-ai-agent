const { Pool } = require('pg');
const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3002;
const cors = require('cors');
app.use(cors());


// Middleware
app.use(cors());
app.use(bodyParser.json());

const pool = new Pool({
    user: 'postgres1',      // Replace with your PostgreSQL username
    host: 'localhost',         // Default is usually 'localhost'
    database: 'mydatabase',  // Replace with your database name
    password: 'postgres',  // Replace with your PostgreSQL password
    port: 5432,                // Default PostgreSQL port
  });

// Route to add food
app.post('/add-food', async (req, res) => {
    const { food, time, type } = req.body;
    try {
        const query = 'INSERT INTO diet (food, time, type) VALUES ($1, $2, $3) RETURNING *';
        const values = [food, time, type];
        const result = await pool.query(query, values);
        res.json({ success: true, data: result.rows[0] });
    } catch (err) {
        console.error(err);
        res.status(500).json({ success: false, message: 'Error inserting data into database' });
    }
});

// Route to get all food data
app.get('/get-food', async (req, res) => {
    try {
        const query = 'SELECT * FROM diet ORDER BY time DESC';
        const result = await pool.query(query);
        res.json({ success: true, data: result.rows });
    } catch (err) {
        console.error(err);
        res.status(500).json({ success: false, message: 'Error fetching data from database' });
    }
});

// Route to update food
app.put('/update-food/:id', async (req, res) => {
    const { id } = req.params;
    const { food, time, type } = req.body;
    try {
        const query = 'UPDATE diet SET food = $1, time = $2, type = $3 WHERE id = $4 RETURNING *';
        const values = [food, time, type, id];
        const result = await pool.query(query, values);
        if (result.rows.length === 0) {
            res.status(404).json({ success: false, message: 'Food item not found' });
        } else {
            res.json({ success: true, data: result.rows[0] });
        }
    } catch (err) {
        console.error(err);
        res.status(500).json({ success: false, message: 'Error updating data in database' });
    }
});

// Route to delete food
app.delete('/delete-food/:id', async (req, res) => {
    const { id } = req.params;
    try {
        const query = 'DELETE FROM diet WHERE id = $1 RETURNING *';
        const result = await pool.query(query, [id]);
        if (result.rows.length === 0) {
            res.status(404).json({ success: false, message: 'Food item not found' });
        } else {
            res.json({ success: true, data: result.rows[0] });
        }
    } catch (err) {
        console.error(err);
        res.status(500).json({ success: false, message: 'Error deleting data from database' });
    }
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});