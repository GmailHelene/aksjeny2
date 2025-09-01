```javascript
const express = require('express');
const router = express.Router();
const { getWatchlist, addStockToWatchlist, getUserWatchlists } = require('../services/watchlistService');
const { getAIInsightsForWatchlist, getMarketTrendsForWatchlist } = require('../services/analyticsService');
const { Watchlist, WatchlistStock, AIInsight, MarketTrend } = require('../models'); // Example model import

async function addStockToWatchlist(watchlistId, symbol, userId) {
    // Replace with your actual DB query
    return await WatchlistStock.create({ watchlistId, symbol, userId });
}

async function getWatchlist(watchlistId, userId) {
    // Replace with your actual DB query
    return await Watchlist.findOne({
        where: { id: watchlistId, userId },
        include: [WatchlistStock]
    });
}

async function getAIInsightsForWatchlist(watchlistId) {
    // Replace with your actual DB query
    return await AIInsight.findAll({ where: { watchlistId } });
}

async function getMarketTrendsForWatchlist(watchlistId) {
    // Replace with your actual DB query
    return await MarketTrend.findAll({ where: { watchlistId } });
}

async function getUserWatchlists(userId) {
    return await Watchlist.findAll({ where: { userId } });
}

// Add stock to watchlist
router.post('/:id/add', async (req, res) => {
    try {
        const { symbol } = req.body;
        await addStockToWatchlist(req.params.id, symbol, req.user.id); // Implement real add
        const updatedList = await getWatchlist(req.params.id, req.user.id); // Fetch updated list
        res.json({ success: true, watchlist: updatedList });
    } catch (err) {
        res.status(500).json({ success: false, error: "Teknisk feil." });
    }
});

// Get watchlist details
router.get('/:id', async (req, res) => {
    try {
        const watchlist = await getWatchlist(req.params.id, req.user.id);
        const aiInsights = await getAIInsightsForWatchlist(req.params.id); // Implement real AI insights
        const marketTrends = await getMarketTrendsForWatchlist(req.params.id); // Implement real market trends
        res.render('watchlist_detail', {
            watchlist,
            aiInsights,
            marketTrends
        });
    } catch (err) {
        res.status(500).render('error', { error: "Teknisk feil." });
    }
});

// Get all watchlists for user
router.get('/', async (req, res) => {
    try {
        const lists = await getUserWatchlists(req.user.id);
        res.render('watchlists', { lists });
    } catch (err) {
        res.status(500).render('error', { error: "Teknisk feil." });
    }
});

module.exports = router;
```