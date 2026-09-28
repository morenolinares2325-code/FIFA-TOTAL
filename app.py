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
    "Fácil":   {"speed": 2.4, "reaction": 0.7},
    "Normal":  {"speed": 2.8, "reaction": 0.85},
    "Difícil": {"speed": 3.2, "reaction": 0.95},
    "Leyenda": {"speed": 3.6, "reaction": 1.0},
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
    ("cesped", "Clásico"), ("sonido", True),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def render_match(eq_jug, eq_riv, tac_jug, tac_riv, dif, cesped, sonido):
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
        "difSpeed": d["speed"], "difReaction": d["reaction"],
        "cesped": cesped, "sonido": sonido,
    }

    html = r"""
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#05070b; display:flex; justify-content:center; align-items:center;
       font-family:'Courier New', monospace; padding:8px; }
#wrap { position:relative; border:3px solid #00d4a8; border-radius:14px;
        box-shadow: 0 0 60px rgba(0,212,168,0.35); overflow:hidden; background:#0a0e14; }
canvas { display:block; image-rendering: pixelated; }
#controls {
    position:absolute; bottom:8px; left:12px; right:12px;
    display:flex; align-items:center; gap:22px;
    color:#c8d4e0; font-size:11px; pointer-events:none; z-index:20;
    padding:8px 14px; background:linear-gradient(90deg, rgba(0,0,0,0.8), rgba(0,0,0,0.4));
    border-radius:10px; border:1px solid rgba(0,212,168,0.25);
}
.key-group { display:flex; align-items:center; gap:8px; }
.key-block { display:flex; flex-direction:column; align-items:center; gap:2px; }
.key-row { display:flex; gap:2px; }
.key {
    display:inline-flex; align-items:center; justify-content:center;
    min-width:22px; height:22px; padding:0 6px;
    background:linear-gradient(180deg, #1a2430, #0a0f18);
    border:1px solid #00d4a8; border-radius:5px;
    color:#00ffc8; font-weight:800; font-size:11px;
    box-shadow: 0 0 8px rgba(0,212,168,0.4);
}
.key.wide { padding: 0 18px; }
.key-label { color:#7a8699; font-size:10px; letter-spacing:1.5px; text-transform:uppercase; font-weight:700; }
.info { color:#00ffc8; font-weight:700; letter-spacing:1px; font-size:11px; }
#bigAlert { position:absolute; top:40%; left:50%;
    transform: translate(-50%,-50%); font-size:42px; font-weight:900;
    letter-spacing:6px; opacity:0; pointer-events:none; z-index:15;
    transition:opacity 0.2s; text-shadow: 0 0 30px currentColor; }
</style></head><body>
<div id="wrap">
    <canvas id="game" width="1000" height="700"></canvas>
    <div id="controls">
        <div class="key-group">
            <div class="key-block">
                <span class="key">W</span>
                <div class="key-row">
                    <span class="key">A</span><span class="key">S</span><span class="key">D</span>
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
            <span class="info">__TJ__ vs __TR__</span>
        </div>
    </div>
    <div id="bigAlert"></div>
</div>
<script>
const CFG = __DATA__;

const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const W = canvas.width, H = canvas.height;

// =====================================================
// CÁMARA ESTÁTICA CON PERSPECTIVA (sin zoom dinámico)
// =====================================================
const ISO = {
    fieldW: 1000, fieldH: 620,
    centerX: 500, centerY: 310,
    topScaleX: 0.78, bottomScaleX: 1.10, baseScaleY: 0.66,
    baseX: W/2, baseY: H/2 + 10,
};

function toScreen(x, y) {
    const depth = y / ISO.fieldH;
    const scaleX = ISO.topScaleX + (ISO.bottomScaleX - ISO.topScaleX) * depth;
    const nx = (x - ISO.centerX) / ISO.centerX;
    const ny = (y - ISO.centerY) / ISO.centerY;
    const sx = ISO.baseX + nx * (ISO.fieldW / 2) * scaleX;
    const sy = ISO.baseY + ny * (ISO.fieldH / 2) * ISO.baseScaleY;
    return { sx, sy, depth, scaleX };
}

// =====================================================
// CÉSPED
// =====================================================
const CESPEDES = {
    "Clásico": { dark:"#0a5522", light:"#0f6f2e", line:"#e8f4ff" },
    "Mojado":  { dark:"#052a12", light:"#0a4a1f", line:"#ffffff" },
    "Seco":    { dark:"#4a521a", light:"#6a7a2a", line:"#f0e8c0" },
    "Nieve":   { dark:"#c8d0d8", light:"#e8eef2", line:"#3a4a5a" },
};

// =====================================================
// SPRITES NÍTIDOS (16×22)
// =====================================================
const SPRITES = {
    idle: [
        ".....HHHHHH.....",
        "....HHHHHHHH....",
        "....HHHHHHHH....",
        "....HSSSSSSH....",
        "....HS@SS@SH....",
        "....HSSSSSSH....",
        ".....SS//SS.....",
        ".....SSSSSS.....",
        "....JJJJJJJJ....",
        "...JJJCCCCJJJ...",
        "...JJJNNNNJJJ...",
        "..JJJJNNNNJJJJ..",
        "..JJJJJJJJJJJJ..",
        ".KJJJJJJJJJJJJK.",
        ".KJJJJJJJJJJJJK.",
        "..JJJJJJJJJJJJ..",
        "..PPPPPPPPPPPP..",
        "..PPPPPPPPPPPP..",
        "..PPPPPPPPPPPP..",
        "..PPPP..PPPPPP..",
        "..BBBB..BBBBBB..",
        "..BBBB..BBBBBB..",
    ],
    run1: [
        ".....HHHHHH.....",
        "....HHHHHHHH....",
        "....HHHHHHHH....",
        "....HSSSSSSH....",
        "....HS@SS@SH....",
        "....HSSSSSSH....",
        ".....SS//SS.....",
        ".....SSSSSS.....",
        "....JJJJJJJJ....",
        "...JJJCCCCJJJ...",
        "...JJJNNNNJJJ...",
        "..JJJJNNNNJJJJ..",
        "..JJJJJJJJJJJJ..",
        ".KJJJJJJJJJJJJK.",
        ".KJJJJJJJJJJJJK.",
        "..JJJJJJJJJJJJ..",
        "..PPPPPPPPPPPP..",
        "..PPPPPPPPPPPP..",
        "..PPPPPPPPPP....",
        "..PPPP...PPPP...",
        "..BBBB...PPPP...",
        "..BBBB...BBBB...",
    ],
    run2: [
        ".....HHHHHH.....",
        "....HHHHHHHH....",
        "....HHHHHHHH....",
        "....HSSSSSSH....",
        "....HS@SS@SH....",
        "....HSSSSSSH....",
        ".....SS//SS.....",
        ".....SSSSSS.....",
        "....JJJJJJJJ....",
        "...JJJCCCCJJJ...",
        "...JJJNNNNJJJ...",
        "..JJJJNNNNJJJJ..",
        "..JJJJJJJJJJJJ..",
        ".KJJJJJJJJJJJJK.",
        ".KJJJJJJJJJJJJK.",
        "..JJJJJJJJJJJJ..",
        "..PPPPPPPPPPPP..",
        "...PPPPPPPPPPPP.",
        "...PPPP..PPPPP..",
        "..PPPP....PPPP..",
        "..BBBB....BBBB..",
        "..BBBB....BBBB..",
    ],
    shoot: [
        ".....HHHHHH.....",
        "....HHHHHHHH....",
        "....HHHHHHHH....",
        "....HSSSSSSH....",
        "....HS@SS@SH....",
        "....HSSSSSSH....",
        ".....SS//SS.....",
        ".....SSSSSS.....",
        "....JJJJJJJJ....",
        "...JJJCCCCJJJ...",
        "...JJJNNNNJJJ...",
        "..JJJJNNNNJJJJ..",
        "..JJJJJJJJJJJJ..",
        "KJJJJJJJJJJJJJJK",
        "KJJJJJJJJJJJJJJK",
        "..JJJJJJJJJJJJ..",
        "..PPPPPPPPPPPP..",
        "..PPPPPPPPPPPP..",
        "..PPPPPPPPPPPP..",
        "..PPPP..PPPPPP..",
        "..BBBB..BBBBBB..",
        "..BBBB..BBBBBB..",
    ],
    celebrate: [
        "..S..HHHHHH..S..",
        "..S..HHHHHH..S..",
        "..S.HHHHHHHH.S..",
        "..S.HSSSSSSH.S..",
        "..S.HS@SS@SH.S..",
        "..S.HSSSSSSH.S..",
        "...S.SS//SS.S...",
        "....SSSSSSSS....",
        "....JJJJJJJJ....",
        "...JJJCCCCJJJ...",
        "...JJJNNNNJJJ...",
        "..JJJJNNNNJJJJ..",
        "..JJJJJJJJJJJJ..",
        ".KJJJJJJJJJJJJK.",
        ".KJJJJJJJJJJJJK.",
        "..JJJJJJJJJJJJ..",
        "..PPPPPPPPPPPP..",
        "..PPPPPPPPPPPP..",
        "..PPPPPPPPPPPP..",
        "..PPPP..PPPPPP..",
        "..BBBB..BBBBBB..",
        "..BBBB..BBBBBB..",
    ],
    fallen: [
        "..................",
        "..................",
        "..................",
        "..................",
        "......HHHHHH......",
        ".....HHHHHHHH.....",
        ".....HSSSSSSH.....",
        ".....HS@SS@SH.....",
        ".....HSSSSSSH.....",
        "......SS//SS......",
        "......SSSSSS......",
        "....JJJJJJJJJJ....",
        "...JJJCCCCCCJJJ...",
        "...JJJNNNNNNJJJ...",
        "..JJJJNNNNNNJJJJ..",
        "..JJJJJJJJJJJJJJ..",
        ".KJJJJJJJJJJJJJJK.",
        "..PPPPPPPPPPPPPP..",
        "..PPPPPPPPPPPPPP..",
        "..PPPPPPPPPPPPPP..",
        "..BBBB......BBBB..",
        "..BBBB......BBBB..",
    ],
};

function drawPixelSprite(sprite, x, y, pixelSize, color1, color2, dorsal, facingRight, isControlled) {
    const h = sprite.length;
    const w = sprite[0].length;
    const offsetX = -w * pixelSize / 2;
    const offsetY = -h * pixelSize;
    
    // Sombra simple
    ctx.fillStyle = 'rgba(0,0,0,0.35)';
    ctx.beginPath();
    ctx.ellipse(x, y + 3, w * pixelSize * 0.4, h * pixelSize * 0.12, 0, 0, Math.PI * 2);
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
                case 'S': color = '#f0c8a0'; break;
                case '@': color = '#0a0a0a'; break;
                case '/': color = '#a04020'; break;
                case 'J': color = color1; break;
                case 'C': color = color2; break;
                case 'N': color = '#ffffff'; break;
                case 'P': color = '#1a1a2a'; break;
                case 'B': color = '#0a0a0a'; break;
                case 'K': color = color2; break;
                default: color = '#ff00ff';
            }
            ctx.fillStyle = color;
            ctx.fillRect(Math.round(px), Math.round(py), pixelSize, pixelSize);
        }
    }
    
    // Dorsal
    ctx.font = `bold ${Math.round(pixelSize * 4)}px Courier New`;
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillStyle = 'rgba(0,0,0,0.85)';
    ctx.strokeStyle = 'rgba(255,255,255,0.95)';
    ctx.lineWidth = 2;
    const dorsalY = y - h * pixelSize * 0.45;
    ctx.strokeText(dorsal, x, dorsalY);
    ctx.fillText(dorsal, x, dorsalY);
    
    if (isControlled) {
        ctx.strokeStyle = '#00ffc8'; ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.ellipse(x, y + 2, w * pixelSize * 0.6, h * pixelSize * 0.12, 0, 0, Math.PI * 2);
        ctx.stroke();
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
    ctx.ellipse(x + 3, y + 6, r * 1.1, r * 0.5, 0, 0, Math.PI * 2);
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
// CAMPO
// =====================================================
function drawField() {
    const c = CESPEDES[CFG.cesped];
    const tl = toScreen(0, 0);
    const tr = toScreen(ISO.fieldW, 0);
    const br = toScreen(ISO.fieldW, ISO.fieldH);
    const bl = toScreen(0, ISO.fieldH);
    
    // Fondo
    ctx.fillStyle = c.dark;
    ctx.beginPath();
    ctx.moveTo(tl.sx, tl.sy); ctx.lineTo(tr.sx, tr.sy);
    ctx.lineTo(br.sx, br.sy); ctx.lineTo(bl.sx, bl.sy);
    ctx.closePath(); ctx.fill();
    
    // Franjas
    const stripes = 12;
    for (let i = 0; i < stripes; i += 2) {
        const x1 = (i / stripes) * ISO.fieldW;
        const x2 = ((i + 1) / stripes) * ISO.fieldW;
        const p1 = toScreen(x1, 0), p2 = toScreen(x2, 0);
        const p3 = toScreen(x2, ISO.fieldH), p4 = toScreen(x1, ISO.fieldH);
        ctx.fillStyle = c.light;
        ctx.beginPath();
        ctx.moveTo(p1.sx, p1.sy); ctx.lineTo(p2.sx, p2.sy);
        ctx.lineTo(p3.sx, p3.sy); ctx.lineTo(p4.sx, p4.sy);
        ctx.closePath(); ctx.fill();
    }
    
    // Líneas
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
    
    ctx.strokeStyle = c.line; 
    ctx.lineWidth = 2;
    
    drawIsoRect(0, 0, ISO.fieldW, ISO.fieldH);
    drawIsoLine(ISO.centerX, 0, ISO.centerX, ISO.fieldH);
    drawIsoCircle(ISO.centerX, ISO.centerY, 55);
    drawIsoRect(0, ISO.centerY - 90, 85, 180);
    drawIsoRect(ISO.fieldW - 85, ISO.centerY - 90, 85, 180);
    drawIsoRect(0, ISO.centerY - 45, 32, 90);
    drawIsoRect(ISO.fieldW - 32, ISO.centerY - 45, 32, 90);
    
    // Puntos de penalti
    const pPen1 = toScreen(65, ISO.centerY);
    const pPen2 = toScreen(ISO.fieldW - 65, ISO.centerY);
    ctx.fillStyle = c.line;
    ctx.beginPath(); ctx.arc(pPen1.sx, pPen1.sy, 2, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(pPen2.sx, pPen2.sy, 2, 0, Math.PI*2); ctx.fill();
    
    // Porterías
    const GOAL_H = 50;
    const GOAL_DEPTH = 22;
    
    // Portería izquierda - red
    const gTL = toScreen(0, ISO.centerY - GOAL_H);
    const gBL = toScreen(0, ISO.centerY + GOAL_H);
    const gBTL = toScreen(-GOAL_DEPTH, ISO.centerY - GOAL_H);
    const gBBL = toScreen(-GOAL_DEPTH, ISO.centerY + GOAL_H);
    
    // Fondo de la red
    ctx.fillStyle = 'rgba(255,255,255,0.08)';
    ctx.beginPath();
    ctx.moveTo(gTL.sx, gTL.sy); ctx.lineTo(gBL.sx, gBL.sy);
    ctx.lineTo(gBBL.sx, gBBL.sy); ctx.lineTo(gBTL.sx, gBTL.sy);
    ctx.closePath(); ctx.fill();
    
    // Mallado
    ctx.strokeStyle = 'rgba(255,255,255,0.4)'; 
    ctx.lineWidth = 1;
    for (let i = 0; i <= 8; i++) {
        const t = i / 8;
        const y1 = gTL.sy + (gBL.sy - gTL.sy) * t;
        const y2 = gBTL.sy + (gBBL.sy - gBTL.sy) * t;
        ctx.beginPath(); ctx.moveTo(gTL.sx, y1); ctx.lineTo(gBTL.sx, y2); ctx.stroke();
    }
    for (let i = 0; i <= 6; i++) {
        const t = i / 6;
        const x1 = gTL.sx + (gBTL.sx - gTL.sx) * t;
        const y1 = gTL.sy + (gBTL.sy - gTL.sy) * t;
        const x2 = gBL.sx + (gBBL.sx - gBL.sx) * t;
        const y2 = gBL.sy + (gBBL.sy - gBL.sy) * t;
        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    }
    
    // Postes
    ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(gTL.sx, gTL.sy); ctx.lineTo(gBTL.sx, gBTL.sy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(gBL.sx, gBL.sy); ctx.lineTo(gBBL.sx, gBBL.sy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(gBTL.sx, gBTL.sy); ctx.lineTo(gBBL.sx, gBBL.sy); ctx.stroke();
    
    // Portería derecha
    const gTR = toScreen(ISO.fieldW, ISO.centerY - GOAL_H);
    const gBR = toScreen(ISO.fieldW, ISO.centerY + GOAL_H);
    const gBTR = toScreen(ISO.fieldW + GOAL_DEPTH, ISO.centerY - GOAL_H);
    const gBBR = toScreen(ISO.fieldW + GOAL_DEPTH, ISO.centerY + GOAL_H);
    
    ctx.fillStyle = 'rgba(255,255,255,0.08)';
    ctx.beginPath();
    ctx.moveTo(gTR.sx, gTR.sy); ctx.lineTo(gBR.sx, gBR.sy);
    ctx.lineTo(gBBR.sx, gBBR.sy); ctx.lineTo(gBTR.sx, gBTR.sy);
    ctx.closePath(); ctx.fill();
    
    ctx.strokeStyle = 'rgba(255,255,255,0.4)'; ctx.lineWidth = 1;
    for (let i = 0; i <= 8; i++) {
        const t = i / 8;
        const y1 = gTR.sy + (gBR.sy - gTR.sy) * t;
        const y2 = gBTR.sy + (gBBR.sy - gBTR.sy) * t;
        ctx.beginPath(); ctx.moveTo(gTR.sx, y1); ctx.lineTo(gBTR.sx, y2); ctx.stroke();
    }
    for (let i = 0; i <= 6; i++) {
        const t = i / 6;
        const x1 = gTR.sx + (gBTR.sx - gTR.sx) * t;
        const y1 = gTR.sy + (gBTR.sy - gTR.sy) * t;
        const x2 = gBR.sx + (gBBR.sx - gBR.sx) * t;
        const y2 = gBR.sy + (gBBR.sy - gBR.sy) * t;
        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    }
    
    ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(gTR.sx, gTR.sy); ctx.lineTo(gBTR.sx, gBTR.sy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(gBR.sx, gBR.sy); ctx.lineTo(gBBR.sx, gBBR.sy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(gBTR.sx, gBTR.sy); ctx.lineTo(gBBR.sx, gBBR.sy); ctx.stroke();
}

// =====================================================
// MARCADOR
// =====================================================
function drawScoreboard(score, time) {
    const x = 20, y = 20, w = 220, h = 85;
    ctx.fillStyle = 'rgba(0,0,0,0.85)'; ctx.fillRect(x + 4, y + 4, w, h);
    ctx.fillStyle = '#1a1a2a'; ctx.fillRect(x, y, w, h);
    ctx.strokeStyle = '#00ff88'; ctx.lineWidth = 2; ctx.strokeRect(x, y, w, h);
    ctx.fillStyle = '#00ff88'; ctx.fillRect(x, y, 70, 22);
    ctx.fillStyle = '#000000'; ctx.font = 'bold 14px Courier New';
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText('MIN', x + 35, y + 11);
    ctx.fillStyle = '#ffffff'; ctx.font = 'bold 40px Courier New';
    ctx.fillText(score.you + '-' + score.rival, x + w/2, y + 52);
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

const you = { players: [] };
const rival = { players: [] };

CFG.formJug.forEach(([fx, fy], i) => {
    const dd = CFG.jugadores[i] || {};
    you.players.push({
        x: fx * FIELD.w, y: fy * FIELD.h, vx: 0, vy: 0,
        num: dd.num || i+1, name: dd.nombre || 'Jugador',
        vel: dd.vel || 75, tir: dd.tir || 75, def: dd.def || 75,
        pas: dd.pas || 75, reg: dd.reg || 75,
        isControlled: i === 0, side: 'you', facingRight: true,
        state: 'idle', stateTimer: 0,
        homeX: fx * FIELD.w, homeY: fy * FIELD.h,
    });
});
CFG.formRiv.forEach(([fx, fy], i) => {
    const dd = CFG.rivales[i] || {};
    rival.players.push({
        x: FIELD.w - fx * FIELD.w, y: fy * FIELD.h, vx: 0, vy: 0,
        num: dd.num || i+1, name: dd.nombre || 'Rival',
        vel: dd.vel || 75, tir: dd.tir || 75, def: dd.def || 75,
        pas: dd.pas || 75, reg: dd.reg || 75,
        isControlled: false, side: 'rival', facingRight: false,
        state: 'idle', stateTimer: 0,
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
    const boost = 0.7 + (p.vel / 100) * 0.6;
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

function attemptTackle(defender, attacker) {
    if (defender.state === 'tackle' || defender.state === 'fallen') return false;
    if (defender.tackleCooldown > 0) return false;
    defender.state = 'tackle'; defender.stateTimer = 15;
    defender.tackleCooldown = 180;
    playKick();
    const prob = 0.35 + (defender.def - attacker.reg) / 250;
    const success = Math.random() < Math.max(0.15, Math.min(0.85, prob));
    if (success) {
        const angle = Math.atan2(attacker.y - defender.y, attacker.x - defender.x);
        ball.vx = Math.cos(angle) * 5; ball.vy = Math.sin(angle) * 5;
        attacker.state = 'fallen'; attacker.stateTimer = 30;
        lastBallToucher = defender;
        return true;
    } else {
        defender.state = 'fallen'; defender.stateTimer = 40;
        attacker.state = 'fallen'; attacker.stateTimer = 30;
        playWhistle();
        gameState = "foul"; freezeTimer = 90;
        showBigAlert("FALTA", "#ffdd00");
        ball.vx = 0; ball.vy = 0;
        return false;
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
        if (ball.y > gTop && ball.y < gBot) return false;
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

function rivalTackleCheck() {
    if (gameState !== "play") return;
    const owner = findBallOwner();
    if (!owner || owner.side !== 'you') return;
    for (let i = 0; i < rival.players.length; i++) {
        const r = rival.players[i];
        if (i === 0) continue;
        if (r.state === 'tackle' || r.state === 'fallen') continue;
        if (r.tackleCooldown === undefined) r.tackleCooldown = 0;
        if (r.tackleCooldown > 0) continue;
        const d = dist(r, owner);
        if (d < 25 && Math.random() < 0.04) {
            attemptTackle(r, owner);
            break;
        }
    }
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
    updatePlayer(p, dx, dy, 4.0);
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
            p.state = 'shoot'; p.stateTimer = 12;
            lastBallToucher = p; playKick();
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
                target = { x: FIELD.w - 25, y: Math.max(FIELD.h/2 - 60, Math.min(FIELD.h/2 + 60, ball.y)) };
            } else if (i <= 4) {
                target = { x: Math.max(FIELD.w * 0.55, Math.min(FIELD.w - 60, ball.x + 130)), y: FIELD.h/2 + (i - 2.5) * 60 };
            } else if (i <= 7) {
                target = { x: FIELD.w * 0.55 + (i - 6) * 40, y: ball.y * 0.4 + FIELD.h/2 * 0.6 };
            } else {
                target = { x: Math.min(FIELD.w - 80, ball.x + 180), y: FIELD.h/2 + (i - 9) * 80 };
            }
        } else {
            const carrier = owner;
            if (i === 0) target = { x: FIELD.w - 25, y: FIELD.h/2 };
            else if (i <= 4) target = { x: FIELD.w * 0.55, y: FIELD.h/2 + (i - 2.5) * 60 };
            else if (i <= 7) target = { x: carrier.x + (i - 6) * 60, y: carrier.y + (i % 2 === 0 ? 70 : -70) };
            else target = { x: Math.min(FIELD.w - 80, carrier.x + 200), y: FIELD.h/2 + (i - 9) * 90 };
        }
        const dx = target.x - p.x, dy = target.y - p.y;
        if (dx !== 0) p.facingRight = dx > 0;
        const d = Math.hypot(dx, dy) || 1;
        let speed;
        if (i === 0) speed = CFG.difSpeed * 0.5;
        else if (i <= 4) speed = CFG.difSpeed * 0.85;
        else if (i <= 7) speed = CFG.difSpeed * 0.95;
        else speed = CFG.difSpeed;
        if (d > 4) updatePlayer(p, dx/d, dy/d, speed);
        else { p.vx *= 0.85; p.vy *= 0.85; }
    }
}

function findBallOwner() {
    let owner = null, minDist = 999;
    const all = [...you.players, ...rival.players];
    for (const p of all) {
        if (p.x < 0) continue;
        const d = dist(p, ball);
        if (d < minDist && d < PR + BR + 5) { minDist = d; owner = p; }
    }
    return owner;
}

function updateBall() {
    if (gameState !== "play") return;
    ball.x += ball.vx; ball.y += ball.vy;
    ball.vx *= 0.97; ball.vy *= 0.97;
    const all = [...you.players, ...rival.players];
    for (const p of all) {
        if (p.x < 0) continue;
        if (p.state === 'tackle' || p.state === 'fallen') continue;
        const d = dist(p, ball);
        if (d < PR + BR) {
            const angle = Math.atan2(ball.y - p.y, ball.x - p.x);
            ball.x = p.x + Math.cos(angle) * (PR + BR + 1);
            ball.y = p.y + Math.sin(angle) * (PR + BR + 1);
            ball.vx += Math.cos(angle) * 2;
            ball.vy += Math.sin(angle) * 2;
            lastBallToucher = p;
        }
    }
    if (checkOutOfBounds()) return;
    const gTop = FIELD.h/2 - 45, gBot = FIELD.h/2 + 45;
    if (ball.x + BR > FIELD.w && ball.y > gTop && ball.y < gBot) {
        score.you++; flashMessage("¡GOL!"); playGoal();
        you.players[0].state = 'celebrate'; you.players[0].stateTimer = 100;
        resetPositions();
    }
    if (ball.x - BR < 0 && ball.y > gTop && ball.y < gBot) {
        score.rival++; flashMessage("Gol rival"); playGoal();
        resetPositions();
    }
}

function resetPositions() {
    ball.x = FIELD.w/2; ball.y = FIELD.h/2;
    ball.vx = 0; ball.vy = 0;
    you.players.forEach((p, i) => {
        if (p.x < 0) return;
        p.x = CFG.formJug[i][0] * FIELD.w; 
        p.y = CFG.formJug[i][1] * FIELD.h;
        p.state = 'idle'; p.stateTimer = 0;
        p.vx = 0; p.vy = 0;
    });
    rival.players.forEach((p, i) => {
        if (p.x < 0) return;
        p.x = FIELD.w - CFG.formRiv[i][0] * FIELD.w; 
        p.y = CFG.formRiv[i][1] * FIELD.h;
        p.state = 'idle'; p.stateTimer = 0;
        p.vx = 0; p.vy = 0;
    });
    gameState = "play"; freezeTimer = 0;
}

function flashMessage(text) { message = text; messageTimer = 100; }

function attemptDribble() {
    const p = you.players[0];
    dribbleCooldown = 90;
    let nearest = null, nd = 999;
    for (const r of rival.players) {
        if (r.x < 0) continue;
        const d = dist(p, r);
        if (d < nd) { nd = d; nearest = r; }
    }
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
    if (p.state === 'fallen' && p.stateTimer > 0) return 'fallen';
    const speed = Math.hypot(p.vx, p.vy);
    if (speed > 0.3) return (Math.floor(animTimer / 6) % 2 === 0) ? 'run1' : 'run2';
    return 'idle';
}

function drawAll() {
    // Fondo
    ctx.fillStyle = '#05070b'; 
    ctx.fillRect(0, 0, W, H);
    
    drawField();
    
    // Actualizar posiciones en pantalla
    const all = [...rival.players, ...you.players];
    for (const p of all) {
        if (p.x < 0) continue;
        const scr = toScreen(p.x, p.y);
        p.sx = scr.sx; p.sy = scr.sy;
    }
    
    // Ordenar por Y (los de arriba detrás)
    const sorted = all.filter(p => p.x >= 0).slice().sort((a, b) => a.y - b.y);
    
    for (const p of sorted) {
        const state = getPlayerState(p);
        const sprite = SPRITES[state] || SPRITES.idle;
        // Escala por profundidad: lejos = más pequeños
        const depthScale = 0.85 + (p.y / FIELD.h) * 0.25;
        const pxSize = 2.4 * depthScale;
        
        const isYou = you.players.indexOf(p) !== -1;
        const c1 = isYou ? CFG.colorJug : CFG.colorRiv;
        const c2 = isYou ? CFG.colorJug2 : CFG.colorRiv2;
        
        drawPixelSprite(sprite, p.sx, p.sy, pxSize, c1, c2, p.num, p.facingRight, p.isControlled);
        
        // Nombre
        ctx.font = 'bold 9px Courier New';
        ctx.strokeStyle = 'rgba(0,0,0,0.9)';
        ctx.lineWidth = 3;
        ctx.textAlign = 'center';
        const nameY = p.sy - sprite.length * pxSize - 2;
        ctx.strokeText(p.name, p.sx, nameY);
        ctx.fillStyle = p.isControlled ? '#00ffc8' : '#ffffff';
        ctx.fillText(p.name, p.sx, nameY);
        ctx.textAlign = 'left';
    }
    
    // Balón
    const bp = toScreen(ball.x, ball.y);
    drawBall({ x: bp.sx, y: bp.sy, vx: ball.vx, vy: ball.vy }, 10);
    
    // Marcador
    drawScoreboard(score, matchTime);
    
    // Mensaje central
    if (messageTimer > 0) {
        ctx.fillStyle = 'rgba(0,0,0,0.75)';
        ctx.fillRect(0, H/2 - 55, W, 110);
        ctx.fillStyle = '#ff5c9f';
        ctx.font = 'bold 60px Courier New';
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText(message, W/2, H/2);
        ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
    }
}

function loop(now) {
    const dt = Math.min(50, now - lastTime) / 1000;
    lastTime = now;
    
    if (gameState === "play") {
        matchTime -= dt;
        if (matchTime < 0) matchTime = 0;
    }
    
    animTimer++;
    if (animTimer > 10000) animTimer = 0;
    
    // Timers
    const all = [...you.players, ...rival.players];
    for (const p of all) {
        if (p.stateTimer > 0) p.stateTimer--;
        if (p.stateTimer === 0 && p.state !== 'idle') p.state = 'idle';
        if (p.tackleCooldown > 0) p.tackleCooldown--;
    }
    
    if (gameState === "play") {
        updateControlled();
        updateRival();
        updateBall();
        rivalTackleCheck();
        
        // IA compañeros
        const owner = findBallOwner();
        const theyAttack = owner && owner.side === 'rival';
        for (let i = 1; i < you.players.length; i++) {
            const mate = you.players[i];
            if (mate.x < 0) continue;
            let target;
            if (theyAttack) {
                if (i <= 4) target = { x: FIELD.w * 0.25 + (i - 2) * 30, y: mate.homeY };
                else if (i <= 7) target = { x: ball.x - 60, y: mate.homeY };
                else target = { x: FIELD.w * 0.35, y: mate.homeY };
            } else if (owner && owner.side === 'you') {
                if (i === you.players.indexOf(owner)) continue;
                if (i <= 4) target = { x: mate.homeX + 60, y: mate.homeY };
                else if (i <= 7) target = { x: ball.x + 50, y: ball.y + (i % 2 === 0 ? 80 : -80) };
                else target = { x: Math.min(FIELD.w - 100, ball.x + 150), y: FIELD.h/2 + (i - 9) * 100 };
            } else {
                target = { x: mate.homeX, y: mate.homeY };
            }
            const dx = target.x - mate.x, dy = target.y - mate.y;
            const d = Math.hypot(dx, dy) || 1;
            if (dx !== 0) mate.facingRight = dx > 0;
            if (d > 8) updatePlayer(mate, dx/d, dy/d, 3.0);
            else { mate.vx *= 0.85; mate.vy *= 0.85; }
        }
    } else if (freezeTimer > 0) {
        freezeTimer--;
        if (freezeTimer === 0) gameState = "play";
    }
    
    if (messageTimer > 0) messageTimer--;
    if (dribbleCooldown > 0) dribbleCooldown--;
    
    drawAll();
    requestAnimationFrame(loop);
}

playWhistle();
requestAnimationFrame(loop);
</script>
</body></html>
"""
    html = html.replace("__DATA__", json.dumps(data))
    html = html.replace("__TJ__", tac_jug).replace("__TR__", tac_riv)
    return html


def fase_menu():
    st.markdown('<h1 class="hero-title">⚽ RETRO FOOTBALL 96</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">SUPER EDITION · 1996</p>', unsafe_allow_html=True)
    st.markdown("### 🎚️ Dificultad")
    dif = st.radio("Dificultad", list(DIFICULTADES.keys()), index=1, horizontal=True)
    st.session_state.dificultad = dif
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
        st.session_state.dificultad, st.session_state.cesped, st.session_state.sonido,
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
