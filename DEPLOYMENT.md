# Deployment Guide

## 🚀 Quick Deploy to Railway (Recommended - Best for Dash Apps)

### Why Railway?
- Works perfectly with Dash applications
- Fast deployment (2 minutes)
- $5 free credit/month (~500 hours)
- No cold starts, better performance
- Auto-detects your Procfile

### Steps

1. **Go to Railway**
   - Visit [railway.app](https://railway.app)
   - Sign in with your GitHub account

2. **Deploy**
   - Click **"New Project"**
   - Select **"Deploy from GitHub repo"**
   - Choose **`Market_Simulation`** from the list
   - Railway auto-detects Python and starts deploying

3. **Configure (Auto-detected)**
   - Railway automatically uses your `Procfile`
   - Python version from `runtime.txt`
   - Dependencies from `requirements.txt`

4. **Get Your URL**
   - Click "Settings" → "Networking" → "Generate Domain"
   - Your app will be live at: `https://market-simulation.up.railway.app`

**That's it!** Railway handles everything automatically.

---

## Alternative: Deploy to Render (Free)

### Prerequisites

- GitHub account
- Render account (free signup at render.com)

### Steps

1. **Push to GitHub**

```bash
cd /Users/asiftauhid/Desktop/market_simulation

# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit - Wealth Inequality Simulation"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/market_simulation.git
git branch -M main
git push -u origin main
```

2. **Deploy on Render**

- Go to [render.com](https://render.com) and sign up/login
- Click **"New +"** → **"Web Service"**
- Connect your GitHub account
- Select your `market_simulation` repository
- Render will auto-detect the `render.yaml` file
- Click **"Create Web Service"**
- Wait 2-3 minutes for build and deployment

3. **Access Your App**

Your app will be live at: `https://wealth-inequality-sim.onrender.com`

**Note**: Free tier may spin down after 15 min of inactivity (takes ~30 sec to wake up).

---

## Alternative: Railway

1. **Deploy**

- Go to [railway.app](https://railway.app)
- Sign up/login with GitHub
- Click **"New Project"** → **"Deploy from GitHub repo"**
- Select `market_simulation`
- Railway auto-detects Python and uses `Procfile`
- Deploys automatically!

2. **Get URL**

Railway provides a URL like: `https://market-simulation-production.up.railway.app`

---

## Alternative: Heroku (Paid - $5/month minimum)

1. **Install Heroku CLI**

```bash
brew tap heroku/brew && brew install heroku  # Mac
# Or download from heroku.com
```

2. **Deploy**

```bash
heroku login
heroku create wealth-inequality-sim
git push heroku main
heroku open
```

---

## Local Development

Run locally:

```bash
python app_wealth_inequality.py
```

Open: `http://localhost:8050`

---

## Environment Variables

Optional environment variables for deployment:

- `PORT`: Port to run on (auto-set by hosting platforms)
- `DEBUG`: Set to `true` for debug mode (default: `false`)

---

## Troubleshooting

### App won't start

- Check logs on hosting platform
- Verify all dependencies in `requirements.txt`
- Ensure Python 3.11 is specified

### Slow performance

- Free tiers have limited resources
- Consider upgrading to paid tier if needed
- Reduce default simulation speed in UI

### Connection timeout

- Free tier may sleep after inactivity
- First request takes 30-60 seconds to wake up
- Subsequent requests are fast

---

## Cost

- **Render Free**: $0/month (with sleep after inactivity)
- **Railway Free Trial**: $5 credit (then pay-as-you-go)
- **Heroku Eco**: $5/month (no sleep)
- **Render Starter**: $7/month (no sleep)

**Recommendation**: Start with Render free tier, upgrade if you need 24/7 availability.
