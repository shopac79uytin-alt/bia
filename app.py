import streamlit as st

st.set_page_config(
    page_title="Bida Mini 11 Bi trên Streamlit", page_icon="🎱", layout="centered"
)

st.title("🎱 Mini Billiards - 6 Lỗ & 11 Bi")
st.write(
    "Trò chơi bida thu nhỏ chuẩn 6 lỗ. Kéo và thả bi cái (trắng) để đánh các bi màu xuống lỗ!"
)

# Mã HTML/JS tối ưu hóa hiển thị 6 lỗ và 11 viên bi
pool_game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pool Game 11 Balls 6 Pockets</title>
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
            border: 14px solid #4a2e18;
            border-radius: 8px;
            box-shadow: 0px 0px 25px rgba(0,0,0,0.9);
        }
    </style>
</head>
<body>
    <canvas id="poolCanvas" width="840" height="440"></canvas>

    <script>
        const canvas = document.getElementById('poolCanvas');
        const ctx = canvas.getContext('2d');

        const BALL_RADIUS = 11;
        const POCKET_RADIUS = 20;
        const FRICTION = 0.985;
        
        // Tọa độ biên bàn bida
        const TABLE_X = 35;
        const TABLE_Y = 35;
        const TABLE_W = 770;
        const TABLE_H = 370;

        // Định nghĩa chính xác 6 lỗ (4 góc và 2 lỗ giữa cạnh)
        const pockets = [
            { x: TABLE_X, y: TABLE_Y },                                     // Góc trên-trái
            { x: TABLE_X + TABLE_W / 2, y: TABLE_Y - 4 },                   // Lỗ giữa trên
            { x: TABLE_X + TABLE_W, y: TABLE_Y },                           // Góc trên-phải
            { x: TABLE_X, y: TABLE_Y + TABLE_H },                           // Góc dưới-trái
            { x: TABLE_X + TABLE_W / 2, y: TABLE_Y + TABLE_H + 4 },         // Lỗ giữa dưới
            { x: TABLE_X + TABLE_W, y: TABLE_Y + TABLE_H }                  // Góc dưới-phải
        ];

        // 11 viên bi (1 bi cái trắng + 10 bi màu)
        let balls = [
            { id: 0, x: 220, y: 220, vx: 0, vy: 0, color: '#ffffff', isCue: true, active: true },
            { id: 1, x: 550, y: 220, vx: 0, vy: 0, color: '#f1c40f', active: true }, // Vàng
            { id: 2, x: 575, y: 202, vx: 0, vy: 0, color: '#3498db', active: true }, // Xanh dương
            { id: 3, x: 575, y: 238, vx: 0, vy: 0, color: '#e74c3c', active: true }, // Đỏ
            { id: 4, x: 600, y: 184, vx: 0, vy: 0, color: '#9b59b6', active: true }, // Tím
            { id: 5, x: 600, y: 220, vx: 0, vy: 0, color: '#e67e22', active: true }, // Cam
            { id: 6, x: 600, y: 256, vx: 0, vy: 0, color: '#1abc9c', active: true }, // Xanh ngọc
            { id: 7, x: 625, y: 184, vx: 0, vy: 0, color: '#2ecc71', active: true }, // Xanh lá
            { id: 8, x: 625, y: 220, vx: 0, vy: 0, color: '#d35400', active: true }, // Nâu đậm
            { id: 9, x: 625, y: 256, vx: 0, vy: 0, color: '#7f8c8d', active: true }, // Xám sáng
            { id: 10, x: 650, y: 220, vx: 0, vy: 0, color: '#2c3e50', active: true }// Đen
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
            if (dist < BALL_RADIUS * 2.2 && speed < 0.2) {
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

                // Kiểm tra rơi xuống lỗ
                pockets.forEach(pocket => {
                    let distToPocket = Math.hypot(ball.x - pocket.x, ball.y - pocket.y);
                    if (distToPocket < POCKET_RADIUS) {
                        if (ball.isCue) {
                            // Bi trắng rơi xuống lỗ -> Đặt lại vị trí xuất phát
                            ball.x = 220;
                            ball.y = 220;
                            ball.vx = 0;
                            ball.vy = 0;
                        } else {
                            // Bi màu rơi xuống lỗ -> Biến mất
                            ball.active = false;
                            ball.vx = 0;
                            ball.vy = 0;
                        }
                    }
                });

                // Va chạm thành bàn
                if (ball.x - BALL_RADIUS < TABLE_X) { ball.x = TABLE_X + BALL_RADIUS; ball.vx *= -1; }
                if (ball.x + BALL_RADIUS > TABLE_X + TABLE_W) { ball.x = TABLE_X + TABLE_W - BALL_RADIUS; ball.vx *= -1; }
                if (ball.y - BALL_RADIUS < TABLE_Y) { ball.y = TABLE_Y + BALL_RADIUS; ball.vy *= -1; }
                if (ball.y + BALL_RADIUS > TABLE_Y + TABLE_H) { ball.y = TABLE_Y + TABLE_H - BALL_RADIUS; ball.vy *= -1; }
            });

            // Va chạm đàn hồi giữa các bi
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

            // Vẽ mặt bàn bida
            ctx.fillStyle = '#0f6336';
            ctx.fillRect(TABLE_X, TABLE_Y, TABLE_W, TABLE_H);

            // Vẽ 6 lỗ bida với viền sang trọng dễ nhận diện
            pockets.forEach(pocket => {
                ctx.beginPath();
                ctx.arc(pocket.x, pocket.y, POCKET_RADIUS, 0, Math.PI * 2);
                ctx.fillStyle = '#05180f';
                ctx.fill();
                ctx.lineWidth = 4;
                ctx.strokeStyle = '#2b170c';
                ctx.stroke();
                ctx.closePath();
            });

            // Vẽ đường căn lực (gậy ảo) khi kéo chuột
            if (isDragging) {
                const cue = balls.find(b => b.isCue);
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
                ctx.lineWidth = 2.5;
                ctx.setLineDash([5, 5]);
                ctx.beginPath();
                ctx.moveTo(cue.x, cue.y);
                ctx.lineTo(mouseX, mouseY);
                ctx.stroke();
                ctx.setLineDash([]);
            }

            // Vẽ các viên bi
            balls.forEach(ball => {
                if (!ball.active) return;
                ctx.beginPath();
                ctx.arc(ball.x, ball.y, BALL_RADIUS, 0, Math.PI * 2);
                ctx.fillStyle = ball.color;
                ctx.fill();
                ctx.lineWidth = 1.5;
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

st.components.v1.html(pool_game_html, height=500, scrolling=False)

st.markdown("---")
st.markdown("### Hướng dẫn:")
st.markdown(
    "- Bàn chuẩn **6 lỗ**: 4 góc và 2 lỗ giữa hai bên băng dài.\n"
    "- Gồm đúng **11 viên bi** tổng cộng (1 bi cái trắng + 10 bi màu).\n"
    "- Kéo ngược từ bi trắng để lấy lực và ngắm bắn."
)
