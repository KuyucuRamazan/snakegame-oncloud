from flask import Flask, render_template_string

app = Flask(__name__)

# HTML, CSS ve JavaScript kodlarının hepsi burada tek parça halinde
html_code = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yılan Oyunu - Web Sürümü</title>
    <style>
        body {
            background-color: #2c3e50;
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            font-family: 'Arial', sans-serif;
        }
        h1 { margin-bottom: 10px; }
        #game-board {
            border: 4px solid #ecf0f1;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
            background-color: #000;
        }
        #score-board {
            font-size: 24px;
            margin-top: 10px;
        }
        .btn {
            margin-top: 15px;
            padding: 10px 20px;
            font-size: 18px;
            background-color: #e74c3c;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }
        .btn:hover { background-color: #c0392b; }
    </style>
</head>
<body>

    <h1>🐍 Yılan Oyunu</h1>
    <canvas id="game-board" width="400" height="400"></canvas>
    <div id="score-board">Skor: 0</div>
    <button class="btn" onclick="startGame()">Oyunu Yeniden Başlat</button>

    <script>
        const canvas = document.getElementById('game-board');
        const ctx = canvas.getContext('2d');
        const scoreElement = document.getElementById('score-board');

        const gridSize = 20; // Yılanın kare boyutu
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

        // Klavye dinleyicisi
        document.addEventListener('keydown', keyPush);

        function startGame() {
            // Değişkenleri sıfırla
            playerX = 10; playerY = 10;
            velocityX = 0; velocityY = 0;
            score = 0;
            tail = 5;
            trail = [];
            scoreElement.innerText = "Skor: " + score;
            
            clearInterval(gameInterval);
            gameInterval = setInterval(gameLoop, 1000/10); // Saniyede 10 kare (Hız)
        }

        function gameLoop() {
            playerX += velocityX;
            playerY += velocityY;

            // Duvardan geçme özelliği (Sonsuz döngü)
            if(playerX < 0) playerX = tileCount - 1;
            if(playerX > tileCount - 1) playerX = 0;
            if(playerY < 0) playerY = tileCount - 1;
            if(playerY > tileCount - 1) playerY = 0;

            // Arkaplanı temizle
            ctx.fillStyle = 'black';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Yılanı çiz
            ctx.fillStyle = 'lime';
            for(let i = 0; i < trail.length; i++) {
                ctx.fillRect(trail[i].x * gridSize, trail[i].y * gridSize, gridSize - 2, gridSize - 2);
                
                // Kendine çarpma kontrolü
                if(trail[i].x === playerX && trail[i].y === playerY && (velocityX !== 0 || velocityY !== 0)) {
                    tail = 5;
                    score = 0;
                    scoreElement.innerText = "Skor: 0 (Yandın!)";
                }
            }

            trail.push({x: playerX, y: playerY});
            while(trail.length > tail) {
                trail.shift();
            }

            // Yemi çiz
            ctx.fillStyle = 'red';
            ctx.fillRect(appleX * gridSize, appleY * gridSize, gridSize - 2, gridSize - 2);

            // Yemi yeme kontrolü
            if(appleX === playerX && appleY === playerY) {
                tail++;
                score += 10;
                scoreElement.innerText = "Skor: " + score;
                // Rastgele yeni yem konumu
                appleX = Math.floor(Math.random() * tileCount);
                appleY = Math.floor(Math.random() * tileCount);
            }
        }

        function keyPush(evt) {
            switch(evt.keyCode) {
                case 37: // Sol
                    if(velocityX !== 1) { velocityX = -1; velocityY = 0; }
                    break;
                case 38: // Yukarı
                    if(velocityY !== 1) { velocityX = 0; velocityY = -1; }
                    break;
                case 39: // Sağ
                    if(velocityX !== -1) { velocityX = 1; velocityY = 0; }
                    break;
                case 40: // Aşağı
                    if(velocityY !== -1) { velocityX = 0; velocityY = 1; }
                    break;
            }
        }

        // Sayfa açılınca oyunu başlat
        startGame();

    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_code)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')