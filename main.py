```python
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Neon Rhythm Duel",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

html_code = r"""
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
    background: #080818;
    color: white;
}

body {
    animation: bgChange 15s infinite alternate ease-in-out;
}

@keyframes bgChange {
    0% {
        background: radial-gradient(circle at top, #102060, #050510 70%);
    }
    25% {
        background: radial-gradient(circle at top, #501050, #050510 70%);
    }
    50% {
        background: radial-gradient(circle at top, #005050, #050510 70%);
    }
    75% {
        background: radial-gradient(circle at top, #504000, #050510 70%);
    }
    100% {
        background: radial-gradient(circle at top, #202060, #050510 70%);
    }
}

/* 전체 게임 */

#game {
    width: 100vw;
    height: 100vh;
    position: relative;
    overflow: hidden;
}

/* 메뉴 */

.screen {
    position: absolute;
    width: 100%;
    height: 100%;
    z-index: 1000;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    background: rgba(0, 0, 15, 0.88);
    backdrop-filter: blur(10px);
}

#countdownScreen,
#resultScreen {
    display: none;
}

.title {
    font-size: 58px;
    font-weight: 900;
    letter-spacing: 5px;

    background: linear-gradient(
        90deg,
        #00ffff,
        #ff00ff,
        #ffff00
    );

    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;

    text-align: center;
}

.subtitle {
    margin-top: 15px;
    color: #dddddd;
    text-align: center;
    line-height: 1.8;
}

/* 선택 메뉴 */

.menu-section {
    margin-top: 25px;
    text-align: center;
}

.menu-title {
    margin-bottom: 12px;
    font-size: 20px;
    color: #00ffff;
}

.button-row {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
}

.select-button {
    padding: 13px 22px;

    border-radius: 12px;

    border: 1px solid rgba(255,255,255,0.3);

    background: rgba(255,255,255,0.08);

    color: white;

    cursor: pointer;

    font-size: 16px;

    transition: 0.2s;
}

.select-button:hover {
    transform: scale(1.05);
    border-color: #00ffff;
}

.select-button.selected {
    background: linear-gradient(
        90deg,
        #0088ff,
        #b000ff
    );

    box-shadow:
        0 0 15px #00ffff,
        0 0 30px #b000ff;
}

.start-button {
    margin-top: 30px;

    padding: 16px 65px;

    border: none;

    border-radius: 15px;

    color: white;

    font-size: 22px;
    font-weight: bold;

    cursor: pointer;

    background: linear-gradient(
        90deg,
        #00aaff,
        #b000ff
    );

    box-shadow:
        0 0 20px #00aaff,
        0 0 40px #b000ff;

    transition: 0.2s;
}

.start-button:hover {
    transform: scale(1.08);
}

/* 카운트다운 */

#countdownNumber {
    font-size: 150px;
    font-weight: bold;

    text-shadow:
        0 0 25px #00ffff,
        0 0 60px #ff00ff;
}

/* 상단 점수판 */

#topbar {
    position: absolute;

    top: 15px;
    left: 0;

    width: 100%;

    padding: 0 35px;

    display: flex;
    justify-content: space-between;

    z-index: 100;
}

.player-box {
    width: 280px;

    padding: 15px;

    border-radius: 16px;

    background: rgba(0,0,0,0.45);

    border: 1px solid rgba(255,255,255,0.2);

    backdrop-filter: blur(10px);
}

.player1 {
    box-shadow: 0 0 20px rgba(0,255,255,0.25);
}

.player2 {
    box-shadow: 0 0 20px rgba(255,0,255,0.25);
}

.player-name {
    font-size: 19px;
    font-weight: bold;
}

.score {
    font-size: 30px;
    font-weight: bold;

    margin-top: 5px;
}

.combo {
    color: #ffff00;
    margin-top: 5px;
}

#centerInfo {
    text-align: center;
}

#timer {
    font-size: 28px;
    font-weight: bold;
}

#songDisplay {
    margin-top: 5px;
    color: #00ffff;
}

#difficultyDisplay {
    margin-top: 4px;
    color: #dddddd;
}

/* 게임판 */

#arena {
    position: absolute;

    top: 110px;

    width: 100%;
    height: calc(100% - 110px);

    display: flex;

    justify-content: space-around;

    perspective: 900px;
}

.board {
    position: relative;

    width: 43%;
    height: 85%;

    transform: rotateX(14deg);
    transform-style: preserve-3d;
}

.lanes {
    position: absolute;

    width: 100%;
    height: 100%;

    display: flex;

    gap: 8px;

    padding: 0 15px;
}

.lane {
    position: relative;

    flex: 1;

    height: 100%;

    background: linear-gradient(
        to bottom,
        rgba(255,255,255,0.04),
        rgba(0,0,0,0.45)
    );

    border-left:
        1px solid rgba(255,255,255,0.15);

    border-right:
        1px solid rgba(255,255,255,0.08);

    overflow: visible;
}

/* 판정선 */

.judgement-line {
    position: absolute;

    bottom: 12%;

    width: 100%;
    height: 10px;

    background: white;

    box-shadow:
        0 0 8px white,
        0 0 20px #00ffff,
        0 0 40px #00ffff;

    z-index: 30;
}

/* 타일 */

.tile {
    position: absolute;

    left: 7px;

    width: calc(100% - 14px);

    height: 45px;

    border-radius: 10px;

    box-shadow:
        0 0 10px currentColor,
        0 0 28px currentColor;

    z-index: 15;

    will-change: transform, top;
}

.tile::after {
    content: "";

    position: absolute;

    top: 5px;
    left: 5px;
    right: 5px;
    bottom: 5px;

    border-radius: 7px;

    background: rgba(255,255,255,0.25);
}

.tile.hit {
    animation: tileHit 0.25s forwards;
}

@keyframes tileHit {
    from {
        transform: scale(1);
        opacity: 1;
    }

    to {
        transform: scale(1.7);
        opacity: 0;
    }
}

/* 키 */

.key-row {
    position: absolute;

    bottom: 1%;

    width: 100%;

    padding: 0 15px;

    display: flex;

    gap: 8px;

    z-index: 50;
}

.key-box {
    flex: 1;

    height: 52px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 10px;

    background: rgba(0,0,0,0.75);

    border: 2px solid rgba(255,255,255,0.35);

    font-size: 22px;
    font-weight: bold;

    transition: 0.08s;
}

.key-box.active {
    transform: scale(0.92);

    background: white;

    color: black;

    box-shadow: 0 0 25px white;
}

/* 판정 */

.judge-text {
    position: absolute;

    left: 50%;
    top: 48%;

    transform: translate(-50%, -50%);

    font-size: 38px;

    font-weight: bold;

    opacity: 0;

    z-index: 200;

    pointer-events: none;
}

.judge-text.show {
    animation: judgeAnimation 0.65s forwards;
}

@keyframes judgeAnimation {
    0% {
        opacity: 0;
        transform: translate(-50%, -40%) scale(0.7);
    }

    25% {
        opacity: 1;
        transform: translate(-50%, -50%) scale(1.2);
    }

    100% {
        opacity: 0;
        transform: translate(-50%, -75%) scale(1);
    }
}

/* 결과 */

#winner {
    font-size: 52px;
    margin-bottom: 20px;
}

.result-text {
    text-align: center;

    font-size: 24px;

    line-height: 2;
}

@media (max-width: 900px) {

    .title {
        font-size: 38px;
    }

    .player-box {
        width: 180px;
    }

    #topbar {
        padding: 0 10px;
    }

}
</style>
</head>

<body>

<div id="game">

    <!-- 메뉴 -->
    <div class="screen" id="menuScreen">

        <div class="title">
            NEON RHYTHM DUEL
        </div>

        <div class="subtitle">
            PLAYER 1 : Q W E R<br>
            PLAYER 2 : O P [ ]
        </div>

        <div class="menu-section">

            <div class="menu-title">
                🎵 SONG SELECT
            </div>

            <div class="button-row">

                <button class="select-button song selected" data-song="Neon Drive">
                    🌃 Neon Drive
                </button>

                <button class="select-button song" data-song="Cyber Rush">
                    ⚡ Cyber Rush
                </button>

                <button class="select-button song" data-song="Galaxy Beat">
                    🌌 Galaxy Beat
                </button>

                <button class="select-button song" data-song="Final Overload">
                    🔥 Final Overload
                </button>

            </div>

        </div>

        <div class="menu-section">

            <div class="menu-title">
                ⭐ DIFFICULTY
            </div>

            <div class="button-row">

                <button class="select-button difficulty selected" data-difficulty="Easy">
                    EASY
                </button>

                <button class="select-button difficulty" data-difficulty="Normal">
                    NORMAL
                </button>

                <button class="select-button difficulty" data-difficulty="Hard">
                    HARD
                </button>

                <button class="select-button difficulty" data-difficulty="Expert">
                    EXPERT
                </button>

            </div>

        </div>

        <button class="start-button" id="readyButton">
            READY!
        </button>

    </div>


    <!-- 카운트다운 -->
    <div class="screen" id="countdownScreen">

        <div id="countdownNumber">
            3
        </div>

        <div class="subtitle">
            GET READY!
        </div>

    </div>


    <!-- 결과 -->
    <div class="screen" id="resultScreen">

        <div id="winner">
            WINNER
        </div>

        <div class="result-text" id="resultText">
        </div>

        <button class="start-button" id="playAgainButton">
            PLAY AGAIN
        </button>

    </div>


    <!-- 상단 UI -->
    <div id="topbar">

        <div class="player-box player1">

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


        <div id="centerInfo">

            <div id="timer">
                01:00
            </div>

            <div id="songDisplay">
                Neon Drive
            </div>

            <div id="difficultyDisplay">
                EASY
            </div>

        </div>


        <div class="player-box player2">

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


    <!-- 게임판 -->
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

            <div class="key-row">

                <div class="key-box" id="key-q">Q</div>
                <div class="key-box" id="key-w">W</div>
                <div class="key-box" id="key-e">E</div>
                <div class="key-box" id="key-r">R</div>

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

            <div class="key-row">

                <div class="key-box" id="key-o">O</div>
                <div class="key-box" id="key-p">P</div>
                <div class="key-box" id="key-bracketleft">[</div>
                <div class="key-box" id="key-bracketright">]</div>

            </div>

            <div class="judge-text" id="judge2"></div>

        </div>

    </div>

</div>


<script>

/* =========================
   기본 설정
========================= */

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


/* =========================
   곡 데이터
========================= */

const SONGS = {
    "Neon Drive": {
        bpm: 100
    },

    "Cyber Rush": {
        bpm: 112
    },

    "Galaxy Beat": {
        bpm: 125
    },

    "Final Overload": {
        bpm: 138
    }
};


/* =========================
   난이도 데이터
========================= */

const DIFFICULTIES = {

    "Easy": {
        spacing: 1.55,
        doubleChance: 0.02
    },

    "Normal": {
        spacing: 1.30,
        doubleChance: 0.08
    },

    "Hard": {
        spacing: 1.08,
        doubleChance: 0.18
    },

    "Expert": {
        spacing: 0.90,
        doubleChance: 0.32
    }
};


/* =========================
   게임 상태
========================= */

let selectedSong = "Neon Drive";

let selectedDifficulty = "Easy";

let gameStarted = false;

let gameStartTime = 0;

let animationId = null;

let notes = [];

let scores = {
    1: 0,
    2: 0
};

let combos = {
    1: 0,
    2: 0
};


/* =========================
   메뉴 선택
========================= */

document.querySelectorAll(".song").forEach(function(button) {

    button.addEventListener("click", function() {

        document.querySelectorAll(".song").forEach(function(b) {
            b.classList.remove("selected");
        });

        button.classList.add("selected");

        selectedSong = button.dataset.song;

    });

});


document.querySelectorAll(".difficulty").forEach(function(button) {

    button.addEventListener("click", function() {

        document.querySelectorAll(".difficulty").forEach(function(b) {
            b.classList.remove("selected");
        });

        button.classList.add("selected");

        selectedDifficulty = button.dataset.difficulty;

    });

});


/* =========================
   READY 버튼
========================= */

document.getElementById("readyButton").addEventListener(
    "click",
    startCountdown
);


function startCountdown() {

    document.getElementById("menuScreen").style.display = "none";

    document.getElementById("countdownScreen").style.display = "flex";

    const number = document.getElementById("countdownNumber");

    let count = 3;

    number.textContent = count;

    const interval = setInterval(function() {

        count--;

        if (count > 0) {

            number.textContent = count;

        } else if (count === 0) {

            number.textContent = "GO!";

        } else {

            clearInterval(interval);

            document.getElementById("countdownScreen").style.display = "none";

            startGame();

        }

    }, 1000);

}


/* =========================
   게임 시작
========================= */

function startGame() {

    gameStarted = true;

    scores[1] = 0;
    scores[2] = 0;

    combos[1] = 0;
    combos[2] = 0;

    notes = [];

    updateUI();

    document.getElementById("songDisplay").textContent =
        selectedSong;

    document.getElementById("difficultyDisplay").textContent =
        selectedDifficulty.toUpperCase();

    generateSong();

    gameStartTime = performance.now();

    gameLoop();

}


/* =========================
   노트 생성
========================= */

function generateSong() {

    const song = SONGS[selectedSong];

    const difficulty = DIFFICULTIES[selectedDifficulty];

    const beat = 60000 / song.bpm;

    const totalTime = GAME_DURATION * 1000;

    let time = 2500;

    while (time < totalTime) {

        const progress = time / totalTime;

        const interval =
            beat * difficulty.spacing;

        for (let player = 1; player <= 2; player++) {

            const lane =
                Math.floor(Math.random() * 4);

            createNote(player, lane, time);


            /*
            후반으로 갈수록
            동시 타일 증가
            */

            if (
                progress > 0.45 &&
                Math.random() <
                difficulty.doubleChance * progress
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

        }

        time += interval;

    }

}


/* =========================
   타일 생성
========================= */

function createNote(player, lane, hitTime) {

    const boardId =
        player === 1 ? "board1" : "board2";

    const board =
        document.getElementById(boardId);

    const lanes =
        board.querySelectorAll(".lane");

    const tile =
        document.createElement("div");

    tile.className = "tile";

    const color =
        NEON_COLORS[
            Math.floor(
                Math.random() *
                NEON_COLORS.length
            )
        ];

    tile.style.background = color;

    tile.style.color = color;

    tile.style.display = "none";

    lanes[lane].appendChild(tile);

    notes.push({
        player: player,
        lane: lane,
        hitTime: hitTime,
        element: tile,
        hit: false,

        /*
        타일 이동 속도
        낮을수록 빠름
        */
        travelTime: 1700
    });

}


/* =========================
   게임 루프
========================= */

function gameLoop() {

    if (!gameStarted) {
        return;
    }

    const now = performance.now();

    const elapsed =
        now - gameStartTime;

    const remaining =
        Math.max(
            0,
            GAME_DURATION * 1000 - elapsed
        );

    updateTimer(remaining);


    notes.forEach(function(note) {

        if (note.hit) {
            return;
        }

        const appearTime =
            note.hitTime - note.travelTime;

        const progress =
            (elapsed - appearTime) /
            note.travelTime;


        /*
        아직 등장할 시간이 아님
        */

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


        /*
        원근감
        */

        const scale =
            0.30 + p * 0.75;

        const y =
            2 + p * 80;


        note.element.style.top =
            y + "%";

        note.element.style.transform =
            "scale(" + scale + ")";


        /*
        지나간 타일 = 자동 MISS
        */

        if (progress > 1.10) {

            note.hit = true;

            if (note.element.parentNode) {
                note.element.remove();
            }

            registerMiss(note.player);

        }

    });


    if (elapsed >= GAME_DURATION * 1000) {

        endGame();

        return;

    }


    animationId =
        requestAnimationFrame(gameLoop);

}


/* =========================
   타이머
========================= */

function updateTimer(remaining) {

    const totalSeconds =
        Math.ceil(remaining / 1000);

    const minutes =
        Math.floor(totalSeconds / 60);

    const seconds =
        totalSeconds % 60;

    document.getElementById("timer").textContent =
        String(minutes).padStart(2, "0")
        +
        ":"
        +
        String(seconds).padStart(2, "0");

}


/* =========================
   키 입력
========================= */

document.addEventListener("keydown", function(event) {

    if (!gameStarted) {
        return;
    }

    if (event.repeat) {
        return;
    }

    const key =
        event.key.toLowerCase();


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


document.addEventListener("keyup", function(event) {

    const key =
        event.key.toLowerCase();

    deactivateKey(key);

});


/* =========================
   키 애니메이션
========================= */

function activateKey(key) {

    let elementId =
        "key-" + key;


    if (key === "[") {
        elementId = "key-bracketleft";
    }

    if (key === "]") {
        elementId = "key-bracketright";
    }


    const element =
        document.getElementById(elementId);

    if (element) {
        element.classList.add("active");
    }

}


function deactivateKey(key) {

    let elementId =
        "key-" + key;


    if (key === "[") {
        elementId = "key-bracketleft";
    }

    if (key === "]") {
        elementId = "key-bracketright";
    }


    const element =
        document.getElementById(elementId);

    if (element) {
        element.classList.remove("active");
    }

}


/* =========================
   타일 판정
========================= */

function hitLane(player, lane) {

    const elapsed =
        performance.now() - gameStartTime;


    const candidates =
        notes.filter(function(note) {

            return (
                note.player === player &&
                note.lane === lane &&
                !note.hit
            );

        });


    /*
    타일이 없으면 MISS
    */

    if (candidates.length === 0) {

        registerMiss(player);

        return;

    }


    /*
    가장 가까운 타일 찾기
    */

    candidates.sort(function(a, b) {

        return (
            Math.abs(elapsed - a.hitTime)
            -
            Math.abs(elapsed - b.hitTime)
        );

    });


    const note = candidates[0];

    const difference =
        Math.abs(elapsed - note.hitTime);


    /*
    PERFECT
    */

    if (difference <= 120) {

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

    if (difference <= 240) {

        registerHit(
            player,
            note,
            "GREAT",
            600
        );

        return;

    }


    /*
    판정 범위 밖
    */

    registerMiss(player);

}


/* =========================
   성공 처리
========================= */

function registerHit(
    player,
    note,
    judgement,
    baseScore
) {

    note.hit = true;

    combos[player]++;


    /*
    콤보 보너스
    */

    const comboBonus =
        Math.min(
            combos[player] * 15,
            1000
        );


    scores[player] +=
        baseScore + comboBonus;


    showJudgement(
        player,
        judgement
    );


    if (note.element.parentNode) {

        note.element.classList.add("hit");

        setTimeout(function() {

            if (note.element.parentNode) {
                note.element.remove();
            }

        }, 250);

    }


    updateUI();

}


/* =========================
   MISS
========================= */

function registerMiss(player) {

    combos[player] = 0;

    showJudgement(
        player,
        "MISS"
    );

    updateUI();

}


/* =========================
   판정 표시
========================= */

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


    element.textContent =
        judgement;


    if (judgement === "PERFECT") {

        element.style.color = "#00ffff";

    } else if (judgement === "GREAT") {

        element.style.color = "#00ff88";

    } else {

        element.style.color = "#ff3355";

    }


    element.classList.remove("show");

    void element.offsetWidth;

    element.classList.add("show");

}


/* =========================
   UI 업데이트
========================= */

function updateUI() {

    document.getElementById("score1").textContent =
        scores[1].toLocaleString();

    document.getElementById("score2").textContent =
        scores[2].toLocaleString();

    document.getElementById("combo1").textContent =
        combos[1];

    document.getElementById("combo2").textContent =
        combos[2];

}


/* =========================
   게임 종료
========================= */

function endGame() {

    gameStarted = false;

    if (animationId) {
        cancelAnimationFrame(animationId);
    }


    const winner =
        document.getElementById("winner");


    if (scores[1] > scores[2]) {

        winner.textContent =
            "🔵 PLAYER 1 WINS!";

    } else if (scores[2] > scores[1]) {

        winner.textContent =
            "🔴 PLAYER 2 WINS!";

    } else {

        winner.textContent =
            "🤝 DRAW!";

    }


    document.getElementById("resultText").innerHTML =

        "🎵 " + selectedSong +

        "<br>⭐ " + selectedDifficulty +

        "<br><br>" +

        "🔵 PLAYER 1: <b>" +
        scores[1].toLocaleString() +
        "</b>" +

        "<br>" +

        "🔴 PLAYER 2: <b>" +
        scores[2].toLocaleString() +
        "</b>";


    document.getElementById("resultScreen").style.display =
        "flex";

}


/* =========================
   다시 플레이
========================= */

document.getElementById("playAgainButton").addEventListener(
    "click",
    function() {

        location.reload();

    }
);

</script>

</body>
</html>
"""

components.html(
    html_code,
    height=900,
    scrolling=False
)
```
