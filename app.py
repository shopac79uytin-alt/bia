import streamlit as st

st.set_page_config(
    page_title="Bida Mini Xếp Tam Giác trên Streamlit", page_icon="🎱", layout="centered"
)

st.title("🎱 Mini Billiards - Xếp Bi Hình Tam Giác (11 Bi & 6 Lỗ)")
st.write(
    "Các bi màu đã được xếp thành hình tam giác gọn gàng. Kéo bi cái (trắng) và dùng cơ để phá bóng!"
)

# Mã HTML/JS tích hợp bi có số và xếp hình tam giác
pool_game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pool Game Triangle Rack</title>
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

        const BALL_RADIUS = 10;
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

        // Khởi tạo vị trí: Bi trắng ở bên trái, 10 bi màu xếp thành hình tam giác ở bên phải
        let startX = 460;
        let startY = 170;
        let r = BALL_RADIUS * 2.05; // Khoảng cách giữa các tâm bi để khít hình tam giác

        let balls = [
            // Bi cái (trắng)
            { id: 0, number: '', x: 180, y: 170, vx: 0, vy: 0, color: '#ffffff', textColor: '#000', isCue: true, active: true },
            
            // Hàng 1 (1 viên) - Đỉnh tam giác
            { id: 1, number: '1', x: startX, y: startY, vx: 0, vy: 0, color: '#f1c40f', textColor: '#000', isCue: false, active: true },
            
            // Hàng 2 (2 viên)
            { id: 2, number: '2', x: startX + r * 0.866, y: startY - r / 2, vx: 0, vy: 0, color: '#3498db', textColor: '#fff', isCue: false, active: true },
            { id: 3, number: '3', x: startX + r * 0.866, y: startY + r / 2, vx: 0, vy: 0, color: '#e74c3c', textColor: '#fff', isCue: false, active: true },
            
            // Hàng 3 (3 viên)
            { id: 4, number: '4', x: startX + r * 1.732, y: startY - r, vx: 0, vy: 0, color: '#9b59b6', textColor: '#fff', isCue: false, active: true },
            { id: 5, number: '5', x: startX + r * 1.732, y: startY, vx: 0, vy: 0, color: '#e67e22', textColor: '#fff', isCue: false, active: true },
            { id: 6, number: '6', x: startX + r * 1.732, y: startY + r, vx: 0, vy: 0, color: '#1abc9c', textColor: '#fff', isCue: false, active: true },

            // Hàng 4 (4 viên) - Đáy tam giác
            { id: 7, number: '7', x: startX + r * 2.598, y: startY - r * 1.5, vx: 0, vy: 0, color: '#2ecc71', textColor: '#fff', isCue: false, active: true },
            { id: 8, number: '8', x: startX + r * 2.598, y: startY - r * 0.5, vx: 0, vy: 0, color: '#2c3e50', textColor: '#fff', isCue: false, active: true },
            { id: 9, number: '9', x: startX + r * 2.598, y: startY + r * 0.5, vx: 0, vy: 0, color: '#d35400', textColor: '#fff', isCue: false, active: true },
            { id: 10, number: '10', x: startX + r * 2.598, y: startY + r * 1.5, vx: 0, vy: 0, color: '#7f8c8d', textColor: '#fff', isCue: false, active: true }
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

            // Vẽ cây cơ và đường ngắm khi kéo chuột
            if (isDragging && cue.active) {
                let dx = mouseX - cue.x;
                let dy = mouseY - cue.y;
                let angle = Math.atan2(dy, dx);
                let pullDistance = Math.min(Math.hypot(dx, dy), 120);

                ctx.strokeStyle = 'rgba(255, 255, 255, 0.7)';
                ctx.lineWidth = 2;
                ctx.setLineDash([4, 4]);
                ctx.beginPath();
                ctx.moveTo(cue.x, cue.y);
                ctx.lineTo(cue.x - dx * 1.5, cue.y - dy * 1.5);
                ctx.stroke();
                ctx.setLineDash([]);

                ctx.save();
                ctx.translate(cue.x, cue.y);
                ctx.rotate(angle);

                let cueLength = 180;
                let offset = 15 + pullDistance;

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

            // Vẽ bi và số trên bi
            balls.forEach(ball => {
                if (!ball.active) return;
                
                // Thân bi
                ctx.beginPath();
                ctx.arc(ball.x, ball.y, BALL_RADIUS, 0, Math.PI * 2);
                ctx.fillStyle = ball.color;
                ctx.fill();
                ctx.lineWidth = 1.2;
                ctx.strokeStyle = '#000000';
                ctx.stroke();
                ctx.closePath();

                // Số trên bi (nếu có)
                if (!ball.isCue) {
                    ctx.fillStyle = ball.textColor;
                    ctx.font = 'bold 10px sans-serif';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(ball.number, ball.x, ball.y);
                }
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
st.markdown("### Hướng dẫn chơi:")
st.markdown(
    "- **Xếp bi:** 10 viên bi màu được xếp gọn thành hình tam giác ở đầu bàn.\n"
    "- **Cách đánh:** Kéo ngược từ bi trắng (có cây cơ hướng dẫn) để ngắm và thả tay để phá bóng."
)
