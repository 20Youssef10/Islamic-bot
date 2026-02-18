"""
Web Server for keeping the bot alive on Render
This Flask app provides a health check endpoint
"""

from flask import Flask, jsonify, render_template_string
import threading
import logging
from datetime import datetime

# Disable Flask's default logging to avoid cluttering the bot logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

# Bot status information
bot_status = {
    "status": "starting",
    "started_at": None,
    "commands_count": 0,
    "guilds_count": 0,
    "last_ping": None,
    "version": "3.0"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Islamic Bot - Status</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #333;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 90%;
            text-align: center;
        }
        .logo {
            font-size: 60px;
            margin-bottom: 20px;
        }
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 28px;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }
        .status-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            border-right: 5px solid #667eea;
        }
        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: bold;
            margin: 10px 0;
        }
        .status-online {
            background: #d4edda;
            color: #155724;
        }
        .status-offline {
            background: #f8d7da;
            color: #721c24;
        }
        .status-starting {
            background: #fff3cd;
            color: #856404;
        }
        .pulse {
            width: 12px;
            height: 12px;
            background: #28a745;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(40, 167, 69, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(40, 167, 69, 0); }
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .stat-item {
            background: #e9ecef;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #999;
            font-size: 14px;
        }
        .links {
            margin-top: 20px;
        }
        .links a {
            display: inline-block;
            padding: 10px 20px;
            margin: 5px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            transition: all 0.3s;
        }
        .links a:hover {
            background: #764ba2;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🤖</div>
        <h1>بوت الأدعية والأذكار</h1>
        <p class="subtitle">Islamic Bot for Discord</p>
        
        <div class="status-card">
            <div class="status-indicator status-{{status}}">
                <span class="pulse"></span>
                <span>{{status_text}}</span>
            </div>
            <p style="margin-top: 10px; color: #666;">
                آخر تحديث: {{last_ping}}
            </p>
        </div>

        <div class="stats">
            <div class="stat-item">
                <div class="stat-value">{{commands}}</div>
                <div class="stat-label">عدد الأوامر</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{{guilds}}</div>
                <div class="stat-label">السيرفرات</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{{version}}</div>
                <div class="stat-label">الإصدار</div>
            </div>
        </div>

        <div class="links">
            <a href="/api/status">API Status</a>
            <a href="/api/stats">Statistics</a>
            <a href="/ping">Ping Test</a>
        </div>

        <div class="footer">
            <p>تم التطوير بإخلاص لله تعالى</p>
            <p>Developed with devotion for Allah</p>
            <p style="margin-top: 10px; font-size: 12px;">
                Started: {{started_at}}
            </p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Main page showing bot status"""
    status_map = {
        "online": ("online", "متصل - Online"),
        "offline": ("offline", "غير متصل - Offline"),
        "starting": ("starting", "جاري التشغيل - Starting"),
        "error": ("offline", "خطأ - Error")
    }
    
    status_class, status_text = status_map.get(bot_status["status"], ("starting", "جاري التشغيل"))
    
    return render_template_string(
        HTML_TEMPLATE,
        status=status_class,
        status_text=status_text,
        commands=bot_status["commands_count"],
        guilds=bot_status["guilds_count"],
        version=bot_status["version"],
        last_ping=bot_status["last_ping"] or "غير متوفر",
        started_at=bot_status["started_at"] or "غير متوفر"
    )

@app.route('/ping')
def ping():
    """Simple ping endpoint for uptime monitoring"""
    return jsonify({
        "status": "alive",
        "timestamp": datetime.now().isoformat(),
        "bot_status": bot_status["status"]
    })

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    bot_status["last_ping"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return jsonify({
        "status": "healthy",
        "bot_status": bot_status["status"],
        "timestamp": datetime.now().isoformat(),
        "version": bot_status["version"]
    })

@app.route('/api/status')
def api_status():
    """API endpoint for bot status"""
    return jsonify({
        "bot": {
            "status": bot_status["status"],
            "version": bot_status["version"],
            "started_at": bot_status["started_at"],
            "last_ping": bot_status["last_ping"]
        },
        "stats": {
            "commands": bot_status["commands_count"],
            "guilds": bot_status["guilds_count"]
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/stats')
def api_stats():
    """Detailed statistics API"""
    return jsonify({
        "status": "success",
        "data": bot_status,
        "timestamp": datetime.now().isoformat()
    })

def update_bot_status(status, commands=0, guilds=0):
    """Update bot status from the main bot"""
    bot_status["status"] = status
    bot_status["commands_count"] = commands
    bot_status["guilds_count"] = guilds
    if bot_status["started_at"] is None:
        bot_status["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def run_web_server():
    """Run the Flask web server in a separate thread"""
    def run():
        # Run Flask on port 10000 (Render's default)
        app.run(
            host='0.0.0.0',
            port=10000,
            debug=False,
            threaded=True,
            use_reloader=False  # Important: Disable reloader when running in thread
        )
    
    # Start Flask in a daemon thread
    server_thread = threading.Thread(target=run, daemon=True)
    server_thread.start()
    print("✅ Web server started on http://0.0.0.0:10000")

if __name__ == "__main__":
    # For testing the web server standalone
    run_web_server()
    
    # Keep the main thread alive
    import time
    while True:
        time.sleep(1)
