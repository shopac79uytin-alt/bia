import streamlit as st

st.set_page_config(
    page_title="Bida Mini 2 Đội trên Streamlit", page_icon="🎱", layout="centered"
)

# Quản lý trạng thái màn hình (Menu -> Game)
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "team1_name" not in st.session_state:
    st.session_state.team1_name = "Đội 1 (Player 1)"
if "team2_name" not in st.session_state:
    st.session_state.team2_name = "Đội 2 (Player 2)"

# GIAO DIỆN MENU GAME
if not st.session_state.game_started:
    st.title("🎱 Chào mừng đến với Mini Billiards 2 Đội")
    st.write(
        "Thiết lập thông tin các đội chơi trước khi bước vào bàn bida đỉnh cao!"
    )

    st.markdown("### 📝 Nhập thông tin đội chơi")
    team1 = st.text_input("Tên Đội 1:", value="Đội Đỏ")
    team2 = st.text_input("Tên Đội 2:", value="Đội Xanh")

    if st.button("🚀 Bắt đầu trận đấu", type="primary"):
        st.session_state.team1_name = team1
        st.session_state.team2_name = team2
        st.session_state.game_started = True
        st.rerun()

# GIAO DIỆN TRÒ CHƠI BIDA CHÍNH
else:
    # Truyền tên đội vào HTML thông qua chuỗi Python
    t1 = st.session_state.team1_name
    t2 = st.session_state.team2_name

    pool_game_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Pool Game 2 Teams</title>
        <style>
            body {{
                margin: 0;
                background: #0e1117;
                display: flex;
                flex-direction: column;
                align-items: center;
                color: white;
                font-family: sans-serif;
            }}
            #scoreboard {{
                display: flex;
                justify-content: space-around;
                width: 680px;
                background: #161b22;
                padding: 10px;
                border-radius: 6px;
                margin-bottom: 10px;
                border: 1px solid #30363d;
            }}
            .team-box {{
                text-align: center;
                font-size: 14px;
            }}
            .active-turn {{
                color: #2ecc71;
                font-weight: bold;
                border-bottom: 2px solid #2ecc71;
                padding-bottom: 2px;
            }}
            canvas {{
                background: #0f6336;
                border: 12px solid #4a2e18;
                border-radius: 8px;
                box-shadow: 0px 0px 20px rgba(0,0,0,0.9);
            }}
        </style>
    </head>
    <body>
        <div id="scoreboard">
            <div class="team-box" id="t1Box">
                <span id="t1Name">{t1}</span><br>Điểm: <span id="t1Score">0</span>
            </div>
            <div class="team-box" id="turnIndicator">Đang tải lượt...</div>
            <div class="team-box" id="t2Box">
                <span id="t2Name">{t2}</span><br>Điểm: <span id="t2Score">0</span>
            </div>
        </div>

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
                {{ x: TABLE_X, y: TABLE_Y }},
                {{ x: TABLE_X + TABLE_W / 2, y: TABLE_Y - 3 }},
                {{ x: TABLE_X + TABLE_W, y: TABLE_Y }},
                {{ x: TABLE_X, y: TABLE_Y + TABLE_H }},
                {{ x: TABLE_X + TABLE_W / 2, y: TABLE_Y + TABLE_H + 3 }},
                {{ x: TABLE_X + TABLE_W, y: TABLE_Y + TABLE_H }}
            ];

            let startX = 460;
            let startY = 170;
            let r = BALL_RADIUS * 2.05;

            let balls = [
                {{ id: 0, number: '', x: 180, y: 170, vx: 0, vy: 0, color: '#ffffff', textColor: '#000', isCue: true, active: true }},
                {{ id: 1, number: '1', x: startX, y: startY, vx: 0, vy: 0, color: '#f1c40f', textColor: '#000', isCue: false, active: true }},
                {{ id: 2, number: '2', x: startX + r * 0.866, y: startY - r / 2, vx: 0, vy: 0, color: '#3498db', textColor: '#fff', isCue: false, active: true }},
                {{ id: 3, number: '3', x: startX + r * 0.866, y: startY + r / 2, vx: 0, vy: 0, color: '#e74c3c', textColor: '#fff', isCue: false, active: true }},
                {{ id: 4, number: '4', x: startX + r * 1.732, y: startY - r, vx: 0, vy: 0, color: '#9b59b6', textColor: '#fff', isCue: false, active: true }},
                {{ id: 5, number: '5', x: startX + r * 1.732, y: startY, vx: 0, vy: 0, color: '#e67e22', textColor: '#fff', isCue: false, active: true }},
                {{ id: 6, number: '6', x: startX + r * 1.732, y: startY + r, vx: 0, vy: 0, color: '#1abc9c', textColor: '#fff', isCue: false, active: true }},
                {{ id: 7, number: '7', x: startX + r * 2.598, y: startY - r * 1.5, vx: 0, vy: 0, color: '#2ecc71', textColor: '#fff', isCue: false, active: true }},
                {{ id: 8, number: '8', x: startX + r * 2.598, y: startY - r * 0.5, vx: 0, vy: 0, color: '#2c3e50', textColor: '#fff', isCue: false, active: true }},
                {{ id: 9, number: '9', x: startX + r * 2.598, y: startY + r * 0.5, vx: 0, vy: 0, color: '#d35400', textColor: '#fff', isCue: false, active: true }},
                {{ id: 10, number: '10', x: startX + r * 2.598, y: startY + r * 1.5, vx: 0, vy: 0, color: '#7f8c8d', textColor: '#fff', isCue: false, active: true }}
            ];

            let score1 = 0;
            let score2 = 0;
            let currentTurn = 1; // 1: Đội 1, 2: Đội 2
            let ballInHoleThisTurn = false;
            let whiteBallFoul = false;

            let isDragging = false;
            let mouseX = 0;
            let mouseY = 0;

            function updateScoreboard() {{
                document.getElementById('t1Score').innerText = score1;
                document.getElementById('t2Score').innerText = score2;
                
                let indicator = document.getElementById('turnIndicator');
                let t1Box = document.getElementById('t1Box');
                let t2Box = document.getElementById('t2Box');

                if (currentTurn === 1) {{
                    indicator.innerHTML = "Lượt đánh: <b style='color:#f1c40f'>{t1}</b>";
                    t1Box.className = "team-box active-turn";
                    t2Box.className = "team-box";
                }} else {{
                    indicator.innerHTML = "Lượt đánh: <b style='color:#3498db'>{t2}</b>";
                    t1Box.className = "team-box";
                    t2Box.className = "team-box active-turn";
                }}
            }}

            // Kiểm tra xem tất cả các bi có đang đứng yên không
            function areBallsStopped() {{
                return balls.every(b => Math.hypot(b.vx, b.vy) < 0.05);
            }}

            canvas.addEventListener('mousedown', (e) => {{
                if (!areBallsStopped()) return; // Chỉ cho phép đánh khi bóng đã dừng hẳn

                const rect = canvas.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const cue = balls.find(b => b.isCue);
                
                if (!cue.active) return;
                let dist = Math.hypot(cue.x - x, cue.y - y);
                if (dist < BALL_RADIUS * 2.5) {{
                    isDragging = true;
                    ballInHoleThisTurn = false;
                    whiteBallFoul = false;
                }}
            });

            canvas.addEventListener('mousemove', (e) => {{
                const rect = canvas.getBoundingClientRect();
                mouseX = e.clientX - rect.left;
                mouseY = e.clientY - rect.top;
            });

            canvas.addEventListener('mouseup', (e) => {{
                if (isDragging) {
                    const cue = balls.find(b => b.isCue);
                    cue.vx = (cue.x - mouseX) * 0.16;
                    cue.vy = (cue.y - mouseY) * 0.16;
                    isDragging = false;
                }
            }});

            let wasMoving = false;

            function update() {{
                let moving = !areBallsStopped();

                balls.forEach(ball => {{
                    if (!ball.active) return;

                    ball.x += ball.vx;
                    ball.y += ball.vy;
                    ball.vx *= FRICTION;
                    ball.vy *= FRICTION;

                    if (Math.abs(ball.vx) < 0.05) ball.vx = 0;
                    if (Math.abs(ball.vy) < 0.05) ball.vy = 0;

                    pockets.forEach(pocket => {{
                        let distToPocket = Math.hypot(ball.x - pocket.x, ball.y - pocket.y);
                        if (distToPocket < POCKET_RADIUS) {{
                            if (ball.isCue) {{
                                ball.x = 180;
                                ball.y = 170;
                                ball.vx = 0;
                                ball.vy = 0;
                                whiteBallFoul = true;
                            }} else {{
                                ball.active = false;
                                ball.vx = 0;
                                ball.vy = 0;
                                ballInHoleThisTurn = true;
                                if (currentTurn === 1) score1++;
                                else score2++;
                            }}
                        }}
                    }});

                    if (ball.x - BALL_RADIUS < TABLE_X) {{ ball.x = TABLE_X + BALL_RADIUS; ball.vx *= -1; }}
                    if (ball.x + BALL_RADIUS > TABLE_X + TABLE_W) {{ ball.x = TABLE_X + TABLE_W - BALL_RADIUS; ball.vx *= -1; }}
                    if (ball.y - BALL_RADIUS < TABLE_Y) {{ ball.y = TABLE_Y + BALL_RADIUS; ball.vy *= -1; }}
                    if (ball.y + BALL_RADIUS > TABLE_Y + TABLE_H) {{ ball.y = TABLE_Y + TABLE_H - BALL_RADIUS; ball.vy *= -1; }}
                }});

                // Va chạm giữa các bi
                for (let i = 0; i < balls.length; i++) {{
                    for (let j = i + 1; j < balls.length; j++) {{
                        let b1 = balls[i];
                        let b2 = balls[j];
                        if (!b1.active || !b2.active) continue;

                        let dx = b2.x - b1.x;
                        let dy = b2.y - b1.y;
                        let dist = Math.hypot(dx, dy);

                        if (dist < BALL_RADIUS * 2) {{
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
                        }}
                    }}
                }}

                // Xử lý đổi lượt khi bóng dừng hẳn sau một cú đánh
                if (wasMoving && !moving) {{
                    if (!ballInHoleThisTurn || whiteBallFoul) {{
                        currentTurn = currentTurn === 1 ? 2 : 1;
                    }}
                    // Nếu ghi được điểm và không phạm lỗi, đội đó được đánh tiếp
                }}
                wasMoving = moving;
                updateScoreboard();
            }}

            function draw() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = '#0f6336';
                ctx.fillRect(TABLE_X, TABLE_Y, TABLE_W, TABLE_H);

                pockets.forEach(pocket => {{
                    ctx.beginPath();
                    ctx.arc(pocket.x, pocket.y, POCKET_RADIUS, 0, Math.PI * 2);
                    ctx.fillStyle = '#05180f';
                    ctx.fill();
                    ctx.lineWidth = 3;
                    ctx.strokeStyle = '#2b170c';
                    ctx.stroke();
                    ctx.closePath();
                }});

                const cue = balls.find(b => b.isCue);

                if (isDragging && cue.active && areBallsStopped()) {{
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
                }}

                balls.forEach(ball => {{
                    if (!ball.active) return;
                    
                    ctx.beginPath();
                    ctx.arc(ball.x, ball.y, BALL_RADIUS, 0, Math.PI * 2);
                    ctx.fillStyle = ball.color;
                    ctx.fill();
                    ctx.lineWidth = 1.2;
                    ctx.strokeStyle = '#000000';
                    ctx.stroke();
                    ctx.closePath();

                    if (!ball.isCue) {{
                        ctx.fillStyle = ball.textColor;
                        ctx.font = 'bold 10px sans-serif';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText(ball.number, ball.x, ball.y);
                    }}
                }});
            }}

            function loop() {{
                update();
                draw();
                requestAnimationFrame(loop);
            }}

            loop();
        </script>
    </body>
    </html>
    """

    st.components.v1.html(pool_game_html, height=460, scrolling=False)

    st.markdown("---")
    if st.button("🔄 Quay lại Menu / Đặt lại trận đấu"):
        st.session_state.game_started = False
        st.rerun()
