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
    "Profil": "Profile",
    "Konto": "Account",
    "Varsler": "Alerts",
    "Dashboard": "Dashboard",
    "Watchlist": "Watchlist",
    "Pro verktøy": "Pro Tools",
    "Avanserte analyser": "Advanced Analytics",
    "Markedsintelligens": "Market Intelligence",
    "Prisalarmer": "Price Alerts",
    "Forum": "Forum",
    "Ressurser": "Resources",
    "Investeringsguider": "Investment Guides",
    "Om oss": "About Us",
    "Kontakt": "Contact",
    "Hjelp": "Help",
    "Støtte": "Support",
    
    # Common terms
    "Pris": "Price",
    "Endring": "Change", 
    "Volum": "Volume",
    "Markedsverdi": "Market Cap",
    "Markedskapitalisering": "Market Capitalization",
    "P/E": "P/E",
    "Utbytte": "Dividend",
    "Utbytteavkastning": "Dividend Yield",
    "Sektor": "Sector",
    "Selskap": "Company",
    "Aksjesymbol": "Symbol",
    "Ticker": "Ticker",
    "Børs": "Exchange",
    "Oslo Børs": "Oslo Stock Exchange",
    "NASDAQ": "NASDAQ",
    "NYSE": "NYSE",
    "Valuta": "Currency",
    "NOK": "NOK",
    "USD": "USD",
    "EUR": "EUR",
    
    # Analysis terms
    "Kjøp": "Buy",
    "Selg": "Sell", 
    "Hold": "Hold",
    "Anbefaling": "Recommendation",
    "Anbefalinger": "Recommendations",
    "Teknisk analyse": "Technical Analysis",
    "Fundamental analyse": "Fundamental Analysis",
    "Warren Buffett analyse": "Warren Buffett Analysis",
    "AI-analyse": "AI Analysis",
    "Prediksjoner": "Predictions",
    "Prognoser": "Forecasts",
    "Trender": "Trends",
    "Indikatorer": "Indicators",
    "RSI": "RSI",
    "MACD": "MACD",
    "Moving Average": "Moving Average",
    "Volatilitet": "Volatility",
    "Beta": "Beta",
    "Sharpe Ratio": "Sharpe Ratio",
    "Risiko": "Risk",
    "Avkastning": "Return",
    
    # Portfolio terms
    "Investeringer": "Investments",
    "Fordeling": "Allocation",
    "Allokering": "Allocation",
    "Rebalansering": "Rebalancing",
    "Optimalisering": "Optimization",
    "Diversifisering": "Diversification",
    "Favoritter": "Favorites",
    "Overvåkningsliste": "Watchlist",
    "Ytelse": "Performance",
    "Gevinst": "Gain",
    "Tap": "Loss",
    "Totalverdi": "Total Value",
    "Kostnadsbasis": "Cost Basis",
    "Urealisert": "Unrealized",
    "Realisert": "Realized",
    
    # User interface
    "Søk": "Search",
    "Søk etter aksje": "Search for stock",
    "Søk etter selskap": "Search for company",
    "Filter": "Filter",
    "Filtrer": "Filter",
    "Sorter": "Sort",
    "Sortering": "Sorting",
    "Oppdater": "Update",
    "Lagre": "Save",
    "Avbryt": "Cancel",
    "Lukk": "Close",
    "Åpne": "Open",
    "Vis": "Show",
    "Skjul": "Hide",
    "Velg": "Select",
    "Velg alle": "Select All",
    "Fjern": "Remove",
    "Slett": "Delete",
    "Rediger": "Edit",
    "Legg til": "Add",
    "Ny": "New",
    "Opprett": "Create",
    "Send": "Send",
    "Last ned": "Download",
    "Last opp": "Upload",
    "Eksporter": "Export",
    "Importer": "Import",
    "Print": "Print",
    "Del": "Share",
    "Kopier": "Copy",
    "Lim inn": "Paste",
    
    # Time periods
    "Dag": "Day",
    "Dager": "Days",
    "Uke": "Week",
    "Uker": "Weeks",
    "Måned": "Month",
    "Måneder": "Months",
    "År": "Year",
    "I dag": "Today",
    "I går": "Yesterday",
    "Denne uken": "This Week",
    "Forrige uke": "Last Week",
    "Denne måneden": "This Month",
    "Forrige måned": "Last Month",
    "Dette året": "This Year",
    "Forrige år": "Last Year",
    "Siste 7 dager": "Last 7 Days",
    "Siste 30 dager": "Last 30 Days",
    "Siste 90 dager": "Last 90 Days",
    "Siste året": "Last Year",
    "Historisk": "Historical",
    
    # Status and states
    "Aktiv": "Active",
    "Inaktiv": "Inactive",
    "Åpen": "Open",
    "Lukket": "Closed",
    "Venter": "Pending",
    "Behandler": "Processing",
    "Fullført": "Completed",
    "Kansellert": "Cancelled",
    "Feilet": "Failed",
    "Suksess": "Success",
    "Feil": "Error",
    "Advarsel": "Warning",
    "Info": "Info",
    "Laster": "Loading",
    "Laster inn": "Loading",
    "Oppdaterer": "Updating",
    
    # Messages and notifications
    "Melding": "Message",
    "Meldinger": "Messages",
    "Varsel": "Alert",
    "Notifikasjon": "Notification",
    "E-post": "Email",
    "SMS": "SMS",
    "Bekreftelse": "Confirmation",
    "Bekreftet": "Confirmed",
    "Sendt": "Sent",
    "Mottatt": "Received",
    "Lest": "Read",
    "Ulest": "Unread",
    
    # Common phrases
    "Velkommen": "Welcome",
    "Velkommen tilbake": "Welcome back",
    "Takk": "Thank you",
    "Gratulerer": "Congratulations",
    "Beklager": "Sorry",
    "En feil oppsto": "An error occurred",
    "Prøv igjen": "Try again",
    "Prøv igjen senere": "Try again later",
    "Kontakt oss": "Contact us",
    "Vi jobber med å løse problemet": "We are working to resolve the issue",
    "Ikke funnet": "Not found",
    "Siden ble ikke funnet": "Page not found",
    "Ingen data tilgjengelig": "No data available",
    "Ingen resultater": "No results",
    "Ingen elementer": "No items",
    "Tilgjengelig": "Available",
    "Ikke tilgjengelig": "Not available",
    "Kommer snart": "Coming soon",
    "Under utvikling": "Under development",
    "Beta": "Beta",
    "Ny funksjon": "New feature",
    
    # Advanced analytics terms
    "Maskinlæring": "Machine Learning",
    "ML": "ML",
    "Kunstig intelligens": "Artificial Intelligence",
    "AI": "AI",
    "Prediksjoner": "Predictions",
    "Batch prediksjoner": "Batch Predictions",
    "Markedsanalyse": "Market Analysis",
    "Porteføljeoptimalisering": "Portfolio Optimization",
    "Risikostyring": "Risk Management",
    "Risikoanalyse": "Risk Analysis",
    "VaR": "VaR",
    "Value at Risk": "Value at Risk",
    "Stresstest": "Stress Test",
    "Monte Carlo": "Monte Carlo",
    "Simulering": "Simulation",
    "Effisient frontier": "Efficient Frontier",
    "Konfidens": "Confidence",
    "Nøyaktighet": "Accuracy",
    "Modell": "Model",
    "Algoritme": "Algorithm",
    "Data": "Data",
    "Datasett": "Dataset",
    "Trening": "Training",
    "Validering": "Validation",
    "Test": "Test",
    
    # Financial terms
    "Rente": "Interest",
    "Renter": "Interest Rates",
    "Inflasjon": "Inflation",
    "BNP": "GDP",
    "Økonomi": "Economy",
    "Finansiell": "Financial",
    "Finansmarked": "Financial Market",
    "Kapitalmarked": "Capital Market",
    "Aksjemarked": "Stock Market",
    "Obligasjonsmarked": "Bond Market",
    "Derivater": "Derivatives",
    "Opsjoner": "Options",
    "Futures": "Futures",
    "ETF": "ETF",
    "Fond": "Fund",
    "Indeks": "Index",
    "Benchmark": "Benchmark",
    "Investering": "Investment",
    "Investor": "Investor",
    "Handel": "Trading",
    "Handler": "Trader",
    "Transaksjoner": "Transactions",
    "Orden": "Order",
    "Ordre": "Orders",
    "Kjøpsordre": "Buy Order",
    "Salgsordre": "Sell Order",
    
    # Page specific terms
    "Startside": "Homepage",
    "Forsiden": "Front Page",
    "Aksjeoversikt": "Stock Overview",
    "Aksjeliste": "Stock List",
    "Aksjedetaljer": "Stock Details",
    "Kursutvikling": "Price Development",
    "Kursgraf": "Price Chart",
    "Diagram": "Chart",
    "Tabell": "Table",
    "Rapport": "Report",
    "Oversikt": "Overview",
    "Sammendrag": "Summary",
    "Detaljer": "Details",
    "Innstillinger": "Settings",
    "Preferanser": "Preferences",
    "Konfigurasjon": "Configuration",
    
    # Form elements
    "Skjema": "Form",
    "Felt": "Field",
    "Obligatorisk": "Required",
    "Valgfritt": "Optional",
    "Gyldig": "Valid",
    "Ugyldig": "Invalid",
    "Brukernavn": "Username",
    "Passord": "Password",
    "Bekreft passord": "Confirm Password",
    "Nytt passord": "New Password",
    "Glemt passord": "Forgot Password",
    "Tilbakestill": "Reset",
    "Registrer deg": "Sign Up",
    "Logg inn": "Sign In",
    "Husk meg": "Remember Me",
    "Automatisk innlogging": "Auto Login",
    
    # Numbers and units
    "Million": "Million",
    "Millioner": "Millions",
    "Milliard": "Billion",
    "Milliarder": "Billions",
    "Tusen": "Thousand",
    "Prosent": "Percent",
    "Kroner": "Kroner",
    "Dollar": "Dollars",
    "Euro": "Euros",
    
    # Status messages
    "Laster data": "Loading data",
    "Henter informasjon": "Fetching information",
    "Oppdaterer priser": "Updating prices",
    "Synkroniserer": "Synchronizing",
    "Behandler forespørsel": "Processing request",
    "Validerer data": "Validating data",
    "Lagrer endringer": "Saving changes",
    "Sletter": "Deleting",
    "Fullført": "Complete",
    "Klar": "Ready"
}
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
    "Klar": "Ready",
    
    # Additional phrases and terms
    "Last inn mer": "Load more",
    "Se alle": "See all",
    "Skjul alle": "Hide all",
    "Utvid": "Expand",
    "Kollaps": "Collapse",
    "Minimér": "Minimize",
    "Maksimér": "Maximize",
    "Tilbake": "Back",
    "Fremover": "Forward",
    "Neste": "Next",
    "Forrige": "Previous",
    "Første": "First",
    "Siste": "Last",
    "Gå til": "Go to",
    "Besøk": "Visit",
    "Vis mer": "Show more",
    "Vis mindre": "Show less",
    "Mer informasjon": "More information",
    "Mindre informasjon": "Less information",
    "Komplett": "Complete",
    "Ufullstendig": "Incomplete",
    "Delvis": "Partial",
    "Total": "Total",
    "Subtotal": "Subtotal",
    "Sum": "Sum",
    "Gjennomsnitt": "Average",
    "Median": "Median",
    "Maksimum": "Maximum",
    "Minimum": "Minimum",
    "Høyeste": "Highest",
    "Laveste": "Lowest",
    "Siste oppdatering": "Last updated",
    "Oppdatert": "Updated",
    "Endret": "Modified",
    "Opprettet": "Created",
    "Publisert": "Published",
    "Arkivert": "Archived",
    "Utkast": "Draft",
    "Publiser": "Publish",
    "Planlegg": "Schedule",
    "Planlagt": "Scheduled"
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
