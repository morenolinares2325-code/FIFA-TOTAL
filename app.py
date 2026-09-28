import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="Retro Football 96",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    header[data-testid="stHeader"] { background: transparent; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    .stApp { background: radial-gradient(ellipse at top, #0d1520 0%, #05070b 60%); color: #e8edf4; }
    .block-container { padding-top: 1rem; max-width: 1300px; }
    .stButton button {
        background: linear-gradient(135deg, #00d4a8 0%, #00ffc8 100%);
        color: #05070b; border: none; border-radius: 12px;
        font-weight: 800; padding: 12px 24px;
        letter-spacing: 1px; box-shadow: 0 4px 24px rgba(0,212,168,0.35);
        text-transform: uppercase; font-size: 0.9rem; width: 100%;
    }
    .stButton button:hover { transform: translateY(-2px); box-shadow: 0 8px 40px rgba(0,212,168,0.6); }
    .hero-title {
        text-align: center;
        background: linear-gradient(135deg, #00ffc8 0%, #00d4a8 40%, #7c5cff 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 3rem; font-weight: 900; letter-spacing: -2px;
        filter: drop-shadow(0 0 30px rgba(0,212,168,0.4)); margin: 0;
    }
    .hero-sub { text-align: center; color: #7a8699; font-size: 0.85rem;
        letter-spacing: 4px; margin: 6px 0 24px 0; text-transform: uppercase; }
    .team-card {
        background: linear-gradient(135deg, rgba(20,26,36,0.95), rgba(15,20,28,0.98));
        border: 2px solid rgba(0,212,168,0.2); border-radius: 16px;
        padding: 16px; text-align: center; margin-bottom: 10px;
    }
    .team-flag { font-size: 2.5rem; }
    .team-name { color: #e8edf4; font-weight: 800; font-size: 1rem; letter-spacing: 1px; }
    .team-rating { color: #00d4a8; font-size: 0.8rem; font-weight: 700; }
    .tactic-card {
        background: linear-gradient(135deg, rgba(20,26,36,0.95), rgba(15,20,28,0.98));
        border: 2px solid rgba(124,92,255,0.3); border-radius: 16px;
        padding: 14px; text-align: center; margin-bottom: 10px;
    }
    .tactic-name { color: #a58cff; font-weight: 800; font-size: 1.3rem; letter-spacing: 2px; }
    .tactic-desc { color: #7a8699; font-size: 0.75rem; margin-top: 4px; }
    .player-row {
        background: rgba(20,26,36,0.6); border-left: 3px solid #00d4a8;
        border-radius: 8px; padding: 6px 10px; margin-bottom: 4px;
        display: grid; grid-template-columns: 28px 1fr 40px 200px;
        gap: 6px; align-items: center;
    }
    .player-name { color: #e8edf4; font-weight: 600; font-size: 0.85rem; }
    .player-pos { background: linear-gradient(135deg,#7c5cff,#a58cff); color: white;
        font-size: 0.6rem; font-weight: 800; padding: 2px 5px; border-radius: 4px;
        letter-spacing: 1px; text-align: center; }
    .player-num { color: #00d4a8; font-weight: 900; font-size: 0.95rem; text-align: center; }
    .stats-bar { display: flex; gap: 4px; font-size: 0.65rem; }
    .stat-value { color: #00ffc8; font-weight: 800; font-size: 0.7rem; }
    .stat-value.high { color: #ff5c9f; }
    div[role="radiogroup"] { flex-direction: row !important; gap: 8px; flex-wrap: wrap; }
</style>
""", unsafe_allow_html=True)

DIFICULTADES = {
    "Fácil":   {"speed": 2.6, "vision": 0.5,  "reaction": 0.7},
    "Normal":  {"speed": 3.2, "vision": 0.7,  "reaction": 0.85},
    "Difícil": {"speed": 3.7, "vision": 0.85, "reaction": 0.95},
    "Leyenda": {"speed": 4.3, "vision": 1.0,  "reaction": 1.0},
}

EQUIPOS = {
    "España": {
        "flag": "🇪🇸", "rating": 89, "color": "#ff3b5c", "color2": "#ffdd00",
        "jugadores": [
            {"num":1,"nombre":"Zubizarreta","pos":"POR","vel":55,"tir":20,"def":88,"pas":70,"reg":40},
            {"num":2,"nombre":"Luis Enrique","pos":"DEF","vel":82,"tir":68,"def":84,"pas":80,"reg":76},
            {"num":3,"nombre":"Hierro","pos":"DEF","vel":70,"tir":82,"def":88,"pas":79,"reg":62},
            {"num":4,"nombre":"Nadal","pos":"DEF","vel":71,"tir":55,"def":86,"pas":74,"reg":60},
            {"num":5,"nombre":"Sergi","pos":"DEF","vel":84,"tir":62,"def":82,"pas":80,"reg":78},
            {"num":6,"nombre":"Guardiola","pos":"MED","vel":72,"tir":70,"def":76,"pas":91,"reg":78},
            {"num":7,"nombre":"Amor","pos":"MED","vel":73,"tir":74,"def":72,"pas":84,"reg":76},
            {"num":8,"nombre":"Raúl","pos":"MED","vel":86,"tir":90,"def":55,"pas":82,"reg":88},
            {"num":9,"nombre":"Alfonso","pos":"DEL","vel":82,"tir":87,"def":45,"pas":75,"reg":82},
            {"num":10,"nombre":"Pizzi","pos":"DEL","vel":78,"tir":85,"def":48,"pas":78,"reg":80},
            {"num":11,"nombre":"Kiko","pos":"DEL","vel":87,"tir":83,"def":42,"pas":74,"reg":89},
        ]
    },
    "Brasil": {
        "flag": "🇧🇷", "rating": 91, "color": "#ffd700", "color2": "#00a859",
        "jugadores": [
            {"num":1,"nombre":"Taffarel","pos":"POR","vel":58,"tir":22,"def":90,"pas":72,"reg":42},
            {"num":2,"nombre":"Cafu","pos":"DEF","vel":89,"tir":68,"def":85,"pas":82,"reg":85},
            {"num":3,"nombre":"Aldair","pos":"DEF","vel":72,"tir":55,"def":89,"pas":76,"reg":60},
            {"num":4,"nombre":"Márcio Santos","pos":"DEF","vel":70,"tir":52,"def":87,"pas":73,"reg":58},
            {"num":5,"nombre":"Branco","pos":"DEF","vel":76,"tir":82,"def":80,"pas":78,"reg":72},
            {"num":6,"nombre":"Dunga","pos":"MED","vel":74,"tir":76,"def":83,"pas":88,"reg":74},
            {"num":7,"nombre":"Mauro Silva","pos":"MED","vel":78,"tir":70,"def":84,"pas":82,"reg":74},
            {"num":8,"nombre":"Rai","pos":"MED","vel":79,"tir":86,"def":62,"pas":89,"reg":84},
            {"num":9,"nombre":"Bebeto","pos":"DEL","vel":85,"tir":88,"def":48,"pas":80,"reg":88},
            {"num":10,"nombre":"Romário","pos":"DEL","vel":90,"tir":95,"def":40,"pas":78,"reg":96},
            {"num":11,"nombre":"Mazinho","pos":"DEL","vel":82,"tir":78,"def":68,"pas":80,"reg":82},
        ]
    },
    "Italia": {
        "flag": "🇮🇹", "rating": 88, "color": "#1e4a9c", "color2": "#ffffff",
        "jugadores": [
            {"num":1,"nombre":"Pagliuca","pos":"POR","vel":56,"tir":20,"def":89,"pas":68,"reg":38},
            {"num":2,"nombre":"Mussi","pos":"DEF","vel":78,"tir":55,"def":84,"pas":76,"reg":66},
            {"num":3,"nombre":"Maldini","pos":"DEF","vel":87,"tir":68,"def":93,"pas":82,"reg":82},
            {"num":4,"nombre":"Baresi","pos":"DEF","vel":72,"tir":52,"def":95,"pas":84,"reg":66},
            {"num":5,"nombre":"Costacurta","pos":"DEF","vel":74,"tir":55,"def":90,"pas":78,"reg":62},
            {"num":6,"nombre":"Albertini","pos":"MED","vel":76,"tir":78,"def":74,"pas":90,"reg":78},
            {"num":7,"nombre":"Donadoni","pos":"MED","vel":85,"tir":80,"def":68,"pas":84,"reg":88},
            {"num":8,"nombre":"R. Baggio","pos":"MED","vel":82,"tir":92,"def":48,"pas":88,"reg":92},
            {"num":9,"nombre":"Signori","pos":"DEL","vel":84,"tir":90,"def":42,"pas":78,"reg":85},
            {"num":10,"nombre":"Casiraghi","pos":"DEL","vel":80,"tir":84,"def":46,"pas":76,"reg":80},
            {"num":11,"nombre":"Zola","pos":"DEL","vel":82,"tir":88,"def":44,"pas":86,"reg":94},
        ]
    },
    "Argentina": {
        "flag": "🇦🇷", "rating": 90, "color": "#75c2f0", "color2": "#ffffff",
        "jugadores": [
            {"num":1,"nombre":"Goycochea","pos":"POR","vel":55,"tir":20,"def":88,"pas":70,"reg":40},
            {"num":2,"nombre":"Vázquez","pos":"DEF","vel":76,"tir":55,"def":82,"pas":74,"reg":62},
            {"num":3,"nombre":"Chamot","pos":"DEF","vel":72,"tir":58,"def":84,"pas":76,"reg":64},
            {"num":4,"nombre":"Ruggeri","pos":"DEF","vel":76,"tir":58,"def":88,"pas":74,"reg":66},
            {"num":5,"nombre":"Cáceres","pos":"DEF","vel":74,"tir":60,"def":83,"pas":76,"reg":66},
            {"num":6,"nombre":"Redondo","pos":"MED","vel":78,"tir":75,"def":82,"pas":91,"reg":86},
            {"num":7,"nombre":"Basualdo","pos":"MED","vel":82,"tir":70,"def":76,"pas":80,"reg":76},
            {"num":8,"nombre":"Simeone","pos":"MED","vel":79,"tir":78,"def":82,"pas":82,"reg":76},
            {"num":9,"nombre":"Batistuta","pos":"DEL","vel":82,"tir":94,"def":44,"pas":76,"reg":80},
            {"num":10,"nombre":"Maradona","pos":"DEL","vel":82,"tir":92,"def":42,"pas":96,"reg":99},
            {"num":11,"nombre":"Caniggia","pos":"DEL","vel":94,"tir":84,"def":38,"pas":76,"reg":90},
        ]
    },
    "Francia": {
        "flag": "🇫🇷", "rating": 87, "color": "#1e3a8a", "color2": "#ffffff",
        "jugadores": [
            {"num":1,"nombre":"Lama","pos":"POR","vel":57,"tir":20,"def":87,"pas":70,"reg":38},
            {"num":2,"nombre":"Angloma","pos":"DEF","vel":80,"tir":55,"def":82,"pas":76,"reg":70},
            {"num":3,"nombre":"Blanc","pos":"DEF","vel":72,"tir":62,"def":86,"pas":80,"reg":64},
            {"num":4,"nombre":"Desailly","pos":"DEF","vel":76,"tir":58,"def":90,"pas":78,"reg":62},
            {"num":5,"nombre":"Lizarazu","pos":"DEF","vel":84,"tir":60,"def":84,"pas":82,"reg":82},
            {"num":6,"nombre":"Deschamps","pos":"MED","vel":76,"tir":72,"def":82,"pas":88,"reg":76},
            {"num":7,"nombre":"Petit","pos":"MED","vel":80,"tir":76,"def":78,"pas":84,"reg":78},
            {"num":8,"nombre":"Zidane","pos":"MED","vel":78,"tir":88,"def":62,"pas":96,"reg":96},
            {"num":9,"nombre":"Djorkaeff","pos":"DEL","vel":82,"tir":86,"def":46,"pas":86,"reg":86},
            {"num":10,"nombre":"Dugarry","pos":"DEL","vel":78,"tir":82,"def":48,"pas":80,"reg":80},
            {"num":11,"nombre":"Henry","pos":"DEL","vel":93,"tir":86,"def":40,"pas":82,"reg":90},
        ]
    },
    "Alemania": {
        "flag": "🇩🇪", "rating": 89, "color": "#1a1a1a", "color2": "#ffdd00",
        "jugadores": [
            {"num":1,"nombre":"Köpke","pos":"POR","vel":56,"tir":20,"def":88,"pas":70,"reg":40},
            {"num":2,"nombre":"Reuter","pos":"DEF","vel":80,"tir":60,"def":84,"pas":78,"reg":72},
            {"num":3,"nombre":"Kohler","pos":"DEF","vel":74,"tir":55,"def":89,"pas":76,"reg":62},
            {"num":4,"nombre":"Sammer","pos":"DEF","vel":78,"tir":68,"def":90,"pas":82,"reg":78},
            {"num":5,"nombre":"Helmer","pos":"DEF","vel":78,"tir":60,"def":84,"pas":76,"reg":74},
            {"num":6,"nombre":"Eilts","pos":"MED","vel":74,"tir":72,"def":82,"pas":84,"reg":74},
            {"num":7,"nombre":"Möller","pos":"MED","vel":82,"tir":86,"def":60,"pas":86,"reg":86},
            {"num":8,"nombre":"Häßler","pos":"MED","vel":80,"tir":82,"def":58,"pas":88,"reg":88},
            {"num":9,"nombre":"Klinsmann","pos":"DEL","vel":84,"tir":89,"def":46,"pas":78,"reg":84},
            {"num":10,"nombre":"Völler","pos":"DEL","vel":82,"tir":87,"def":44,"pas":78,"reg":80},
            {"num":11,"nombre":"Bierhoff","pos":"DEL","vel":76,"tir":88,"def":50,"pas":74,"reg":70},
        ]
    },
}

TACTICAS = {
    "4-4-2": {"desc": "Equilibrada · Clásica"},
    "4-3-3": {"desc": "Ofensiva · Presión alta"},
    "3-5-2": {"desc": "Dominio del medio"},
    "5-3-2": {"desc": "Defensiva · Contraataque"},
}

FORMACIONES = {
    "4-4-2": [(0.08,0.50),(0.22,0.15),(0.22,0.40),(0.22,0.60),(0.22,0.85),
              (0.48,0.15),(0.48,0.40),(0.48,0.60),(0.48,0.85),(0.75,0.40),(0.75,0.60)],
    "4-3-3": [(0.08,0.50),(0.22,0.15),(0.22,0.40),(0.22,0.60),(0.22,0.85),
              (0.48,0.25),(0.48,0.50),(0.48,0.75),(0.75,0.20),(0.75,0.50),(0.75,0.80)],
    "3-5-2": [(0.08,0.50),(0.20,0.30),(0.20,0.50),(0.20,0.70),
              (0.42,0.10),(0.42,0.35),(0.42,0.50),(0.42,0.65),(0.42,0.90),
              (0.75,0.40),(0.75,0.60)],
    "5-3-2": [(0.08,0.50),(0.20,0.10),(0.20,0.30),(0.20,0.50),(0.20,0.70),(0.20,0.90),
              (0.45,0.30),(0.45,0.50),(0.45,0.70),(0.75,0.40),(0.75,0.60)],
}

for key, default in [
    ("fase", "menu"), ("dificultad", "Normal"),
    ("equipo_jugador", None), ("equipo_rival", None),
    ("tactica_jugador", None), ("tactica_rival", None),
    ("cesped", "Clásico"), ("balon", "Clásico"),
    ("publico", True), ("sonido", True),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def render_match(eq_jug, eq_riv, tac_jug, tac_riv, dif, cesped, balon, publico, sonido):
    jug = EQUIPOS[eq_jug]
    riv = EQUIPOS[eq_riv]
    form_jug = FORMACIONES[tac_jug]
    form_riv = FORMACIONES[tac_riv]
    d = DIFICULTADES[dif]

    data = {
        "jugadores": jug["jugadores"], "rivales": riv["jugadores"],
        "formJug": form_jug, "formRiv": form_riv,
        "colorJug": jug["color"], "colorJug2": jug["color2"],
        "colorRiv": riv["color"], "colorRiv2": riv["color2"],
        "nombreJug": eq_jug, "nombreRiv": eq_riv,
        "flagJug": jug["flag"], "flagRiv": riv["flag"],
        "difSpeed": d["speed"], "difVision": d["vision"], "difReaction": d["reaction"],
        "cesped": cesped, "balon": balon,
        "publico": publico, "sonido": sonido,
    }

    html = r"""
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#05070b; display:flex; justify-content:center; align-items:center;
       font-family:'Courier New', monospace; padding:8px; }
#wrap { position:relative; border:3px solid #00d4a8; border-radius:14px;
        box-shadow: 0 0 60px rgba(0,212,168,0.35); overflow:hidden; background:#0a0e14; }
canvas { display:block; }
#controls {
    position: absolute;
    bottom: 8px; left: 12px; right: 12px;
    display: flex;
    align-items: center;
    gap: 22px;
    color: #c8d4e0;
    font-size: 11px;
    pointer-events: none;
    z-index: 20;
    padding: 8px 14px;
    background: linear-gradient(90deg, rgba(0,0,0,0.75), rgba(0,0,0,0.4));
    border-radius: 10px;
    border: 1px solid rgba(0,212,168,0.25);
    backdrop-filter: blur(6px);
    font-family: 'Courier New', monospace;
}
.key-group { display: flex; align-items: center; gap: 8px; }
.key-block { display: flex; flex-direction: column; align-items: center; gap: 2px; }
.key-row { display: flex; gap: 2px; }
.key {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 22px;
    height: 22px;
    padding: 0 6px;
    background: linear-gradient(180deg, #1a2430, #0a0f18);
    border: 1px solid #00d4a8;
    border-radius: 5px;
    color: #00ffc8;
    font-weight: 800;
    font-size: 11px;
    box-shadow: 0 0 8px rgba(0,212,168,0.4), inset 0 -2px 0 rgba(0,0,0,0.4);
    text-shadow: 0 0 6px rgba(0,255,200,0.6);
}
.key.wide { padding: 0 18px; letter-spacing: 1px; font-size: 10px; }
.key-label { color: #7a8699; font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 700; }
.info { color: #00ffc8; font-weight: 700; letter-spacing: 1px; font-size: 11px; }
#bigAlert { position:absolute; top:40%; left:50%;
    transform: translate(-50%,-50%); font-size:42px; font-weight:900;
    letter-spacing:6px; opacity:0; pointer-events:none; z-index:15;
    transition:opacity 0.2s; text-shadow: 0 0 30px currentColor; }
#cardAlert { position:absolute; top:55%; right:20px;
    font-size:52px; opacity:0; pointer-events:none; z-index:16;
    transition:opacity 0.2s; }
</style></head><body>
<div id="wrap">
    <canvas id="game" width="960" height="700"></canvas>
    <div id="controls">
        <div class="key-group">
            <div class="key-block">
                <span class="key">W</span>
                <div class="key-row">
                    <span class="key">A</span>
                    <span class="key">S</span>
                    <span class="key">D</span>
                </div>
            </div>
            <span class="key-label">Mover</span>
        </div>
        <div class="key-group">
            <span class="key wide">ESPACIO</span>
            <span class="key-label">Pase</span>
        </div>
        <div class="key-group">
            <span class="key">Q</span>
            <span class="key-label">Regate</span>
        </div>
        <div class="key-group" style="margin-left:auto;">
            <span class="info">__TJ__ vs __TR__ · __DIF__</span>
        </div>
    </div>
    <div id="bigAlert"></div>
    <div id="cardAlert">🟨</div>
</div>
<script>
const CFG = __DATA__;

const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const W = canvas.width, H = canvas.height;

// =====================================================
// CÁMARA CON PERSPECTIVA CÓNICA + SEGUIMIENTO
// =====================================================
const ISO = {
    fieldW: 1100, fieldH: 700,
    centerX: 550, centerY: 350,
    topScaleX: 0.75, bottomScaleX: 1.15, baseScaleY: 0.68,
    baseX: W/2, baseY: H/2 + 30,
    camX: 0, camY: 0, targetCamX: 0, targetCamY: 0,
    zoom: 1.35, targetZoom: 1.35,
};

function toScreen(x, y) {
    const depth = y / ISO.fieldH;
    const scaleX = ISO.topScaleX + (ISO.bottomScaleX - ISO.topScaleX) * depth;
    const nx = (x - ISO.centerX) / ISO.centerX;
    const ny = (y - ISO.centerY) / ISO.centerY;
    const zoomFactor = ISO.zoom;
    const camOffsetX = ISO.camX * scaleX;
    const camOffsetY = ISO.camY * ISO.baseScaleY;
    const sx = ISO.baseX + nx * (ISO.fieldW / 2) * scaleX * zoomFactor + camOffsetX;
    const sy = ISO.baseY + ny * (ISO.fieldH / 2) * ISO.baseScaleY * zoomFactor + camOffsetY;
    return { sx, sy, depth, scaleX };
}

function updateCamera() {
    const targetX = (ball.x - ISO.centerX) * 0.42;
    const targetY = (ball.y - ISO.centerY) * 0.20;
    ISO.targetCamX = -targetX;
    ISO.targetCamY = -targetY;
    const distRight = Math.abs(ball.x - ISO.fieldW);
    const distLeft = Math.abs(ball.x - 0);
    const minDist = Math.min(distRight, distLeft);
    if (minDist < 180) ISO.targetZoom = 1.55;
    else if (minDist < 380) ISO.targetZoom = 1.45;
    else ISO.targetZoom = 1.35;
    ISO.camX += (ISO.targetCamX - ISO.camX) * 0.08;
    ISO.camY += (ISO.targetCamY - ISO.camY) * 0.08;
    ISO.zoom += (ISO.targetZoom - ISO.zoom) * 0.05;
}

function hexToRgb(hex) {
    if (hex.startsWith('rgb')) {
        const m = hex.match(/\d+/g);
        return m ? {r: +m[0], g: +m[1], b: +m[2]} : null;
    }
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? { r: parseInt(result[1],16), g: parseInt(result[2],16), b: parseInt(result[3],16) } : null;
}

// =====================================================
// CÉSPED
// =====================================================
const CESPEDES = {
    "Clásico": { dark:"#0a5522", light:"#0f6f2e", line:"#e8f4ff",
                 crowd:["#5a3a2a","#3a2a1a","#4a3a2a","#6a4a3a"] },
    "Mojado":  { dark:"#052a12", light:"#0a4a1f", line:"#ffffff",
                 crowd:["#2a1a0a","#3a1a1a","#1a1a2a","#2a2a3a"] },
    "Seco":    { dark:"#4a521a", light:"#6a7a2a", line:"#f0e8c0",
                 crowd:["#6a5a3a","#5a4a2a","#4a3a2a","#7a6a4a"] },
    "Nieve":   { dark:"#c8d0d8", light:"#e8eef2", line:"#3a4a5a",
                 crowd:["#8a8a9a","#6a6a7a","#9a8a7a","#7a7a8a"] },
};

// =====================================================
// SPRITES DETALLADOS (14×24)
// =====================================================
const SPRITES = {
    idle: [
        "....HHHHHH....","...HHHHHHHH...","...HHSSSSHH...","..HHSSSSSSHH..",
        "..HSSSSSSSSH..","..HS@SSSS@SH..","..HSSSSSSSSH..","...SSS//SSS...",
        "....SSSSSS....","....SSSSSS....","...JJJJJJJJ...","..JJCCCCCCJJ..",
        "..JJNNNNNNJJ..",".JJJNNNNNNJJJ.",".JJJJJJJJJJJJ.",".jJJJJJJJJJJj.",
        ".jJJJJJJJJJJj.","..JJJJJJJJJJ..","..PPPPPPPPPP..","..PPPPPPPPPP..",
        "..PPPPPPPPPP..","..PPP....PPP..","..BBB....BBB..","..bbb....bbb..",
    ],
    run1: [
        "....HHHHHH....","...HHHHHHHH...","...HHSSSSHH...","..HHSSSSSSHH..",
        "..HSSSSSSSSH..","..HS@SSSS@SH..","..HSSSSSSSSH..","...SSS//SSS...",
        "....SSSSSS....","...JJJJJJJJ...","..JJCCCCCCJJ..","..JJNNNNNNJJ..",
        ".JJJNNNNNNJJJ.",".JJJJJJJJJJJJ.",".jJJJJJJJJJJj.","..JJJJJJJJJJ..",
        "..PPPPPPPPPP..","..PPPPPPPPPP..","..PPPPPPPPP...",".PPP....PPPP..",
        ".BBB....PPPP..",".bbb....PPP...","........BBB...","........bbb...",
    ],
    run2: [
        "....HHHHHH....","...HHHHHHHH...","...HHSSSSHH...","..HHSSSSSSHH..",
        "..HSSSSSSSSH..","..HS@SSSS@SH..","..HSSSSSSSSH..","...SSS//SSS...",
        "....SSSSSS....","....SSSSSS....","...JJJJJJJJ...","..JJCCCCCCJJ..",
        "..JJNNNNNNJJ..",".JJJNNNNNNJJJ.",".JJJJJJJJJJJJ.",".jJJJJJJJJJJj.",
        "..JJJJJJJJJJ..","..PPPPPPPPPP..","...PPPPPPPPP..","..PPPP....PPP.",
        "..PPPP....PPP.","..BBB.....BBB.","..bbb.....bbb.","..............",
    ],
    shoot: [
        "....HHHHHH....","...HHHHHHHH...","...HHSSSSHH...","..HHSSSSSSHH..",
        "..HSSSSSSSSH..","..HS@SSSS@SH..","..HSSSSSSSSH..","...SSS//SSS...",
        "....SSSSSS....","....SSSSSS....","...JJJJJJJJ...","..JJCCCCCCJJ..",
        "..JJNNNNNNJJ..","..JJNNNNNNJJ..",".JJJJJJJJJJJJ.","jJJJJJJJJJJJJj",
        "jJJJJJJJJJJJJj","..JJJJJJJJJJ..","..PPPPPPPPPP..","..PPPPPPPPPP..",
        "..PPPPPPPPPP..","..PPP....PPP..","..BBB....BBB..","..bbb....bbb..",
    ],
    celebrate: [
        "..S.HHHHHH.S..","..S.HHHHHH.S..","..S.HHSSHH.S..","..SHHSSSSHHS..",
        "..SHSSSSSSHS..","...HS@SS@SH...","...HSSSSSSH...","....SS//SS....",
        "....SSSSSS....","...JJJJJJJJ...","..JJCCCCCCJJ..","..JJNNNNNNJJ..",
        ".JJJNNNNNNJJJ.",".JJJJJJJJJJJJ.","jJJJJJJJJJJJJj","jJJJJJJJJJJJJj",
        "..JJJJJJJJJJ..","..PPPPPPPPPP..","..PPPPPPPPPP..","..PPPPPPPPPP..",
        "..PPP....PPP..","..BBB....BBB..","..bbb....bbb..","..............",
    ],
    tackle: [
        "......................","......................","......................",
        "......................","......................","..........HHHHHH......",
        ".........HHHHHHHH.....","........HHSSSSSSHH....",".......HSS@SSSS@SSH...",
        ".......HSSSSSSSSSSH...","........SSS//SSSS.....","......JJJJJJJJJJJ.....",
        ".....JJJCCCCCCCJJJ....","....JJJJNNNNNJJJJJ....","...JJJJJJJJJJJJJJJ....",
        "..JJJJJJJJJJJJJJJJ....",".jjJJJJJJJJJJJJJJJjj..","..PPPPPPPPPPPPPPPP....",
        ".PPPPP...........PPP..","BBBB..............BBB.","bbb................bbb",
    ],
    fallen: [
        "......................","......................","......................",
        "......................","......................","......................",
        ".........HHHHHH.......","........HHHHHHHH......",".......HHSSSSSSHH.....",
        "......HSS@SSSS@SSH....","......HSSSSSSSSSSH....",".......SSS//SSSS......",
        "....JJJJJJJJJJJJJ.....","...JJJCCCCCCCCCJJJ....","..JJJJNNNNNNNJJJJJ....",
        ".JJJJJJJJJJJJJJJJJ....","jjJJJJJJJJJJJJJJJJjj..","..PPPPPPPPPPPPPPPP....",
        ".PPPPP..........PPPP..","BBBB..............BBB.","bbb................bbb",
    ],
};

function drawPixelSprite(sprite, x, y, pixelSize, color1, color2, dorsal, facingRight, isControlled, depth) {
    const h = sprite.length;
    const w = sprite[0].length;
    const offsetX = -w * pixelSize / 2;
    const offsetY = -h * pixelSize;
    const fogAlpha = 0.15 + depth * 0.85;
    
    const shadowOffsetY = 3 + depth * 4;
    const shadowScale = 0.6 + depth * 0.4;
    ctx.fillStyle = `rgba(0,0,0,${0.25 + depth * 0.25})`;
    ctx.beginPath();
    ctx.ellipse(x, y + shadowOffsetY, w * pixelSize * 0.45 * shadowScale,
                w * pixelSize * 0.18 * shadowScale, 0, 0, Math.PI * 2);
    ctx.fill();
    
    for (let row = 0; row < h; row++) {
        for (let col = 0; col < w; col++) {
            const c = facingRight ? col : (w - 1 - col);
            const ch = sprite[row][c];
            if (ch === '.') continue;
            const px = x + offsetX + col * pixelSize;
            const py = y + offsetY + row * pixelSize;
            let color;
            switch (ch) {
                case 'H': color = '#1a0f08'; break;
                case 'h': color = '#3a2810'; break;
                case 'S': color = '#f0c8a0'; break;
                case '@': color = '#0a0a0a'; break;
                case '/': color = '#a04020'; break;
                case 'J': color = color1; break;
                case 'j': color = color2; break;
                case 'C': color = color2; break;
                case 'N': color = '#ffffff'; break;
                case 'P': color = '#1a1a2a'; break;
                case 'p': color = '#2a2a3a'; break;
                case 'B': color = '#0a0a0a'; break;
                case 'b': color = '#3a3a3a'; break;
                default: color = '#ff00ff';
            }
            if (depth < 1) {
                const fogR = 60, fogG = 80, fogB = 110;
                const rgb = hexToRgb(color);
                if (rgb) {
                    const mix = (1 - fogAlpha) * 0.5;
                    const r = Math.round(rgb.r * (1 - mix) + fogR * mix);
                    const g = Math.round(rgb.g * (1 - mix) + fogG * mix);
                    const b = Math.round(rgb.b * (1 - mix) + fogB * mix);
                    color = `rgb(${r},${g},${b})`;
                }
            }
            ctx.fillStyle = color;
            ctx.fillRect(Math.round(px), Math.round(py), pixelSize, pixelSize);
        }
    }
    
    ctx.font = `bold ${Math.round(pixelSize * 4.5)}px Courier New`;
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillStyle = 'rgba(0,0,0,0.85)';
    ctx.strokeStyle = 'rgba(255,255,255,0.9)';
    ctx.lineWidth = 2;
    const dorsalY = y - h * pixelSize * 0.45;
    ctx.strokeText(dorsal, x, dorsalY);
    ctx.fillText(dorsal, x, dorsalY);
    
    if (isControlled) {
        ctx.strokeStyle = '#00ffc8'; ctx.lineWidth = 2;
        ctx.shadowColor = '#00ffc8'; ctx.shadowBlur = 18;
        ctx.beginPath();
        ctx.ellipse(x, y + 3, w * pixelSize * 0.68, h * pixelSize * 0.14, 0, 0, Math.PI * 2);
        ctx.stroke();
        ctx.shadowBlur = 0;
    }
    ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
}

// =====================================================
// BALÓN
// =====================================================
let ballRotation = 0;
function drawBall(ball, radius) {
    const { x, y } = ball;
    const r = radius;
    const speed = Math.hypot(ball.vx || 0, ball.vy || 0);
    ballRotation += speed * 0.03;
    
    ctx.fillStyle = 'rgba(0,0,0,0.45)';
    ctx.beginPath();
    ctx.ellipse(x + 3, y + 7, r * 1.1, r * 0.5, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#111111';
    drawPolygon(x, y, 5, r * 0.35, ballRotation);
    for (let i = 0; i < 5; i++) {
        const a = (i / 5) * Math.PI * 2 - Math.PI / 2 + ballRotation;
        drawPolygon(x + Math.cos(a) * r * 0.72, y + Math.sin(a) * r * 0.72, 5, r * 0.28, a);
    }
    ctx.strokeStyle = 'rgba(0,0,0,0.5)'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.stroke();
    ctx.fillStyle = 'rgba(255,255,255,0.5)';
    ctx.beginPath(); ctx.arc(x - r*0.35, y - r*0.4, r*0.3, 0, Math.PI * 2); ctx.fill();
}
function drawPolygon(cx, cy, sides, radius, rotation) {
    ctx.beginPath();
    for (let i = 0; i < sides; i++) {
        const a = rotation + (i / sides) * Math.PI * 2 - Math.PI / 2;
        const px = cx + Math.cos(a) * radius, py = cy + Math.sin(a) * radius;
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    }
    ctx.closePath(); ctx.fill();
}

// =====================================================
// PÚBLICO
// =====================================================
function drawCrowd() {
    const cp = CESPEDES[CFG.cesped].crowd;
    const gradTop = ctx.createLinearGradient(0, 0, 0, 110);
    gradTop.addColorStop(0, '#05070b');
    gradTop.addColorStop(1, '#151a24');
    ctx.fillStyle = gradTop;
    ctx.fillRect(0, 0, W, 110);
    for (let fila = 0; fila < 3; fila++) {
        const baseY = 8 + fila * 26;
        const size = 5 + fila;
        const spacing = 6 + fila;
        const alpha = 0.6 + fila * 0.15;
        ctx.globalAlpha = alpha;
        for (let x = 4; x < W - 4; x += spacing) {
            const idx = (x + fila * 13) % cp.length;
            ctx.fillStyle = cp[idx];
            ctx.fillRect(x, baseY + 2, size - 1, size - 1);
            ctx.fillStyle = '#e8b890';
            ctx.fillRect(x + 1, baseY, size - 3, size - 3);
        }
    }
    ctx.globalAlpha = 1;
    ctx.fillStyle = '#1a1a2a'; ctx.fillRect(0, 95, W, 15);
    ctx.fillStyle = '#00d4a8'; ctx.font = 'bold 10px Courier New'; ctx.textAlign = 'center';
    for (let i = 0; i < 6; i++) ctx.fillText('RETRO FOOTBALL 96', W/2 + (i - 2.5) * 160, 106);
    ctx.textAlign = 'left';
    const gradBot = ctx.createLinearGradient(0, H - 90, 0, H);
    gradBot.addColorStop(0, '#151a24'); gradBot.addColorStop(1, '#05070b');
    ctx.fillStyle = gradBot; ctx.fillRect(0, H - 90, W, 90);
    ctx.fillStyle = '#1a1a2a'; ctx.fillRect(0, H - 90, W, 15);
    ctx.fillStyle = '#ff9f43'; ctx.font = 'bold 10px Courier New'; ctx.textAlign = 'center';
    for (let i = 0; i < 6; i++) ctx.fillText('· FIFA TOTAL ·', W/2 + (i - 2.5) * 160, H - 79);
    ctx.textAlign = 'left';
    for (let fila = 0; fila < 2; fila++) {
        const baseY = H - 70 + fila * 32;
        const size = 6 + fila;
        const spacing = 7 + fila;
        const alpha = 0.7 + fila * 0.15;
        ctx.globalAlpha = alpha;
        for (let x = 4; x < W - 4; x += spacing) {
            const idx = (x + fila * 17 + 3) % cp.length;
            ctx.fillStyle = cp[idx];
            ctx.fillRect(x, baseY + 2, size - 1, size - 1);
            ctx.fillStyle = '#e8b890';
            ctx.fillRect(x + 1, baseY, size - 3, size - 3);
        }
    }
    ctx.globalAlpha = 1;
}

// =====================================================
// CAMPO CON PORTERÍAS REALISTAS
// =====================================================
function drawField() {
    const c = CESPEDES[CFG.cesped];
    const tl = toScreen(0, 0);
    const tr = toScreen(ISO.fieldW, 0);
    const br = toScreen(ISO.fieldW, ISO.fieldH);
    const bl = toScreen(0, ISO.fieldH);
    ctx.fillStyle = c.dark;
    ctx.beginPath();
    ctx.moveTo(tl.sx, tl.sy); ctx.lineTo(tr.sx, tr.sy);
    ctx.lineTo(br.sx, br.sy); ctx.lineTo(bl.sx, bl.sy);
    ctx.closePath(); ctx.fill();
    
    const stripes = 14;
    for (let i = 0; i < stripes; i++) {
        const x1 = (i / stripes) * ISO.fieldW;
        const x2 = ((i + 1) / stripes) * ISO.fieldW;
        if (i % 2 === 0) continue;
        const p1 = toScreen(x1, 0), p2 = toScreen(x2, 0);
        const p3 = toScreen(x2, ISO.fieldH), p4 = toScreen(x1, ISO.fieldH);
        ctx.fillStyle = c.light;
        ctx.beginPath();
        ctx.moveTo(p1.sx, p1.sy); ctx.lineTo(p2.sx, p2.sy);
        ctx.lineTo(p3.sx, p3.sy); ctx.lineTo(p4.sx, p4.sy);
        ctx.closePath(); ctx.fill();
    }
    ctx.globalAlpha = 0.08;
    for (let i = 0; i < 300; i++) {
        const rx = Math.random() * ISO.fieldW;
        const ry = Math.random() * ISO.fieldH;
        const p = toScreen(rx, ry);
        const size = 1 + Math.random() * 2;
        ctx.fillStyle = i % 2 === 0 ? '#ffffff' : '#000000';
        ctx.fillRect(p.sx, p.sy, size, size);
    }
    ctx.globalAlpha = 1;
    
    const drawIsoLine = (x1, y1, x2, y2) => {
        const p1 = toScreen(x1, y1), p2 = toScreen(x2, y2);
        ctx.beginPath(); ctx.moveTo(p1.sx, p1.sy); ctx.lineTo(p2.sx, p2.sy); ctx.stroke();
    };
    const drawIsoRect = (x, y, w, h) => {
        drawIsoLine(x, y, x+w, y); drawIsoLine(x+w, y, x+w, y+h);
        drawIsoLine(x+w, y+h, x, y+h); drawIsoLine(x, y+h, x, y);
    };
    const drawIsoCircle = (cx, cy, r) => {
        ctx.beginPath();
        for (let i = 0; i <= 40; i++) {
            const a = (i / 40) * Math.PI * 2;
            const p = toScreen(cx + Math.cos(a)*r, cy + Math.sin(a)*r);
            if (i === 0) ctx.moveTo(p.sx, p.sy); else ctx.lineTo(p.sx, p.sy);
        }
        ctx.stroke();
    };
    ctx.strokeStyle = c.line; ctx.lineWidth = 2;
    ctx.shadowColor = c.line; ctx.shadowBlur = 4;
    drawIsoRect(0, 0, ISO.fieldW, ISO.fieldH);
    drawIsoLine(ISO.centerX, 0, ISO.centerX, ISO.fieldH);
    drawIsoCircle(ISO.centerX, ISO.centerY, 60);
    drawIsoRect(0, ISO.centerY - 100, 90, 200);
    drawIsoRect(ISO.fieldW - 90, ISO.centerY - 100, 90, 200);
    drawIsoRect(0, ISO.centerY - 50, 35, 100);
    drawIsoRect(ISO.fieldW - 35, ISO.centerY - 50, 35, 100);
    const pPen1 = toScreen(70, ISO.centerY);
    const pPen2 = toScreen(ISO.fieldW - 70, ISO.centerY);
    ctx.fillStyle = c.line;
    ctx.beginPath(); ctx.arc(pPen1.sx, pPen1.sy, 2, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(pPen2.sx, pPen2.sy, 2, 0, Math.PI*2); ctx.fill();
    
    // ============ PORTERÍAS REALISTAS ============
    const GOAL_H = 60;
    const GOAL_DEPTH = 28;
    const gTopL = toScreen(0, ISO.centerY - GOAL_H);
    const gBotL = toScreen(0, ISO.centerY + GOAL_H);
    const gBackTopL = toScreen(-GOAL_DEPTH, ISO.centerY - GOAL_H);
    const gBackBotL = toScreen(-GOAL_DEPTH, ISO.centerY + GOAL_H);
    ctx.strokeStyle = 'rgba(200,220,255,0.35)'; ctx.lineWidth = 1;
    for (let i = 0; i <= 10; i++) {
        const t = i / 10;
        const y1 = gTopL.sy + (gBotL.sy - gTopL.sy) * t;
        const y2 = gBackTopL.sy + (gBackBotL.sy - gBackTopL.sy) * t;
        ctx.beginPath(); ctx.moveTo(gTopL.sx, y1); ctx.lineTo(gBackTopL.sx, y2); ctx.stroke();
    }
    for (let i = 0; i <= 8; i++) {
        const t = i / 8;
        const x1 = gTopL.sx + (gBackTopL.sx - gTopL.sx) * t;
        const y1 = gTopL.sy + (gBackTopL.sy - gTopL.sy) * t;
        const x2 = gBotL.sx + (gBackBotL.sx - gBotL.sx) * t;
        const y2 = gBotL.sy + (gBackBotL.sy - gBotL.sy) * t;
        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    }
    ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 4;
    ctx.shadowColor = '#ffffff'; ctx.shadowBlur = 6;
    ctx.beginPath(); ctx.moveTo(gTopL.sx, gTopL.sy); ctx.lineTo(gBackTopL.sx, gBackTopL.sy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(gBotL.sx, gBotL.sy); ctx.lineTo(gBackBotL.sx, gBackBotL.sy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(gBackTopL.sx, gBackTopL.sy); ctx.lineTo(gBackBotL.sx, gBackBotL.sy); ctx.stroke();
    
    const gTopR = toScreen(ISO.fieldW, ISO.centerY - GOAL_H);
    const gBotR = toScreen(ISO.fieldW, ISO.centerY + GOAL_H);
    const gBackTopR = toScreen(ISO.fieldW + GOAL_DEPTH, ISO.centerY - GOAL_H);
    const gBackBotR = toScreen(ISO.fieldW + GOAL_DEPTH, ISO.centerY + GOAL_H);
    ctx.strokeStyle = 'rgba(200,220,255,0.35)'; ctx.lineWidth = 1;
    for (let i = 0; i <= 10; i++) {
        const t = i / 10;
        const y1 = gTopR.sy + (gBotR.sy - gTopR.sy) * t;
        const y2 = gBackTopR.sy + (gBackBotR.sy - gBackTopR.sy) * t;
        ctx.beginPath(); ctx.moveTo(gTopR.sx, y1); ctx.lineTo(gBackTopR.sx, y2); ctx.stroke();
    }
    for (let i = 0; i <= 8; i++) {
        const t = i / 8;
        const x1 = gTopR.sx + (gBackTopR.sx - gTopR.sx) * t;
        const y1 = gTopR.sy + (gBackTopR.sy - gTopR.sy) * t;
        const x2 = gBotR.sx + (gBackBotR.sx - gBotR.sx) * t;
        const y2 = gBotR.sy + (gBackBotR.sy - gBotR.sy) * t;
        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    }
    ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(gTopR.sx, gTopR.sy); ctx.lineTo(gBackTopR.sx, gBackTopR.sy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(gBotR.sx, gBotR.sy); ctx.lineTo(gBackBotR.sx, gBackBotR.sy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(gBackTopR.sx, gBackTopR.sy); ctx.lineTo(gBackBotR.sx, gBackBotR.sy); ctx.stroke();
    ctx.shadowBlur = 0;
}

// =====================================================
// MARCADOR
// =====================================================
function drawScoreboard(score, time) {
    const x = 20, y = 20, w = 240, h = 90;
    ctx.fillStyle = 'rgba(0,0,0,0.7)'; ctx.fillRect(x + 4, y + 4, w, h);
    ctx.fillStyle = '#1a1a2a'; ctx.fillRect(x, y, w, h);
    ctx.strokeStyle = '#00ff88'; ctx.lineWidth = 2; ctx.strokeRect(x, y, w, h);
    ctx.fillStyle = '#00ff88'; ctx.fillRect(x, y, 70, 22);
    ctx.fillStyle = '#000000'; ctx.font = 'bold 14px Courier New';
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText('MIN', x + 35, y + 11);
    ctx.fillStyle = '#000000'; ctx.font = 'bold 36px Courier New';
    ctx.fillText(score.you + '-' + score.rival, x + w/2, y + 55);
    const mm = Math.floor(time / 60).toString().padStart(2, '0');
    const ss = Math.floor(time % 60).toString().padStart(2, '0');
    ctx.fillStyle = '#00ff88'; ctx.fillRect(x, y + h - 22, w, 22);
    ctx.fillStyle = '#000000'; ctx.font = 'bold 16px Courier New';
    ctx.fillText(mm + ':' + ss, x + w/2, y + h - 11);
    ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
}

// =====================================================
// SONIDOS
// =====================================================
let audioCtx = null;
if (CFG.sonido) {
    try { audioCtx = new (window.AudioContext || window.webkitAudioContext)(); } catch(e) {}
}
function playWhistle() {
    if (!audioCtx) return;
    const o = audioCtx.createOscillator(), g = audioCtx.createGain();
    o.type = 'sine'; o.frequency.value = 2200;
    g.gain.setValueAtTime(0.15, audioCtx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.4);
    o.connect(g).connect(audioCtx.destination);
    o.start(); o.stop(audioCtx.currentTime + 0.4);
}
function playKick() {
    if (!audioCtx) return;
    const o = audioCtx.createOscillator(), g = audioCtx.createGain();
    o.type = 'square';
    o.frequency.setValueAtTime(200, audioCtx.currentTime);
    o.frequency.exponentialRampToValueAtTime(60, audioCtx.currentTime + 0.1);
    g.gain.setValueAtTime(0.2, audioCtx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
    o.connect(g).connect(audioCtx.destination);
    o.start(); o.stop(audioCtx.currentTime + 0.15);
}
function playGoal() {
    if (!audioCtx) return;
    const bs = audioCtx.sampleRate * 1.5;
    const buf = audioCtx.createBuffer(1, bs, audioCtx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < bs; i++) d[i] = (Math.random()*2-1) * (1 - i/bs);
    const noise = audioCtx.createBufferSource(); noise.buffer = buf;
    const f = audioCtx.createBiquadFilter();
    f.type = 'bandpass'; f.frequency.value = 500; f.Q.value = 0.7;
    const g = audioCtx.createGain(); g.gain.value = 0.3;
    noise.connect(f).connect(g).connect(audioCtx.destination);
    noise.start();
}
function startAmbient() {
    if (!audioCtx) return;
    const bs = audioCtx.sampleRate * 4;
    const buf = audioCtx.createBuffer(1, bs, audioCtx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < bs; i++) d[i] = Math.random()*2-1;
    const noise = audioCtx.createBufferSource(); noise.buffer = buf; noise.loop = true;
    const f = audioCtx.createBiquadFilter();
    f.type = 'bandpass'; f.frequency.value = 800; f.Q.value = 0.5;
    const g = audioCtx.createGain(); g.gain.value = 0.02;
    noise.connect(f).connect(g).connect(audioCtx.destination);
    noise.start();
}
startAmbient();

// =====================================================
// ESTADO
// =====================================================
const FIELD = { w: ISO.fieldW, h: ISO.fieldH };
const PR = 9, BR = 6;
let keys = {};
let matchTime = 90;
let score = { you: 0, rival: 0 };
let message = "";
let messageTimer = 0;
let lastTime = performance.now();
let dribbleCooldown = 0;
let animTimer = 0;
let gameState = "play";
let freezeTimer = 0;
let lastBallToucher = null;
const cards = {};
const particles = [];

function spawnParticles(x, y, color, count) {
    for (let i = 0; i < count; i++) {
        const angle = Math.random() * Math.PI * 2;
        const speed = 1 + Math.random() * 3;
        particles.push({
            x, y, vx: Math.cos(angle) * speed, vy: Math.sin(angle) * speed - 1,
            life: 30 + Math.random() * 20, maxLife: 50, color,
            size: 2 + Math.random() * 3,
        });
    }
}
function updateParticles() {
    for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx; p.y += p.vy; p.vy += 0.15; p.vx *= 0.96; p.life--;
        if (p.life <= 0) particles.splice(i, 1);
    }
}
function drawParticles() {
    particles.forEach(p => {
        const alpha = p.life / p.maxLife;
        ctx.globalAlpha = alpha;
        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size * alpha, 0, Math.PI * 2);
        ctx.fill();
    });
    ctx.globalAlpha = 1;
}

// =====================================================
// JUGADORES
// =====================================================
const you = { players: [] };
const rival = { players: [] };

CFG.formJug.forEach(([fx, fy], i) => {
    const dd = CFG.jugadores[i] || {};
    you.players.push({
        x: fx * FIELD.w, y: fy * FIELD.h, vx: 0, vy: 0,
        num: dd.num || i+1, name: dd.nombre || dd.name || 'Jugador',
        vel: dd.vel || 75, tir: dd.tir || 75, def: dd.def || 75,
        pas: dd.pas || 75, reg: dd.reg || 75,
        isControlled: i === 0, side: 'you', facingRight: true,
        state: 'idle', stateTimer: 0, isGK: i === 0 && dd.pos === "POR",
        homeX: fx * FIELD.w, homeY: fy * FIELD.h,
    });
});
CFG.formRiv.forEach(([fx, fy], i) => {
    const dd = CFG.rivales[i] || {};
    rival.players.push({
        x: FIELD.w - fx * FIELD.w, y: fy * FIELD.h, vx: 0, vy: 0,
        num: dd.num || i+1, name: dd.nombre || dd.name || 'Rival',
        vel: dd.vel || 75, tir: dd.tir || 75, def: dd.def || 75,
        pas: dd.pas || 75, reg: dd.reg || 75,
        isControlled: false, side: 'rival', facingRight: false,
        state: 'idle', stateTimer: 0, isGK: i === 0 && dd.pos === "POR",
        homeX: FIELD.w - fx * FIELD.w, homeY: fy * FIELD.h,
    });
});

const ball = { x: FIELD.w/2, y: FIELD.h/2, vx: 0, vy: 0 };

window.addEventListener('keydown', e => {
    const k = e.key.toLowerCase();
    keys[k] = true;
    if (e.key === ' ') e.preventDefault();
    if (k === 'q' && dribbleCooldown <= 0 && gameState === "play") attemptDribble();
});
window.addEventListener('keyup', e => { keys[e.key.toLowerCase()] = false; });

function dist(a, b) { return Math.hypot(a.x - b.x, a.y - b.y); }
function clampToField(o, r) {
    o.x = Math.max(r, Math.min(FIELD.w - r, o.x));
    o.y = Math.max(r, Math.min(FIELD.h - r, o.y));
}
function updatePlayer(p, dx, dy, baseSpeed) {
    if (p.state === 'fallen' || p.state === 'tackle') return;
    const boost = 0.6 + (p.vel / 100) * 0.8;
    const speed = baseSpeed * boost;
    const len = Math.hypot(dx, dy);
    if (len > 0) {
        p.vx = (dx / len) * speed; p.vy = (dy / len) * speed;
    } else { p.vx *= 0.85; p.vy *= 0.85; }
    p.x += p.vx; p.y += p.vy;
    clampToField(p, PR);
}

function showBigAlert(text, color) {
    const a = document.getElementById('bigAlert');
    a.textContent = text; a.style.color = color; a.style.opacity = '1';
    setTimeout(() => a.style.opacity = '0', 1200);
}
function showCard(type) {
    const a = document.getElementById('cardAlert');
    a.textContent = type; a.style.opacity = '1';
    setTimeout(() => a.style.opacity = '0', 1500);
}

function attemptTackle(defender, attacker) {
    if (defender.state === 'tackle' || defender.state === 'fallen') return false;
    if (defender.tackleCooldown > 0) return false;
    defender.state = 'tackle'; defender.stateTimer = 18;
    defender.tackleCooldown = 120;
    playKick();
    const prob = 0.35 + (defender.def - attacker.reg) / 250;
    const success = Math.random() < Math.max(0.15, Math.min(0.85, prob));
    if (success) {
        const angle = Math.atan2(attacker.y - defender.y, attacker.x - defender.x);
        ball.vx = Math.cos(angle) * 5; ball.vy = Math.sin(angle) * 5;
        attacker.state = 'fallen'; attacker.stateTimer = 40;
        lastBallToucher = defender;
        return true;
    } else {
        defender.state = 'fallen'; defender.stateTimer = 60;
        attacker.state = 'fallen'; attacker.stateTimer = 40;
        commitFoul(defender, attacker);
        return false;
    }
}

function commitFoul(defender, attacker) {
    playWhistle();
    gameState = "foul"; freezeTimer = 120;
    const isInBox =
        (defender.side === 'you' && attacker.x < 90 && Math.abs(attacker.y - ISO.centerY) < 100) ||
        (defender.side === 'rival' && attacker.x > FIELD.w - 90 && Math.abs(attacker.y - ISO.centerY) < 100);
    if (isInBox) {
        showBigAlert("¡PENALTI!", "#ff3b5c"); gameState = "penalty";
        if (defender.side === 'you') { ball.x = 70; ball.y = ISO.centerY; }
        else { ball.x = FIELD.w - 70; ball.y = ISO.centerY; }
    } else {
        showBigAlert("FALTA", "#ffdd00");
        ball.x = attacker.x; ball.y = attacker.y;
    }
    ball.vx = 0; ball.vy = 0;
    const cardRoll = Math.random();
    if (cardRoll < 0.35) {
        const id = defender.side + '_' + defender.num;
        cards[id] = cards[id] || { yellow: 0 };
        cards[id].yellow++; showCard("🟨");
        defender.state = 'fallen'; defender.stateTimer = 120;
        if (cards[id].yellow >= 2) {
            showCard("🟥"); cards[id].red = true;
            defender.x = -200; defender.y = -200;
        }
    } else if (cardRoll < 0.5) {
        const id = defender.side + '_' + defender.num;
        cards[id] = cards[id] || { yellow: 0 };
        cards[id].red = true; showCard("🟥");
        defender.x = -200; defender.y = -200;
    }
}

function checkOutOfBounds() {
    if (ball.y - BR < 0 || ball.y + BR > FIELD.h) {
        const y = ball.y < FIELD.h/2 ? BR + 10 : FIELD.h - BR - 10;
        ball.y = y;
        ball.x = Math.max(50, Math.min(FIELD.w - 50, ball.x));
        ball.vx = 0; ball.vy = 0;
        gameState = "throwin"; freezeTimer = 60;
        showBigAlert("SAQUE DE BANDA", "#00d4a8"); playWhistle();
        return true;
    }
    if (ball.x - BR < 0 || ball.x + BR > FIELD.w) {
        const gTop = FIELD.h/2 - 45, gBot = FIELD.h/2 + 45;
        const isGoal = (ball.y > gTop && ball.y < gBot);
        if (isGoal) return false;
        const isLeft = ball.x < FIELD.w/2;
        const cornerY = ball.y < FIELD.h/2 ? 10 : FIELD.h - 10;
        ball.x = isLeft ? 10 : FIELD.w - 10;
        ball.y = cornerY;
        ball.vx = 0; ball.vy = 0;
        gameState = "corner"; freezeTimer = 60;
        showBigAlert("CÓRNER", "#ffdd00"); playWhistle();
        return true;
    }
    return false;
}

function checkOffside() {
    if (gameState !== "play") return;
    if (lastBallToucher !== you.players[0]) return;
    if (Math.abs(ball.vx) < 5 && Math.abs(ball.vy) < 5) return;
    let receiver = null, rdist = 999;
    you.players.forEach((p, i) => {
        if (i === 0 || p.state === 'fallen') return;
        const d = dist(p, ball);
        if (d < 40 && d < rdist) { rdist = d; receiver = p; }
    });
    if (!receiver) return;
    let lastDefenderX = FIELD.w;
    rival.players.forEach(r => { if (r.x < lastDefenderX) lastDefenderX = r.x; });
    if (receiver.x > lastDefenderX + 5 && receiver.x > FIELD.w / 2) {
        playWhistle(); showBigAlert("FUERA DE JUEGO", "#ff3b5c");
        gameState = "freeze"; freezeTimer = 90;
        ball.x = receiver.x; ball.y = receiver.y;
        ball.vx = 0; ball.vy = 0;
    }
}

function rivalTackleCheck() {
    if (gameState !== "play") return;
    const owner = findBallOwner();
    if (!owner || owner.side !== 'you') return;
    rival.players.forEach(r => {
        if (r.state === 'tackle' || r.state === 'fallen') return;
        if (r.tackleCooldown === undefined) r.tackleCooldown = 0;
        if (r.tackleCooldown > 0) return;
        const idx = rival.players.indexOf(r);
        if (idx === 0) return;
        const d = dist(r, owner);
        if (d < 30 && Math.random() < 0.08) attemptTackle(r, owner);
    });
}

function updateControlled() {
    if (gameState !== "play") return;
    const p = you.players[0];
    if (p.state === 'fallen' || p.state === 'tackle') return;
    let dx = 0, dy = 0;
    if (keys['w'] || keys['arrowup']) dy -= 1;
    if (keys['s'] || keys['arrowdown']) dy += 1;
    if (keys['a'] || keys['arrowleft']) dx -= 1;
    if (keys['d'] || keys['arrowright']) dx += 1;
    if (dx !== 0) p.facingRight = dx > 0;
    updatePlayer(p, dx, dy, 4.5);
    if (keys[' '] && dist(p, ball) < PR + BR + 8) {
        let best = null, bestScore = -Infinity;
        for (let i = 1; i < you.players.length; i++) {
            const mate = you.players[i];
            const fwd = mate.x - p.x;
            if (fwd > 0 && fwd < 350) {
                const s = fwd - Math.abs(mate.y - p.y) * 0.5 + (mate.pas - 75) * 2;
                if (s > bestScore) { bestScore = s; best = mate; }
            }
        }
        if (best) {
            const angle = Math.atan2(best.y - ball.y, best.x - ball.x);
            ball.vx = Math.cos(angle) * 9; ball.vy = Math.sin(angle) * 9;
            keys[' '] = false;
            p.state = 'shoot'; p.stateTimer = 15;
            lastBallToucher = p; playKick();
            const bp2 = toScreen(ball.x, ball.y);
            spawnParticles(bp2.sx, bp2.sy, '#ffffff', 8);
            setTimeout(() => checkOffside(), 100);
        }
    }
}

function updateRival() {
    if (gameState !== "play") return;
    const owner = findBallOwner();
    const weAttack = !owner || owner.side === 'you';
    for (let i = 0; i < rival.players.length; i++) {
        const p = rival.players[i];
        if (p.state === 'fallen' || p.state === 'tackle') continue;
        if (p.x < 0) continue;
        let target;
        if (weAttack) {
            if (i === 0) {
                target = { x: FIELD.w - 25, y: Math.max(FIELD.h/2 - 70, Math.min(FIELD.h/2 + 70, ball.y)) };
            } else if (i <= 4) {
                const zoneY = FIELD.h/2 + (i - 2.5) * 55;
                target = { x: Math.max(FIELD.w * 0.55, Math.min(FIELD.w - 60, ball.x + 120)), y: zoneY * 0.7 + ball.y * 0.3 };
            } else if (i <= 7) {
                const dToBall = dist(p, ball);
                if (dToBall < 180 && owner && owner.side === 'you') target = ball;
                else target = { x: FIELD.w * 0.5 + (i - 6) * 40, y: ball.y * 0.5 + (FIELD.h/2) * 0.5 };
            } else {
                const dToBall = dist(p, ball);
                if (dToBall < 220) target = ball;
                else target = { x: Math.min(FIELD.w - 80, ball.x + 200), y: FIELD.h/2 + (i - 9) * 70 };
            }
        } else {
            const carrier = owner;
            if (i === 0) target = { x: FIELD.w - 25, y: FIELD.h/2 };
            else if (i <= 4) target = { x: FIELD.w * 0.55, y: FIELD.h/2 + (i - 2.5) * 55 };
            else if (i <= 7) target = { x: carrier.x + (i - 6) * 60, y: carrier.y + (i % 2 === 0 ? 60 : -60) };
            else target = { x: Math.min(FIELD.w - 80, carrier.x + 220 + (i - 9) * 50), y: FIELD.h/2 + (i - 9) * 80 };
        }
        const dx = target.x - p.x, dy = target.y - p.y;
        if (dx !== 0) p.facingRight = dx > 0;
        const d = Math.hypot(dx, dy) || 1;
        let speed;
        if (i === 0) speed = CFG.difSpeed * 0.6;
        else if (i <= 4) speed = CFG.difSpeed * 0.85;
        else if (i <= 7) speed = CFG.difSpeed * 0.95;
        else speed = CFG.difSpeed;
        if (d > 4) updatePlayer(p, dx/d, dy/d, speed);
        else { p.vx *= 0.85; p.vy *= 0.85; }
    }
}

function findBallOwner() {
    let owner = null, minDist = 999;
    [...you.players, ...rival.players].forEach(p => {
        if (p.x < 0) return;
        const d = dist(p, ball);
        if (d < minDist && d < PR + BR + 5) { minDist = d; owner = p; }
    });
    return owner;
}

function updateBall(dt) {
    if (gameState !== "play") return;
    ball.x += ball.vx; ball.y += ball.vy;
    ball.vx *= 0.97; ball.vy *= 0.97;
    [...you.players, ...rival.players].forEach(p => {
        if (p.x < 0) return;
        if (p.state === 'tackle' || p.state === 'fallen') return;
        const d = dist(p, ball);
        if (d < PR + BR) {
            const angle = Math.atan2(ball.y - p.y, ball.x - p.x);
            ball.x = p.x + Math.cos(angle) * (PR + BR + 1);
            ball.y = p.y + Math.sin(angle) * (PR + BR + 1);
            ball.vx += Math.cos(angle) * 2;
            ball.vy += Math.sin(angle) * 2;
            lastBallToucher = p;
        }
    });
    if (checkOutOfBounds()) return;
    const gTop = FIELD.h/2 - 45, gBot = FIELD.h/2 + 45;
    if (ball.x + BR > FIELD.w && ball.y > gTop && ball.y < gBot) {
        score.you++; flashMessage("¡GOL!"); playGoal();
        const bp3 = toScreen(ball.x, ball.y);
        spawnParticles(bp3.sx, bp3.sy, '#00ffc8', 40);
        spawnParticles(bp3.sx, bp3.sy, '#ff5c9f', 30);
        you.players[0].state = 'celebrate'; you.players[0].stateTimer = 120;
        resetPositions("kickoff", "rival");
    }
    if (ball.x - BR < 0 && ball.y > gTop && ball.y < gBot) {
        score.rival++; flashMessage("Gol rival"); playGoal();
        const bp4 = toScreen(ball.x, ball.y);
        spawnParticles(bp4.sx, bp4.sy, '#ff3b5c', 40);
        resetPositions("kickoff", "you");
    }
}

function resetPositions(type, kickoffSide) {
    ball.x = FIELD.w/2; ball.y = FIELD.h/2;
    ball.vx = 0; ball.vy = 0;
    CFG.formJug.forEach(([fx, fy], i) => {
        const p = you.players[i];
        if (p.x < 0) return;
        p.x = fx * FIELD.w; p.y = fy * FIELD.h;
        p.state = 'idle'; p.stateTimer = 0;
        p.vx = 0; p.vy = 0;
    });
    CFG.formRiv.forEach(([fx, fy], i) => {
        const p = rival.players[i];
        if (p.x < 0) return;
        p.x = FIELD.w - fx * FIELD.w; p.y = fy * FIELD.h;
        p.state = 'idle'; p.stateTimer = 0;
        p.vx = 0; p.vy = 0;
    });
    gameState = "play"; freezeTimer = 0;
}

function flashMessage(text) { message = text; messageTimer = 120; }

function attemptDribble() {
    const p = you.players[0];
    dribbleCooldown = 90;
    let nearest = null, nd = 999;
    rival.players.forEach(r => {
        if (r.x < 0) return;
        const d = dist(p, r);
        if (d < nd) { nd = d; nearest = r; }
    });
    if (!nearest || nd > 60) { p.vx *= 1.4; p.vy *= 1.4; return; }
    const prob = 0.4 + (p.reg - nearest.def) / 200 + (p.vel - nearest.vel) / 300;
    const success = Math.random() < Math.max(0.15, Math.min(0.9, prob));
    if (success) {
        const angle = Math.atan2(ball.y - p.y, ball.x - p.x);
        p.x += Math.cos(angle) * 35; p.y += Math.sin(angle) * 35;
        clampToField(p, PR);
        showBigAlert("¡REGATE!", "#00ffc8");
    } else {
        p.vx *= 0.3; p.vy *= 0.3;
        showBigAlert("PERDIDO", "#ff3b5c");
    }
}

function getPlayerState(p) {
    if (p.state === 'celebrate' && p.stateTimer > 0) return 'celebrate';
    if (p.state === 'shoot' && p.stateTimer > 0) return 'shoot';
    if (p.state === 'tackle' && p.stateTimer > 0) return 'tackle';
    if (p.state === 'fallen' && p.stateTimer > 0) return 'fallen';
    const speed = Math.hypot(p.vx, p.vy);
    if (speed > 0.3) return (Math.floor(animTimer / 6) % 2 === 0) ? 'run1' : 'run2';
    return 'idle';
}

function drawAll() {
    updateCamera();
    ctx.fillStyle = '#05070b'; ctx.fillRect(0, 0, W, H);
    drawCrowd(); drawField();
    [...rival.players, ...you.players].forEach(p => {
        if (p.x < 0) return;
        const scr = toScreen(p.x, p.y);
        p.sx = scr.sx; p.sy = scr.sy; p.depth = scr.depth;
    });
    const allPlayers = [
        ...rival.players.map(p => ({...p, sideKey: 'rival'})),
        ...you.players.map(p => ({...p, sideKey: 'you'})),
    ].filter(p => p.x >= 0).sort((a, b) => a.y - b.y);
    allPlayers.forEach(p => {
        const state = getPlayerState(p);
        const sprite = SPRITES[state] || SPRITES.idle;
        const depthScale = 0.75 + p.depth * 0.5;
        const pxSize = 2.2 * depthScale;
        const c1 = p.sideKey === 'you' ? CFG.colorJug : CFG.colorRiv;
        const c2 = p.sideKey === 'you' ? CFG.colorJug2 : CFG.colorRiv2;
        drawPixelSprite(sprite, p.sx, p.sy, pxSize, c1, c2, p.num, p.facingRight, p.isControlled, p.depth);
        ctx.font = 'bold 10px Courier New';
        ctx.strokeStyle = 'rgba(0,0,0,0.9)'; ctx.lineWidth = 3;
        ctx.textAlign = 'center';
        const nameY = p.sy - sprite.length * pxSize - 2;
        ctx.strokeText(p.name, p.sx, nameY);
        ctx.fillStyle = p.isControlled ? '#00ffc8' : '#ffffff';
        ctx.fillText(p.name, p.sx, nameY);
        ctx.textAlign = 'left';
    });
    const bp = toScreen(ball.x, ball.y);
    drawBall({ x: bp.sx, y: bp.sy, vx: ball.vx, vy: ball.vy }, 10);
    drawScoreboard(score, matchTime);
    if (messageTimer > 0) {
        ctx.fillStyle = 'rgba(0,0,0,0.75)'; ctx.fillRect(0, H/2 - 55, W, 110);
        ctx.fillStyle = '#ff5c9f'; ctx.font = 'bold 60px Courier New';
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.shadowColor = '#ff5c9f'; ctx.shadowBlur = 40;
        ctx.fillText(message, W/2, H/2);
        ctx.shadowBlur = 0;
        ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
    }
}

function loop(now) {
    const dt = Math.min(50, now - lastTime) / 1000;
    lastTime = now;
    if (gameState === "play" || gameState === "penalty") {
        matchTime -= dt;
        if (matchTime < 0) matchTime = 0;
    }
    animTimer++;
    if (animTimer > 10000) animTimer = 0;
    [...you.players, ...rival.players].forEach(p => {
        if (p.stateTimer > 0) p.stateTimer--;
        if (p.stateTimer === 0 && p.state !== 'idle') p.state = 'idle';
        if (p.tackleCooldown > 0) p.tackleCooldown--;
    });
    if (gameState === "play") {
        updateControlled(); updateRival(); updateBall(dt); rivalTackleCheck();
        const owner = findBallOwner();
        const youAttack = owner && owner.side === 'you';
        const theyAttack = owner && owner.side === 'rival';
        for (let i = 1; i < you.players.length; i++) {
            const mate = you.players[i];
            if (mate.x < 0) continue;
            let target;
            if (theyAttack) {
                if (i <= 4) target = { x: FIELD.w * 0.28 + (i - 2) * 30, y: mate.homeY };
                else if (i <= 7) target = { x: ball.x - 60, y: mate.homeY };
                else target = { x: FIELD.w * 0.35, y: mate.homeY };
            } else if (youAttack) {
                if (i === you.players.indexOf(owner)) continue;
                if (i <= 4) target = { x: mate.homeX + 80, y: mate.homeY };
                else if (i <= 7) target = { x: ball.x + 60 + (i - 6) * 50, y: ball.y + (i % 2 === 0 ? 90 : -90) };
                else target = { x: Math.min(FIELD.w - 100, ball.x + 180), y: FIELD.h/2 + (i - 9) * 110 };
            } else {
                target = { x: mate.homeX, y: mate.homeY };
            }
            const dx = target.x - mate.x, dy = target.y - mate.y;
            const d = Math.hypot(dx, dy) || 1;
            if (dx !== 0) mate.facingRight = dx > 0;
            if (d > 8) updatePlayer(mate, dx/d, dy/d, 3.2);
            else { mate.vx *= 0.85; mate.vy *= 0.85; }
        }
    } else if (freezeTimer > 0) {
        freezeTimer--;
        if (freezeTimer === 0) gameState = "play";
    }
    if (messageTimer > 0) messageTimer--;
    if (dribbleCooldown > 0) dribbleCooldown--;
    updateParticles();
    drawAll();
    drawParticles();
    requestAnimationFrame(loop);
}

playWhistle();
requestAnimationFrame(loop);
</script>
</body></html>
"""
    html = html.replace("__DATA__", json.dumps(data))
    html = html.replace("__TJ__", tac_jug).replace("__TR__", tac_riv).replace("__DIF__", dif)
    return html


def fase_menu():
    st.markdown('<h1 class="hero-title">⚽ RETRO FOOTBALL 96</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">SUPER EDITION · 1996</p>', unsafe_allow_html=True)
    st.markdown("### 🎚️ Dificultad")
    dif = st.radio("Dificultad", list(DIFICULTADES.keys()), index=1, horizontal=True)
    st.session_state.dificultad = dif
    st.markdown("### 📋 Reglas activas")
    st.markdown("- ⚽ Tackle del rival\n- 🟨 Faltas con tarjetas\n- 🚩 Córners y saques de banda\n- 🎯 Penaltis\n- 🚫 Fuera de juego")
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if st.button("▶️ CONTINUAR", use_container_width=True):
            st.session_state.fase = "equipos"; st.rerun()

def fase_equipos():
    st.markdown('<h1 class="hero-title">SELECCIONA EQUIPOS</h1>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([3, 1, 3])
    with col1:
        st.markdown("### 🔴 Tu equipo")
        for nombre, eq in EQUIPOS.items():
            sel = st.session_state.equipo_jugador == nombre
            bd = "3px solid #00ffc8" if sel else "2px solid rgba(0,212,168,0.2)"
            st.markdown(f'<div class="team-card" style="border:{bd}"><div class="team-flag">{eq["flag"]}</div><div class="team-name">{nombre}</div><div class="team-rating">⭐ {eq["rating"]}</div></div>', unsafe_allow_html=True)
            if st.button(f"Elegir {nombre}", key=f"jug_{nombre}", use_container_width=True):
                st.session_state.equipo_jugador = nombre; st.rerun()
    with col2:
        st.markdown('<div style="text-align:center;font-size:2rem;color:#ff5c9f;font-weight:900;padding-top:60px;">VS</div>', unsafe_allow_html=True)
    with col3:
        st.markdown("### 🔵 Rival")
        for nombre, eq in EQUIPOS.items():
            if nombre == st.session_state.equipo_jugador: continue
            sel = st.session_state.equipo_rival == nombre
            bd = "3px solid #ff5c9f" if sel else "2px solid rgba(0,212,168,0.2)"
            st.markdown(f'<div class="team-card" style="border:{bd}"><div class="team-flag">{eq["flag"]}</div><div class="team-name">{nombre}</div><div class="team-rating">⭐ {eq["rating"]}</div></div>', unsafe_allow_html=True)
            if st.button(f"Elegir {nombre}", key=f"riv_{nombre}", use_container_width=True):
                st.session_state.equipo_rival = nombre; st.rerun()
    st.markdown("---")
    ca, cb, cc = st.columns([1,1,1])
    with ca:
        if st.button("⬅️ Volver", use_container_width=True):
            st.session_state.fase = "menu"; st.rerun()
    with cc:
        if st.session_state.equipo_jugador and st.session_state.equipo_rival:
            if st.button("➡️ Tácticas", use_container_width=True):
                st.session_state.fase = "tacticas"; st.rerun()

def fase_tacticas():
    st.markdown('<h1 class="hero-title">TÁCTICAS</h1>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"### 🔴 {st.session_state.equipo_jugador}")
        for n, i in TACTICAS.items():
            sel = st.session_state.tactica_jugador == n
            bd = "3px solid #00ffc8" if sel else "2px solid rgba(124,92,255,0.3)"
            st.markdown(f'<div class="tactic-card" style="border:{bd}"><div class="tactic-name">{n}</div><div class="tactic-desc">{i["desc"]}</div></div>', unsafe_allow_html=True)
            if st.button(f"Usar {n}", key=f"tj_{n}", use_container_width=True):
                st.session_state.tactica_jugador = n; st.rerun()
    with c2:
        st.markdown(f"### 🔵 {st.session_state.equipo_rival}")
        for n, i in TACTICAS.items():
            sel = st.session_state.tactica_rival == n
            bd = "3px solid #ff5c9f" if sel else "2px solid rgba(124,92,255,0.3)"
            st.markdown(f'<div class="tactic-card" style="border:{bd}"><div class="tactic-name">{n}</div><div class="tactic-desc">{i["desc"]}</div></div>', unsafe_allow_html=True)
            if st.button(f"Usar {n}", key=f"tr_{n}", use_container_width=True):
                st.session_state.tactica_rival = n; st.rerun()
    st.markdown("---")
    ca, cb, cc = st.columns([1,1,1])
    with ca:
        if st.button("⬅️ Volver", use_container_width=True):
            st.session_state.fase = "equipos"; st.rerun()
    with cc:
        if st.session_state.tactica_jugador and st.session_state.tactica_rival:
            if st.button("➡️ Alineación", use_container_width=True):
                st.session_state.fase = "alineacion"; st.rerun()

def fase_alineacion():
    st.markdown('<h1 class="hero-title">ALINEACIÓN</h1>', unsafe_allow_html=True)
    jug = EQUIPOS[st.session_state.equipo_jugador]
    cl, cr = st.columns([2, 1])
    with cl:
        st.markdown("### 👥 Once inicial")
        for i, p in enumerate(jug["jugadores"]):
            pos = "GK" if i == 0 else p["pos"]
            st.markdown(f'''<div class="player-row">
                <div class="player-num">{p['num']}</div>
                <div class="player-name">{p['nombre']}</div>
                <div class="player-pos">{pos}</div>
                <div class="stats-bar">
                    <span>VEL <span class="stat-value {'high' if p['vel']>=85 else ''}">{p['vel']}</span></span>
                    <span>TIR <span class="stat-value {'high' if p['tir']>=85 else ''}">{p['tir']}</span></span>
                    <span>DEF <span class="stat-value {'high' if p['def']>=85 else ''}">{p['def']}</span></span>
                    <span>PAS <span class="stat-value {'high' if p['pas']>=85 else ''}">{p['pas']}</span></span>
                    <span>REG <span class="stat-value {'high' if p['reg']>=85 else ''}">{p['reg']}</span></span>
                </div></div>''', unsafe_allow_html=True)
    with cr:
        st.markdown("### ⚙️ Config")
        st.session_state.cesped = st.radio("Césped", ["Clásico","Mojado","Seco","Nieve"], index=["Clásico","Mojado","Seco","Nieve"].index(st.session_state.cesped))
        st.session_state.sonido = st.checkbox("Sonido", value=st.session_state.sonido)
    st.markdown("---")
    ca, cb, cc = st.columns([1,1,1])
    with ca:
        if st.button("⬅️ Volver", use_container_width=True):
            st.session_state.fase = "tacticas"; st.rerun()
    with cc:
        if st.button("⚽ JUGAR", use_container_width=True):
            st.session_state.fase = "partido"; st.rerun()

def fase_partido():
    st.markdown('<h1 class="hero-title">⚽ EN JUEGO</h1>', unsafe_allow_html=True)
    html = render_match(
        st.session_state.equipo_jugador, st.session_state.equipo_rival,
        st.session_state.tactica_jugador, st.session_state.tactica_rival,
        st.session_state.dificultad, st.session_state.cesped,
        st.session_state.balon, st.session_state.publico, st.session_state.sonido,
    )
    components.html(html, height=780, scrolling=False)
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if st.button("🔙 Volver al menú", use_container_width=True):
            st.session_state.fase = "menu"; st.rerun()

if st.session_state.fase == "menu": fase_menu()
elif st.session_state.fase == "equipos": fase_equipos()
elif st.session_state.fase == "tacticas": fase_tacticas()
elif st.session_state.fase == "alineacion": fase_alineacion()
elif st.session_state.fase == "partido": fase_partido()
