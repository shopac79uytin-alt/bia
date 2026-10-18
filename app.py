import streamlit as st

st.set_page_config(
    page_title="Bida Mini 12 Bi trên Streamlit", page_icon="🎱", layout="centered"
)

st.title("🎱 Mini Billiards (Bida) - 6 Lỗ & 12 Bi")
st.write(
    "Đưa các viên bi vào lỗ bằng cách kéo thả bi cái. Bi trắng rơi xuống lỗ sẽ được đặt lại vị trí cũ!"
)

# Mã HTML + JavaScript tích hợp bàn bida 6 lỗ và 12 viên bi
pool_game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pool Game 12 Balls 6 Pockets</title>
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
        const POCKET_RADIUS = 18;
        const FRICTION = 0.985;
        const TABLE_X = 25;
        const TABLE_Y = 25;
        const TABLE_W = 750;
        const TABLE_H = 350;

        // Định nghĩa 6 lỗ trên bàn bida (4 góc và 2 lỗ giữa băng trên/dưới)
        const pockets = [
            { x: TABLE_X, y: TABLE_Y },                                // Góc trên bên trái
            { x: TABLE_X + TABLE_W / 2, y: TABLE_Y - 2 },              // Lỗ giữa trên
            { x: TABLE_X + TABLE_W, y: TABLE_Y },                      // Góc trên bên phải
            { x: TABLE_X, y: TABLE_Y + TABLE_H },                      // Góc dưới bên trái
            { x: TABLE_X + TABLE_W / 2, y: TABLE_Y + TABLE_H + 2 },    // Lỗ giữa dưới
            { x: TABLE_X + TABLE_W, y: TABLE_Y + TABLE_H }             // Góc dưới bên phải
        ];

        // Khởi tạo 12 viên bi (1 bi trắng cái + 11 bi màu)
        let balls = [
            { id: 0, x: 200, y: 200, vx: 0, vy: 0, color: 'white', isCue: true, active: true },
            { id: 1, x: 530, y: 200, vx: 0, vy: 0, color: '#f1c40f', active: true }, // Vàng
            { id: 2, x: 555, y: 185, vx: 0, vy: 0, color: '#3498db', active: true }, // Xanh dương
            { id: 3, x: 555, y: 215, vx: 0, vy: 0, color: '#e74c3c', active: true }, // Đỏ
            { id: 4, x: 580, y: 170, vx: 0, vy: 0, color: '#9b59b6', active: true }, // Tím
            { id: 5, x: 580, y: 200, vx: 0, vy: 0, color: '#e67e22', active: true }, // Cam
            { id: 6, x: 580, y: 230, vx: 0, vy: 0, color: '#1abc9c', active: true }, // Xanh ngọc
            { id: 7, x: 605, y: 155, vx: 0, vy: 0, color: '#34495e', active: true }, // Xám đậm
            { id: 8, x: 605, y: 185, vx: 0, vy: 0, color: '#2ecc71', active: true }, // Xanh lá
            { id: 9, x: 605, y: 215, vx: 0, vy: 0, color: '#d35400', active: true }, // Nâu cam
            { id: 10, x: 605, y: 245, vx: 0, vy: 0, color: '#7f8c8d', active: true },// Xám nhạt
            { id: 11, x: 630, y: 200, vx: 0, vy: 0, color: '#2c3e50', active: true } // Đen
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
                if (!ball.active) return;

                ball.x += ball.vx;
                ball.y += ball.vy;
                ball.vx *= FRICTION;
                ball.vy *= FRICTION;

                if (Math.abs(ball.vx) < 0.05) ball.vx = 0;
                if (Math.abs(ball.vy) < 0.05) ball.vy = 0;

                // Kiểm tra rơi vào lỗ
                pockets.forEach(pocket => {
                    let distToPocket = Math.hypot(ball.x - pocket.x, ball.y - pocket.y);
                    if (distToPocket < POCKET_RADIUS) {
                        if (ball.isCue) {
                            // Bi cái rơi xuống lỗ -> Đặt lại vị trí ban đầu và đứng yên
                            ball.x = 200;
                            ball.y = 200;
                            ball.vx = 0;
                            ball.vy = 0;
                        } else {
                            // Bi màu rơi xuống lỗ -> Biến mất khỏi bàn
                            ball.active = false;
                            ball.vx = 0;
                            ball.vy = 0;
                        }
                    }
                });

                // Va chạm thành bàn (trừ khu vực lân cận lỗ để bi có thể rơi vào lỗ góc/cạnh)
                if (ball.x - BALL_RADIUS < TABLE_X) { ball.x = TABLE_X + BALL_RADIUS; ball.vx *= -1; }
                if (ball.x + BALL_RADIUS > TABLE_X + TABLE_W) { ball.x = TABLE_X + TABLE_W - BALL_RADIUS; ball.vx *= -1; }
                if (ball.y - BALL_RADIUS < TABLE_Y) { ball.y = TABLE_Y + BALL_RADIUS; ball.vy *= -1; }
                if (ball.y + BALL_RADIUS > TABLE_Y + TABLE_H) { ball.y = TABLE_Y + TABLE_H - BALL_RADIUS; ball.vy *= -1; }
            });

            // Va chạm giữa các bi với nhau
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

            // Vẽ bàn bida
            ctx.fillStyle = '#0d5c31';
            ctx.fillRect(TABLE_X, TABLE_Y, TABLE_W, TABLE_H);

            // Vẽ 6 lỗ bida (màu đen)
            pockets.forEach(pocket => {
                ctx.beginPath();
                ctx.arc(pocket.x, pocket.y, POCKET_RADIUS, 0, Math.PI * 2);
                ctx.fillStyle = '#051f0f';
                ctx.fill();
                ctx.strokeStyle = '#2c1810';
                ctx.lineWidth = 3;
                ctx.stroke();
                ctx.closePath();
            });

            // Vẽ đường ngắm khi kéo bi cái
            if (isDragging) {
                const cue = balls.find(b => b.isCue);
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.7)';
                ctx.lineWidth = 2;
                ctx.setLineDash([4, 4]);
                ctx.beginPath();
                ctx.moveTo(cue.x, cue.y);
                ctx.lineTo(mouseX, mouseY);
                ctx.stroke();
                ctx.setLineDash([]);
            }

            // Vẽ các bi (chỉ vẽ bi đang active)
            balls.forEach(ball => {
                if (!ball.active) return;
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
st.markdown("### Luật chơi đơn giản:")
st.markdown(
    "1. **Tổng số bi:** Gồm 1 bi cái màu trắng và 11 viên bi màu.\n"
    "2. **6 lỗ bàn:** Có 4 lỗ ở 4 góc và 2 lỗ ở chính giữa 2 cạnh dài.\n"
    "3. **Bi trắng lọt lỗ:** Nếu bi trắng vô tình rơi xuống lỗ, nó sẽ tự động được hồi sinh lại vị trí xuất phát.\n"
    "4. **Bi màu lọt lỗ:** Sẽ biến mất khỏi bàn chơi."
)
