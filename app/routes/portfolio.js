const { Router } = require('express');
const router = Router();
const { Portfolio, PortfolioStock } = require('../models'); // Example model import

async function getUserPortfolios(userId) {
    return await Portfolio.findAll({ where: { userId } });
}

async function addStockToPortfolio(portfolioId, symbol, amount, userId) {
    return await PortfolioStock.create({ portfolioId, symbol, amount, userId });
}

async function getPortfolio(portfolioId, userId) {
    return await Portfolio.findOne({
        where: { id: portfolioId, userId },
        include: [PortfolioStock]
    });
}

async function createPortfolio(userId, name) {
    return await Portfolio.create({ userId, name });
}

router.get('/', async (req, res) => {
    try {
        const portfolios = await getUserPortfolios(req.user.id);
        res.render('portfolio', { portfolios });
    } catch (err) {
        res.status(500).render('error', { error: "Teknisk feil." });
    }
});

router.post('/:id/add', async (req, res) => {
    try {
        const { symbol, amount } = req.body;
        await addStockToPortfolio(req.params.id, symbol, amount, req.user.id); // Implement real add
        const updatedPortfolio = await getPortfolio(req.params.id, req.user.id);
        res.json({ success: true, portfolio: updatedPortfolio });
    } catch (err) {
        res.status(500).json({ success: false, error: "Teknisk feil." });
    }
});

router.post('/create', async (req, res) => {
    try {
        const { name } = req.body;
        const portfolio = await createPortfolio(req.user.id, name); // Implement real creation
        if (!portfolio) {
            return res.status(400).json({ success: false, error: "Kunne ikke opprette portefølje." });
        }
        res.json({ success: true, portfolio });
    } catch (err) {
        res.status(500).json({ success: false, error: "Teknisk feil." });
    }
});

module.exports = router;