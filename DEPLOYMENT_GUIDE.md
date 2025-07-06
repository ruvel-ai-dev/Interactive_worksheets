# Deployment Guide - AI Worksheet Converter

## Custom Domain Deployment on Replit

### Step 1: Deploy on Replit
1. Click the **Deploy** button in your Replit interface
2. Choose **Autoscale Deployments** for production traffic
3. Configure your deployment settings:
   - **Name**: ai-worksheet-converter
   - **Build Command**: (leave empty - Flask app auto-detected)
   - **Run Command**: gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app

### Step 2: Configure Custom Domain
1. In your deployment dashboard, go to **Domains**
2. Click **Add Custom Domain**
3. Enter your domain (e.g., `worksheetconverter.com`)
4. Replit will provide DNS records to configure

### Step 3: DNS Configuration
Add these records to your domain provider (GoDaddy, Namecheap, etc.):

```
Type: CNAME
Name: @ (or your subdomain)
Value: [provided by Replit]
TTL: 300
```

For subdomains like `app.yourdomain.com`:
```
Type: CNAME  
Name: app
Value: [provided by Replit]
TTL: 300
```

### Step 4: Environment Variables for Production
Set these in your Replit deployment:

**Required:**
- `OPENAI_API_KEY`: Your OpenAI API key
- `STRIPE_SECRET_KEY`: Your Stripe secret key
- `SESSION_SECRET`: Random secure string
- `DATABASE_URL`: PostgreSQL connection string (Replit provides this)

**Optional (for email verification):**
- `MAIL_SERVER`: smtp.gmail.com
- `MAIL_PORT`: 587
- `MAIL_USE_TLS`: true
- `MAIL_USERNAME`: your-email@gmail.com
- `MAIL_PASSWORD`: your-app-password
- `MAIL_DEFAULT_SENDER`: noreply@yourdomain.com

### Step 5: SSL Certificate
Replit automatically provides SSL certificates for custom domains. Your site will be accessible via HTTPS within 24 hours of DNS propagation.

### Step 6: Production Checklist
- [ ] Domain DNS records configured
- [ ] Environment variables set
- [ ] Email sending configured (optional)
- [ ] Stripe webhook endpoints updated to new domain
- [ ] Test all functionality on new domain

### Monitoring & Scaling
- **Autoscaling**: Automatically handles traffic spikes
- **Monitoring**: Built-in logs and metrics in Replit dashboard
- **Database**: Managed PostgreSQL with automatic backups
- **Uptime**: 99.9% SLA with Replit's infrastructure

### Cost Estimation
- **Replit Autoscale**: $0.35/hour when running + resource usage
- **Custom Domain**: Free with Replit deployment
- **Database**: Included with deployment
- **SSL Certificate**: Free with custom domain

### Common Issues & Solutions

**DNS Propagation Delay**
- Wait up to 48 hours for global DNS propagation
- Use `nslookup yourdomain.com` to check status

**Email Not Sending**
- Verify SMTP credentials
- Check Gmail app password (not regular password)
- Ensure "Less secure app access" is enabled

**Stripe Webhooks**
- Update webhook URLs to point to new domain
- Test webhook endpoints after deployment

### Support
For deployment issues:
- Replit Documentation: docs.replit.com
- Replit Discord: replit.com/discord
- Email Support: support@replit.com