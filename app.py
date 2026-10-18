import streamlit as st

st.set_page_config(
    page_title="Bida Mini trên Streamlit", page_icon="🎱", layout="centered"
)

st.title("🎱 Mini Billiards (Bida) Game")
st.write(
    "Kéo chuột trên bàn bida để ngắm hướng và lực đánh, sau đó thả ra để đánh bi cái!"
)

# Mã HTML + JavaScript nhúng để chạy game bida mượt mà
pool_game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pool Game</title>
    <style>
        body {
            margin: 0;
            background: #0e1117;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: white;
            font-family: sans-serif;
        }
        canvas {
            background: #0d5c31;
            border: 10px solid #5c3a21;
            border-radius: 6px;
            box-shadow: 0px 0px 20px rgba(0,0,0,0.8);
        }
    </style>
</head>
<body>
    <canvas id="poolCanvas" width="800" height="400"></canvas>

    <script>
        const canvas = document.getElementById('poolCanvas');
        const ctx = canvas.getContext('2d');

        const BALL_RADIUS = 10;
        const FRICTION = 0.985;
        const TABLE_X = 20;
        const TABLE_Y = 20;
        const TABLE_W = 760;
        const TABLE_H = 360;

        let balls = [
            { x: 200, y: 200, vx: 0, vy: 0, color: 'white', isCue: true },
            { x: 550, y: 200, vx: 0, vy: 0, color: 'yellow', isCue: false },
            { x: 580, y: 180, vx: 0, vy: 0, color: 'blue', isCue: false },
            { x: 580, y: 220, vx: 0, vy: 0, color: 'red', isCue: false },
            { x: 610, y: 160, vx: 0, vy: 0, color: 'purple', isCue: false },
            { x: 610, y: 200, vx: 0, vy: 0, color: 'black', isCue: false },
            { x: 610, y: 240, vx: 0, vy: 0, color: 'orange', isCue: false }
        ];

        let isDragging = false;
        let mouseX = 0;
        let mouseY = 0;

        canvas.addEventListener('mousedown', (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const cue = balls.find(b => b.isCue);
            
            let speed = Math.hypot(cue.vx, cue.vy);
            let dist = Math.hypot(cue.x - x, cue.y - y);
            if (dist < BALL_RADIUS * 2 && speed < 0.2) {
                isDragging = true;
            }
        });

        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            mouseX = e.clientX - rect.left;
            mouseY = e.clientY - rect.top;
        });

        canvas.addEventListener('mouseup', (e) => {
            if (isDragging) {
                const cue = balls.find(b => b.isCue);
                let fuerzaX = (cue.x - mouseX) * 0.15;
                let fuerzaY = (cue.y - mouseY) * 0.15;
                cue.vx = fuerzaX;
                cue.vy = fuerzaY;
                isDragging = false;
            }
        });

        function update() {
            balls.forEach(ball => {
                ball.x += ball.vx;
                ball.y += ball.vy;
                ball.vx *= FRICTION;
                ball.vy *= FRICTION;

                if (Math.abs(ball.vx) < 0.05) ball.vx = 0;
                if (Math.abs(ball.vy) < 0.05) ball.vy = 0;

                if (ball.x - BALL_RADIUS < TABLE_X) { ball.x = TABLE_X + BALL_RADIUS; ball.vx *= -1; }
                if (ball.x + BALL_RADIUS > TABLE_X + TABLE_W) { ball.x = TABLE_X + TABLE_W - BALL_RADIUS; ball.vx *= -1; }
                if (ball.y - BALL_RADIUS < TABLE_Y) { ball.y = TABLE_Y + BALL_RADIUS; ball.vy *= -1; }
                if (ball.y + BALL_RADIUS > TABLE_Y + TABLE_H) { ball.y = TABLE_Y + TABLE_H - BALL_RADIUS; ball.vy *= -1; }
            });

            for (let i = 0; i < balls.length; i++) {
                for (let j = i + 1; j < balls.length; j++) {
                    let b1 = balls[i];
                    let b2 = balls[j];
                    let dx = b2.x - b1.x;
                    let dy = b2.y - b1.y;
                    let dist = Math.hypot(dx, dy);

                    if (dist < BALL_RADIUS * 2) {
                        let angle = Math.atan2(dy, dx);
                        let sin = Math.sin(angle);
                        let cos = Math.cos(angle);

                        let vx1 = b1.vx * cos + b1.vy * sin;
                        let vy1 = b1.vy * cos - b1.vx * sin;
                        let vx2 = b2.vx * cos + b2.vy * sin;
                        let vy2 = b2.vy * cos - b2.vx * sin;

                        let temp = vx1;
                        vx1 = vx2;
                        vx2 = temp;

                        b1.vx = vx1 * cos - vy1 * sin;
                        b1.vy = vy1 * cos + vx1 * sin;
                        b2.vx = vx2 * cos - vy2 * sin;
                        b2.vy = vy2 * cos + vx2 * sin;

                        let overlap = (BALL_RADIUS * 2 - dist) / 2;
                        b1.x -= overlap * Math.cos(angle);
                        b1.y -= overlap * Math.sin(angle);
                        b2.x += overlap * Math.cos(angle);
                        b2.y += overlap * Math.sin(angle);
                    }
                }
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = '#0d5c31';
            ctx.fillRect(TABLE_X, TABLE_Y, TABLE_W, TABLE_H);

            if (isDragging) {
                const cue = balls.find(b => b.isCue);
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
                ctx.lineWidth = 2;
                ctx.setLineDash([4, 4]);
                ctx.beginPath();
                ctx.moveTo(cue.x, cue.y);
                ctx.lineTo(mouseX, mouseY);
                ctx.stroke();
                ctx.setLineDash([]);
            }

            balls.forEach(ball => {
                ctx.beginPath();
                ctx.arc(ball.x, ball.y, BALL_RADIUS, 0, Math.PI * 2);
                ctx.fillStyle = ball.color;
                ctx.fill();
                ctx.strokeStyle = '#000';
                ctx.lineWidth = 1.5;
                ctx.stroke();
                ctx.closePath();
            });
        }

        function loop() {
            update();
            draw();
            requestAnimationFrame(loop);
        }

        loop();
    </script>
</body>
</html>
"""

st.components.v1.html(pool_game_html, height=450, scrolling=False)

st.markdown("---")
st.markdown("### Hướng dẫn chơi:")
st.markdown(
    "1. Nhấn giữ chuột vào **bi màu trắng** (bi cái) trên bàn.\n"
    "2. Kéo ngược hướng bạn muốn đánh (giống như kéo dây cung).\n"
    "3. Thả chuột để đẩy bi đi và va chạm với các bi khác!"
)
