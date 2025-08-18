# Streamlit Cloud Deployment Guide

## 🚀 Quick Start Deployment

This guide explains how to deploy the Shopify Bulk Importer to Streamlit Cloud for easy access without local installation.

## Prerequisites

1. **GitHub Account** - For hosting the code
2. **Streamlit Cloud Account** - Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **Shopify API Credentials** - From your Shopify admin panel

## Step 1: Prepare GitHub Repository

### Option A: Fork This Repository
1. Fork this repository to your GitHub account
2. Make sure the repository is either public or you have Streamlit Cloud connected to your GitHub

### Option B: Create New Repository
1. Create a new private/public repository on GitHub
2. Push this code to your repository:
```bash
git remote add origin https://github.com/yourusername/shopify-bulk-importer.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Streamlit Cloud

1. **Login to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app" button
   - Select your repository
   - Branch: `main`
   - Main file path: `streamlit_app.py`

3. **Configure Secrets**
   - Click on "Advanced settings" before deploying
   - Go to "Secrets" section
   - Add your Shopify credentials:
   ```toml
   SHOPIFY_API_KEY = "your-api-key-here"
   SHOPIFY_API_SECRET = "your-api-secret-here"
   SHOPIFY_ACCESS_TOKEN = "your-access-token-here"
   SHOPIFY_SHOP_DOMAIN = "your-shop.myshopify.com"
   ```

4. **Deploy**
   - Click "Deploy" button
   - Wait for the app to build and deploy (3-5 minutes)
   - You'll get a URL like: `https://your-app-name.streamlit.app`

## Step 3: Share with Your Team

Once deployed, share the URL with your team members. They can access the app directly from any browser without installation.

### Access Control (Optional)
- In Streamlit Cloud settings, you can set viewer email addresses
- This restricts access to only authorized users

## 📝 Important Notes

### Data Security
- All API credentials are stored securely in Streamlit Cloud secrets
- Never commit credentials to GitHub
- Use `.gitignore` to exclude `.env` files

### File Storage
- Uploaded files (CSV/Excel) are temporary and not persisted
- Cache files are stored temporarily during session
- For permanent storage, consider integrating cloud storage

### Performance
- Free tier supports up to 1GB memory
- Suitable for teams up to 50 concurrent users
- For larger deployments, consider Streamlit Cloud Team/Enterprise plans

### Updating the App
1. Push changes to GitHub:
```bash
git add .
git commit -m "Update features"
git push origin main
```
2. Streamlit Cloud automatically redeploys within minutes

## 🔧 Troubleshooting

### App Won't Start
- Check logs in Streamlit Cloud dashboard
- Verify all dependencies in `requirements.txt`
- Ensure secrets are correctly formatted

### API Connection Issues
- Verify Shopify credentials in secrets
- Check API rate limits
- Ensure shop domain format is correct (without https://)

### Import Errors
- Verify products data format matches templates
- Check browser console for JavaScript errors
- Clear browser cache if UI issues persist

## 🎯 Benefits for Office Use

✅ **Zero Installation** - Access from any computer with a browser
✅ **Always Updated** - Latest version automatically deployed
✅ **Centralized Access** - Same URL for entire team
✅ **No Dependencies** - No Python, pip, or package conflicts
✅ **Secure** - API keys stored securely in cloud
✅ **Scalable** - Handles multiple users simultaneously

## 📧 Support

For issues or questions:
1. Check app logs in Streamlit Cloud dashboard
2. Review this documentation
3. Contact your system administrator

---

**Note**: This deployment method is ideal for internal tools with moderate usage. For production e-commerce operations with high volume, consider dedicated hosting solutions.