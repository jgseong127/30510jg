import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="NEON RHYTHM DUEL",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">

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
    background: #050510;
    color: white;
}

body {
    animation: backgroundShift 18s infinite alternate ease-in-out;
}

@keyframes backgroundShift {
    0% {
        background: radial-gradient(circle at top, #15154f, #050510 70%);
    }
    25% {
        background: radial-gradient(circle at top, #3b1250, #050510 70%);
    }
    50% {
        background: radial-gradient(circle at top, #073d4a, #050510 70%);
    }
    75% {
        background: radial-gradient(circle at top, #3a3210, #050510 70%);
    }
    100% {
        background: radial-gradient(circle at top, #17264d, #050510 70%);
    }
}

#game {
    width: 100vw;
    height: 100vh;
    position: relative;
    overflow: hidden;
}

/* ================= HUD ================= */

#topbar {
    position: absolute;
    top: 18px;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    padding: 0 45px;
    z-index: 100;
    pointer-events: none;
}

.player-score {
    width: 330px;
    padding: 18px;
    border-radius: 18px;
    background: rgba(0,0,0,0.35);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.15);
}

.p1 {
    box-shadow: 0 0 25px rgba(0,255,255,0.2);
}

.p2 {
    box-shadow: 0 0 25px rgba(255,0,200,0.2);
}

.player-name {
    font-size: 22px;
    font-weight: bold;
    letter-spacing: 2px;
}

.score {
    font-size: 35px;
    margin-top: 6px;
    font-weight: bold;
}

.combo {
    font-size: 20px;
    margin-top: 6px;
    color: #ffd800;
}

#timerBox {
    text-align: center;
    font-size: 26px;
    font-weight: bold;
    text-shadow: 0 0 15px white;
}

#difficulty {
    font-size: 14px;
    margin-top: 8px;
    color: #cccccc;
}

/* ================= PLAY AREA ================= */

#arena {
    position: absolute;
    top: 100px;
    width: 100%;
    height: calc(100% - 100px);
    display: flex;
    justify-content: space-around;
    perspective: 900px;
}

/* ================= PLAYER BOARD ================= */

.board {
    position: relative;
    width: 42%;
    height: 88%;
    transform: rotateX(18deg);
    transform-style: preserve-3d;
}

/* Lane area */

.lanes {
    position: absolute;
    width: 100%;
    height: 100%;
    display: flex;
    gap: 10px;
    padding: 0 20px;
}

.lane {
    position: relative;
    flex: 1;
    height: 100%;
    overflow: visible;

    background:
        linear-gradient(
            to bottom,
            rgba(255,255,255,0.03),
            rgba(0,0,0,0.4)
        );

    border-left: 1px solid rgba(255,255,255,0.15);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* ================= JUDGEMENT LINE ================= */

.judgement-line {
    position: absolute;
    bottom: 12%;
    width: 100%;
    height: 12px;

    background: white;

    box-shadow:
        0 0 8px white,
        0 0 20px #00ffff,
        0 0 45px #00ffff;

    z-index: 20;
}

/* ================= KEY LABEL ================= */

.key-label {
    position: absolute;
    bottom: 2%;
    width: 100%;
    display: flex;
    gap: 10px;
    padding: 0 20px;
    z-index: 40;
}

.key {
    flex: 1;
    height: 55px;

    display: flex;
    justify-content: center;
    align-items: center;

    font-size: 25px;
    font-weight: bold;

    border-radius: 12px;

    background: rgba(0,0,0,0.65);

    border: 2px solid rgba(255,255,255,0.4);

    transition: 0.08s;
}

.key.active {
    transform: scale(0.9);
    background: white;
    color: black;
    box-shadow: 0 0 25px white;
}

/* ================= TILE ================= */

.tile {
    position: absolute;

    width: calc(100% - 16px);
    left: 8px;

    height: 55px;

    border-radius: 12px;

    transform-style: preserve-3d;

    box-shadow:
        0 0 12px currentColor,
        0 0 30px currentColor;

    transition: transform 0.05s;
}

.tile::after {
    content: "";

    position: absolute;

    top: 6px;
    left: 6px;
    right: 6px;
    bottom: 6px;

    border-radius: 8px;

    background: rgba(255,255,255,0.3);
}

.tile.hit {
    animation: hitAnimation 0.25s forwards;
}

@keyframes hitAnimation {
    0% {
        transform: scale(1);
        opacity: 1;
    }

    100% {
        transform: scale(1.8);
        opacity: 0;
    }
}

/* ================= JUDGEMENT ================= */

.judge-text {
    position: absolute;

    left: 50%;
    top: 45%;

    transform: translate(-50%, -50%);

    font-size: 42px;
    font-weight: bold;

    opacity: 0;

    pointer-events: none;

    z-index: 200;

    text-shadow:
        0 0 10px white,
        0 0 30px currentColor;
}

.judge-text.show {
    animation: judgeAnimation 0.7s forwards;
}

@keyframes judgeAnimation {
    0% {
        opacity: 0;
        transform: translate(-50%, -40%) scale(0.7);
    }

    30% {
        opacity: 1;
        transform: translate(-50%, -50%) scale(1.2);
    }

    100% {
        opacity: 0;
        transform: translate(-50%, -70%) scale(1);
    }
}

/* ================= START SCREEN ================= */

#startScreen,
#resultScreen {
    position: absolute;

    z-index: 1000;

    width: 100%;
    height: 100%;

    display: flex;

    flex-direction: column;

    justify-content: center;
    align-items: center;

    background: rgba(0,0,10,0.82);

    backdrop-filter: blur(12px);
}

#resultScreen {
    display: none;
}

.title {
    font-size: 65px;
    font-weight: 900;
    letter-spacing: 8px;

    background: linear-gradient(
        90deg,
        #00ffff,
        #ff00ff,
        #ffff00
    );

    -webkit-background-clip: text;
    color: transparent;

    text-shadow: 0 0 30px rgba(0,255,255,0.3);
}

.subtitle {
    margin-top: 20px;
    font-size: 20px;
    color: #cccccc;
    text-align: center;
    line-height: 1.8;
}

.start-button {
    margin-top: 35px;

    padding: 18px 70px;

    border: none;

    border-radius: 15px;

    font-size: 25px;
    font-weight: bold;

    cursor: pointer;

    color: white;

    background:
        linear-gradient(
            90deg,
            #00bfff,
            #b000ff
        );

    box-shadow:
        0 0 25px #00bfff,
        0 0 50px #b000ff;

    transition: 0.2s;
}

.start-button:hover {
    transform: scale(1.08);
}

.instructions {
    margin-top: 30px;

    display: flex;

    gap: 80px;

    font-size: 18px;
}

.instructions div {
    text-align: center;
    line-height: 2;
}

/* ================= RESULT ================= */

#winner {
    font-size: 55px;
    margin-bottom: 20px;
}

.result-score {
    font-size: 25px;
    line-height: 2;
}

</style>
</head>

<body>

<div id="game">

    <!-- ================= START ================= -->

    <div id="startScreen">

        <div class="title">
            NEON RHYTHM DUEL
        </div>

        <div class="subtitle">
            1 VS 1 네온 리듬 배틀<br>
            약 1분 동안 더 높은 점수를 획득하세요!
        </div>

        <div class="instructions">

            <div>
                🔵 PLAYER 1<br>
                <b>Q &nbsp; W &nbsp; E &nbsp; R</b>
            </div>

            <div>
                🔴 PLAYER 2<br>
                <b>O &nbsp; P &nbsp; [ &nbsp; ]</b>
            </div>

        </div>

        <button class="start-button" onclick="startGame()">
            GAME START
        </button>

    </div>


    <!-- ================= RESULT ================= -->

    <div id="resultScreen">

        <div id="winner">
            PLAYER 1 WINS!
        </div>

        <div class="result-score" id="resultScore"></div>

        <button class="start-button" onclick="location.reload()">
            PLAY AGAIN
        </button>

    </div>


    <!-- ================= HUD ================= -->

    <div id="topbar">

        <div class="player-score p1">

            <div class="player-name">
                🔵 PLAYER 1
            </div>

            <div class="score" id="score1">
                0
            </div>

            <div class="combo">
                COMBO: <span id="combo1">0</span>
            </div>

        </div>


        <div id="timerBox">

            <div id="timer">
                01:00
            </div>

            <div id="difficulty">
                EASY
            </div>

        </div>


        <div class="player-score p2">

            <div class="player-name">
                🔴 PLAYER 2
            </div>

            <div class="score" id="score2">
                0
            </div>

            <div class="combo">
                COMBO: <span id="combo2">0</span>
            </div>

        </div>

    </div>


    <!-- ================= ARENA ================= -->

    <div id="arena">

        <!-- PLAYER 1 -->

        <div class="board" id="board1">

            <div class="lanes">

                <div class="lane"></div>
                <div class="lane"></div>
                <div class="lane"></div>
                <div class="lane"></div>

            </div>

            <div class="judgement-line"></div>

            <div class="key-label">

                <div class="key" id="key-q">Q</div>
                <div class="key" id="key-w">W</div>
                <div class="key" id="key-e">E</div>
                <div class="key" id="key-r">R</div>

            </div>

            <div class="judge-text" id="judge1"></div>

        </div>


        <!-- PLAYER 2 -->

        <div class="board" id="board2">

            <div class="lanes">

                <div class="lane"></div>
                <div class="lane"></div>
                <div class="lane"></div>
                <div class="lane"></div>

            </div>

            <div class="judgement-line"></div>

            <div class="key-label">

                <div class="key" id="key-o">O</div>
                <div class="key" id="key-p">P</div>
                <div class="key" id="key-[">[</div>
                <div class="key" id="key-]">]</div>

            </div>

            <div class="judge-text" id="judge2"></div>

        </div>

    </div>

</div>


<script>

/* =========================================================
   GAME SETTINGS
========================================================= */

const GAME_DURATION = 60;

const PLAYER1_KEYS = ["q", "w", "e", "r"];
const PLAYER2_KEYS = ["o", "p", "[", "]"];

const NEON_COLORS = [
    "#00ffff",
    "#ff00ff",
    "#00ff88",
    "#ffff00",
    "#ff6600",
    "#8a2bff"
];


/* =========================================================
   GAME STATE
========================================================= */

let gameStarted = false;

let startTime = 0;

let animationFrame;

let notes = [];

let audioContext;

let scores = {
    1: 0,
    2: 0
};

let combos = {
    1: 0,
    2: 0
};


/* =========================================================
   CREATE NOTE
========================================================= */

function createNote(player, lane, spawnTime) {

    const board = document.getElementById(
        player === 1 ? "board1" : "board2"
    );

    const lanes = board.querySelectorAll(".lane");

    const note = document.createElement("div");

    note.className = "tile";

    note.style.background =
        NEON_COLORS[Math.floor(Math.random() * NEON_COLORS.length)];

    note.style.color = note.style.background;

    lanes[lane].appendChild(note);

    const noteData = {

        player: player,

        lane: lane,

        spawnTime: spawnTime,

        duration: 2500,

        element: note,

        hit: false

    };

    notes.push(noteData);
}


/* =========================================================
   CREATE SONG / RHYTHM PATTERN
========================================================= */

function generateSong() {

    notes = [];

    const totalTime = GAME_DURATION * 1000;

    let time = 1000;

    while (time < totalTime) {

        let progress = time / totalTime;

        let interval;

        /*
            Difficulty increases gradually
        */

        if (progress < 0.25) {

            interval = 850;

        } else if (progress < 0.50) {

            interval = 650;

        } else if (progress < 0.75) {

            interval = 480;

        } else {

            interval = 330;

        }


        for (let player = 1; player <= 2; player++) {

            let lane = Math.floor(Math.random() * 4);

            createNote(
                player,
                lane,
                time
            );


            /*
                Mid game:
                sometimes two simultaneous notes
            */

            if (
                progress > 0.40 &&
                Math.random() < progress * 0.45
            ) {

                let secondLane;

                do {

                    secondLane =
                        Math.floor(Math.random() * 4);

                } while (secondLane === lane);

                createNote(
                    player,
                    secondLane,
                    time
                );
            }


            /*
                Late game:
                sometimes three notes
            */

            if (
                progress > 0.75 &&
                Math.random() < 0.30
            ) {

                let thirdLane;

                do {

                    thirdLane =
                        Math.floor(Math.random() * 4);

                } while (
                    thirdLane === lane
                );

                createNote(
                    player,
                    thirdLane,
                    time
                );
            }

        }

        time += interval;

    }

}


/* =========================================================
   AUDIO
========================================================= */

function initAudio() {

    audioContext =
        new (window.AudioContext || window.webkitAudioContext)();

}


function playTone(frequency, duration = 0.08, volume = 0.05) {

    if (!audioContext) return;

    const oscillator =
        audioContext.createOscillator();

    const gain =
        audioContext.createGain();

    oscillator.frequency.value = frequency;

    oscillator.type = "sine";

    gain.gain.value = volume;

    oscillator.connect(gain);

    gain.connect(audioContext.destination);

    oscillator.start();

    gain.gain.exponentialRampToValueAtTime(
        0.001,
        audioContext.currentTime + duration
    );

    oscillator.stop(
        audioContext.currentTime + duration
    );

}


function startBackgroundBeat() {

    const beatInterval = setInterval(() => {

        if (!gameStarted) {

            clearInterval(beatInterval);

            return;
        }

        playTone(110, 0.12, 0.04);

    }, 500);

}


/* =========================================================
   START GAME
========================================================= */

function startGame() {

    document.getElementById("startScreen")
        .style.display = "none";

    gameStarted = true;

    scores[1] = 0;
    scores[2] = 0;

    combos[1] = 0;
    combos[2] = 0;

    initAudio();

    generateSong();

    startTime = performance.now();

    startBackgroundBeat();

    gameLoop();

}


/* =========================================================
   GAME LOOP
========================================================= */

function gameLoop() {

    if (!gameStarted) return;

    const now = performance.now();

    const elapsed =
        now - startTime;

    const remaining =
        Math.max(
            0,
            GAME_DURATION * 1000 - elapsed
        );


    updateTimer(remaining);

    updateDifficulty(elapsed);


    notes.forEach(note => {

        if (note.hit) return;

        const noteStart =
            note.spawnTime - note.duration;

        const progress =
            (elapsed - noteStart) / note.duration;


        /*
            Before appearing
        */

        if (progress < 0) {

            note.element.style.display = "none";

            return;

        }


        note.element.style.display = "block";


        /*
            Perspective movement

            Start small and far away,
            become bigger near player.
        */

        const p =
            Math.min(
                Math.max(progress, 0),
                1.2
            );

        const scale =
            0.35 + p * 0.75;

        const y =
            5 + p * 82;


        note.element.style.top =
            y + "%";

        note.element.style.transform =
            `scale(${scale})`;


        /*
            Missed note
        */

        if (progress > 1.08) {

            note.hit = true;

            note.element.remove();

            registerMiss(note.player);

        }

    });


    if (elapsed >= GAME_DURATION * 1000) {

        endGame();

        return;

    }

    animationFrame =
        requestAnimationFrame(gameLoop);

}


/* =========================================================
   TIMER
========================================================= */

function updateTimer(remaining) {

    const totalSeconds =
        Math.ceil(remaining / 1000);

    const minutes =
        Math.floor(totalSeconds / 60);

    const seconds =
        totalSeconds % 60;

    document.getElementById("timer")
        .innerText =
            String(minutes).padStart(2, "0")
            + ":"
            + String(seconds).padStart(2, "0");

}


/* =========================================================
   DIFFICULTY
========================================================= */

function updateDifficulty(elapsed) {

    const progress =
        elapsed / (GAME_DURATION * 1000);

    let text;

    if (progress < 0.25) {

        text = "EASY";

    } else if (progress < 0.50) {

        text = "NORMAL";

    } else if (progress < 0.75) {

        text = "HARD";

    } else {

        text = "INSANE";

    }

    document.getElementById("difficulty")
        .innerText = text;

}


/* =========================================================
   KEYBOARD
========================================================= */

document.addEventListener("keydown", event => {

    if (!gameStarted) return;

    const key =
        event.key.toLowerCase();

    /*
        Prevent browser shortcuts / scrolling
    */

    if (
        PLAYER1_KEYS.includes(key) ||
        PLAYER2_KEYS.includes(key)
    ) {

        event.preventDefault();

    }


    if (PLAYER1_KEYS.includes(key)) {

        const lane =
            PLAYER1_KEYS.indexOf(key);

        activateKey(key);

        hitLane(1, lane);

    }


    if (PLAYER2_KEYS.includes(key)) {

        const lane =
            PLAYER2_KEYS.indexOf(key);

        activateKey(key);

        hitLane(2, lane);

    }

});


document.addEventListener("keyup", event => {

    const key =
        event.key.toLowerCase();

    const element =
        document.getElementById("key-" + key);

    if (element) {

        element.classList.remove("active");

    }

});


function activateKey(key) {

    const element =
        document.getElementById("key-" + key);

    if (element) {

        element.classList.add("active");

        setTimeout(() => {

            element.classList.remove("active");

        }, 80);

    }

}


/* =========================================================
   HIT SYSTEM
========================================================= */

function hitLane(player, lane) {

    const elapsed =
        performance.now() - startTime;


    /*
        Find notes in same lane
    */

    const candidates =
        notes.filter(note =>

            note.player === player &&

            note.lane === lane &&

            !note.hit

        );


    /*
        No tile = MISS
    */

    if (candidates.length === 0) {

        registerMiss(player);

        return;

    }


    /*
        Find closest note
    */

    candidates.sort((a, b) =>

        Math.abs(elapsed - a.spawnTime)
        -
        Math.abs(elapsed - b.spawnTime)

    );


    const note =
        candidates[0];


    const difference =
        Math.abs(
            elapsed - note.spawnTime
        );


    /*
        PERFECT
    */

    if (difference <= 90) {

        registerHit(
            player,
            note,
            "PERFECT",
            1000
        );

        return;

    }


    /*
        GREAT
    */

    if (difference <= 180) {

        registerHit(
            player,
            note,
            "GREAT",
            500
        );

        return;

    }


    /*
        Outside judgement area
    */

    registerMiss(player);

}


/* =========================================================
   HIT
========================================================= */

function registerHit(
    player,
    note,
    judgement,
    baseScore
) {

    note.hit = true;

    combos[player]++;


    /*
        Combo bonus
    */

    const comboBonus =
        combos[player] * 10;


    scores[player] +=
        baseScore + comboBonus;


    /*
        Animation
    */

    note.element.classList.add("hit");


    setTimeout(() => {

        if (note.element) {

            note.element.remove();

        }

    }, 250);


    showJudgement(
        player,
        judgement
    );


    /*
        Sound
    */

    if (judgement === "PERFECT") {

        playTone(660, 0.08, 0.08);

    } else {

        playTone(440, 0.08, 0.06);

    }


    updateScoreUI();

}


/* =========================================================
   MISS
========================================================= */

function registerMiss(player) {

    combos[player] = 0;

    showJudgement(
        player,
        "MISS"
    );

    playTone(120, 0.12, 0.04);

    updateScoreUI();

}


/* =========================================================
   SHOW JUDGEMENT
========================================================= */

function showJudgement(
    player,
    judgement
) {

    const element =
        document.getElementById(
            player === 1
                ? "judge1"
                : "judge2"
        );


    element.innerText =
        judgement;


    if (judgement === "PERFECT") {

        element.style.color =
            "#00ffff";

    }

    else if (judgement === "GREAT") {

        element.style.color =
            "#00ff88";

    }

    else {

        element.style.color =
            "#ff3355";

    }


    element.classList.remove("show");

    void element.offsetWidth;

    element.classList.add("show");

}


/* =========================================================
   UPDATE UI
========================================================= */

function updateScoreUI() {

    document.getElementById("score1")
        .innerText =
            scores[1].toLocaleString();


    document.getElementById("score2")
        .innerText =
            scores[2].toLocaleString();


    document.getElementById("combo1")
        .innerText =
            combos[1];


    document.getElementById("combo2")
        .innerText =
            combos[2];

}


/* =========================================================
   END GAME
========================================================= */

function endGame() {

    gameStarted = false;

    cancelAnimationFrame(animationFrame);


    const resultScreen =
        document.getElementById(
            "resultScreen"
        );


    const winner =
        document.getElementById(
            "winner"
        );


    if (scores[1] > scores[2]) {

        winner.innerText =
            "🔵 PLAYER 1 WINS!";

    }

    else if (scores[2] > scores[1]) {

        winner.innerText =
            "🔴 PLAYER 2 WINS!";

    }

    else {

        winner.innerText =
            "🤝 DRAW!";

    }


    document.getElementById("resultScore")
        .innerHTML = `

        🔵 PLAYER 1: 
        <b>${scores[1].toLocaleString()}</b>

        <br>

        🔴 PLAYER 2: 
        <b>${scores[2].toLocaleString()}</b>

        <br><br>

        최고 점수를 획득한 플레이어가 승리했습니다!

        `;


    resultScreen.style.display =
        "flex";

}

</script>

</body>
</html>
"""


components.html(
    GAME_HTML,
    height=850,
    scrolling=False
)
