```python
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
    color: white;
    background: #050510;
}

body {
    animation: backgroundShift 20s infinite alternate ease-in-out;
}

@keyframes backgroundShift {

    0% {
        background:
        radial-gradient(circle at top, #14235c, #050510 70%);
    }

    25% {
        background:
        radial-gradient(circle at top, #4b155b, #050510 70%);
    }

    50% {
        background:
        radial-gradient(circle at top, #064d55, #050510 70%);
    }

    75% {
        background:
        radial-gradient(circle at top, #523a08, #050510 70%);
    }

    100% {
        background:
        radial-gradient(circle at top, #172d63, #050510 70%);
    }

}

#game {
    width: 100vw;
    height: 100vh;
    position: relative;
    overflow: hidden;
}


/* ===============================
   TOP HUD
================================ */

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

    width: 300px;

    padding: 16px;

    border-radius: 18px;

    background: rgba(0,0,0,0.45);

    backdrop-filter: blur(12px);

    border:
    1px solid rgba(255,255,255,0.15);

}

.p1 {

    box-shadow:
    0 0 25px rgba(0,255,255,0.25);

}

.p2 {

    box-shadow:
    0 0 25px rgba(255,0,200,0.25);

}

.player-name {

    font-size: 20px;

    font-weight: bold;

    letter-spacing: 2px;

}

.score {

    font-size: 32px;

    margin-top: 5px;

    font-weight: bold;

}

.combo {

    font-size: 18px;

    margin-top: 5px;

    color: #ffe600;

}

#timerBox {

    text-align: center;

    font-size: 25px;

    font-weight: bold;

    text-shadow:
    0 0 15px white;

}

#songName {

    font-size: 15px;

    color: #00ffff;

    margin-top: 5px;

}

#difficulty {

    font-size: 14px;

    color: #dddddd;

    margin-top: 4px;

}


/* ===============================
   ARENA
================================ */

#arena {

    position: absolute;

    top: 100px;

    width: 100%;

    height: calc(100% - 100px);

    display: flex;

    justify-content: space-around;

    perspective: 900px;

}

.board {

    position: relative;

    width: 42%;

    height: 88%;

    transform:
    rotateX(18deg);

    transform-style:
    preserve-3d;

}

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

    border-left:
    1px solid rgba(255,255,255,0.15);

    border-right:
    1px solid rgba(255,255,255,0.08);

}


/* ===============================
   JUDGEMENT LINE
================================ */

.judgement-line {

    position: absolute;

    bottom: 12%;

    width: 100%;

    height: 10px;

    background: white;

    box-shadow:

    0 0 8px white,

    0 0 20px #00ffff,

    0 0 45px #00ffff;

    z-index: 30;

}


/* ===============================
   KEYS
================================ */

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

    font-size: 24px;

    font-weight: bold;

    border-radius: 12px;

    background:
    rgba(0,0,0,0.7);

    border:
    2px solid rgba(255,255,255,0.4);

    transition: 0.08s;

}

.key.active {

    transform:
    scale(0.90);

    background: white;

    color: black;

    box-shadow:
    0 0 25px white;

}


/* ===============================
   TILES
================================ */

.tile {

    position: absolute;

    width:
    calc(100% - 16px);

    left: 8px;

    height: 52px;

    border-radius: 12px;

    box-shadow:

    0 0 12px currentColor,

    0 0 35px currentColor;

    z-index: 15;

}

.tile::after {

    content: "";

    position: absolute;

    top: 5px;

    left: 5px;

    right: 5px;

    bottom: 5px;

    border-radius: 8px;

    background:
    rgba(255,255,255,0.28);

}

.tile.hit {

    animation:
    hitAnimation 0.25s forwards;

}

@keyframes hitAnimation {

    0% {

        transform:
        scale(1);

        opacity: 1;

    }

    100% {

        transform:
        scale(1.8);

        opacity: 0;

    }

}


/* ===============================
   JUDGEMENT TEXT
================================ */

.judge-text {

    position: absolute;

    left: 50%;

    top: 48%;

    transform:
    translate(-50%, -50%);

    font-size: 42px;

    font-weight: bold;

    opacity: 0;

    z-index: 200;

    pointer-events: none;

}

.judge-text.show {

    animation:
    judgeAnimation 0.7s forwards;

}

@keyframes judgeAnimation {

    0% {

        opacity: 0;

        transform:
        translate(-50%, -40%)
        scale(0.7);

    }

    30% {

        opacity: 1;

        transform:
        translate(-50%, -50%)
        scale(1.2);

    }

    100% {

        opacity: 0;

        transform:
        translate(-50%, -70%)
        scale(1);

    }

}


/* ===============================
   MENU
================================ */

.screen {

    position: absolute;

    z-index: 1000;

    width: 100%;

    height: 100%;

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;

    background:
    rgba(0,0,10,0.88);

    backdrop-filter:
    blur(15px);

}

#resultScreen,
#countdownScreen {

    display: none;

}

.title {

    font-size: 60px;

    font-weight: 900;

    letter-spacing: 7px;

    background:

    linear-gradient(
        90deg,
        #00ffff,
        #ff00ff,
        #ffff00
    );

    -webkit-background-clip: text;

    color: transparent;

}

.subtitle {

    margin-top: 15px;

    font-size: 18px;

    color: #cccccc;

}

.menu-section {

    margin-top: 25px;

    text-align: center;

}

.menu-title {

    font-size: 20px;

    margin-bottom: 12px;

    color: #00ffff;

}

.buttons {

    display: flex;

    gap: 12px;

    flex-wrap: wrap;

    justify-content: center;

}

.menu-button {

    padding:
    14px 25px;

    border-radius: 12px;

    border:
    1px solid rgba(255,255,255,0.25);

    background:
    rgba(255,255,255,0.08);

    color: white;

    font-size: 16px;

    cursor: pointer;

    transition: 0.2s;

}

.menu-button:hover {

    transform:
    scale(1.07);

    border-color:
    #00ffff;

}

.menu-button.selected {

    background:

    linear-gradient(
        90deg,
        #0088ff,
        #c000ff
    );

    box-shadow:

    0 0 20px #00ffff;

}

.start-button {

    margin-top: 28px;

    padding:
    16px 65px;

    border: none;

    border-radius: 15px;

    font-size: 23px;

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

}

#countdownNumber {

    font-size: 150px;

    font-weight: bold;

    text-shadow:

    0 0 30px #00ffff,

    0 0 70px #ff00ff;

}

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


<!-- ===============================
     SONG MENU
================================ -->

<div class="screen" id="menuScreen">

    <div class="title">
        NEON RHYTHM DUEL
    </div>

    <div class="subtitle">

        🎮 PLAYER 1: Q W E R
        &nbsp;&nbsp;&nbsp;

        🎮 PLAYER 2: O P [ ]

    </div>


    <div class="menu-section">

        <div class="menu-title">
            🎵 SONG SELECT
        </div>

        <div class="buttons">

            <button
            class="menu-button song selected"
            data-song="Neon Drive">
            🌃 Neon Drive
            </button>

            <button
            class="menu-button song"
            data-song="Cyber Rush">
            ⚡ Cyber Rush
            </button>

            <button
            class="menu-button song"
            data-song="Galaxy Beat">
            🌌 Galaxy Beat
            </button>

            <button
            class="menu-button song"
            data-song="Final Overload">
            🔥 Final Overload
            </button>

        </div>

    </div>


    <div class="menu-section">

        <div class="menu-title">
            ⭐ DIFFICULTY
        </div>

        <div class="buttons">

            <button
            class="menu-button difficulty selected"
            data-difficulty="Easy">
            EASY
            </button>

            <button
            class="menu-button difficulty"
            data-difficulty="Normal">
            NORMAL
            </button>

            <button
            class="menu-button difficulty"
            data-difficulty="Hard">
            HARD
            </button>

            <button
            class="menu-button difficulty"
            data-difficulty="Expert">
            EXPERT
            </button>

        </div>

    </div>


    <button
    class="start-button"
    onclick="prepareGame()">

        READY?

    </button>

</div>



<!-- ===============================
     COUNTDOWN
================================ -->

<div
class="screen"
id="countdownScreen">

    <div
    id="countdownNumber">

        3

    </div>

    <div
    class="subtitle">

        GET READY!

    </div>

</div>



<!-- ===============================
     RESULT
================================ -->

<div
class="screen"
id="resultScreen">

    <div
    id="winner">

        PLAYER 1 WINS!

    </div>

    <div
    class="result-score"
    id="resultScore">

    </div>

    <button
    class="start-button"
    onclick="location.reload()">

        PLAY AGAIN

    </button>

</div>



<!-- ===============================
     HUD
================================ -->

<div id="topbar">

    <div
    class="player-score p1">

        <div class="player-name">
            🔵 PLAYER 1
        </div>

        <div
        class="score"
        id="score1">
            0
        </div>

        <div class="combo">

            COMBO:
            <span id="combo1">
                0
            </span>

        </div>

    </div>


    <div id="timerBox">

        <div id="timer">
            01:00
        </div>

        <div id="songName">
            Neon Drive
        </div>

        <div id="difficulty">
            EASY
        </div>

    </div>


    <div
    class="player-score p2">

        <div class="player-name">
            🔴 PLAYER 2
        </div>

        <div
        class="score"
        id="score2">
            0
        </div>

        <div class="combo">

            COMBO:

            <span id="combo2">
                0
            </span>

        </div>

    </div>

</div>



<!-- ===============================
     ARENA
================================ -->

<div id="arena">


<!-- PLAYER 1 -->

<div
class="board"
id="board1">

    <div class="lanes">

        <div class="lane"></div>
        <div class="lane"></div>
        <div class="lane"></div>
        <div class="lane"></div>

    </div>

    <div
    class="judgement-line">
    </div>

    <div
    class="key-label">

        <div
        class="key"
        id="key-q">
            Q
        </div>

        <div
        class="key"
        id="key-w">
            W
        </div>

        <div
        class="key"
        id="key-e">
            E
        </div>

        <div
        class="key"
        id="key-r">
            R
        </div>

    </div>

    <div
    class="judge-text"
    id="judge1">
    </div>

</div>



<!-- PLAYER 2 -->

<div
class="board"
id="board2">

    <div class="lanes">

        <div class="lane"></div>
        <div class="lane"></div>
        <div class="lane"></div>
        <div class="lane"></div>

    </div>

    <div
    class="judgement-line">
    </div>

    <div
    class="key-label">

        <div
        class="key"
        id="key-o">
            O
        </div>

        <div
        class="key"
        id="key-p">
            P
        </div>

        <div
        class="key"
        id="key-[">
            [
        </div>

        <div
        class="key"
        id="key-]">
            ]
        </div>

    </div>

    <div
    class="judge-text"
    id="judge2">
    </div>

</div>


</div>

</div>



<script>

/* =========================================
   SETTINGS
========================================= */

const GAME_DURATION = 60;

const PLAYER1_KEYS =
["q", "w", "e", "r"];

const PLAYER2_KEYS =
["o", "p", "[", "]"];


/* =========================================
   SONG DATA
========================================= */

const SONGS = {

    "Neon Drive": {

        bpm: 100,

        description:
        "쉬운 네온 드라이브"

    },

    "Cyber Rush": {

        bpm: 115,

        description:
        "빠른 사이버 리듬"

    },

    "Galaxy Beat": {

        bpm: 130,

        description:
        "우주 스타일 비트"

    },

    "Final Overload": {

        bpm: 145,

        description:
        "최종 고속 배틀"

    }

};


/* =========================================
   DIFFICULTY DATA
========================================= */

const DIFFICULTIES = {

    "Easy": {

        intervalMultiplier: 1.45,

        doubleChance: 0.03

    },

    "Normal": {

        intervalMultiplier: 1.15,

        doubleChance: 0.10

    },

    "Hard": {

        intervalMultiplier: 0.95,

        doubleChance: 0.22

    },

    "Expert": {

        intervalMultiplier: 0.78,

        doubleChance: 0.38

    }

};


const NEON_COLORS = [

    "#00ffff",

    "#ff00ff",

    "#00ff88",

    "#ffff00",

    "#ff6600",

    "#8a2bff"

];


/* =========================================
   GAME STATE
========================================= */

let selectedSong =
"Neon Drive";

let selectedDifficulty =
"Easy";

let gameStarted =
false;

let startTime =
0;

let animationFrame;

let notes = [];

let scores = {

    1: 0,
    2: 0

};

let combos = {

    1: 0,
    2: 0

};

let audioContext;


/* =========================================
   MENU BUTTONS
========================================= */

document
.querySelectorAll(".song")
.forEach(button => {

    button.addEventListener(
        "click",
        () => {

            document
            .querySelectorAll(".song")
            .forEach(b =>
                b.classList.remove("selected")
            );

            button
            .classList.add("selected");

            selectedSong =
            button.dataset.song;

        }
    );

});


document
.querySelectorAll(".difficulty")
.forEach(button => {

    button.addEventListener(
        "click",
        () => {

            document
            .querySelectorAll(".difficulty")
            .forEach(b =>
                b.classList.remove("selected")
            );

            button
            .classList.add("selected");

            selectedDifficulty =
            button.dataset.difficulty;

        }
    );

});


/* =========================================
   PREPARE GAME
========================================= */

function prepareGame() {

    document
    .getElementById("menuScreen")
    .style.display =
    "none";


    document
    .getElementById("countdownScreen")
    .style.display =
    "flex";


    let count = 3;

    const countdownElement =
    document.getElementById(
        "countdownNumber"
    );


    countdownElement.innerText =
    count;


    const countdown =
    setInterval(() => {

        count--;


        if (count > 0) {

            countdownElement.innerText =
            count;

        }

        else if (count === 0) {

            countdownElement.innerText =
            "GO!";

        }

        else {

            clearInterval(countdown);

            document
            .getElementById(
                "countdownScreen"
            )
            .style.display =
            "none";

            startGame();

        }

    }, 1000);

}


/* =========================================
   AUDIO
========================================= */

function initAudio() {

    audioContext =
    new (
        window.AudioContext ||
        window.webkitAudioContext
    )();

}


function playTone(
    frequency,
    duration = 0.08,
    volume = 0.05
) {

    if (!audioContext) return;

    const oscillator =
    audioContext.createOscillator();

    const gain =
    audioContext.createGain();

    oscillator.frequency.value =
    frequency;

    oscillator.type =
    "sine";

    gain.gain.value =
    volume;

    oscillator.connect(gain);

    gain.connect(
        audioContext.destination
    );

    oscillator.start();

    gain.gain
    .exponentialRampToValueAtTime(
        0.001,
        audioContext.currentTime + duration
    );

    oscillator.stop(
        audioContext.currentTime + duration
    );

}


/* =========================================
   CREATE NOTE
========================================= */

function createNote(
    player,
    lane,
    hitTime
) {

    const board =
    document.getElementById(
        player === 1
        ? "board1"
        : "board2"
    );


    const lanes =
    board.querySelectorAll(".lane");


    const note =
    document.createElement("div");


    note.className =
    "tile";


    const color =
    NEON_COLORS[
        Math.floor(
            Math.random()
            *
            NEON_COLORS.length
        )
    ];


    note.style.background =
    color;


    note.style.color =
    color;


    lanes[lane]
    .appendChild(note);


    notes.push({

        player,

        lane,

        hitTime,

        element: note,

        hit: false,

        /*
        Faster tile movement
        */

        duration: 1800

    });

}


/* =========================================
   GENERATE SONG
========================================= */

function generateSong() {

    notes = [];


    const song =
    SONGS[selectedSong];


    const difficulty =
    DIFFICULTIES[
        selectedDifficulty
    ];


    /*
    BPM → beat interval
    */

    const beat =
    60000 / song.bpm;


    let time =
    2500;


    const totalTime =
    GAME_DURATION * 1000;


    while (
        time < totalTime
    ) {

        /*
        Easier spacing
        */

        let interval =
        beat
        *
        difficulty.intervalMultiplier;


        /*
        Gradually harder
        */

        const progress =
        time / totalTime;


        for (
            let player = 1;
            player <= 2;
            player++
        ) {

            const lane =
            Math.floor(
                Math.random() * 4
            );


            createNote(
                player,
                lane,
                time
            );


            /*
            Double notes appear
            mostly later in song
            */

            if (

                progress > 0.55

                &&

                Math.random()
                <
                difficulty.doubleChance
                *
                progress

            ) {

                let lane2;

                do {

                    lane2 =
                    Math.floor(
                        Math.random() * 4
                    );

                }

                while (
                    lane2 === lane
                );


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


/* =========================================
   START GAME
========================================= */

function startGame() {

    scores[1] = 0;
    scores[2] = 0;

    combos[1] = 0;
    combos[2] = 0;


    updateScoreUI();


    document
    .getElementById("songName")
    .innerText =
    selectedSong;


    document
    .getElementById("difficulty")
    .innerText =
    selectedDifficulty.toUpperCase();


    initAudio();


    generateSong();


    gameStarted =
    true;


    startTime =
    performance.now();


    gameLoop();

}


/* =========================================
   GAME LOOP
========================================= */

function gameLoop() {

    if (!gameStarted) return;


    const now =
    performance.now();


    const elapsed =
    now - startTime;


    const remaining =
    Math.max(
        0,
        GAME_DURATION * 1000 - elapsed
    );


    updateTimer(remaining);


    notes.forEach(note => {

        if (note.hit) return;


        /*
        Tile starts far away
        */

        const startTimeNote =
        note.hitTime
        -
        note.duration;


        const progress =
        (
            elapsed
            -
            startTimeNote
        )
        /
        note.duration;


        if (progress < 0) {

            note.element.style.display =
            "none";

            return;

        }


        note.element.style.display =
        "block";


        /*
        Faster perspective movement
        */

        const p =
        Math.min(
            Math.max(progress, 0),
            1.15
        );


        const scale =
        0.28
        +
        p * 0.82;


        const y =
        2
        +
        p * 82;


        note.element.style.top =
        y + "%";


        note.element.style.transform =
        `scale(${scale})`;


        /*
        Automatic miss
        */

        if (progress > 1.10) {

            note.hit = true;

            note.element.remove();

            registerMiss(
                note.player
            );

        }

    });


    if (
        elapsed >=
        GAME_DURATION * 1000
    ) {

        endGame();

        return;

    }


    animationFrame =
    requestAnimationFrame(
        gameLoop
    );

}


/* =========================================
   TIMER
========================================= */

function updateTimer(
    remaining
) {

    const seconds =
    Math.ceil(
        remaining / 1000
    );


    const minutes =
    Math.floor(
        seconds / 60
    );


    const secs =
    seconds % 60;


    document
    .getElementById("timer")
    .innerText =

    String(minutes)
    .padStart(2, "0")

    +

    ":"

    +

    String(secs)
    .padStart(2, "0");

}


/* =========================================
   KEY INPUT
========================================= */

document.addEventListener(
    "keydown",
    event => {

        if (!gameStarted)
        return;


        if (event.repeat)
        return;


        const key =
        event.key.toLowerCase();


        if (
            PLAYER1_KEYS.includes(key)
            ||
            PLAYER2_KEYS.includes(key)
        ) {

            event.preventDefault();

        }


        if (
            PLAYER1_KEYS.includes(key)
        ) {

            const lane =
            PLAYER1_KEYS.indexOf(key);


            activateKey(key);


            hitLane(
                1,
                lane
            );

        }


        if (
            PLAYER2_KEYS.includes(key)
        ) {

            const lane =
            PLAYER2_KEYS.indexOf(key);


            activateKey(key);


            hitLane(
                2,
                lane
            );

        }

    }
);


document.addEventListener(
    "keyup",
    event => {

        const key =
        event.key.toLowerCase();


        const element =
        document.getElementById(
            "key-" + key
        );


        if (element) {

            element
            .classList
            .remove("active");

        }

    }
);


function activateKey(key) {

    const element =
    document.getElementById(
        "key-" + key
    );


    if (element) {

        element
        .classList
        .add("active");

    }

}


/* =========================================
   HIT DETECTION
========================================= */

function hitLane(
    player,
    lane
) {

    const elapsed =
    performance.now()
    -
    startTime;


    const candidates =
    notes.filter(note =>

        note.player === player

        &&

        note.lane === lane

        &&

        !note.hit

    );


    /*
    Empty lane = MISS
    */

    if (
        candidates.length === 0
    ) {

        registerMiss(player);

        return;

    }


    candidates.sort(
        (a, b) =>

        Math.abs(
            elapsed - a.hitTime
        )

        -

        Math.abs(
            elapsed - b.hitTime
        )

    );


    const note =
    candidates[0];


    const difference =
    Math.abs(
        elapsed
        -
        note.hitTime
    );


    /*
    PERFECT
    */

    if (
        difference <= 110
    ) {

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

    if (
        difference <= 220
    ) {

        registerHit(
            player,
            note,
            "GREAT",
            600
        );

        return;

    }


    /*
    Outside judgement timing
    */

    registerMiss(player);

}


/* =========================================
   HIT
========================================= */

function registerHit(
    player,
    note,
    judgement,
    baseScore
) {

    note.hit =
    true;


    combos[player]++;


    /*
    Combo bonus
    */

    const comboBonus =
    Math.min(
        combos[player] * 15,
        1000
    );


    scores[player] +=

    baseScore

    +

    comboBonus;


    note.element
    .classList
    .add("hit");


    setTimeout(() => {

        note.element.remove();

    }, 250);


    showJudgement(
        player,
        judgement
    );


    if (
        judgement === "PERFECT"
    ) {

        playTone(
            700,
            0.07,
            0.07
        );

    }

    else {

        playTone(
            500,
            0.07,
            0.05
        );

    }


    updateScoreUI();

}


/* =========================================
   MISS
========================================= */

function registerMiss(
    player
) {

    combos[player] =
    0;


    showJudgement(
        player,
        "MISS"
    );


    playTone(
        130,
        0.10,
        0.04
    );


    updateScoreUI();

}


/* =========================================
   JUDGEMENT DISPLAY
========================================= */

function showJudgement(
    player,
    judgement
) {

    const element =
    document.getElementById(

        player === 1
        ?

        "judge1"

        :

        "judge2"

    );


    element.innerText =
    judgement;


    if (
        judgement === "PERFECT"
    ) {

        element.style.color =
        "#00ffff";

    }

    else if (
        judgement === "GREAT"
    ) {

        element.style.color =
        "#00ff88";

    }

    else {

        element.style.color =
        "#ff3355";

    }


    element
    .classList
    .remove("show");


    void element.offsetWidth;


    element
    .classList
    .add("show");

}


/* =========================================
   UPDATE SCORE
========================================= */

function updateScoreUI() {

    document
    .getElementById("score1")
    .innerText =
    scores[1]
    .toLocaleString();


    document
    .getElementById("score2")
    .innerText =
    scores[2]
    .toLocaleString();


    document
    .getElementById("combo1")
    .innerText =
    combos[1];


    document
    .getElementById("combo2")
    .innerText =
    combos[2];

}


/* =========================================
   END GAME
========================================= */

function endGame() {

    gameStarted =
    false;


    cancelAnimationFrame(
        animationFrame
    );


    const resultScreen =
    document.getElementById(
        "resultScreen"
    );


    const winner =
    document.getElementById(
        "winner"
    );


    if (
        scores[1] > scores[2]
    ) {

        winner.innerText =
        "🔵 PLAYER 1 WINS!";

    }

    else if (
        scores[2] > scores[1]
    ) {

        winner.innerText =
        "🔴 PLAYER 2 WINS!";

    }

    else {

        winner.innerText =
        "🤝 DRAW!";

    }


    document
    .getElementById(
        "resultScore"
    )
    .innerHTML =

    `

    🎵 ${selectedSong}

    <br>

    ⭐ ${selectedDifficulty}

    <br><br>

    🔵 PLAYER 1:
    <b>
    ${scores[1].toLocaleString()}
    </b>

    <br>

    🔴 PLAYER 2:
    <b>
    ${scores[2].toLocaleString()}
    </b>

    <br><br>

    최고 점수를 기록한 플레이어가 승리!

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
```
