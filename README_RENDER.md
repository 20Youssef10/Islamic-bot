# 🚀 Quick Render Deployment

## One-Click Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## Manual Steps

### 1. Prepare Your Repository

Make sure your repository has these files:
```
├── main.py                 # Main bot + Flask server
├── web_server.py          # Keep-alive web server
├── requirements.txt       # Dependencies including Flask
├── render.yaml           # Render configuration
├── bot/                  # Bot commands
├── services/             # All services
├── db/                   # Database models
└── data/                 # Database storage
```

### 2. Required Files Content

#### requirements.txt
```
discord.py==2.4.0
python-dotenv==1.0.0
Flask==3.0.0
Werkzeug==3.0.1
requests==2.32.3
APScheduler==3.10.4
numpy==1.26.0
scikit-learn==1.3.2
```

#### render.yaml
```yaml
services:
  - type: web
    name: islamic-bot
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    envVars:
      - key: DISCORD_TOKEN
        sync: false
      - key: GUILD_ID
        sync: false
    healthCheckPath: /health
```

### 3. Environment Variables

Set these in Render dashboard:

1. **DISCORD_TOKEN**
   - Get from: https://discord.com/developers/applications
   - Your bot's token

2. **GUILD_ID** (Optional)
   - Your Discord server ID
   - Right-click server → Copy ID

### 4. URLs After Deployment

Replace `islamic-bot` with your service name:

| URL | Description |
|-----|-------------|
| `https://islamic-bot.onrender.com/` | Status Dashboard |
| `https://islamic-bot.onrender.com/health` | Health Check |
| `https://islamic-bot.onrender.com/ping` | Ping Test |
| `https://islamic-bot.onrender.com/api/status` | API Status |

### 5. Features

✅ **Web Dashboard** - Beautiful status page
✅ **Keep Alive** - Flask server prevents sleep
✅ **Health Checks** - /health endpoint for monitoring
✅ **Auto-restart** - Bot reconnects automatically
✅ **Logs** - View logs in Render dashboard

### 6. Troubleshooting

**Bot shows offline:**
- Check DISCORD_TOKEN is correct
- Check bot has proper intents enabled

**Service sleeps:**
- Normal on free tier after 15 min
- Will wake up on HTTP request
- Bot stays connected to Discord

**Build fails:**
- Check requirements.txt syntax
- Check Python version (3.12+ recommended)

## 📖 Full Guide

See [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md) for detailed instructions.

## 🌟 Bot Features

- 88+ Discord commands
- Complete Quran (114 Surahs, 6236 Ayahs)
- Hourly random messages
- Prayer times & Qibla direction
- Ramadan, Hajj & Umrah guides
- Sunnah collection
- And much more!

---

**Ready to deploy?** Click the button above! 🚀
