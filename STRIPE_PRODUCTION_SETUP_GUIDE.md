# Stripe Production Setup Guide

## Dette dokumentet forklarer hvordan du setter opp Stripe for produksjon

### 1. Opprett Stripe-konto
1. Gå til https://dashboard.stripe.com/register
2. Opprett en ny konto eller logg inn på eksisterende konto
3. Aktiver Live-modus når du er klar for produksjon

### 2. Hent API-nøkler
1. Gå til Stripe Dashboard > Developers > API keys
2. Kopier følgende nøkler:
   - **Publishable key**: `pk_live_...` (kan være offentlig)
   - **Secret key**: `sk_live_...` (må holdes hemmelig!)

⚠️ **VIKTIG**: Live-mode secret key vises kun EN gang. Lagre den trygt!

### 3. Opprett produkter og priser
1. Gå til Dashboard > More > Product catalog
2. Klikk "+Add product"
3. Opprett to produkter:

#### Månedlig abonnement:
- Navn: "Månedlig abonnement"
- Beskrivelse: "399 NOK per måned" 
- Pricing model: Flat-rate pricing > Recurring
- Pris: 399 NOK
- Billing period: Monthly
- Noter ned Price ID (format: `price_xxxxx`)

#### Årlig abonnement:
- Navn: "Årlig abonnement"  
- Beskrivelse: "2999 NOK per år"
- Pricing model: Flat-rate pricing > Recurring
- Pris: 2999 NOK
- Billing period: Yearly  
- Noter ned Price ID (format: `price_xxxxx`)

### 4. Sett miljøvariabler på Railway

Kjør følgende kommandoer i terminalen (erstatt med dine faktiske verdier):

```bash
# Logg inn på Railway
railway login

# Sett Stripe API-nøkler
railway variables set STRIPE_SECRET_KEY="sk_live_din_secret_key_her"
railway variables set STRIPE_PUBLIC_KEY="pk_live_din_public_key_her"

# Sett Price IDs for abonnementene
railway variables set STRIPE_MONTHLY_PRICE_ID="price_din_monthly_price_id"
railway variables set STRIPE_YEARLY_PRICE_ID="price_din_yearly_price_id"

# Valgfritt: Webhook secret (hvis du bruker webhooks)
railway variables set STRIPE_WEBHOOK_SECRET="whsec_din_webhook_secret"
```

### 5. Test konfigurasjonen

Etter deployment, test at betalingslenkene fungerer:
1. Gå til /pricing på nettsiden
2. Klikk på "Velg månedlig" eller "Velg årlig"
3. Du skal bli redirected til Stripe Checkout
4. Test med Stripe test-kort: 4242 4242 4242 4242

### 6. Sikkerhetstips

- Aldri commit Stripe secret keys til Git
- Bruk sterke passord på Stripe-kontoen
- Aktiver to-faktor autentisering på Stripe
- Overvåk transaksjoner regelmessig

### Feilsøking

Hvis betalingslenkene ikke fungerer:
1. Sjekk at miljøvariablene er riktig satt på Railway
2. Kontroller at Price IDs er korrekte i Stripe Dashboard
3. Se i applikasjonslogs for feilmeldinger
4. Verifiser at Stripe er i Live-modus (ikke Test-modus)

### Webhook konfigurering (valgfritt)

For å motta betalingsbekreftelser:
1. Gå til Stripe Dashboard > Developers > Webhooks
2. Klikk "Add endpoint"
3. URL: `https://ditt-domene.com/stripe/webhook`
4. Velg events: `checkout.session.completed`
5. Kopier webhook secret til `STRIPE_WEBHOOK_SECRET`

---

**Kontakt support hvis du trenger hjelp med Stripe-konfigurering!**
