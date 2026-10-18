import streamlit as st

st.set_page_config(
    page_title="Bida Mini Có Cây Cơ trên Streamlit", page_icon="🎱", layout="centered"
)

st.title("🎱 Mini Billiards - Có Cây Cơ (6 Lỗ & 11 Bi)")
st.write(
    "Kéo ngược từ bi trắng để lấy lực và ngắm bắn bằng cây cơ trực quan!"
)

# Mã HTML/JS tích hợp cây cơ hiển thị tương tác
pool_game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pool Game with Cue Stick</title>
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
            background: #0f6336;
            border: 12px solid #4a2e18;
            border-radius: 8px;
            box-shadow: 0px 0px 20px rgba(0,0,0,0.9);
        }
    </style>
</head>
<body>
    <canvas id="poolCanvas" width="680" height="340"></canvas>

    <script>
        const canvas = document.getElementById('poolCanvas');
        const ctx = canvas.getContext('2d');

        const BALL_RADIUS = 9;
        const POCKET_RADIUS = 16;
        const FRICTION = 0.985;
        
        const TABLE_X = 30;
        const TABLE_Y = 30;
        const TABLE_W = 620;
        const TABLE_H = 280;

        const pockets = [
            { x: TABLE_X, y: TABLE_Y },
            { x: TABLE_X + TABLE_W / 2, y: TABLE_Y - 3 },
            { x: TABLE_X + TABLE_W, y: TABLE_Y },
            { x: TABLE_X, y: TABLE_Y + TABLE_H },
            { x: TABLE_X + TABLE_W / 2, y: TABLE_Y + TABLE_H + 3 },
            { x: TABLE_X + TABLE_W, y: TABLE_Y + TABLE_H }
        ];

        let balls = [
            { id: 0, x: 180, y: 170, vx: 0, vy: 0, color: '#ffffff', isCue: true, active: true },
            { id: 1, x: 450, y: 170, vx: 0, vy: 0, color: '#f1c40f', active: true },
            { id: 2, x: 472, y: 155, vx: 0, vy: 0, color: '#3498db', active: true },
            { id: 3, x: 472, y: 185, vx: 0, vy: 0, color: '#e74c3c', active: true },
            { id: 4, x: 494, y: 140, vx: 0, vy: 0, color: '#9b59b6', active: true },
            { id: 5, x: 494, y: 170, vx: 0, vy: 0, color: '#e67e22', active: true },
            { id: 6, x: 494, y: 200, vx: 0, vy: 0, color: '#1abc9c', active: true },
            { id: 7, x: 516, y: 140, vx: 0, vy: 0, color: '#2ecc71', active: true },
            { id: 8, x: 516, y: 170, vx: 0, vy: 0, color: '#d35400', active: true },
            { id: 9, x: 516, y: 200, vx: 0, vy: 0, color: '#7f8c8d', active: true },
            { id: 10, x: 538, y: 170, vx: 0, vy: 0, color: '#2c3e50', active: true }
        ];

        let isDragging = false;
        let mouseX = 0;
        let mouseY = 0;

        canvas.addEventListener('mousedown', (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const cue = balls.find(b => b.isCue);
            
            if (!cue.active) return;
            let speed = Math.hypot(cue.vx, cue.vy);
            let dist = Math.hypot(cue.x - x, cue.y - y);
            if (dist < BALL_RADIUS * 2.5 && speed < 0.2) {
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
                cue.vx = (cue.x - mouseX) * 0.16;
                cue.vy = (cue.y - mouseY) * 0.16;
                isDragging = false;
            }
        });

        function update() {
            balls.forEach(ball => {
                if (!ball.active) return;

                ball.x += ball.vx;
                ball.y += ball.vy;
                ball.vx *= FRICTION;
                ball.vy *= FRICTION;

                if (Math.abs(ball.vx) < 0.05) ball.vx = 0;
                if (Math.abs(ball.vy) < 0.05) ball.vy = 0;

                pockets.forEach(pocket => {
                    let distToPocket = Math.hypot(ball.x - pocket.x, ball.y - pocket.y);
                    if (distToPocket < POCKET_RADIUS) {
                        if (ball.isCue) {
                            ball.x = 180;
                            ball.y = 170;
                            ball.vx = 0;
                            ball.vy = 0;
                        } else {
                            ball.active = false;
                            ball.vx = 0;
                            ball.vy = 0;
                        }
                    }
                });

                if (ball.x - BALL_RADIUS < TABLE_X) { ball.x = TABLE_X + BALL_RADIUS; ball.vx *= -1; }
                if (ball.x + BALL_RADIUS > TABLE_X + TABLE_W) { ball.x = TABLE_X + TABLE_W - BALL_RADIUS; ball.vx *= -1; }
                if (ball.y - BALL_RADIUS < TABLE_Y) { ball.y = TABLE_Y + BALL_RADIUS; ball.vy *= -1; }
                if (ball.y + BALL_RADIUS > TABLE_Y + TABLE_H) { ball.y = TABLE_Y + TABLE_H - BALL_RADIUS; ball.vy *= -1; }
            });

            for (let i = 0; i < balls.length; i++) {
                for (let j = i + 1; j < balls.length; j++) {
                    let b1 = balls[i];
                    let b2 = balls[j];
                    if (!b1.active || !b2.active) continue;

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

            // Vẽ bàn
            ctx.fillStyle = '#0f6336';
            ctx.fillRect(TABLE_X, TABLE_Y, TABLE_W, TABLE_H);

            // Vẽ 6 lỗ
            pockets.forEach(pocket => {
                ctx.beginPath();
                ctx.arc(pocket.x, pocket.y, POCKET_RADIUS, 0, Math.PI * 2);
                ctx.fillStyle = '#05180f';
                ctx.fill();
                ctx.lineWidth = 3;
                ctx.strokeStyle = '#2b170c';
                ctx.stroke();
                ctx.closePath();
            });

            const cue = balls.find(b => b.isCue);

            // Vẽ cây cơ và đường ngắm khi đang kéo chuột
            if (isDragging && cue.active) {
                let dx = mouseX - cue.x;
                let dy = mouseY - cue.y;
                let angle = Math.atan2(dy, dx);
                let pullDistance = Math.min(Math.hypot(dx, dy), 120); // Giới hạn khoảng kéo

                // Vẽ đường ngắm chấm bi đứt nét hướng bắn
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.7)';
                ctx.lineWidth = 2;
                ctx.setLineDash([4, 4]);
                ctx.beginPath();
                ctx.moveTo(cue.x, cue.y);
                ctx.lineTo(cue.x - dx * 1.5, cue.y - dy * 1.5);
                ctx.stroke();
                ctx.setLineDash([]);

                // Vẽ cây cơ bida
                ctx.save();
                ctx.translate(cue.x, cue.y);
                ctx.rotate(angle); // Xoay theo hướng kéo

                let cueLength = 180;
                let offset = 15 + pullDistance; // Khoảng cách lùi cơ theo lực kéo

                // Thân cơ (màu gỗ)
                let gradient = ctx.createLinearGradient(offset, 0, offset + cueLength, 0);
                gradient.addColorStop(0, '#d35400');
                gradient.addColorStop(1, '#5a3d28');
                
                ctx.beginPath();
                ctx.moveTo(offset, -3);
                ctx.lineTo(offset + cueLength, -6);
                ctx.lineTo(offset + cueLength, 6);
                ctx.lineTo(offset, 3);
                ctx.fillStyle = gradient;
                ctx.fill();
                ctx.closePath();

                ctx.restore();
            }

            // Vẽ bi
            balls.forEach(ball => {
                if (!ball.active) return;
                ctx.beginPath();
                ctx.arc(ball.x, ball.y, BALL_RADIUS, 0, Math.PI * 2);
                ctx.fillStyle = ball.color;
                ctx.fill();
                ctx.lineWidth = 1.2;
                ctx.strokeStyle = '#000000';
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

st.components.v1.html(pool_game_html, height=400, scrolling=False)

st.markdown("---")
st.markdown("### Hướng dẫn:")
st.markdown(
    "- Nhấn giữ và kéo chuột từ **bi trắng** ra xa để xuất hiện **cây cơ bida**.\n"
    "- Kéo càng xa lực đánh càng mạnh, thả tay ra để cơ đập vào bi trắng!"
)
