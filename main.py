```python
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Neon Rhythm Duel",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html, body {
    width: 100%;
    height: 100%;
    overflow: hidden;
    font-family: Arial, sans-serif;
    background: #070711;
    color: white;
}

body {
    animation: bg 16s ease-in-out infinite alternate;
}

@keyframes bg {
    0% { background: radial-gradient(circle at top, #102a66, #070711 70%); }
    33% { background: radial-gradient(circle at top, #4a125c, #070711 70%); }
    66% { background: radial-gradient(circle at top, #075a5a, #070711 70%); }
    100% { background: radial-gradient(circle at top, #5a3b08, #070711 70%); }
}

#game {
    width: 100vw;
    height: 100vh;
    position: relative;
    overflow: hidden;
}

/* ===== MENU ===== */

.screen {
    position: absolute;
    inset: 0;
    z-index: 1000;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    background: rgba(0, 0, 15, 0.9);
}

#countdownScreen,
#resultScreen {
    display: none;
}

.title {
    font-size: 52px;
    font-weight: 900;
    text-align: center;

    background: linear-gradient(90deg, #00ffff, #ff00ff, #ffff00);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.subtitle {
    margin-top: 15px;
    text-align: center;
    color: #dddddd;
    line-height: 1.8;
}

.menu-title {
    margin-top: 25px;
    margin-bottom: 10px;
    text-align: center;
    color: #00ffff;
    font-size: 20px;
}

.button-row {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
}

.choice {
    padding: 12px 20px;
    border-radius: 10px;

    border: 1px solid #555;
    background: rgba(255,255,255,0.08);
    color: white;

    cursor: pointer;
    font-size: 15px;
}

.choice:hover {
    border-color: #00ffff;
}

.choice.selected {
    background: linear-gradient(90deg, #0066ff, #b000ff);
    box-shadow: 0 0 18px #00ffff;
}

.big-button {
    margin-top: 30px;
    padding: 15px 60px;

    border: none;
    border-radius: 14px;

    color: white;
    font-size: 22px;
    font-weight: bold;

    cursor: pointer;

    background: linear-gradient(90deg, #0099ff, #b000ff);
    box-shadow: 0 0 25px #00aaff;
}

#countdownNumber {
    font-size: 140px;
    font-weight: bold;
    text-shadow: 0 0 25px #00ffff, 0 0 60px #ff00ff;
}

/* ===== HUD ===== */

#hud {
    position: absolute;
    top: 15px;
    left: 0;
    width: 100%;

    display: flex;
    justify-content: space-between;

    padding: 0 30px;
    z-index: 100;
}

.player-panel {
    width: 260px;
    padding: 14px;

    background: rgba(0,0,0,0.45);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 15px;
}

.player-name {
    font-size: 18px;
    font-weight: bold;
}

.score {
    font-size: 30px;
    font-weight: bold;
    margin-top: 4px;
}

.combo {
    margin-top: 5px;
    color: #ffff00;
}

#gameInfo {
    text-align: center;
}

#timer {
    font-size: 28px;
    font-weight: bold;
}

#songText {
    color: #00ffff;
    margin-top: 4px;
}

/* ===== GAME BOARD ===== */

#arena {
    position: absolute;
    top: 110px;

    width: 100%;
    height: calc(100% - 110px);

    display: flex;
    justify-content: space-around;
}

.board {
    position: relative;

    width: 43%;
    height: 82%;

    transform: perspective(800px) rotateX(12deg);
}

.lanes {
    position: absolute;
    inset: 0;

    display: flex;
    gap: 8px;

    padding: 0 15px;
}

.lane {
    position: relative;
    flex: 1;

    background: linear-gradient(
        to bottom,
        rgba(255,255,255,0.05),
        rgba(0,0,0,0.55)
    );

    border-left: 1px solid rgba(255,255,255,0.18);
    border-right: 1px solid rgba(255,255,255,0.08);

    overflow: hidden;
}

/* 판정선 */

.judge-line {
    position: absolute;

    left: 0;
    bottom: 12%;

    width: 100%;
    height: 8px;

    background: white;

    box-shadow:
        0 0 10px white,
        0 0 25px #00ffff,
        0 0 45px #00ffff;

    z-index: 20;
}

/* 타일 */

.note {
    position: absolute;

    left: 8px;
    width: calc(100% - 16px);

    height: 42px;

    border-radius: 10px;

    box-shadow:
        0 0 12px currentColor,
        0 0 30px currentColor;
}

.note.hit {
    animation: hitAnim 0.2s forwards;
}

@keyframes hitAnim {
    from {
        opacity: 1;
        transform: scale(1);
    }
    to {
        opacity: 0;
        transform: scale(1.6);
    }
}

/* 키 */

.keys {
    position: absolute;

    bottom: 0;

    width: 100%;

    display: flex;
    gap: 8px;

    padding: 0 15px;

    z-index: 30;
}

.key {
    flex: 1;

    height: 52px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 10px;

    background: rgba(0,0,0,0.8);
    border: 2px solid rgba(255,255,255,0.4);

    font-size: 21px;
    font-weight: bold;
}

.key.active {
    background: white;
    color: black;
    transform: scale(0.92);
    box-shadow: 0 0 20px white;
}

/* 판정 글자 */

.judgement {
    position: absolute;

    top: 45%;
    left: 50%;

    transform: translate(-50%, -50%);

    font-size: 36px;
    font-weight: bold;

    opacity: 0;

    z-index: 50;
}

.judgement.show {
    animation: judgeAnim 0.6s forwards;
}

@keyframes judgeAnim {
    0% {
        opacity: 0;
        transform: translate(-50%, -40%) scale(0.8);
    }
    25% {
        opacity: 1;
        transform: translate(-50%, -50%) scale(1.15);
    }
    100% {
        opacity: 0;
        transform: translate(-50%, -70%) scale(1);
    }
}

#winner {
    font-size: 48px;
    margin-bottom: 20px;
}

.result {
    text-align: center;
    font-size: 24px;
    line-height: 2;
}
</style>
</head>

<body>

<div id="game">

    <!-- MENU -->
    <div class="screen" id="menuScreen">

        <div class="title">NEON RHYTHM DUEL</div>

        <div class="subtitle">
            PLAYER 1: Q W E R<br>
            PLAYER 2: O P [ ]
        </div>

        <div class="menu-title">🎵 SONG SELECT</div>

        <div class="button-row">
            <button class="choice song selected" data-song="Neon Drive">Neon Drive</button>
            <button class="choice song" data-song="Cyber Rush">Cyber Rush</button>
            <button class="choice song" data-song="Galaxy Beat">Galaxy Beat</button>
            <button class="choice song" data-song="Final Overload">Final Overload</button>
        </div>

        <div class="menu-title">⭐ DIFFICULTY</div>

        <div class="button-row">
            <button class="choice difficulty selected" data-difficulty="Easy">EASY</button>
            <button class="choice difficulty" data-difficulty="Normal">NORMAL</button>
            <button class="choice difficulty" data-difficulty="Hard">HARD</button>
            <button class="choice difficulty" data-difficulty="Expert">EXPERT</button>
        </div>

        <button class="big-button" id="startButton">READY!</button>

    </div>


    <!-- COUNTDOWN -->
    <div class="screen" id="countdownScreen">

        <div id="countdownNumber">3</div>

        <div class="subtitle">
            GET READY!
        </div>

    </div>


    <!-- RESULT -->
    <div class="screen" id="resultScreen">

        <div id="winner"></div>

        <div class="result" id="resultText"></div>

        <button class="big-button" onclick="location.reload()">
            PLAY AGAIN
        </button>

    </div>


    <!-- HUD -->

    <div id="hud">

        <div class="player-panel">

            <div class="player-name">🔵 PLAYER 1</div>

            <div class="score" id="score1">0</div>

            <div class="combo">
                COMBO: <span id="combo1">0</span>
            </div>

        </div>


        <div id="gameInfo">

            <div id="timer">01:00</div>

            <div id="songText">Neon Drive</div>

            <div id="difficultyText">EASY</div>

        </div>


        <div class="player-panel">

            <div class="player-name">🔴 PLAYER 2</div>

            <div class="score" id="score2">0</div>

            <div class="combo">
                COMBO: <span id="combo2">0</span>
            </div>

        </div>

    </div>


    <!-- ARENA -->

    <div id="arena">

        <!-- PLAYER 1 -->

        <div class="board" id="board1">

            <div class="lanes">

                <div class="lane"></div>
                <div class="lane"></div>
                <div class="lane"></div>
                <div class="lane"></div>

            </div>

            <div class="judge-line"></div>

            <div class="keys">

                <div class="key" id="key-q">Q</div>
                <div class="key" id="key-w">W</div>
                <div class="key" id="key-e">E</div>
                <div class="key" id="key-r">R</div>

            </div>

            <div class="judgement" id="judge1"></div>

        </div>


        <!-- PLAYER 2 -->

        <div class="board" id="board2">

            <div class="lanes">

                <div class="lane"></div>
                <div class="lane"></div>
                <div class="lane"></div>
                <div class="lane"></div>

            </div>

            <div class="judge-line"></div>

            <div class="keys">

                <div class="key" id="key-o">O</div>
                <div class="key" id="key-p">P</div>
                <div class="key" id="key-left">[</div>
                <div class="key" id="key-right">]</div>

            </div>

            <div class="judgement" id="judge2"></div>

        </div>

    </div>

</div>


<script>

/* =========================
   GAME DATA
========================= */

const GAME_TIME = 60;

const P1_KEYS = ["q", "w", "e", "r"];

const P2_KEYS = ["o", "p", "[", "]"];

const COLORS = [
    "#00ffff",
    "#ff00ff",
    "#00ff88",
    "#ffff00",
    "#ff6600",
    "#8a2bff"
];

const SONGS = {
    "Neon Drive": 100,
    "Cyber Rush": 112,
    "Galaxy Beat": 125,
    "Final Overload": 138
};

const DIFFICULTIES = {

    Easy: {
        spacing: 1.55,
        doubleChance: 0.02
    },

    Normal: {
        spacing: 1.30,
        doubleChance: 0.08
    },

    Hard: {
        spacing: 1.08,
        doubleChance: 0.18
    },

    Expert: {
        spacing: 0.90,
        doubleChance: 0.32
    }
};


/* =========================
   STATE
========================= */

let selectedSong = "Neon Drive";
let selectedDifficulty = "Easy";

let running = false;
let startTime = 0;

let notes = [];

let score1 = 0;
let score2 = 0;

let combo1 = 0;
let combo2 = 0;


/* =========================
   MENU
========================= */

document.querySelectorAll(".song").forEach(button => {

    button.addEventListener("click", () => {

        document.querySelectorAll(".song").forEach(b => {
            b.classList.remove("selected");
        });

        button.classList.add("selected");

        selectedSong = button.dataset.song;

    });

});


document.querySelectorAll(".difficulty").forEach(button => {

    button.addEventListener("click", () => {

        document.querySelectorAll(".difficulty").forEach(b => {
            b.classList.remove("selected");
        });

        button.classList.add("selected");

        selectedDifficulty = button.dataset.difficulty;

    });

});


document.getElementById("startButton").addEventListener(
    "click",
    countdown
);


/* =========================
   COUNTDOWN
========================= */

function countdown() {

    document.getElementById("menuScreen").style.display = "none";

    document.getElementById("countdownScreen").style.display = "flex";

    let number = 3;

    const element =
        document.getElementById("countdownNumber");

    element.textContent = number;

    const timer = setInterval(() => {

        number--;

        if (number > 0) {

            element.textContent = number;

        } else if (number === 0) {

            element.textContent = "GO!";

        } else {

            clearInterval(timer);

            document.getElementById("countdownScreen").style.display = "none";

            startGame();

        }

    }, 1000);

}


/* =========================
   START GAME
========================= */

function startGame() {

    running = true;

    notes = [];

    score1 = 0;
    score2 = 0;

    combo1 = 0;
    combo2 = 0;

    updateUI();

    document.getElementById("songText").textContent =
        selectedSong;

    document.getElementById("difficultyText").textContent =
        selectedDifficulty.toUpperCase();

    generateNotes();

    startTime = performance.now();

    gameLoop();

}


/* =========================
   GENERATE NOTES
========================= */

function generateNotes() {

    const bpm = SONGS[selectedSong];

    const settings =
        DIFFICULTIES[selectedDifficulty];

    const beat =
        60000 / bpm;

    let time = 2500;

    while (time < GAME_TIME * 1000) {

        const progress =
            time / (GAME_TIME * 1000);

        const interval =
            beat * settings.spacing;

        for (let player = 1; player <= 2; player++) {

            const lane =
                Math.floor(Math.random() * 4);

            createNote(player, lane, time);

            if (
                progress > 0.5 &&
                Math.random() <
                settings.doubleChance * progress
            ) {

                let lane2;

                do {

                    lane2 =
                        Math.floor(Math.random() * 4);

                } while (lane2 === lane);

                createNote(
                    player,
                    lane2,
                    time
                );

            }

        }

        time += interval;

    }

}


function createNote(player, lane, hitTime) {

    const board =
        document.getElementById(
            player === 1
                ? "board1"
                : "board2"
        );

    const lanes =
        board.querySelectorAll(".lane");

    const element =
        document.createElement("div");

    element.className = "note";

    const color =
        COLORS[
            Math.floor(Math.random() * COLORS.length)
        ];

    element.style.background = color;

    element.style.color = color;

    element.style.display = "none";

    lanes[lane].appendChild(element);

    notes.push({
        player: player,
        lane: lane,
        hitTime: hitTime,
        element: element,
        hit: false,
        travelTime: 1700
    });

}


/* =========================
   GAME LOOP
========================= */

function gameLoop() {

    if (!running) return;

    const elapsed =
        performance.now() - startTime;

    const remaining =
        Math.max(
            0,
            GAME_TIME * 1000 - elapsed
        );

    updateTimer(remaining);


    notes.forEach(note => {

        if (note.hit) return;

        const appearTime =
            note.hitTime - note.travelTime;

        const progress =
            (elapsed - appearTime) /
            note.travelTime;

        if (progress < 0) {

            note.element.style.display = "none";

            return;

        }

        note.element.style.display = "block";

        const p =
            Math.min(
                Math.max(progress, 0),
                1.15
            );

        const scale =
            0.35 + p * 0.70;

        const y =
            2 + p * 78;

        note.element.style.top =
            y + "%";

        note.element.style.transform =
            "scale(" + scale + ")";


        /* 자동 MISS */

        if (progress > 1.12) {

            note.hit = true;

            if (note.element.parentNode) {
                note.element.remove();
            }

            miss(note.player);

        }

    });


    if (elapsed >= GAME_TIME * 1000) {

        endGame();

        return;

    }

    requestAnimationFrame(gameLoop);

}


/* =========================
   TIMER
========================= */

function updateTimer(remaining) {

    const seconds =
        Math.ceil(remaining / 1000);

    const minutes =
        Math.floor(seconds / 60);

    const secs =
        seconds % 60;

    document.getElementById("timer").textContent =
        String(minutes).padStart(2, "0")
        +
        ":"
        +
        String(secs).padStart(2, "0");

}


/* =========================
   KEY INPUT
========================= */

document.addEventListener("keydown", event => {

    if (!running) return;

    if (event.repeat) return;

    const key =
        event.key.toLowerCase();


    if (
        P1_KEYS.includes(key) ||
        P2_KEYS.includes(key)
    ) {

        event.preventDefault();

    }


    if (P1_KEYS.includes(key)) {

        activateKey(key);

        hitNote(
            1,
            P1_KEYS.indexOf(key)
        );

    }


    if (P2_KEYS.includes(key)) {

        activateKey(key);

        hitNote(
            2,
            P2_KEYS.indexOf(key)
        );

    }

});


document.addEventListener("keyup", event => {

    deactivateKey(
        event.key.toLowerCase()
    );

});


function getKeyElement(key) {

    if (key === "[") {
        return document.getElementById("key-left");
    }

    if (key === "]") {
        return document.getElementById("key-right");
    }

    return document.getElementById(
        "key-" + key
    );

}


function activateKey(key) {

    const element =
        getKeyElement(key);

    if (element) {

        element.classList.add("active");

    }

}


function deactivateKey(key) {

    const element =
        getKeyElement(key);

    if (element) {

        element.classList.remove("active");

    }

}


/* =========================
   HIT DETECTION
========================= */

function hitNote(player, lane) {

    const elapsed =
        performance.now() - startTime;


    const possible =
        notes.filter(note => {

            return (
                note.player === player &&
                note.lane === lane &&
                !note.hit
            );

        });


    /* 빈 칸을 누르면 MISS */

    if (possible.length === 0) {

        miss(player);

        return;

    }


    possible.sort((a, b) => {

        return (
            Math.abs(elapsed - a.hitTime)
            -
            Math.abs(elapsed - b.hitTime)
        );

    });


    const note =
        possible[0];

    const difference =
        Math.abs(
            elapsed - note.hitTime
        );


    if (difference <= 120) {

        hit(
            player,
            note,
            "PERFECT",
            1000
        );

    }

    else if (difference <= 240) {

        hit(
            player,
            note,
            "GREAT",
            600
        );

    }

    else {

        miss(player);

    }

}


/* =========================
   SUCCESS
========================= */

function hit(player, note, text, points) {

    note.hit = true;


    if (player === 1) {

        combo1++;

        score1 +=
            points +
            Math.min(combo1 * 15, 1000);

    } else {

        combo2++;

        score2 +=
            points +
            Math.min(combo2 * 15, 1000);

    }


    note.element.classList.add("hit");


    setTimeout(() => {

        if (note.element.parentNode) {
            note.element.remove();
        }

    }, 200);


    showJudge(player, text);

    updateUI();

}


/* =========================
   MISS
========================= */

function miss(player) {

    if (player === 1) {

        combo1 = 0;

    } else {

        combo2 = 0;

    }

    showJudge(player, "MISS");

    updateUI();

}


/* =========================
   JUDGEMENT
========================= */

function showJudge(player, text) {

    const element =
        document.getElementById(
            player === 1
                ? "judge1"
                : "judge2"
        );

    element.textContent = text;


    if (text === "PERFECT") {

        element.style.color = "#00ffff";

    }

    else if (text === "GREAT") {

        element.style.color = "#00ff88";

    }

    else {

        element.style.color = "#ff3355";

    }


    element.classList.remove("show");

    void element.offsetWidth;

    element.classList.add("show");

}


/* =========================
   UI
========================= */

function updateUI() {

    document.getElementById("score1").textContent =
        score1.toLocaleString();

    document.getElementById("score2").textContent =
        score2.toLocaleString();

    document.getElementById("combo1").textContent =
        combo1;

    document.getElementById("combo2").textContent =
        combo2;

}


/* =========================
   END GAME
========================= */

function endGame() {

    running = false;

    const winner =
        document.getElementById("winner");


    if (score1 > score2) {

        winner.textContent =
            "🔵 PLAYER 1 WINS!";

    }

    else if (score2 > score1) {

        winner.textContent =
            "🔴 PLAYER 2 WINS!";

    }

    else {

        winner.textContent =
            "🤝 DRAW!";

    }


    document.getElementById("resultText").innerHTML =

        "🎵 " + selectedSong +

        "<br>⭐ " + selectedDifficulty +

        "<br><br>" +

        "🔵 PLAYER 1 SCORE: <b>" +
        score1.toLocaleString() +
        "</b>" +

        "<br>" +

        "🔴 PLAYER 2 SCORE: <b>" +
        score2.toLocaleString() +
        "</b>";


    document.getElementById("resultScreen").style.display =
        "flex";

}

</script>

</body>
</html>
"""

components.html(
    GAME_HTML,
    height=900,
    scrolling=False
)
```
