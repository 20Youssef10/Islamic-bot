# 🚀 Deploy Islamic Bot on Render

This guide will help you deploy the Islamic Discord Bot on Render.com for **24/7 hosting**.

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Create Discord Bot](#create-discord-bot)
3. [Deploy on Render](#deploy-on-render)
4. [Environment Variables](#environment-variables)
5. [Keep Alive Configuration](#keep-alive-configuration)
6. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

Before you start, make sure you have:
- [ ] Discord account
- [ ] GitHub account (or GitLab/Bitbucket)
- [ ] Render account (free tier available)
- [ ] Bot source code uploaded to Git

---

## 🤖 Step 1: Create Discord Bot

### 1.1 Create a New Application
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Name it: `Islamic Bot` (or any name you prefer)
4. Click **"Create"**

### 1.2 Get Bot Token
1. In your application, go to **"Bot"** tab (left sidebar)
2. Click **"Add Bot"** → **"Yes, do it!"**
3. Under **"Token"** section, click **"Copy"** 
   - ⚠️ **Keep this token secret!** Never share it

### 1.3 Enable Privileged Intents
1. In the **"Bot"** tab, scroll to **"Privileged Gateway Intents"**
2. Enable:
   - ✅ **MESSAGE CONTENT INTENT**
   - ✅ **SERVER MEMBERS INTENT**
   - ✅ **PRESENCE INTENT**
3. Click **"Save Changes"**

### 1.4 Invite Bot to Your Server
1. Go to **"OAuth2"** → **"URL Generator"**
2. Select scopes:
   - ✅ **bot**
   - ✅ **applications.commands**
3. Select Bot Permissions:
   - ✅ **Administrator** (or minimum required)
4. Copy the generated URL
5. Open URL in browser and invite to your server

---

## 🌐 Step 2: Prepare Your Code

### 2.1 Update Files

Make sure these files are in your repository:

```
islamic-bot/
├── bot/
│   ├── __init__.py
│   ├── commands.py
│   └── discord_client.py
├── services/
│   ├── __init__.py
│   ├── hourly_messages_service.py
│   └── ... (all services)
├── db/
│   ├── __init__.py
│   ├── database.py
│   └── models.py
├── data/
│   └── (database files)
├── main.py
├── web_server.py          ← NEW! Keep alive server
├── requirements.txt       ← Updated with Flask
├── render.yaml           ← Render configuration
├── .env                  ← Environment variables (don't commit!)
└── .gitignore
```

### 2.2 Create .env File (Local Testing)

Create a `.env` file in your project root (DO NOT commit this to Git!):

```env
DISCORD_TOKEN=your_discord_bot_token_here
GUILD_ID=your_discord_server_id_here
```

### 2.3 Create .gitignore

```gitignore
# Environment variables
.env
.env.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Database
*.db
*.db-journal
data/*.db
data/*.db-journal

# Logs
*.log
logs/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

---

## 🚀 Step 3: Deploy on Render

### 3.1 Sign Up / Log In
1. Go to [Render.com](https://render.com)
2. Sign up with GitHub (recommended) or email
3. Verify your email

### 3.2 Create New Web Service

1. Click **"New"** → **"Web Service"**
2. Connect your GitHub/GitLab repository
3. Select the repository containing your bot
4. Click **"Connect"**

### 3.3 Configure Service

Fill in the form:

| Field | Value |
|-------|-------|
| **Name** | `islamic-bot` (or your preferred name) |
| **Environment** | `Python 3` |
| **Region** | Choose closest to you (e.g., Frankfurt for EU) |
| **Branch** | `main` (or your default branch) |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python main.py` |
| **Plan** | `Free` |

### 3.4 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these variables:

1. **DISCORD_TOKEN**
   - Key: `DISCORD_TOKEN`
   - Value: `Your_Discord_Bot_Token_From_Step_1`

2. **GUILD_ID** (Optional but recommended)
   - Key: `GUILD_ID`
   - Value: `Your_Discord_Server_ID`
   - To get this: Right-click your server in Discord → "Copy Server ID" (enable Developer Mode first)

### 3.5 Deploy

1. Click **"Create Web Service"**
2. Render will start building your bot
3. Wait for the build to complete (2-3 minutes)
4. Check the **Logs** tab for any errors

---

## 🔧 Step 4: Keep Alive Configuration

The bot includes a Flask web server that:
- ✅ Keeps the bot alive on Render
- ✅ Provides a status dashboard
- ✅ Responds to health checks

### Web Server Features:

- **Dashboard**: `https://your-service-name.onrender.com/`
- **Health Check**: `https://your-service-name.onrender.com/health`
- **API Status**: `https://your-service-name.onrender.com/api/status`

### URLs (after deployment):

Replace `islamic-bot` with your service name:

```
🌐 Dashboard:    https://islamic-bot.onrender.com/
💓 Health Check: https://islamic-bot.onrender.com/health
📊 API Status:   https://islamic-bot.onrender.com/api/status
🔍 Ping Test:    https://islamic-bot.onrender.com/ping
```

---

## 🔍 Step 5: Verify Deployment

### 5.1 Check Logs

In Render dashboard:
1. Go to your service
2. Click **"Logs"** tab
3. You should see:
   ```
   ✅ Web server started on http://0.0.0.0:10000
   ✅ Logged in as YourBot#1234
   ```

### 5.2 Test in Discord

1. Go to your Discord server
2. Type: `/help`
3. Bot should respond with command list

### 5.3 Test Web Dashboard

1. Open: `https://your-service-name.onrender.com/`
2. You should see the Islamic Bot status page
3. Status should show: **"متصل - Online"**

---

## ⚙️ Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_TOKEN` | ✅ Yes | Your Discord bot token |
| `GUILD_ID` | ❌ No | Your Discord server ID |
| `PYTHON_VERSION` | ❌ No | Python version (default: 3.12) |

---

## 🔧 Troubleshooting

### Issue 1: Bot shows "Offline"
**Solution:**
1. Check logs in Render dashboard
2. Verify `DISCORD_TOKEN` is correct
3. Make sure bot has required intents enabled
4. Redeploy after fixing

### Issue 2: "Module not found" error
**Solution:**
```bash
# Update requirements.txt
pip freeze > requirements.txt

# Or manually add missing packages
echo "package-name" >> requirements.txt
```

### Issue 3: Bot stops after some time
**Solution:**
- On Render free tier, services spin down after 15 minutes of inactivity
- The web server keeps it alive for HTTP requests
- Discord bot will reconnect automatically

### Issue 4: Database errors
**Solution:**
```python
# Make sure data directory exists
import os
os.makedirs('data', exist_ok=True)
```

### Issue 5: Web server not starting
**Solution:**
1. Check if Flask is in requirements.txt
2. Verify web_server.py exists
3. Check main.py imports web_server

---

## 📊 Render Free Tier Limitations

| Feature | Limit |
|---------|-------|
| **Web Services** | 1 free service |
| **Build Minutes** | 500 minutes/month |
| **Bandwidth** | 100 GB/month |
| **Disk** | 512 MB |
| **Sleep** | Spins down after 15 min inactivity |
| **Uptime** | Not guaranteed (best effort) |

**Note:** The bot will automatically wake up when:
- Someone visits the web dashboard
- Discord sends events to the bot
- Scheduled jobs run

---

## 🔄 Updating Your Bot

### Method 1: Auto-deploy (Recommended)
1. Push changes to GitHub
2. Render automatically deploys
3. Check "Deploys" tab for status

### Method 2: Manual Deploy
1. Go to Render dashboard
2. Click "Manual Deploy" → "Deploy latest commit"

---

## 🌟 Optional: Custom Domain

### Add Custom Domain (Paid Feature)
1. Go to your service settings
2. Click "Custom Domain"
3. Add your domain
4. Follow DNS configuration instructions

---

## 📚 Useful Links

- [Render Documentation](https://render.com/docs)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Discord Developer Portal](https://discord.com/developers/applications)

---

## ✅ Deployment Checklist

Before considering your deployment complete:

- [ ] Discord bot created and token copied
- [ ] Bot invited to server with proper permissions
- [ ] Code pushed to GitHub
- [ ] Render service created
- [ ] Environment variables set (DISCORD_TOKEN)
- [ ] Service deployed successfully
- [ ] Logs show bot is online
- [ ] `/help` command works in Discord
- [ ] Web dashboard loads correctly
- [ ] Health check endpoint responds
- [ ] Hourly messages scheduled (if enabled)

---

## 🎉 Success!

Your Islamic Bot is now running 24/7 on Render! 

**What's working:**
- ✅ Discord bot commands
- ✅ Scheduled azkar (6 AM & 6 PM)
- ✅ Hourly random messages
- ✅ Complete Quran (/mushaf)
- ✅ Web dashboard
- ✅ Health monitoring

**Next Steps:**
1. Share your bot with friends
2. Invite to more servers
3. Customize commands
4. Add more features

---

## 🆘 Need Help?

If you encounter issues:

1. Check Render logs first
2. Verify all environment variables
3. Test locally before deploying
4. Check Discord bot permissions
5. Review this guide again

**جزاك الله خيراً!** (May Allah reward you!)

---

**Last Updated:** 2024
**Version:** 3.0
**Author:** Islamic Bot Team
