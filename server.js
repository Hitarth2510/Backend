const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

// Initialize Express
const app = express();
app.use(cors());
app.use(express.json());

// MongoDB connection string (replace with your actual connection string)
const uri = 'mongodb://localhost:27017/';

// Connect to MongoDB
mongoose.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('Connected to MongoDB'))
    .catch(err => console.error('Failed to connect to MongoDB', err));

// Create a schema and model for gunshot data
const gunshotSchema = new mongoose.Schema({
    timestamp: { type: String, required: true },
    direction: { type: Number, required: true }
});

const GunshotData = mongoose.model('GunshotData', gunshotSchema);

// API route to fetch the latest gunshot direction
app.get('/gunshot-direction', async (req, res) => {
    try {
        // Fetch the latest entry (sorted by timestamp)
        const latestData = await GunshotData.findOne().sort({ timestamp: -1 });
        if (latestData) {
            res.json(latestData);
        } else {
            res.status(404).json({ error: 'No gunshot data found' });
        }
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch data' });
    }
});

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
