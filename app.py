from flask import Flask, render_template_string, send_file
import os

app = Flask(__name__)

# Manifest.json
@app.route('/manifest.json')
def manifest():
    manifest_content = '''{
  "name": "Yılan Oyunu - Snake Game",
  "short_name": "Yılan",
  "description": "Klasik yılan oyunu - Mobil ve bilgisayarda oynayın!",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#667eea",
  "theme_color": "#667eea",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "/icon-192",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icon-512",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}'''
    return manifest_content, 200, {'Content-Type': 'application/json'}

# Service Worker
@app.route('/sw.js')
def service_worker():
    sw_content = '''
const CACHE_NAME = 'yilan-v1';
const urlsToCache = ['/'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => response || fetch(event.request))
  );
});
'''
    return sw_content, 200, {'Content-Type': 'application/javascript'}

# Icon dosyalarını serve et
@app.route('/icon-192')
def icon_192():
    if os.path.exists('icon-192.png'):
        return send_file('icon-192.png', mimetype='image/png')
    # Yoksa boş dön
    return '', 404

@app.route('/icon-512')
def icon_512():
    if os.path.exists('icon-512.png'):
        return send_file('icon-512.png', mimetype='image/png')
    return '', 404

# Ana sayfa
@app.route('/')
def index():
    html_code = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#667eea">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Yılan Oyunu">
    <link rel="manifest" href="/manifest.json">
    <link rel="apple-touch-icon" href="/icon-192">
    <title>🐍 Yılan Oyunu</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden;
        }
        h1 { 
            margin: 10px 0;
            font-size: 28px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        #install-banner {
            position: fixed;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255,255,255,0.95);
            color: #667eea;
            padding: 12px 20px;
            border-radius: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            display: none;
            z-index: 1000;
            font-weight: bold;
        }
        #install-banner button {
            margin-left: 10px;
            padding: 8px 16px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            font-weight: bold;
        }
        #game-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 15px;
        }
        #game-board {
            border: 4px solid #fff;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            background-color: #1a1a2e;
            border-radius: 10px;
        }
        #score-board {
            font-size: 24px;
            font-weight: bold;
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        .btn {
            margin: 5px;
            padding: 12px 24px;
            font-size: 18px;
            background: rgba(255,255,255,0.9);
            color: #667eea;
            border: none;
            cursor: pointer;
            border-radius: 25px;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s;
        }
        .btn:hover { 
            background-color: #fff;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        .btn:active {
            transform: translateY(0);
        }
        
        #mobile-controls {
            display: grid;
            grid-template-columns: repeat(3, 80px);
            grid-template-rows: repeat(3, 80px);
            gap: 10px;
            margin-top: 20px;
        }
        .control-btn {
            background: rgba(255,255,255,0.9);
            border: none;
            border-radius: 15px;
            font-size: 32px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.2s;
            user-select: none;
            -webkit-user-select: none;
            touch-action: manipulation;
        }
        .control-btn:active {
            transform: scale(0.95);
            background: rgba(255,255,255,0.7);
        }
        #up { grid-column: 2; grid-row: 1; }
        #left { grid-column: 1; grid-row: 2; }
        #down { grid-column: 2; grid-row: 3; }
        #right { grid-column: 3; grid-row: 2; }
        
        @media (max-width: 480px) {
            h1 { font-size: 24px; }
            #game-board {
                width: 90vw !important;
                height: 90vw !important;
                max-width: 400px;
                max-height: 400px;
            }
            #mobile-controls {
                grid-template-columns: repeat(3, 70px);
                grid-template-rows: repeat(3, 70px);
            }
        }
    </style>
</head>
<body>

    <!-- PWA Kurulum Banner -->
    <div id="install-banner">
        📱 Bu oyunu telefonunuza kurun!
        <button id="install-btn">Kur</button>
        <button id="close-banner" style="background: transparent; color: #667eea;">✕</button>
    </div>

    <h1>🐍 Yılan Oyunu</h1>
    <div id="game-container">
        <canvas id="game-board" width="400" height="400"></canvas>
        <div id="score-board">Skor: 0</div>
        <button class="btn" onclick="startGame()">🔄 Yeniden Başlat</button>
        
        <div id="mobile-controls">
            <button class="control-btn" id="up" ontouchstart="changeDirection('UP')" onclick="changeDirection('UP')">⬆️</button>
            <button class="control-btn" id="left" ontouchstart="changeDirection('LEFT')" onclick="changeDirection('LEFT')">⬅️</button>
            <button class="control-btn" id="down" ontouchstart="changeDirection('DOWN')" onclick="changeDirection('DOWN')">⬇️</button>
            <button class="control-btn" id="right" ontouchstart="changeDirection('RIGHT')" onclick="changeDirection('RIGHT')">➡️</button>
        </div>
    </div>

    <script>
        // PWA Kurulum kodu
        let deferredPrompt;
        const installBanner = document.getElementById('install-banner');
        const installBtn = document.getElementById('install-btn');
        const closeBanner = document.getElementById('close-banner');

        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            installBanner.style.display = 'block';
        });

        installBtn.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                console.log('Kurulum:', outcome);
                deferredPrompt = null;
                installBanner.style.display = 'none';
            }
        });

        closeBanner.addEventListener('click', () => {
            installBanner.style.display = 'none';
        });

        // Service Worker kaydet
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js')
                .then(() => console.log('✅ PWA aktif!'))
                .catch(err => console.log('❌ SW error:', err));
        }

        // Oyun kodu
        const canvas = document.getElementById('game-board');
        const ctx = canvas.getContext('2d');
        const scoreElement = document.getElementById('score-board');

        const gridSize = 20;
        const tileCount = canvas.width / gridSize;
        
        let score = 0;
        let velocityX = 0;
        let velocityY = 0;
        let playerX = 10;
        let playerY = 10;
        let appleX = 5;
        let appleY = 5;
        let trail = [];
        let tail = 5;
        let gameInterval;

        document.addEventListener('keydown', keyPush);

        let touchStartX = 0;
        let touchStartY = 0;
        canvas.addEventListener('touchstart', (e) => {
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
        });
        canvas.addEventListener('touchend', (e) => {
            const touchEndX = e.changedTouches[0].clientX;
            const touchEndY = e.changedTouches[0].clientY;
            const deltaX = touchEndX - touchStartX;
            const deltaY = touchEndY - touchStartY;
            
            if(Math.abs(deltaX) > Math.abs(deltaY)) {
                if(deltaX > 15 && velocityX !== -1) { 
                    velocityX = 1; velocityY = 0;
                    gameLoop();
                }
                else if(deltaX < -15 && velocityX !== 1) { 
                    velocityX = -1; velocityY = 0;
                    gameLoop();
                }
            } else {
                if(deltaY > 15 && velocityY !== -1) { 
                    velocityX = 0; velocityY = 1;
                    gameLoop();
                }
                else if(deltaY < -15 && velocityY !== 1) { 
                    velocityX = 0; velocityY = -1;
                    gameLoop();
                }
            }
        });

        function changeDirection(dir) {
            switch(dir) {
                case 'UP': 
                    if(velocityY !== 1) { 
                        velocityX = 0; 
                        velocityY = -1;
                        gameLoop();
                    } 
                    break;
                case 'DOWN': 
                    if(velocityY !== -1) { 
                        velocityX = 0; 
                        velocityY = 1;
                        gameLoop();
                    } 
                    break;
                case 'LEFT': 
                    if(velocityX !== 1) { 
                        velocityX = -1; 
                        velocityY = 0;
                        gameLoop();
                    } 
                    break;
                case 'RIGHT': 
                    if(velocityX !== -1) { 
                        velocityX = 1; 
                        velocityY = 0;
                        gameLoop();
                    } 
                    break;
            }
        }

        function startGame() {
            playerX = 10; playerY = 10;
            velocityX = 0; velocityY = 0;
            score = 0;
            tail = 5;
            trail = [];
            scoreElement.innerText = "Skor: " + score;
            
            clearInterval(gameInterval);
            gameInterval = setInterval(gameLoop, 1000/15);
        }

        function gameLoop() {
            playerX += velocityX;
            playerY += velocityY;

            if(playerX < 0) playerX = tileCount - 1;
            if(playerX > tileCount - 1) playerX = 0;
            if(playerY < 0) playerY = tileCount - 1;
            if(playerY > tileCount - 1) playerY = 0;

            ctx.fillStyle = '#0f3460';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.strokeStyle = 'rgba(255,255,255,0.05)';
            ctx.lineWidth = 1;
            for(let i = 0; i < tileCount; i++) {
                ctx.beginPath();
                ctx.moveTo(i * gridSize, 0);
                ctx.lineTo(i * gridSize, canvas.height);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(0, i * gridSize);
                ctx.lineTo(canvas.width, i * gridSize);
                ctx.stroke();
            }

            ctx.fillStyle = '#16C79A';
            for(let i = 0; i < trail.length; i++) {
                ctx.fillRect(trail[i].x * gridSize, trail[i].y * gridSize, gridSize - 2, gridSize - 2);
                
                if(trail[i].x === playerX && trail[i].y === playerY && (velocityX !== 0 || velocityY !== 0)) {
                    tail = 5;
                    score = 0;
                    scoreElement.innerText = "💥 Skor: 0";
                }
            }

            trail.push({x: playerX, y: playerY});
            while(trail.length > tail) {
                trail.shift();
            }

            ctx.fillStyle = '#F94C66';
            ctx.beginPath();
            ctx.arc(appleX * gridSize + gridSize/2, appleY * gridSize + gridSize/2, gridSize/2 - 2, 0, Math.PI * 2);
            ctx.fill();

            if(appleX === playerX && appleY === playerY) {
                tail++;
                score += 10;
                scoreElement.innerText = "🎯 Skor: " + score;
                appleX = Math.floor(Math.random() * tileCount);
                appleY = Math.floor(Math.random() * tileCount);
            }
        }

        function keyPush(evt) {
            switch(evt.keyCode) {
                case 37: changeDirection('LEFT'); break;
                case 38: changeDirection('UP'); break;
                case 39: changeDirection('RIGHT'); break;
                case 40: changeDirection('DOWN'); break;
            }
        }

        startGame();
    </script>
</body>
</html>
"""
    return render_template_string(html_code)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')