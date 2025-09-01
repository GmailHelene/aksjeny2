const { Favorite } = require('../models'); // Example model import

async function getUserFavorites(userId) {
    // Replace with your actual DB query
    return await Favorite.findAll({ where: { userId } });
}

router.get('/', async (req, res) => {
    if (!req.user) {
        return res.redirect('/login');
    }
    
    // Fetch user data and favorites
    const userData = await getUserData(req.user.id);
    const favorites = await getUserFavorites(req.user.id);

    res.render('profile', {
        title: 'Min Profil - Aksjeradar',
        user: userData,
        favorites,
        csrfToken: req.csrfToken()
    });
});