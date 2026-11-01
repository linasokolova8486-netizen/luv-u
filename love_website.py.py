
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

# =====================================
# НАСТРОЙКИ
# =====================================

st.set_page_config(
    page_title="For You ❤️",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================
# ПОИСК МУЗЫКИ
# =====================================

song_path = Path(__file__).parent / "song.mp3"

if song_path.exists():
    audio_data = base64.b64encode(
        song_path.read_bytes()
    ).decode("utf-8")

    audio_source = f"data:audio/mpeg;base64,{audio_data}"
else:
    audio_source = ""
    st.error(
        "Не найден song.mp3. Положи файл song.mp3 в ту же папку, "
        "где находится love_website.py.py."
    )

# =====================================
# СКРЫВАЕМ ИНТЕРФЕЙС STREAMLIT
# =====================================

st.markdown("""
<style>
    #MainMenu,
    header,
    footer,
    [data-testid="stHeader"],
    [data-testid="stToolbar"] {
        display: none !important;
    }

    .stApp {
        background: #030205;
    }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    iframe {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# САЙТ И АНИМАЦИЯ
# =====================================

html_code = r"""
<!DOCTYPE html>
<html lang="ru">

<head>
<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<style>

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #030205;
    font-family: Georgia, serif;
}

#screen {
    position: relative;
    width: 100%;
    height: 100vh;
    min-height: 650px;
    background:
        radial-gradient(
            ellipse at center,
            #100510 0%,
            #060308 55%,
            #020103 100%
        );
    overflow: hidden;
}

canvas {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
}

#start {
    position: absolute;
    inset: 0;
    z-index: 10;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    background: #030205;
    cursor: pointer;
    transition: opacity 1.5s ease;
}

#startText {
    color: #ffb4d2;
    font-size: clamp(25px, 5vw, 40px);
    text-shadow:
        0 0 10px #ff347e,
        0 0 30px #ff176c,
        0 0 60px #ff176c;
    animation: glow 2s infinite alternate;
    text-align: center;
    padding: 20px;
}

#startHint {
    margin-top: 20px;
    color: #a77b91;
    font-size: 13px;
    letter-spacing: 4px;
    animation: blink 2s infinite;
}

@keyframes glow {
    from {
        text-shadow: 0 0 10px #ff347e;
        transform: scale(1);
    }

    to {
        text-shadow:
            0 0 20px #ff347e,
            0 0 50px #ff176c;
        transform: scale(1.04);
    }
}

@keyframes blink {
    0%, 100% { opacity: 0.35; }
    50% { opacity: 1; }
}

#message {
    position: absolute;
    z-index: 4;
    width: 100%;
    top: 53%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    opacity: 0;
    transition: opacity 3s ease;
    pointer-events: none;
}

#message h1 {
    color: #ffd1e4;
    font-size: clamp(27px, 5vw, 45px);
    text-shadow:
        0 0 12px #ff2676,
        0 0 35px #ff176c;
    margin-bottom: 18px;
}

#message h2 {
    color: #fff0f7;
    font-size: clamp(18px, 3.5vw, 27px);
    line-height: 1.5;
    text-shadow: 0 0 15px #ff438c;
}

#message p {
    color: #ff91ba;
    font-size: 13px;
    letter-spacing: 4px;
    margin-top: 22px;
    text-shadow: 0 0 15px #ff438c;
}

#musicLabel {
    position: absolute;
    bottom: 25px;
    left: 0;
    width: 100%;
    text-align: center;
    color: #a77b91;
    font-size: 12px;
    letter-spacing: 3px;
    opacity: 0;
    transition: opacity 2s;
    z-index: 5;
}

</style>
</head>

<body>

<div id="screen">

    <canvas id="canvas"></canvas>

    <div id="start">
        <div id="startText">
            Нажми на меня ❤️
        </div>

        <div id="startHint">
            JUST FOR YOU
        </div>
    </div>

    <div id="message">

        <h1>Люблю тебя ❤️</h1>

        <h2>
            Ты для меня<br>
            самая особенная
        </h2>

        <p>✨ YOU ARE MY UNIVERSE ✨</p>

    </div>

    <div id="musicLabel">
        ♫ LET THE WORLD BURN
    </div>

</div>

<audio id="music" preload="auto" src="__AUDIO_SRC__"></audio>

<script>

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const startScreen = document.getElementById("start");
const message = document.getElementById("message");
const musicLabel = document.getElementById("musicLabel");
const music = document.getElementById("music");

let width;
let height;
let started = false;
let startTime = 0;
let animationFrame;

let boundary = [];
let inside = [];
let stars = [];
let floatingHearts = [];

const random = (min, max) =>
    Math.random() * (max - min) + min;

// =====================================
// РАЗМЕР ЭКРАНА
// =====================================

function resize() {

    const dpr = Math.min(
        window.devicePixelRatio || 1,
        2
    );

    width = window.innerWidth;
    height = window.innerHeight;

    canvas.width = width * dpr;
    canvas.height = height * dpr;

    canvas.style.width = width + "px";
    canvas.style.height = height + "px";

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    createScene();
}

window.addEventListener("resize", resize);

// =====================================
// ФОРМА СЕРДЦА
// =====================================

function heartPoint(t) {

    return {
        x: 16 * Math.pow(Math.sin(t), 3),

        y: -(
            13 * Math.cos(t)
            - 5 * Math.cos(2 * t)
            - 2 * Math.cos(3 * t)
            - Math.cos(4 * t)
        )
    };
}

// =====================================
// СОЗДАНИЕ ЧАСТИЦ
// =====================================

function createScene() {

    boundary = [];
    inside = [];
    stars = [];
    floatingHearts = [];

    // Контур сердца
    const outlineCount = 520;

    for (let i = 0; i < outlineCount; i++) {

        const t = (i / outlineCount) * Math.PI * 2;

        const p = heartPoint(t);

        boundary.push({
            x: p.x,
            y: p.y,
            delay: (i / outlineCount) * 7,
            size: random(1.2, 2.8),
            color: Math.random() > 0.5
                ? "#ff3c82"
                : "#ffb0d0",
            phase: random(0, 10)
        });
    }

    // Частицы внутри сердца
    for (let i = 0; i < 1000; i++) {

        const t = random(0, Math.PI * 2);
        const r = Math.sqrt(Math.random());

        const p = heartPoint(t);

        inside.push({
            x: p.x * r,
            y: p.y * r,
            delay: 7.3 + random(0, 2.2),
            size: random(0.7, 2.3),
            color: Math.random() > 0.5
                ? "#ff4b91"
                : "#ffc1dc",
            phase: random(0, 10)
        });
    }

    // Звёзды
    for (let i = 0; i < 150; i++) {

        stars.push({
            x: random(0, width),
            y: random(0, height),
            size: random(0.5, 2),
            phase: random(0, 10),
            speed: random(1, 4)
        });
    }

    // Маленькие сердечки
    for (let i = 0; i < 35; i++) {

        floatingHearts.push({
            x: random(0, width),
            y: random(0, height),
            size: random(7, 16),
            speed: random(0.2, 0.65),
            phase: random(0, 10)
        });
    }
}

// =====================================
// КООРДИНАТЫ СЕРДЦА
// =====================================

function getScale() {

    return Math.min(
        width / 43,
        height / 43
    ) * 0.82;
}

function heartPosition(x, y) {

    const scale = getScale();

    return {
        x: width / 2 + x * scale,
        y: height / 2 - 15 + y * scale
    };
}

// =====================================
// РИСОВАНИЕ ЧАСТИЦ
// =====================================

function drawParticle(p, elapsed, isInside) {

    if (elapsed < p.delay) return;

    const progress = Math.min(
        1,
        (elapsed - p.delay) / 0.65
    );

    const target = heartPosition(p.x, p.y);

    const originX = width / 2;
    const originY = height / 2;

    const x = originX +
        (target.x - originX) * progress;

    const y = originY +
        (target.y - originY) * progress;

    const twinkle =
        0.65 + 0.35 * Math.sin(
            elapsed * 3 + p.phase
        );

    ctx.globalAlpha = progress * twinkle;

    ctx.fillStyle = p.color;
    ctx.shadowBlur = isInside ? 7 : 13;
    ctx.shadowColor = p.color;

    ctx.beginPath();

    ctx.arc(
        x,
        y,
        p.size,
        0,
        Math.PI * 2
    );

    ctx.fill();
}

// =====================================
// ЗВЁЗДОЧКИ
// =====================================

function drawStars(elapsed) {

    stars.forEach(star => {

        const alpha = 0.3 +
            0.7 * (
                (Math.sin(elapsed * star.speed + star.phase) + 1) / 2
            );

        ctx.globalAlpha = alpha;
        ctx.fillStyle = "#ffffff";
        ctx.shadowBlur = 8;
        ctx.shadowColor = "#ffb0d0";

        ctx.beginPath();

        ctx.arc(
            star.x,
            star.y,
            star.size,
            0,
            Math.PI * 2
        );

        ctx.fill();
    });
}

// =====================================
// МАЛЕНЬКИЕ СЕРДЕЧКИ
// =====================================

function drawFloatingHearts(elapsed) {

    floatingHearts.forEach(heart => {

        heart.y -= heart.speed;

        heart.x += Math.sin(
            elapsed + heart.phase
        ) * 0.35;

        if (heart.y < -30) {
            heart.y = height + 30;
            heart.x = random(0, width);
        }

        ctx.globalAlpha = 0.4;
        ctx.fillStyle = "#ff5b98";
        ctx.font = heart.size + "px Arial";
        ctx.shadowBlur = 12;
        ctx.shadowColor = "#ff176c";

        ctx.fillText(
            "♥",
            heart.x,
            heart.y
        );
    });
}

// =====================================
// ОСНОВНАЯ АНИМАЦИЯ
// =====================================

function animate(timestamp) {

    if (!started) return;

    if (!startTime) {
        startTime = timestamp;
    }

    const elapsed = (timestamp - startTime) / 1000;

    ctx.clearRect(0, 0, width, height);

    drawStars(elapsed);

    // Сначала рисуется контур
    boundary.forEach(p => {
        drawParticle(p, elapsed, false);
    });

    // Затем заполняется сердце
    inside.forEach(p => {
        drawParticle(p, elapsed, true);
    });

    // Пульсация после прорисовки
    if (elapsed > 10) {

        const pulse =
            1 + Math.sin(elapsed * 2) * 0.018;

        // Небольшое свечение вокруг сердца
        const scale = getScale();

        const glow = ctx.createRadialGradient(
            width / 2,
            height / 2 - 15,
            5,
            width / 2,
            height / 2 - 15,
            260 * scale / 13
        );

        glow.addColorStop(0, "rgba(255, 20, 100, 0.035)");
        glow.addColorStop(1, "rgba(255, 20, 100, 0)");

        ctx.fillStyle = glow;
        ctx.fillRect(0, 0, width, height);

        ctx.globalAlpha = 1;

        ctx.save();

        ctx.translate(width / 2, height / 2 - 15);
        ctx.scale(pulse, pulse);
        ctx.translate(-width / 2, -(height / 2 - 15));

        boundary.forEach(p => {
            if (elapsed > 10) {
                const pos = heartPosition(p.x, p.y);

                ctx.fillStyle = p.color;
                ctx.globalAlpha = 0.55;
                ctx.shadowBlur = 8;
                ctx.shadowColor = p.color;

                ctx.beginPath();
                ctx.arc(
                    pos.x,
                    pos.y,
                    p.size * 0.5,
                    0,
                    Math.PI * 2
                );
                ctx.fill();
            }
        });

        ctx.restore();
    }

    ctx.globalAlpha = 1;
    ctx.shadowBlur = 0;

    drawFloatingHearts(elapsed);

    // Показываем надписи после рисования
    if (elapsed > 9.5) {
        message.style.opacity = "1";
        musicLabel.style.opacity = "1";
    }

    animationFrame = requestAnimationFrame(animate);
}

// =====================================
// НАЖАТИЕ НА СТАРТОВЫЙ ЭКРАН
// =====================================


startScreen.addEventListener("click", () => {

    if (started) return;

    started = true;

    startScreen.style.opacity = "0";

    setTimeout(() => {
        startScreen.style.display = "none";
    }, 1500);

    // ВАЖНО: play() вызывается сразу внутри клика.
    // Если сначала ждать loadedmetadata через await,
    // браузер может потерять разрешение на запуск звука.
    if (music.src) {
        try {
            music.currentTime = 45;

            const playRequest = music.play();

            if (playRequest !== undefined) {
                playRequest.catch((error) => {
                    console.error("Ошибка запуска музыки:", error);
                    alert("Браузер не смог запустить музыку: " + error.message);
                });
            }

        } catch (error) {
            console.error("Ошибка музыки:", error);
            alert("Не удалось запустить песню: " + error.message);
        }
    } else {
        alert("Не найден файл song.mp3 рядом с файлом love_website.py.py!");
    }

    startTime = 0;
    animationFrame = requestAnimationFrame(animate);

});

// =====================================
// ЗАПУСК
// =====================================

resize();

</script>

</body>
</html>
"""

# Подставляем аудиофайл
html_code = html_code.replace(
    "__AUDIO_SRC__",
    audio_source
)

# Показываем сайт
components.html(
    html_code,
    height=760,
    scrolling=False
)
