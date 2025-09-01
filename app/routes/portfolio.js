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
        const portfolios = await getUserPortfolios(req.user.id); // Make sure this returns an array, not null
        res.render('portfolio', { portfolios });
    } catch (err) {
        console.error(err);
        res.status(500).render('error', { error: "Teknisk feil ved lasting av portefølje." });
    }
});

router.post('/:id/add', async (req, res) => {
    try {
        const { symbol, amount } = req.body;
        if (!symbol || !amount) {
            return res.status(400).json({ success: false, error: "Ugyldig input." });
        }
        await addStockToPortfolio(req.params.id, symbol, amount, req.user.id);
        const updatedPortfolio = await getPortfolio(req.params.id, req.user.id);
        if (!updatedPortfolio) {
            return res.status(404).json({ success: false, error: "Portefølje ikke funnet." });
        }
        res.json({ success: true, portfolio: updatedPortfolio });
    } catch (err) {
        console.error(err);
        res.status(500).json({ success: false, error: "Teknisk feil ved lasting av portefølje." });
    }
});

router.post('/create', async (req, res) => {
    try {
        const { name } = req.body;
        if (!name) {
            return res.status(400).json({ success: false, error: "Navn på portefølje mangler." });
        }
        const portfolio = await createPortfolio(req.user.id, name);
        if (!portfolio || !portfolio.id) {
            return res.status(500).json({ success: false, error: "Kunne ikke opprette portefølje." });
        }
        res.json({ success: true, portfolio });
    } catch (err) {
        console.error(err);
        res.status(500).json({ success: false, error: "Teknisk feil." });
    }
});

module.exports = router;