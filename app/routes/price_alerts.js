const express = require('express');
const router = express.Router();
const { PriceAlert } = require('../models'); // Example model import

async function createPriceAlert(userId, symbol, price, direction) {
    // Replace with your actual DB query
    return await PriceAlert.create({ userId, symbol, price, direction });
}

// @route   POST api/alerts/create
// @desc    Create a price alert
// @access  Private
router.post('/create', async (req, res) => {
    try {
        const { symbol, price, direction } = req.body;
        // Validate input
        if (!symbol || !price || !direction) {
            return res.status(400).json({ success: false, error: "Ugyldig input." });
        }
        // Create alert in DB
        const alert = await createPriceAlert(req.user.id, symbol, price, direction);
        if (!alert || !alert.id) {
            return res.status(500).json({ success: false, error: "Kunne ikke opprette prisvarsel." });
        }
        res.json({ success: true, alert });
    } catch (err) {
        console.error(err);
        res.status(500).json({ success: false, error: "Teknisk feil - kontakt support hvis problemet vedvarer." });
    }
});

// @route   GET api/alerts/settings
// @desc    Render settings page for price alerts
// @access  Private
router.get('/settings', (req, res) => {
    res.render('price_alert_settings');
});

module.exports = router;