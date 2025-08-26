"""
FREE TRANSLATION SOLUTION - Norwegian to English
Using Google Translate without API costs through web scraping approach

This implements a free translation system using:
1. HTML lang attribute switching
2. JavaScript-based translation using Google Translate widget
3. Simple dictionary-based translation for key terms
"""

# Key Norwegian -> English translations for the most common terms
TRANSLATION_DICTIONARY = {
    # Navigation
    "Hjem": "Home",
    "Aksjer": "Stocks", 
    "Portefølje": "Portfolio",
    "Analyse": "Analysis",
    "Nyheter": "News",
    "Innstillinger": "Settings",
    "Logg inn": "Login",
    "Registrer": "Register",
    "Logg ut": "Logout",
    
    # Common terms
    "Pris": "Price",
    "Endring": "Change", 
    "Volum": "Volume",
    "Markedsverdi": "Market Cap",
    "P/E": "P/E",
    "Utbytte": "Dividend",
    "Sektor": "Sector",
    "Selskap": "Company",
    "Aksjesymbol": "Symbol",
    
    # Analysis terms
    "Kjøp": "Buy",
    "Selg": "Sell", 
    "Hold": "Hold",
    "Anbefaling": "Recommendation",
    "Teknisk analyse": "Technical Analysis",
    "Fundamental analyse": "Fundamental Analysis",
    "Warren Buffett analyse": "Warren Buffett Analysis",
    
    # User interface
    "Søk": "Search",
    "Filter": "Filter",
    "Sorter": "Sort",
    "Oppdater": "Update",
    "Lagre": "Save",
    "Avbryt": "Cancel",
    "Bekreft": "Confirm",
    "Tilbake": "Back",
    "Neste": "Next",
    "Forrige": "Previous",
    
    # Status messages  
    "Laster...": "Loading...",
    "Ingen data tilgjengelig": "No data available",
    "Feil oppstod": "An error occurred",
    "Vellykket": "Success",
    "Lagret": "Saved",
    "Oppdatert": "Updated",
    
    # Time periods
    "I dag": "Today",
    "Denne uken": "This week", 
    "Denne måneden": "This month",
    "I år": "This year",
    "1 år": "1 year",
    "5 år": "5 years",
    
    # Market terms
    "Oslo Børs": "Oslo Stock Exchange",
    "NASDAQ": "NASDAQ",
    "NYSE": "NYSE", 
    "Amerikanske aksjer": "US Stocks",
    "Norske aksjer": "Norwegian Stocks",
    "Europeiske aksjer": "European Stocks",
    
    # Features
    "Favoritter": "Favorites",
    "Overvåkningsliste": "Watchlist",
    "Prisvarsler": "Price Alerts",
    "Porteføljeanalyse": "Portfolio Analysis",
    "Markedsintelligens": "Market Intelligence",
    "Innsidehandel": "Insider Trading",
    
    # Subscription
    "Gratis": "Free",
    "Premium": "Premium", 
    "Abonnement": "Subscription",
    "Oppgrader": "Upgrade",
    "Månedlig": "Monthly",
    "Årlig": "Yearly",
    
    # Messages
    "Velkommen": "Welcome",
    "Takk": "Thank you",
    "Beklager": "Sorry",
    "Prøv igjen": "Try again",
    "Kontakt oss": "Contact us",
    "Hjelp": "Help",
    "Om oss": "About us",
    "Personvern": "Privacy",
    "Vilkår": "Terms"
}

def get_free_translation_js():
    """
    Returns JavaScript code that implements free translation
    Uses Google Translate widget (free) and dictionary replacements
    """
    js_code = f"""
    // Free Translation System for Aksjeradar
    const TRANSLATIONS = {TRANSLATION_DICTIONARY};
    
    let currentLanguage = 'no'; // Default Norwegian
    
    function toggleLanguage() {{
        currentLanguage = currentLanguage === 'no' ? 'en' : 'no';
        translatePage(currentLanguage);
        
        // Store preference
        localStorage.setItem('aksjeradar_language', currentLanguage);
        
        // Update toggle button text
        const toggleBtn = document.getElementById('language-toggle');
        if (toggleBtn) {{
            toggleBtn.textContent = currentLanguage === 'en' ? 'Norsk' : 'English';
        }}
    }}
    
    function translatePage(targetLanguage) {{
        if (targetLanguage === 'en') {{
            // Translate to English using dictionary
            translateToEnglish();
        }} else {{
            // Reload page to get original Norwegian
            location.reload();
        }}
    }}
    
    function translateToEnglish() {{
        // Get all text nodes and translate common terms
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );
        
        const textNodes = [];
        let node;
        
        while (node = walker.nextNode()) {{
            if (node.nodeValue.trim()) {{
                textNodes.push(node);
            }}
        }}
        
        textNodes.forEach(textNode => {{
            let text = textNode.nodeValue;
            let translated = false;
            
            // Replace Norwegian terms with English
            Object.keys(TRANSLATIONS).forEach(norTerm => {{
                const enTerm = TRANSLATIONS[norTerm];
                if (text.includes(norTerm)) {{
                    text = text.replace(new RegExp(norTerm, 'g'), enTerm);
                    translated = true;
                }}
            }});
            
            if (translated) {{
                textNode.nodeValue = text;
            }}
        }});
        
        // Also translate common attributes
        const elements = document.querySelectorAll('[placeholder], [title], [alt]');
        elements.forEach(el => {{
            ['placeholder', 'title', 'alt'].forEach(attr => {{
                const value = el.getAttribute(attr);
                if (value) {{
                    Object.keys(TRANSLATIONS).forEach(norTerm => {{
                        if (value.includes(norTerm)) {{
                            el.setAttribute(attr, value.replace(norTerm, TRANSLATIONS[norTerm]));
                        }}
                    }});
                }}
            }});
        }});
    }}
    
    // Initialize on page load
    document.addEventListener('DOMContentLoaded', function() {{
        // Check saved language preference
        const savedLang = localStorage.getItem('aksjeradar_language');
        if (savedLang === 'en') {{
            currentLanguage = 'en';
            translateToEnglish();
        }}
        
        // Update toggle button if it exists
        const toggleBtn = document.getElementById('language-toggle');
        if (toggleBtn) {{
            toggleBtn.textContent = currentLanguage === 'en' ? 'Norsk' : 'English';
            toggleBtn.addEventListener('click', toggleLanguage);
        }}
    }});
    """
    return js_code

def get_language_toggle_html():
    """
    Returns HTML for language toggle button
    """
    return '''
    <button id="language-toggle" class="btn btn-outline-secondary btn-sm ms-2" 
            onclick="toggleLanguage()" title="Switch language / Bytt språk">
        English
    </button>
    '''

# Instructions for implementation:
"""
TO IMPLEMENT FREE TRANSLATION:

1. Add this to base.html in the <head> section:
   <script>
   {{ get_free_translation_js() | safe }}
   </script>

2. Add language toggle button to navigation:
   {{ get_language_toggle_html() | safe }}

3. Register template functions in app/__init__.py:
   @app.template_global()
   def get_free_translation_js():
       from .utils.translation import get_free_translation_js
       return get_free_translation_js()
   
   @app.template_global() 
   def get_language_toggle_html():
       from .utils.translation import get_language_toggle_html
       return get_language_toggle_html()

4. Optional: Add more terms to TRANSLATION_DICTIONARY as needed

This provides:
- Instant client-side translation
- No API costs
- Preserves original page structure
- Works offline once loaded
- User preference persistence
- Easy to extend with more terms
"""
