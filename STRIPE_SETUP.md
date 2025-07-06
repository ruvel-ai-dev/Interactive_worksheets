# Stripe Setup Guide for Multi-Currency Subscription

## Step 1: Create Stripe Account
1. Go to [stripe.com](https://stripe.com) and create an account
2. Complete account verification
3. Go to your Stripe Dashboard

## Step 2: Create Products with Multiple Currencies

### Create USD Product
1. In Stripe Dashboard → Products → Create Product
2. Name: "AI Worksheet Converter Premium"
3. Description: "Unlimited worksheet conversions and premium features"
4. Pricing model: Recurring
5. Price: $9.99 USD per month
6. Copy the Price ID (starts with `price_`) - this is your USD price ID

### Create GBP Product  
1. Create another product or add pricing to existing product
2. Same product details but set:
3. Price: £7.99 GBP per month
4. Copy the Price ID - this is your GBP price ID

## Step 3: Update Your Application 

Application updated with the real price IDs:

```python
PRICE_IDS = {
    'usd': 'price_1R...',  # USD $9.99/month
    'gbp': 'price_1R...i'   # GBP £7.99/month
}
```

## Step 4: Get Your Secret Key
1. In Stripe Dashboard → Developers → API Keys
2. Copy the "Secret key" (starts with `sk_`)
3. This should already be set in your Replit secrets as `STRIPE_SECRET_KEY`

## Step 5: Test Your Setup
1. Use Stripe's test mode for initial testing
2. Use test card numbers provided by Stripe
3. Test both USD and GBP pricing flows

## Important Notes
- The GBP price (£7.99) is approximately equivalent to $9.99 USD
- Both products should have the same features
- Test mode allows unlimited testing without real charges
- Switch to live mode only when ready for real customers

## Test Card Numbers (Test Mode Only)
- Successful payment: 4242 4242 4242 4242
- Declined payment: 4000 0000 0000 0002
- Use any future expiry date and any 3-digit CVC
