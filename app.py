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
        "flag": "🇪🇸", "rating": 89, "color": "#c8102e", "color2": "#ffd700",
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
    display:flex; align-items:center; gap:16px;
    color:#c8d4e0; font-size:11px; pointer-events:none; z-index:20;
    padding:8px 14px; background:linear-gradient(90deg, rgba(0,0,0,0.8), rgba(0,0,0,0.4));
    border-radius:10px; border:1px solid rgba(0,212,168,0.25);
}
.key-group { display:flex; align-items:center; gap:6px; }
.key-block { display:flex; flex-direction:column; align-items:center; gap:2px; }
.key-row { display:flex; gap:2px; }
.key {
    display:inline-flex; align-items:center; justify-content:center;
    min-width:20px; height:20px; padding:0 5px;
    background:linear-gradient(180deg, #1a2430, #0a0f18);
    border:1px solid #00d4a8; border-radius:4px;
    color:#00ffc8; font-weight:800; font-size:10px;
    box-shadow: 0 0 6px rgba(0,212,168,0.4);
}
.key.wide { padding: 0 12px; }
.key-label { color:#7a8699; font-size:9px; letter-spacing:1px; text-transform:uppercase; font-weight:700; }
.info { color:#00ffc8; font-weight:700; letter-spacing:1px; font-size:11px; }
#bigAlert { position:absolute; top:35%; left:50%;
    transform: translate(-50%,-50%); font-size:48px; font-weight:900;
    letter-spacing:6px; opacity:0; pointer-events:none; z-index:15;
    transition:opacity 0.2s; text-shadow: 0 0 40px currentColor; }
</style></head><body>
<div id="wrap">
    <canvas id="game" width="1000" height="700"></canvas>
    <div id="controls">
        <div class="key-group">
            <div class="key-block">
                <span class="key">W</span>
                <div class="key-row"><span class="key">A</span><span class="key">S</span><span class="key">D</span></div>
            </div>
            <span class="key-label">Mover</span>
        </div>
        <div class="key-group"><span class="key wide">ESPACIO</span><span class="key-label">Pase</span></div>
        <div class="key-group"><span class="key">E</span><span class="key-label">Tiro</span></div>
        <div class="key-group"><span class="key">Q</span><span class="key-label">Regate</span></div>
        <div class="key-group"><span class="key">TAB</span><span class="key-label">Cambiar</span></div>
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
// CÁMARA FIFA 96 (ROTADA 45° + ZOOM ALTO)
// =====================================================
const ISO = {
    fieldW: 2000, fieldH: 1200,
    camX: 1000, camY: 600,
    targetCamX: 1000, targetCamY: 600,
    scale: 3.0,
    tiltY: 0.52,
    rotation: 0.707,
    centerScreenX: W/2,
    centerScreenY: H/2 - 20,
};

function toScreen(x, y) {
    const dx = x - ISO.camX;
    const dy = y - ISO.camY;
    const rotX = (dx + dy) * ISO.rotation;
    const rotY = (-dx + dy) * ISO.rotation;
    const isoX = rotX * ISO.scale;
    const isoY = rotY * ISO.scale * ISO.tiltY;
    return { sx: ISO.centerScreenX + isoX, sy: ISO.centerScreenY + isoY };
}

function updateCamera() {
    const leadX = ball.vx * 8;
    const leadY = ball.vy * 5;
    ISO.targetCamX = ball.x + leadX;
    ISO.targetCamY = ball.y + leadY;
    ISO.camX += (ISO.targetCamX - ISO.camX) * 0.05;
    ISO.camY += (ISO.targetCamY - ISO.camY) * 0.05;
}

// =====================================================
// CÉSPED
// =====================================================
const CESPEDES = {
    "Clásico": { dark:"#3d8a2b", light:"#4a9e35", line:"#ffffff" },
    "Mojado":  { dark:"#2e6b20", light:"#3a7d28", line:"#e8e8e8" },
    "Seco":    { dark:"#7a8a3a", light:"#8a9a4a", line:"#f0e8c0" },
    "Nieve":   { dark:"#d8e0e8", light:"#eef2f6", line:"#4a5a6a" },
};

// =====================================================
// SPRITES 28x40 (piernas gruesas, cuerpo ancho)
// =====================================================
const SPRITES = {
    idle_down: [
        ".........HHHHHHHHHH.........",
        "........HHHHHHHHHHHH........",
        ".......HHHHHHHHHHHHHH.......",
        "......HHHHHHHHHHHHHHHH......",
        "......HHHsssssssssssHH......",
        ".....HHHsSSSSSSSSSSsHHH.....",
        ".....HHHsS@SSSSSS@SsHHH.....",
        ".....HHHsSSSSSSSSSSsHHH.....",
        ".....HHHsSSSSSSSSSSsHHH.....",
        "......HHsSSS/SS/SSSsHH......",
        ".......HssSSSSSSSSssH.......",
        "........ssSSSSSSSSss........",
        "..........SSSSSSSS..........",
        "..........SSSSSSSS..........",
        "........JJJJJJJJJJJJ........",
        ".......JJJJcJJJJcJJJJ.......",
        "......JJJJJcNNNNcJJJJJ......",
        "......JJJJJcNNNNcJJJJJ......",
        ".....JJJJJJcNNNNcJJJJJJ.....",
        "....KJJJJJJcNNNNcJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        "......JJJJJJJJJJJJJJJJ......",
        ".......JJJJJJJJJJJJJJ.......",
        "........PPPPPPPPPPPP........",
        "........PPPPPPPPPPPP........",
        "........PPPPPPPPPPPP........",
        "........PPPPPPPPPPPP........",
        "........PPPPPPPPPPPP........",
        "........PPPP..PPPPPP........",
        "........PPPP..PPPPPP........",
        "........PPPP..PPPPPP........",
        "........PPPP..PPPPPP........",
        "........BBBB..BBBBBB........",
        "........BBBB..BBBBBB........",
        "........BBBB..BBBBBB........",
        ".........bbb..bbbbb.........",
    ],
    run1_down: [
        ".........HHHHHHHHHH.........",
        "........HHHHHHHHHHHH........",
        ".......HHHHHHHHHHHHHH.......",
        "......HHHHHHHHHHHHHHHH......",
        "......HHHsssssssssssHH......",
        ".....HHHsSSSSSSSSSSsHHH.....",
        ".....HHHsS@SSSSSS@SsHHH.....",
        ".....HHHsSSSSSSSSSSsHHH.....",
        ".....HHHsSSSSSSSSSSsHHH.....",
        "......HHsSSS/SS/SSSsHH......",
        ".......HssSSSSSSSSssH.......",
        "........ssSSSSSSSSss........",
        "..........SSSSSSSS..........",
        "..........SSSSSSSS..........",
        "........JJJJJJJJJJJJ........",
        ".......JJJJcJJJJcJJJJ.......",
        "......JJJJJcNNNNcJJJJJ......",
        "......JJJJJcNNNNcJJJJJ......",
        ".....JJJJJJcNNNNcJJJJJJ.....",
        "....KJJJJJJcNNNNcJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        "......JJJJJJJJJJJJJJJJ......",
        "......PPPPPPPPPPPPPPPP......",
        ".....PPPPPPPPPPPPPPPPPP.....",
        ".....PPPPPP.....PPPPPP......",
        ".....PPPPP.......PPPPP......",
        ".....PPPPP.......PPPPP......",
        ".....BBBB........PPPPP......",
        ".....BBBB........BBBB.......",
        ".....BBBB........BBBB.......",
        ".................BBBB.......",
        ".................BBBB.......",
        ".................bbb........",
        "............................",
        "............................",
        "............................",
        "............................",
    ],
    run2_down: [
        ".........HHHHHHHHHH.........",
        "........HHHHHHHHHHHH........",
        ".......HHHHHHHHHHHHHH.......",
        "......HHHHHHHHHHHHHHHH......",
        "......HHHsssssssssssHH......",
        ".....HHHsSSSSSSSSSSsHHH.....",
        ".....HHHsS@SSSSSS@SsHHH.....",
        ".....HHHsSSSSSSSSSSsHHH.....",
        ".....HHHsSSSSSSSSSSsHHH.....",
        "......HHsSSS/SS/SSSsHH......",
        ".......HssSSSSSSSSssH.......",
        "........ssSSSSSSSSss........",
        "..........SSSSSSSS..........",
        "..........SSSSSSSS..........",
        "........JJJJJJJJJJJJ........",
        ".......JJJJcJJJJcJJJJ.......",
        "......JJJJJcNNNNcJJJJJ......",
        "......JJJJJcNNNNcJJJJJ......",
        ".....JJJJJJcNNNNcJJJJJJ.....",
        "....KJJJJJJcNNNNcJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        "......JJJJJJJJJJJJJJJJ......",
        "......PPPPPPPPPPPPPPPP......",
        ".....PPPPPPPPPPPPPPPPPP.....",
        "......PPPPPP.....PPPPPP.....",
        ".......PPPPP.......PPPPP....",
        ".......PPPPP.......PPPPP....",
        ".......PPPPP.......BBBB.....",
        ".......BBBB........BBBB.....",
        ".......BBBB........BBBB.....",
        ".......BBBB.................",
        ".......BBBB.................",
        "........bbb.................",
        "............................",
        "............................",
        "............................",
        "............................",
    ],
    idle_up: [
        ".........HHHHHHHHHH.........",
        "........HHHHHHHHHHHH........",
        ".......HHHHHHHHHHHHHH.......",
        "......HHHHHHHHHHHHHHHH......",
        "......HHHHHHHHHHHHHHHH......",
        ".....HHHHHHHHHHHHHHHHHH.....",
        ".....HHHHHHHHHHHHHHHHHH.....",
        ".....HHHHHHHHHHHHHHHHHH.....",
        ".....HHHHHHHHHHHHHHHHHH.....",
        "......HHHHHHHHHHHHHHHH......",
        ".......HHHHHHHHHHHHHH.......",
        "........HHHHHHHHHHHH........",
        "..........SSSSSSSS..........",
        "..........SSSSSSSS..........",
        "........JJJJJJJJJJJJ........",
        ".......JJJJcJJJJcJJJJ.......",
        "......JJJJJcNNNNcJJJJJ......",
        "......JJJJJcNNNNcJJJJJ......",
        ".....JJJJJJcNNNNcJJJJJJ.....",
        "....KJJJJJJcNNNNcJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        "......JJJJJJJJJJJJJJJJ......",
        ".......JJJJJJJJJJJJJJ.......",
        "........PPPPPPPPPPPP........",
        "........PPPPPPPPPPPP........",
        "........PPPPPPPPPPPP........",
        "........PPPPPPPPPPPP........",
        "........PPPPPPPPPPPP........",
        "........PPPP..PPPPPP........",
        "........PPPP..PPPPPP........",
        "........PPPP..PPPPPP........",
        "........PPPP..PPPPPP........",
        "........BBBB..BBBBBB........",
        "........BBBB..BBBBBB........",
        "........BBBB..BBBBBB........",
        ".........bbb..bbbbb.........",
    ],
    run1_up: [
        ".........HHHHHHHHHH.........",
        "........HHHHHHHHHHHH........",
        ".......HHHHHHHHHHHHHH.......",
        "......HHHHHHHHHHHHHHHH......",
        "......HHHHHHHHHHHHHHHH......",
        ".....HHHHHHHHHHHHHHHHHH.....",
        ".....HHHHHHHHHHHHHHHHHH.....",
        ".....HHHHHHHHHHHHHHHHHH.....",
        ".....HHHHHHHHHHHHHHHHHH.....",
        "......HHHHHHHHHHHHHHHH......",
        ".......HHHHHHHHHHHHHH.......",
        "........HHHHHHHHHHHH........",
        "..........SSSSSSSS..........",
        "..........SSSSSSSS..........",
        "........JJJJJJJJJJJJ........",
        ".......JJJJcJJJJcJJJJ.......",
        "......JJJJJcNNNNcJJJJJ......",
        "......JJJJJcNNNNcJJJJJ......",
        ".....JJJJJJcNNNNcJJJJJJ.....",
        "....KJJJJJJcNNNNcJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        "......JJJJJJJJJJJJJJJJ......",
        "......PPPPPPPPPPPPPPPP......",
        ".....PPPPPPPPPPPPPPPPPP.....",
        ".....PPPPPP.....PPPPPP......",
        ".....PPPPP.......PPPPP......",
        ".....PPPPP.......PPPPP......",
        ".....BBBB........PPPPP......",
        ".....BBBB........BBBB.......",
        ".....BBBB........BBBB.......",
        ".................BBBB.......",
        ".................BBBB.......",
        ".................bbb........",
        "............................",
        "............................",
        "............................",
        "............................",
    ],
    run2_up: [
        ".........HHHHHHHHHH.........",
        "........HHHHHHHHHHHH........",
        ".......HHHHHHHHHHHHHH.......",
        "......HHHHHHHHHHHHHHHH......",
        "......HHHHHHHHHHHHHHHH......",
        ".....HHHHHHHHHHHHHHHHHH.....",
        ".....HHHHHHHHHHHHHHHHHH.....",
        ".....HHHHHHHHHHHHHHHHHH.....",
        ".....HHHHHHHHHHHHHHHHHH.....",
        "......HHHHHHHHHHHHHHHH......",
        ".......HHHHHHHHHHHHHH.......",
        "........HHHHHHHHHHHH........",
        "..........SSSSSSSS..........",
        "..........SSSSSSSS..........",
        "........JJJJJJJJJJJJ........",
        ".......JJJJcJJJJcJJJJ.......",
        "......JJJJJcNNNNcJJJJJ......",
        "......JJJJJcNNNNcJJJJJ......",
        ".....JJJJJJcNNNNcJJJJJJ.....",
        "....KJJJJJJcNNNNcJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        "......JJJJJJJJJJJJJJJJ......",
        "......PPPPPPPPPPPPPPPP......",
        ".....PPPPPPPPPPPPPPPPPP.....",
        "......PPPPPP.....PPPPPP.....",
        ".......PPPPP.......PPPPP....",
        ".......PPPPP.......PPPPP....",
        ".......PPPPP.......BBBB.....",
        ".......BBBB........BBBB.....",
        ".......BBBB........BBBB.....",
        ".......BBBB.................",
        ".......BBBB.................",
        "........bbb.................",
        "............................",
        "............................",
        "............................",
        "............................",
    ],
    idle_right: [
        ".........HHHHHHHHHHH........",
        "........HHHHHHHHHHHHHH......",
        ".......HHHHHHHHHHHHHHHH.....",
        "......HHHHHHHHHHHHHHHHHH....",
        "......HHHHsssssssssHHHH.....",
        ".....HHHHsSSSSSSSSsHHHH.....",
        ".....HHHHsS@SSSSSSsHHHH.....",
        ".....HHHHsSSSSSSSSsHHHH.....",
        ".....HHHHsSSSSSSSSsHHHH.....",
        "......HHHsSSS/SS/SSsHH......",
        ".......HHsSSSSSSSSSsHH......",
        "........ssSSSSSSSSsss.......",
        "..........SSSSSSSSS.........",
        "..........SSSSSSSSS.........",
        "........JJJJJJJJJJJJ........",
        ".......JJJJJcJJJJcJJJ.......",
        "......JJJJJJcNNNNcJJJJ......",
        "......JJJJJJcNNNNcJJJJ......",
        ".....JJJJJJJcNNNNcJJJJJ.....",
        "....KJJJJJJJcNNNNcJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        "......JJJJJJJJJJJJJJJJ......",
        ".......JJJJJJJJJJJJJJ.......",
        "........PPPPPPPPPPPP........",
        "........PPPPPPPPPPPP........",
        "........PPPPPPPPPPPP........",
        "........PPPPPPPPPPPP........",
        "........PPPPPPPPPPPP........",
        "........PPPP.PPPPPPP........",
        "........PPPP.PPPPPPP........",
        "........PPPP.PPPPPPP........",
        "........PPPP.PPPPPPP........",
        "........BBBB.BBBBBBB........",
        "........BBBB.BBBBBBB........",
        "........BBBB.BBBBBBB........",
        ".........bbb.bbbbbb.........",
    ],
    run1_right: [
        ".........HHHHHHHHHHH........",
        "........HHHHHHHHHHHHHH......",
        ".......HHHHHHHHHHHHHHHH.....",
        "......HHHHHHHHHHHHHHHHHH....",
        "......HHHHsssssssssHHHH.....",
        ".....HHHHsSSSSSSSSsHHHH.....",
        ".....HHHHsS@SSSSSSsHHHH.....",
        ".....HHHHsSSSSSSSSsHHHH.....",
        ".....HHHHsSSSSSSSSsHHHH.....",
        "......HHHsSSS/SS/SSsHH......",
        ".......HHsSSSSSSSSSsHH......",
        "........ssSSSSSSSSsss.......",
        "..........SSSSSSSSS.........",
        "..........SSSSSSSSS.........",
        "........JJJJJJJJJJJJ........",
        ".......JJJJJcJJJJcJJJ.......",
        "......JJJJJJcNNNNcJJJJ......",
        "......JJJJJJcNNNNcJJJJ......",
        ".....JJJJJJJcNNNNcJJJJJ.....",
        "....KJJJJJJJcNNNNcJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        "......JJJJJJJJJJJJJJJJ......",
        "......PPPPPPPPPPPPPPPP......",
        ".....PPPPPPPPPPPPPPPPPP.....",
        ".....PPPPPP.....PPPPPP......",
        ".....PPPPP.......PPPPP......",
        ".....PPPPP.......PPPPP......",
        ".....BBBB........PPPPP......",
        ".....BBBB........BBBB.......",
        ".....BBBB........BBBB.......",
        ".................BBBB.......",
        ".................BBBB.......",
        ".................bbb........",
        "............................",
        "............................",
        "............................",
        "............................",
        "............................",
    ],
    run2_right: [
        ".........HHHHHHHHHHH........",
        "........HHHHHHHHHHHHHH......",
        ".......HHHHHHHHHHHHHHHH.....",
        "......HHHHHHHHHHHHHHHHHH....",
        "......HHHHsssssssssHHHH.....",
        ".....HHHHsSSSSSSSSsHHHH.....",
        ".....HHHHsS@SSSSSSsHHHH.....",
        ".....HHHHsSSSSSSSSsHHHH.....",
        ".....HHHHsSSSSSSSSsHHHH.....",
        "......HHHsSSS/SS/SSsHH......",
        ".......HHsSSSSSSSSSsHH......",
        "........ssSSSSSSSSsss.......",
        "..........SSSSSSSSS.........",
        "..........SSSSSSSSS.........",
        "........JJJJJJJJJJJJ........",
        ".......JJJJJcJJJJcJJJ.......",
        "......JJJJJJcNNNNcJJJJ......",
        "......JJJJJJcNNNNcJJJJ......",
        ".....JJJJJJJcNNNNcJJJJJ.....",
        "....KJJJJJJJcNNNNcJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        "......JJJJJJJJJJJJJJJJ......",
        "......PPPPPPPPPPPPPPPP......",
        ".....PPPPPPPPPPPPPPPPPP.....",
        "......PPPPPP.....PPPPPP.....",
        ".......PPPPP.......PPPPP....",
        ".......PPPPP.......PPPPP....",
        ".......PPPPP.......BBBB.....",
        ".......BBBB........BBBB.....",
        ".......BBBB........BBBB.....",
        ".......BBBB.................",
        ".......BBBB.................",
        "........bbb.................",
        "............................",
        "............................",
        "............................",
        "............................",
        "............................",
    ],
    shoot: [
        ".........HHHHHHHHHH.........",
        "........HHHHHHHHHHHH........",
        ".......HHHHHHHHHHHHHH.......",
        "......HHHHHHHHHHHHHHHH......",
        "......HHHsssssssssssHH......",
        ".....HHHsSSSSSSSSSSsHHH.....",
        ".....HHHsS@SSSSSS@SsHHH.....",
        ".....HHHsSSSSSSSSSSsHHH.....",
        ".....HHHsSSSSSSSSSSsHHH.....",
        "......HHsSSS/SS/SSSsHH......",
        ".......HssSSSSSSSSssH.......",
        "........ssSSSSSSSSss........",
        "..........SSSSSSSS..........",
        "..........SSSSSSSS..........",
        "........JJJJJJJJJJJJ........",
        ".......JJJJcJJJJcJJJJ.......",
        "......JJJJJcNNNNcJJJJJ......",
        "......JJJJJcNNNNcJJJJJ......",
        ".....JJJJJJcNNNNcJJJJJJ.....",
        "....KJJJJJJcNNNNcJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        "....KJJJJJJJJJJJJJJJJJJK....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        ".....JJJJJJJJJJJJJJJJJJ.....",
        "......JJJJJJJJJJJJJJJJ......",
        ".......JJJJJJJJJJJJJJ.......",
        "........PPPPPPPPPPPP........",
        "........PPPPPPPPPPPP........",
        "........PPPPPPPPPPPP........",
        "........PPPPPPPPPPPP........",
        "........PPPPPPPPPPPP........",
        "........PPPP..PPPPPP........",
        "........PPPP..PPPPPP........",
        "........PPPP..PPPPPP........",
        "........PPPP..PPPPPP........",
        "........BBBB..BBBBBB........",
        "........BBBB..BBBBBB........",
        "........BBBB..BBBBBB........",
        ".........bbb..bbbbb.........",
    ],
    celebrate: [
        "..SS....HHHHHHHHHH....SS...",
        "..SS...HHHHHHHHHHHH...SS...",
        "..SS...HHHHHHHHHHHH...SS...",
        "..SS..HHHHHHHHHHHHHH..SS...",
        "..SS..HHHssssssssssHH.SS...",
        "..SS.HHHsSSSSSSSSsHHH.SS...",
        "..SS.HHHsS@SSSSSS@SsH.SS...",
        "..SS.HHHsSSSSSSSSSsH.SS....",
        "..SS..HHsSSS/SS/SSSs.SS....",
        "...S...HssSSSSSSSSs..S.....",
        "........ssSSSSSSSSss.......",
        "..........SSSSSSSS.........",
        "..........SSSSSSSS.........",
        "........JJJJJJJJJJJJ.......",
        ".......JJJJcJJJJcJJJJ......",
        "......JJJJJcNNNNcJJJJJ.....",
        "......JJJJJcNNNNcJJJJJ.....",
        ".....JJJJJJcNNNNcJJJJJJ....",
        "....KJJJJJJcNNNNcJJJJJJK...",
        "....KJJJJJJJJJJJJJJJJJJK...",
        "....KJJJJJJJJJJJJJJJJJJK...",
        "....KJJJJJJJJJJJJJJJJJJK...",
        ".....JJJJJJJJJJJJJJJJJJ....",
        ".....JJJJJJJJJJJJJJJJJJ....",
        "......JJJJJJJJJJJJJJJJ.....",
        ".......JJJJJJJJJJJJJJ......",
        "........PPPPPPPPPPPP.......",
        "........PPPPPPPPPPPP.......",
        "........PPPPPPPPPPPP.......",
        "........PPPPPPPPPPPP.......",
        "........PPPPPPPPPPPP.......",
        "........PPPP..PPPPPP.......",
        "........PPPP..PPPPPP.......",
        "........PPPP..PPPPPP.......",
        "........PPPP..PPPPPP.......",
        "........BBBB..BBBBBB.......",
        "........BBBB..BBBBBB.......",
        "........BBBB..BBBBBB.......",
        ".........bbb..bbbbb........",
    ],
    tackle: [
        "............................",
        "............................",
        "............................",
        "............................",
        "............................",
        "............................",
        "................HHHHHHHH....",
        "...............HHHHHHHHHH...",
        "..............HHHHHHHHHHHH..",
        "..............HHssssssssHH..",
        ".............HHsSSSSSSSSsH..",
        ".............HHsS@SSSS@SSsH.",
        ".............HHsSSSSSSSSsH..",
        "..............HsSS/SS/SSsH..",
        "...............ssSSSSSSss...",
        ".................SSSSSS.....",
        "......JJJJJJJJJJJJJJJJJJ....",
        ".....JJJJcJJJJcJJJJJJJJJ....",
        "....JJJJJcNNNNcJJJJJJJJJJ...",
        "...JJJJJJcNNNNcJJJJJJJJJJ...",
        "..JJJJJJJcNNNNcJJJJJJJJJJJ..",
        "..KJJJJJJJJJJJJJJJJJJJJJJJ..",
        "..KJJJJJJJJJJJJJJJJJJJJJJJ..",
        "...JJJJJJJJJJJJJJJJJJJJJJJ..",
        "....JJJJJJJJJJJJJJJJJJJJJJ..",
        "....PPPPPPPPPPPPPPPPPPPPPP..",
        "...PPPPPPPPPPPPPPPPPPPPPPP..",
        "..PPPPPPPPPPPPPPPPPPPPPPPPP.",
        ".BBBB.....................BB",
        ".BBBB.....................BB",
        "............................",
        "............................",
        "............................",
        "............................",
        "............................",
        "............................",
        "............................",
        "............................",
        "............................",
    ],
    fallen: [
        "............................",
        "............................",
        "............................",
        "............................",
        "............................",
        "............................",
        "............................",
        "................HHHHHHHH....",
        "...............HHHHHHHHHH...",
        "..............HHHHHHHHHHHH..",
        "..............HHssssssssHH..",
        ".............HHsSSSSSSSSsH..",
        ".............HHsS@SSSS@SSsH.",
        ".............HHsSSSSSSSSsH..",
        "..............HsSS/SS/SSsH..",
        "...............ssSSSSSSss...",
        ".................SSSSSS.....",
        "......JJJJJJJJJJJJJJJJJJ....",
        ".....JJJJcJJJJcJJJJJJJJJ....",
        "....JJJJJcNNNNcJJJJJJJJJJ...",
        "...JJJJJJcNNNNcJJJJJJJJJJ...",
        "..JJJJJJJcNNNNcJJJJJJJJJJJ..",
        "..KJJJJJJJJJJJJJJJJJJJJJJJ..",
        "..KJJJJJJJJJJJJJJJJJJJJJJJ..",
        "...JJJJJJJJJJJJJJJJJJJJJJJ..",
        "....JJJJJJJJJJJJJJJJJJJJJJ..",
        "....PPPPPPPPPPPPPPPPPPPPPP..",
        "...PPPPPPPPPPPPPPPPPPPPPPP..",
        ".BBBB.....................BB",
        ".BBBB.....................BB",
        "............................",
        "............................",
        "............................",
        "............................",
        "............................",
        "............................",
        "............................",
        "............................",
        "............................",
    ],
};

function drawPixelSprite(sprite, x, y, pixelSize, color1, color2, dorsal, isControlled, flipX) {
    const h = sprite.length;
    const w = sprite[0].length;
    const offsetX = -w * pixelSize / 2;
    const offsetY = -h * pixelSize;
    
    // Sombra
    ctx.fillStyle = 'rgba(0,0,0,0.4)';
    ctx.beginPath();
    ctx.ellipse(x, y + 4, w * pixelSize * 0.42, h * pixelSize * 0.10, 0, 0, Math.PI * 2);
    ctx.fill();
    
    for (let row = 0; row < h; row++) {
        for (let col = 0; col < w; col++) {
            const srcCol = flipX ? (w - 1 - col) : col;
            const ch = sprite[row][srcCol];
            if (ch === '.') continue;
            const px = x + offsetX + col * pixelSize;
            const py = y + offsetY + row * pixelSize;
            let color;
            switch (ch) {
                case 'H': color = '#3a1f0a'; break;
                case 'h': color = '#5a3a1a'; break;
                case 'S': color = '#f0c8a0'; break;
                case 's': color = '#d0a878'; break;
                case '@': color = '#0a0a0a'; break;
                case '/': color = '#7a2a1a'; break;
                case 'J': color = color1; break;
                case 'c': color = color2; break;
                case 'K': color = color2; break;
                case 'N': color = '#ffffff'; break;
                case 'P': color = '#1a1a2a'; break;
                case 'B': color = '#0a0a0a'; break;
                default: color = '#ff00ff';
            }
            ctx.fillStyle = color;
            ctx.fillRect(Math.round(px), Math.round(py), pixelSize, pixelSize);
        }
    }
    
    // Dorsal
    ctx.font = `bold ${Math.round(pixelSize * 4)}px Courier New`;
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.strokeStyle = 'rgba(0,0,0,0.9)';
    ctx.lineWidth = 3;
    ctx.fillStyle = '#ffffff';
    const dorsalY = y - h * pixelSize * 0.5;
    ctx.strokeText(dorsal, x, dorsalY);
    ctx.fillText(dorsal, x, dorsalY);
    
    if (isControlled) {
        const arrowY = y - h * pixelSize - 18;
        const bounce = Math.sin(animTimer * 0.15) * 3;
        ctx.fillStyle = '#00ffc8';
        ctx.beginPath();
        ctx.moveTo(x - 8, arrowY + bounce);
        ctx.lineTo(x + 8, arrowY + bounce);
        ctx.lineTo(x, arrowY + 12 + bounce);
        ctx.closePath();
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.5;
        ctx.stroke();
        ctx.strokeStyle = '#00ffc8';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.ellipse(x, y + 2, w * pixelSize * 0.5, h * pixelSize * 0.10, 0, 0, Math.PI * 2);
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
    ctx.ellipse(x + 2, y + 5, r * 1.2, r * 0.55, 0, 0, Math.PI * 2);
    ctx.fill();
    
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();
    
    ctx.fillStyle = '#111111';
    drawPolygon(x, y, 5, r * 0.4, ballRotation);
    for (let i = 0; i < 5; i++) {
        const a = (i / 5) * Math.PI * 2 - Math.PI / 2 + ballRotation;
        drawPolygon(x + Math.cos(a) * r * 0.7, y + Math.sin(a) * r * 0.7, 5, r * 0.3, a);
    }
    ctx.strokeStyle = 'rgba(0,0,0,0.6)';
    ctx.lineWidth = 1;
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
// RED ANIMADA
// =====================================================
let netLeftOffset = 0, netLeftVelocity = 0;
let netRightOffset = 0, netRightVelocity = 0;
function kickNet(side, force) {
    if (side === 'left') netLeftVelocity = 0.9 * force;
    else netRightVelocity = 0.9 * force;
}
function updateNets() {
    netLeftVelocity += -netLeftOffset * 0.15;
    netLeftVelocity *= 0.9;
    netLeftOffset += netLeftVelocity;
    netRightVelocity += -netRightOffset * 0.15;
    netRightVelocity *= 0.9;
    netRightOffset += netRightVelocity;
}

// =====================================================
// CAMPO
// =====================================================
function drawField() {
    const c = CESPEDES[CFG.cesped];
    const tl = toScreen(0, 0), tr = toScreen(ISO.fieldW, 0);
    const br = toScreen(ISO.fieldW, ISO.fieldH), bl = toScreen(0, ISO.fieldH);
    
    ctx.fillStyle = c.dark;
    ctx.beginPath();
    ctx.moveTo(tl.sx, tl.sy); ctx.lineTo(tr.sx, tr.sy);
    ctx.lineTo(br.sx, br.sy); ctx.lineTo(bl.sx, bl.sy);
    ctx.closePath(); ctx.fill();
    
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
    
    // Rayas diagonales
    ctx.globalAlpha = 0.06;
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 25;
    for (let i = -20; i < 60; i++) {
        const x1 = i * 80, x2 = x1 + 500;
        const p1 = toScreen(x1, 0), p2 = toScreen(x2, ISO.fieldH);
        ctx.beginPath(); ctx.moveTo(p1.sx, p1.sy); ctx.lineTo(p2.sx, p2.sy); ctx.stroke();
    }
    ctx.globalAlpha = 1;
    
    const drawLine = (x1, y1, x2, y2) => {
        const p1 = toScreen(x1, y1), p2 = toScreen(x2, y2);
        ctx.beginPath(); ctx.moveTo(p1.sx, p1.sy); ctx.lineTo(p2.sx, p2.sy); ctx.stroke();
    };
    const drawRect = (x, y, w, h) => {
        drawLine(x, y, x+w, y); drawLine(x+w, y, x+w, y+h);
        drawLine(x+w, y+h, x, y+h); drawLine(x, y+h, x, y);
    };
    const drawCircle = (cx, cy, r) => {
        ctx.beginPath();
        for (let i = 0; i <= 40; i++) {
            const a = (i / 40) * Math.PI * 2;
            const p = toScreen(cx + Math.cos(a)*r, cy + Math.sin(a)*r);
            if (i === 0) ctx.moveTo(p.sx, p.sy); else ctx.lineTo(p.sx, p.sy);
        }
        ctx.stroke();
    };
    
    ctx.strokeStyle = c.line; ctx.lineWidth = 2;
    drawRect(0, 0, ISO.fieldW, ISO.fieldH);
    drawLine(ISO.centerX, 0, ISO.centerX, ISO.fieldH);
    drawCircle(ISO.centerX, ISO.centerY, 100);
    drawRect(0, ISO.centerY - 200, 160, 400);
    drawRect(ISO.fieldW - 160, ISO.centerY - 200, 160, 400);
    drawRect(0, ISO.centerY - 90, 60, 180);
    drawRect(ISO.fieldW - 60, ISO.centerY - 90, 60, 180);
    
    const pen1 = toScreen(120, ISO.centerY), pen2 = toScreen(ISO.fieldW - 120, ISO.centerY);
    ctx.fillStyle = c.line;
    ctx.beginPath(); ctx.arc(pen1.sx, pen1.sy, 3, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(pen2.sx, pen2.sy, 3, 0, Math.PI*2); ctx.fill();
    
    // Portería IZQUIERDA
    const GOAL_H = 100, GOAL_DEPTH = 45;
    const gTL = toScreen(-GOAL_DEPTH - netLeftOffset * 30, ISO.centerY - GOAL_H);
    const gBL = toScreen(-GOAL_DEPTH - netLeftOffset * 30, ISO.centerY + GOAL_H);
    const gFR = toScreen(0, ISO.centerY - GOAL_H);
    const gFR2 = toScreen(0, ISO.centerY + GOAL_H);
    ctx.fillStyle = 'rgba(0,0,0,0.55)';
    ctx.beginPath();
    ctx.moveTo(gFR.sx, gFR.sy); ctx.lineTo(gFR2.sx, gFR2.sy);
    ctx.lineTo(gBL.sx, gBL.sy); ctx.lineTo(gTL.sx, gTL.sy);
    ctx.closePath(); ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,0.6)'; ctx.lineWidth = 1;
    for (let i = 0; i <= 8; i++) {
        const t = i / 8;
        const x1 = gFR.sx + (gFR2.sx - gFR.sx) * t;
        const y1 = gFR.sy + (gFR2.sy - gFR.sy) * t;
        const x2 = gTL.sx + (gBL.sx - gTL.sx) * t;
        const y2 = gTL.sy + (gBL.sy - gTL.sy) * t;
        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    }
    for (let i = 0; i <= 10; i++) {
        const t = i / 10;
        const x1 = gFR.sx + (gTL.sx - gFR.sx) * t;
        const y1 = gFR.sy + (gTL.sy - gFR.sy) * t;
        const x2 = gFR2.sx + (gBL.sx - gFR2.sx) * t;
        const y2 = gFR2.sy + (gBL.sy - gFR2.sy) * t;
        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    }
    ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 5; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(gFR.sx, gFR.sy); ctx.lineTo(gTL.sx, gTL.sy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(gFR2.sx, gFR2.sy); ctx.lineTo(gBL.sx, gBL.sy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(gTL.sx, gTL.sy); ctx.lineTo(gBL.sx, gBL.sy); ctx.stroke();
    ctx.lineCap = 'butt';
    
    // Portería DERECHA
    const gTR = toScreen(ISO.fieldW + GOAL_DEPTH + netRightOffset * 30, ISO.centerY - GOAL_H);
    const gBR = toScreen(ISO.fieldW + GOAL_DEPTH + netRightOffset * 30, ISO.centerY + GOAL_H);
    const gFL = toScreen(ISO.fieldW, ISO.centerY - GOAL_H);
    const gFL2 = toScreen(ISO.fieldW, ISO.centerY + GOAL_H);
    ctx.fillStyle = 'rgba(0,0,0,0.55)';
    ctx.beginPath();
    ctx.moveTo(gFL.sx, gFL.sy); ctx.lineTo(gFL2.sx, gFL2.sy);
    ctx.lineTo(gBR.sx, gBR.sy); ctx.lineTo(gTR.sx, gTR.sy);
    ctx.closePath(); ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,0.6)'; ctx.lineWidth = 1;
    for (let i = 0; i <= 8; i++) {
        const t = i / 8;
        const x1 = gFL.sx + (gFL2.sx - gFL.sx) * t;
        const y1 = gFL.sy + (gFL2.sy - gFL.sy) * t;
        const x2 = gTR.sx + (gBR.sx - gTR.sx) * t;
        const y2 = gTR.sy + (gBR.sy - gTR.sy) * t;
        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    }
    for (let i = 0; i <= 10; i++) {
        const t = i / 10;
        const x1 = gFL.sx + (gTR.sx - gFL.sx) * t;
        const y1 = gFL.sy + (gTR.sy - gFL.sy) * t;
        const x2 = gFL2.sx + (gBR.sx - gFL2.sx) * t;
        const y2 = gFL2.sy + (gBR.sy - gFL2.sy) * t;
        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    }
    ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 5; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(gFL.sx, gFL.sy); ctx.lineTo(gTR.sx, gTR.sy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(gFL2.sx, gFL2.sy); ctx.lineTo(gBR.sx, gBR.sy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(gTR.sx, gTR.sy); ctx.lineTo(gBR.sx, gBR.sy); ctx.stroke();
    ctx.lineCap = 'butt';
}

// =====================================================
// GRADAS DIAGONALES CON CARTELES
// =====================================================
function drawCrowd() {
    const gradFull = ctx.createLinearGradient(0, 0, 0, H);
    gradFull.addColorStop(0, '#0a1a0a');
    gradFull.addColorStop(0.5, '#0d1f0d');
    gradFull.addColorStop(1, '#0a1a0a');
    ctx.fillStyle = gradFull;
    ctx.fillRect(0, 0, W, H);
    
    const topLeft = toScreen(0, 0);
    const topRight = toScreen(ISO.fieldW, 0);
    const botLeft = toScreen(0, ISO.fieldH);
    const botRight = toScreen(ISO.fieldW, ISO.fieldH);
    
    const colores = ['#e8b890', '#c84040', '#4060c8', '#f0d040', '#40a040', '#e060a0', '#a058c8', '#58c8c8'];
    const gradaH = 120;
    
    const dirX = topRight.sx - topLeft.sx;
    const dirY = topRight.sy - topLeft.sy;
    const len = Math.hypot(dirX, dirY);
    const nx = dirX / len;
    const ny = dirY / len;
    const perpX = -ny;
    const perpY = nx;
    
    const gA = { x: topLeft.sx, y: topLeft.sy };
    const gB = { x: topRight.sx, y: topRight.sy };
    const gC = { x: topRight.sx + perpX * gradaH, y: topRight.sy + perpY * gradaH };
    const gD = { x: topLeft.sx + perpX * gradaH, y: topLeft.sy + perpY * gradaH };
    
    ctx.fillStyle = '#0f0f1a';
    ctx.beginPath();
    ctx.moveTo(gA.x, gA.y); ctx.lineTo(gB.x, gB.y);
    ctx.lineTo(gC.x, gC.y); ctx.lineTo(gD.x, gD.y);
    ctx.closePath(); ctx.fill();
    
    const filas = 14, asientosPorFila = 60;
    for (let fila = 0; fila < filas; fila++) {
        const t = (fila + 1) / (filas + 1);
        for (let asiento = 0; asiento < asientosPorFila; asiento++) {
            const s = asiento / (asientosPorFila - 1);
            const baseX = topLeft.sx + (topRight.sx - topLeft.sx) * s;
            const baseY = topLeft.sy + (topRight.sy - topLeft.sy) * s;
            const px = baseX + perpX * (t * gradaH);
            const py = baseY + perpY * (t * gradaH);
            const idx = (fila * 7 + asiento * 13) % colores.length;
            const tam = 3 + t * 2;
            ctx.fillStyle = colores[idx];
            ctx.fillRect(px, py, tam, tam);
            ctx.fillStyle = '#e8b890';
            ctx.fillRect(px + 0.5, py - 1, tam - 1, tam - 1);
        }
    }
    
    // Cartel publicitario pegado al borde del campo
    const cartelH = 22;
    const cA = { x: topLeft.sx, y: topLeft.sy };
    const cB = { x: topRight.sx, y: topRight.sy };
    const cC = { x: topRight.sx + perpX * cartelH, y: topRight.sy + perpY * cartelH };
    const cD = { x: topLeft.sx + perpX * cartelH, y: topLeft.sy + perpY * cartelH };
    
    ctx.fillStyle = '#0a0e14';
    ctx.beginPath();
    ctx.moveTo(cA.x, cA.y); ctx.lineTo(cB.x, cB.y);
    ctx.lineTo(cC.x, cC.y); ctx.lineTo(cD.x, cD.y);
    ctx.closePath(); ctx.fill();
    
    ctx.strokeStyle = '#00d4a8';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(cC.x, cC.y); ctx.lineTo(cD.x, cD.y);
    ctx.stroke();
    
    ctx.fillStyle = '#00d4a8';
    ctx.font = 'bold 12px Courier New';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    const textos = ['· FIFA TOTAL ·', '· RETRO LIGA ·', '· SOUNDSNIP ·', '· FIFA TOTAL ·', '· RETRO FOOTBALL 96 ·', '· LIGA PRO ·'];
    for (let i = 0; i < 12; i++) {
        const s = (i + 0.5) / 12;
        const baseX = topLeft.sx + (topRight.sx - topLeft.sx) * s;
        const baseY = topLeft.sy + (topRight.sy - topLeft.sy) * s;
        const cx = baseX + perpX * (cartelH / 2);
        const cy = baseY + perpY * (cartelH / 2);
        ctx.fillText(textos[i % textos.length], cx, cy);
    }
    ctx.textAlign = 'left';
    ctx.textBaseline = 'alphabetic';
    
    // Grada inferior
    const gradaInfH = 80;
    const perpX2 = ny;
    const perpY2 = -nx;
    const bA = { x: botLeft.sx, y: botLeft.sy };
    const bB = { x: botRight.sx, y: botRight.sy };
    const bC = { x: botRight.sx + perpX2 * gradaInfH, y: botRight.sy + perpY2 * gradaInfH };
    const bD = { x: botLeft.sx + perpX2 * gradaInfH, y: botLeft.sy + perpY2 * gradaInfH };
    
    ctx.fillStyle = '#0f0f1a';
    ctx.beginPath();
    ctx.moveTo(bA.x, bA.y); ctx.lineTo(bB.x, bB.y);
    ctx.lineTo(bC.x, bC.y); ctx.lineTo(bD.x, bD.y);
    ctx.closePath(); ctx.fill();
    
    for (let fila = 0; fila < 8; fila++) {
        const t = (fila + 1) / 9;
        for (let asiento = 0; asiento < 60; asiento++) {
            const s = asiento / 59;
            const baseX = botLeft.sx + (botRight.sx - botLeft.sx) * s;
            const baseY = botLeft.sy + (botRight.sy - botLeft.sy) * s;
            const px = baseX + perpX2 * (t * gradaInfH);
            const py = baseY + perpY2 * (t * gradaInfH);
            const idx = (fila * 11 + asiento * 5 + 3) % colores.length;
            const tam = 3 + t * 2;
            ctx.fillStyle = colores[idx];
            ctx.fillRect(px, py, tam, tam);
            ctx.fillStyle = '#e8b890';
            ctx.fillRect(px + 0.5, py - 1, tam - 1, tam - 1);
        }
    }
}

// =====================================================
// MARCADOR
// =====================================================
function drawScoreboard(score, time) {
    const x = 20, y = 20;
    ctx.fillStyle = 'rgba(0,0,0,0.8)';
    ctx.fillRect(x, y, 200, 60);
    ctx.strokeStyle = '#00ff88'; ctx.lineWidth = 1.5;
    ctx.strokeRect(x, y, 200, 60);
    const mm = Math.floor(time / 60);
    const ss = Math.floor(time % 60).toString().padStart(2, '0');
    ctx.fillStyle = '#ffffff'; ctx.font = 'bold 20px Courier New';
    ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
    ctx.fillText(`${mm}:${ss}`, x + 12, y + 30);
    ctx.fillStyle = '#ffdd00'; ctx.font = 'bold 30px Courier New';
    ctx.textAlign = 'right';
    ctx.fillText(`${score.you}-${score.rival}`, x + 190, y + 30);
    ctx.fillStyle = '#00ff88';
    ctx.fillRect(x, y + 55, 200, 5);
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
const PR = 14, BR = 8;
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
let controlledIndex = 0;
const cards = {};
const skillParticles = [];

const you = { players: [] };
const rival = { players: [] };

CFG.formJug.forEach(([fx, fy], i) => {
    const dd = CFG.jugadores[i] || {};
    you.players.push({
        x: fx * FIELD.w, y: fy * FIELD.h, vx: 0, vy: 0,
        num: dd.num || i+1, name: dd.nombre || 'Jugador',
        vel: dd.vel || 75, tir: dd.tir || 75, def: dd.def || 75,
        pas: dd.pas || 75, reg: dd.reg || 75,
        isControlled: i === 0, side: 'you', facing: 'down',
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
        isControlled: false, side: 'rival', facing: 'up',
        state: 'idle', stateTimer: 0,
        homeX: FIELD.w - fx * FIELD.w, homeY: fy * FIELD.h,
    });
});

const ball = { x: FIELD.w/2, y: FIELD.h/2, vx: 0, vy: 0 };

const KEYMAP = {
    'w': 'up', 'arrowup': 'up',
    's': 'down', 'arrowdown': 'down',
    'a': 'left', 'arrowleft': 'left',
    'd': 'right', 'arrowright': 'right',
    ' ': 'action', 'q': 'dribble',
    'e': 'shoot',
    'tab': 'switch', 'c': 'switch',
};
function handleKey(e, isDown) {
    const raw = e.key.toLowerCase();
    const action = KEYMAP[raw];
    if (!action) return;
    keys[action] = isDown;
    if (raw.startsWith('arrow') || raw === ' ' || raw === 'tab') e.preventDefault();
    if (isDown && action === 'switch' && gameState === "play") switchToNextPlayer();
    if (isDown && action === 'dribble' && dribbleCooldown <= 0 && gameState === "play") attemptDribble();
}
window.addEventListener('keydown', e => handleKey(e, true), true);
window.addEventListener('keyup', e => handleKey(e, false), true);
document.addEventListener('keydown', e => handleKey(e, true), true);
document.addEventListener('keyup', e => handleKey(e, false), true);
canvas.tabIndex = 0;
canvas.addEventListener('click', () => canvas.focus());
window.addEventListener('click', () => canvas.focus());
canvas.focus();
setTimeout(() => canvas.focus(), 500);

function setControlledIndex(newIndex) {
    you.players.forEach((p, i) => { p.isControlled = (i === newIndex); });
    controlledIndex = newIndex;
}
function switchToNextPlayer() {
    for (let i = 1; i <= you.players.length; i++) {
        const next = (controlledIndex + i) % you.players.length;
        if (next === 0) continue;
        const p = you.players[next];
        if (p.x < 0) continue;
        if (p.state === 'fallen') continue;
        setControlledIndex(next);
        return;
    }
}
function autoSwitchToNearestToBall() {
    let best = controlledIndex, bestDist = Infinity;
    for (let i = 1; i < you.players.length; i++) {
        const p = you.players[i];
        if (p.x < 0) continue;
        if (p.state === 'fallen' || p.state === 'tackle') continue;
        const d = dist(p, ball);
        if (d < bestDist) { bestDist = d; best = i; }
    }
    if (best !== controlledIndex) setControlledIndex(best);
}

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
        const tvx = (dx / len) * speed;
        const tvy = (dy / len) * speed;
        p.vx += (tvx - p.vx) * 0.25;
        p.vy += (tvy - p.vy) * 0.25;
        if (Math.abs(dx) > Math.abs(dy) * 1.3) p.facing = dx > 0 ? 'right' : 'left';
        else if (Math.abs(dy) > Math.abs(dx) * 1.3) p.facing = dy > 0 ? 'down' : 'up';
        else p.facing = dx > 0 ? 'right' : 'left';
    } else {
        p.vx *= 0.88; p.vy *= 0.88;
    }
    p.x += p.vx; p.y += p.vy;
    clampToField(p, PR);
}

function showBigAlert(text, color) {
    const a = document.getElementById('bigAlert');
    a.textContent = text; a.style.color = color; a.style.opacity = '1';
    setTimeout(() => a.style.opacity = '0', 1200);
}

// ========== REGATES ==========
function attemptDribble() {
    const p = you.players[controlledIndex];
    if (!p) return;
    dribbleCooldown = 60;
    let nearest = null, nd = 999;
    for (const r of rival.players) {
        if (r.x < 0) continue;
        const d = dist(p, r);
        if (d < nd) { nd = d; nearest = r; }
    }
    if (!nearest || nd > 80) { p.vx *= 1.6; p.vy *= 1.6; showBigAlert("💨 SPRINT", "#00ffc8"); return; }
    const inBox = p.x > FIELD.w - 250 || p.x < 250;
    const isGood = p.reg >= 80;
    const isElite = p.reg >= 88;
    let skillOptions = ['bicicleta'];
    if (isGood) { skillOptions.push('ruleta'); skillOptions.push('sombrero'); }
    if (isElite) skillOptions.push('cano');
    if (isElite && inBox) skillOptions.push('rabona');
    if (isElite) skillOptions.push('elastica');
    const skill = skillOptions[Math.floor(Math.random() * skillOptions.length)];
    const baseProb = 0.5 + (p.reg - nearest.def) / 150 + (p.vel - nearest.vel) / 250;
    const skillBonus = { 'bicicleta': 0, 'ruleta': -0.05, 'sombrero': -0.1, 'cano': -0.15, 'rabona': -0.2, 'elastica': -0.15 };
    let prob = baseProb + (skillBonus[skill] || 0);
    prob = Math.max(0.15, Math.min(0.92, prob));
    const success = Math.random() < prob;
    executeSkill(p, nearest, skill, success);
}

function executeSkill(p, defender, skill, success) {
    const angle = Math.atan2(ball.y - p.y, ball.x - p.x);
    let exitAngle = angle;
    if (skill === 'ruleta') exitAngle = angle + (Math.random() < 0.5 ? Math.PI/2 : -Math.PI/2);
    else if (skill === 'elastica') exitAngle = angle + (Math.random() < 0.5 ? Math.PI*0.75 : -Math.PI*0.75);
    else if (skill === 'bicicleta') exitAngle = angle + (Math.random() - 0.5) * 0.8;
    if (success) {
        const power = { 'bicicleta': 40, 'ruleta': 55, 'sombrero': 60, 'cano': 65, 'rabona': 75, 'elastica': 80 }[skill] || 50;
        p.x += Math.cos(exitAngle) * power;
        p.y += Math.sin(exitAngle) * power;
        clampToField(p, PR);
        defender.vx *= 0.4; defender.vy *= 0.4;
        const info = {
            'bicicleta': { text: '¡BICICLETA!', color: '#00ffc8' },
            'ruleta':    { text: '¡RULETA!',    color: '#ffdd00' },
            'sombrero':  { text: '¡SOMBRERO!',  color: '#00b8ff' },
            'cano':      { text: '¡CAÑO!',      color: '#ff5c9f' },
            'rabona':    { text: '¡RABONA!',    color: '#a58cff' },
            'elastica':  { text: '¡ELÁSTICA!',  color: '#ff9f43' },
        }[skill];
        showBigAlert(info.text, info.color);
        const scr = toScreen(p.x, p.y);
        for (let i = 0; i < 15; i++) {
            const a = (i / 15) * Math.PI * 2;
            skillParticles.push({ x: scr.sx, y: scr.sy, vx: Math.cos(a)*3, vy: Math.sin(a)*3, life: 30, maxLife: 30, color: info.color, size: 3 });
        }
    } else {
        p.vx *= 0.2; p.vy *= 0.2;
        ball.vx = (Math.random() - 0.5) * 6;
        ball.vy = (Math.random() - 0.5) * 6;
        showBigAlert("❌ PERDIDO", "#ff3b5c");
    }
}

function updateSkillParticles() {
    for (let i = skillParticles.length - 1; i >= 0; i--) {
        const p = skillParticles[i];
        p.x += p.vx; p.y += p.vy;
        p.vx *= 0.94; p.vy *= 0.94;
        p.life--;
        if (p.life <= 0) skillParticles.splice(i, 1);
    }
}
function drawSkillParticles() {
    for (const p of skillParticles) {
        const alpha = p.life / p.maxLife;
        ctx.globalAlpha = alpha;
        ctx.fillStyle = p.color;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.size * alpha, 0, Math.PI * 2); ctx.fill();
    }
    ctx.globalAlpha = 1;
}

// ========== TACKLES ==========
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

// ========== FUERA DE BANDA Y CÓRNER ==========
function checkOutOfBounds() {
    if (ball.y - BR < 0 || ball.y + BR > FIELD.h) {
        const isTop = ball.y < FIELD.h/2;
        const outY = isTop ? BR + 5 : FIELD.h - BR - 5;
        const outX = Math.max(80, Math.min(FIELD.w - 80, ball.x));
        const thrower = (lastBallToucher && lastBallToucher.side === 'you') ? 'rival' : 'you';
        ball.x = outX; ball.y = outY;
        ball.vx = 0; ball.vy = 0;
        gameState = "throwin"; freezeTimer = 90;
        showBigAlert(`SAQUE DE BANDA ${thrower === 'you' ? '(TÚ)' : '(RIVAL)'}`, "#00d4a8");
        playWhistle();
        const throwTeam = thrower === 'you' ? you.players : rival.players;
        let closest = null, closestDist = 999;
        for (const p of throwTeam) {
            if (p.x < 0) continue;
            const d = Math.hypot(p.x - outX, p.y - outY);
            if (d < closestDist) { closestDist = d; closest = p; }
        }
        if (closest) {
            closest.x = outX + (thrower === 'you' ? -30 : 30);
            closest.y = outY;
            if (thrower === 'you') {
                const idx = you.players.indexOf(closest);
                if (idx >= 0) setControlledIndex(idx);
            }
        }
        return true;
    }
    if (ball.x - BR < 0 || ball.x + BR > FIELD.w) {
        const gTop = FIELD.h/2 - 100, gBot = FIELD.h/2 + 100;
        const isGoalArea = ball.y > gTop && ball.y < gBot;
        if (isGoalArea) return false;
        const isLeft = ball.x < FIELD.w/2;
        const isOffensiveCorner = (isLeft && lastBallToucher && lastBallToucher.side === 'rival') ||
                                   (!isLeft && lastBallToucher && lastBallToucher.side === 'you');
        if (isOffensiveCorner) {
            const cornerY = ball.y < FIELD.h/2 ? 20 : FIELD.h - 20;
            ball.x = isLeft ? 20 : FIELD.w - 20;
            ball.y = cornerY;
            ball.vx = 0; ball.vy = 0;
            gameState = "corner"; freezeTimer = 90;
            showBigAlert("CÓRNER", "#ffdd00");
            playWhistle();
        } else {
            ball.x = isLeft ? 100 : FIELD.w - 100;
            ball.y = FIELD.h/2;
            ball.vx = 0; ball.vy = 0;
            gameState = "goalkick"; freezeTimer = 90;
            showBigAlert("SAQUE DE PUERTA", "#a58cff");
            playWhistle();
        }
        return true;
    }
    return false;
}

function checkOffside() {
    if (!lastBallToucher || lastBallToucher.side !== 'you') return;
    if (Math.hypot(ball.vx, ball.vy) < 6) return;
    let receiver = null, minD = 999;
    for (const p of you.players) {
        if (p === lastBallToucher) continue;
        if (p.x < 0) continue;
        const d = dist(p, ball);
        if (d < 100 && d < minD) { minD = d; receiver = p; }
    }
    if (!receiver) return;
    let lastDefenderX = 0;
    for (let i = 1; i < rival.players.length; i++) {
        const r = rival.players[i];
        if (r.x < 0) continue;
        if (r.x > lastDefenderX) lastDefenderX = r.x;
    }
    if (rival.players[0].x > lastDefenderX) lastDefenderX = rival.players[0].x;
    if (receiver.x > lastDefenderX + 20 && receiver.x > FIELD.w / 2) {
        playWhistle();
        showBigAlert("FUERA DE JUEGO", "#ff3b5c");
        gameState = "offside"; freezeTimer = 90;
        ball.x = receiver.x; ball.y = receiver.y;
        ball.vx = 0; ball.vy = 0;
    }
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
        if (d < 30 && Math.random() < 0.04) { attemptTackle(r, owner); break; }
    }
}

function updateControlled() {
    if (gameState !== "play") return;
    const p = you.players[controlledIndex];
    if (!p) return;
    if (p.state === 'fallen' || p.state === 'tackle') return;
    let dx = 0, dy = 0;
    if (keys['up']) dy -= 1;
    if (keys['down']) dy += 1;
    if (keys['left']) dx -= 1;
    if (keys['right']) dx += 1;
    updatePlayer(p, dx, dy, 5.5);
    if (keys['shoot'] && dist(p, ball) < PR + BR + 12) {
        const dirX = p.facing === 'right' ? 1 : p.facing === 'left' ? -1 : 0;
        const dirY = p.facing === 'down' ? 1 : p.facing === 'up' ? -1 : 0;
        const targetX = FIELD.w, targetY = FIELD.h/2;
        const angle = (dirX === 0 && dirY === 0) ? Math.atan2(targetY - ball.y, targetX - ball.x) : Math.atan2(dirY, dirX);
        ball.vx = Math.cos(angle) * 22; ball.vy = Math.sin(angle) * 22;
        keys['shoot'] = false;
        p.state = 'shoot'; p.stateTimer = 15;
        lastBallToucher = p; playKick();
    }
    if (keys['action'] && dist(p, ball) < PR + BR + 12) {
        let best = null, bestScore = -Infinity;
        for (let i = 1; i < you.players.length; i++) {
            if (i === controlledIndex) continue;
            const mate = you.players[i];
            if (mate.x < 0) continue;
            const fwd = mate.x - p.x;
            if (fwd > 0 && fwd < 500) {
                const s = fwd - Math.abs(mate.y - p.y) * 0.5 + (mate.pas - 75) * 2;
                if (s > bestScore) { bestScore = s; best = mate; }
            }
        }
        if (best) {
            const angle = Math.atan2(best.y - ball.y, best.x - ball.x);
            ball.vx = Math.cos(angle) * 14; ball.vy = Math.sin(angle) * 14;
            keys['action'] = false;
            p.state = 'shoot'; p.stateTimer = 12;
            lastBallToucher = p; playKick();
            const receiverIdx = you.players.indexOf(best);
            setTimeout(() => { if (receiverIdx > 0) setControlledIndex(receiverIdx); }, 250);
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
        let target, speedMult = 1.0;
        if (weAttack) {
            const ballNearby = Math.abs(ball.x - p.x) < 400 && Math.abs(ball.y - p.y) < 300;
            if (i === 0) {
                target = { x: FIELD.w - 40, y: Math.max(FIELD.h/2 - 120, Math.min(FIELD.h/2 + 120, ball.y)) };
                speedMult = 0.6;
            } else if (i <= 4) {
                if (ballNearby && owner && owner.side === 'you') {
                    const dToCarrier = dist(p, owner);
                    if (dToCarrier < 250) { target = { x: owner.x, y: owner.y }; speedMult = 1.0; }
                    else { target = { x: ball.x + 100, y: ball.y }; speedMult = 0.9; }
                } else {
                    target = { x: Math.max(FIELD.w * 0.55, ball.x + 150), y: FIELD.h/2 + (i - 2.5) * 100 };
                    speedMult = 0.8;
                }
            } else if (i <= 7) {
                const dToBall = dist(p, ball);
                if (dToBall < 250) { target = { x: ball.x, y: ball.y }; speedMult = 1.0; }
                else { target = { x: (ball.x + FIELD.w) / 2, y: ball.y * 0.6 + FIELD.h/2 * 0.4 }; speedMult = 0.85; }
            } else {
                const dToBall = dist(p, ball);
                if (dToBall < 350) { target = { x: ball.x, y: ball.y }; speedMult = 0.95; }
                else { target = { x: Math.min(FIELD.w - 150, ball.x + 200), y: FIELD.h/2 + (i - 9) * 100 }; speedMult = 0.75; }
            }
        } else {
            const carrier = owner;
            if (i === 0) { target = { x: FIELD.w - 40, y: FIELD.h/2 }; speedMult = 0.5; }
            else if (i <= 4) { target = { x: FIELD.w * 0.6, y: FIELD.h/2 + (i - 2.5) * 100 }; speedMult = 0.7; }
            else if (i <= 7) { target = { x: carrier.x + (i - 6) * 100, y: carrier.y + (i % 2 === 0 ? 130 : -130) }; speedMult = 0.9; }
            else { target = { x: Math.min(FIELD.w - 100, carrier.x + 350 + (i - 9) * 50), y: FIELD.h/2 + (i - 9) * 130 }; speedMult = 1.0; }
        }
        const dx = target.x - p.x, dy = target.y - p.y;
        const d = Math.hypot(dx, dy) || 1;
        const baseSpeed = i === 0 ? CFG.difSpeed * 0.5 : (i <= 4 ? CFG.difSpeed * 0.85 : (i <= 7 ? CFG.difSpeed * 0.95 : CFG.difSpeed));
        if (d > 4) updatePlayer(p, dx/d, dy/d, baseSpeed * 1.8 * speedMult);
        else { p.vx *= 0.9; p.vy *= 0.9; }
    }
}

function findBallOwner() {
    let owner = null, minDist = 999;
    const all = [...you.players, ...rival.players];
    for (const p of all) {
        if (p.x < 0) continue;
        const d = dist(p, ball);
        if (d < minDist && d < PR + BR + 8) { minDist = d; owner = p; }
    }
    return owner;
}

function updateBall() {
    if (gameState !== "play") return;
    const owner = findBallOwner();
    if (owner) {
        const angle = owner.facing === 'right' ? 0 : owner.facing === 'left' ? Math.PI : owner.facing === 'down' ? Math.PI/2 : -Math.PI/2;
        const offset = PR + 6;
        const targetX = owner.x + Math.cos(angle) * offset;
        const targetY = owner.y + Math.sin(angle) * offset;
        ball.x += (targetX - ball.x) * 0.4;
        ball.y += (targetY - ball.y) * 0.4;
        ball.vx *= 0.6; ball.vy *= 0.6;
        return;
    }
    ball.x += ball.vx; ball.y += ball.vy;
    ball.vx *= 0.96; ball.vy *= 0.96;
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
    const gTop = FIELD.h/2 - 100, gBot = FIELD.h/2 + 100;
    if (ball.x + BR > FIELD.w && ball.y > gTop && ball.y < gBot) {
        const force = Math.min(1, Math.hypot(ball.vx, ball.vy) / 15);
        kickNet('right', force);
        score.you++; flashMessage("¡GOL!"); playGoal();
        you.players[controlledIndex].state = 'celebrate';
        you.players[controlledIndex].stateTimer = 100;
        setTimeout(() => resetPositions(), 200);
    }
    if (ball.x - BR < 0 && ball.y > gTop && ball.y < gBot) {
        const force = Math.min(1, Math.hypot(ball.vx, ball.vy) / 15);
        kickNet('left', force);
        score.rival++; flashMessage("Gol rival"); playGoal();
        setTimeout(() => resetPositions(), 200);
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

function getSpriteKey(p) {
    if (p.state === 'celebrate') return 'celebrate';
    if (p.state === 'tackle') return 'tackle';
    if (p.state === 'fallen') return 'fallen';
    if (p.state === 'shoot') return 'shoot';
    const speed = Math.hypot(p.vx, p.vy);
    const moving = speed > 0.3;
    const dir = p.facing;
    if (moving) {
        const frame = (Math.floor(animTimer / 5) % 2 === 0) ? 'run1' : 'run2';
        const key = `${frame}_${dir}`;
        return SPRITES[key] ? key : `idle_${dir}`;
    }
    return `idle_${dir}`;
}

function drawAll() {
    updateCamera();
    ctx.fillStyle = '#05070b';
    ctx.fillRect(0, 0, W, H);
    drawCrowd();
    drawField();
    
    const all = [...rival.players, ...you.players].filter(p => p.x >= 0);
    all.sort((a, b) => a.y - b.y);
    
    for (const p of all) {
        const scr = toScreen(p.x, p.y);
        const spriteKey = getSpriteKey(p);
        const sprite = SPRITES[spriteKey] || SPRITES.idle_down;
        const depthScale = 0.75 + (p.y / FIELD.h) * 0.35;
        const pxSize = 1.15 * depthScale;
        const isYou = you.players.indexOf(p) !== -1;
        const c1 = isYou ? CFG.colorJug : CFG.colorRiv;
        const c2 = isYou ? CFG.colorJug2 : CFG.colorRiv2;
        const flipX = (p.facing === 'left');
        drawPixelSprite(sprite, scr.sx, scr.sy, pxSize, c1, c2, p.num, p.isControlled, flipX);
        
        ctx.font = 'bold 10px Courier New';
        ctx.strokeStyle = 'rgba(0,0,0,0.9)';
        ctx.lineWidth = 3;
        ctx.textAlign = 'center';
        const nameY = scr.sy - sprite.length * pxSize - 2;
        ctx.strokeText(p.name, scr.sx, nameY);
        ctx.fillStyle = p.isControlled ? '#00ffc8' : '#ffffff';
        ctx.fillText(p.name, scr.sx, nameY);
        ctx.textAlign = 'left';
    }
    
    const bp = toScreen(ball.x, ball.y);
    drawBall({ x: bp.sx, y: bp.sy, vx: ball.vx, vy: ball.vy }, 12);
    drawSkillParticles();
    drawScoreboard(score, matchTime);
    
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
    
    const all = [...you.players, ...rival.players];
    for (const p of all) {
        if (p.stateTimer > 0) p.stateTimer--;
        if (p.stateTimer === 0 && p.state !== 'idle') p.state = 'idle';
        if (p.tackleCooldown > 0) p.tackleCooldown--;
    }
    
    if (gameState === "play") {
        const ownerCheck = findBallOwner();
        if (ownerCheck && ownerCheck.side === 'rival' && animTimer % 30 === 0) autoSwitchToNearestToBall();
        
        if (animTimer % 18 === 0) checkOffside();
        
        updateControlled();
        updateRival();
        updateBall();
        rivalTackleCheck();
        updateNets();
        updateSkillParticles();
        
        const owner = findBallOwner();
        const theyAttack = owner && owner.side === 'rival';
        const weAttack2 = owner && owner.side === 'you';
        
        for (let i = 0; i < you.players.length; i++) {
            if (i === controlledIndex) continue;
            if (i === 0) continue;
            const mate = you.players[i];
            if (mate.x < 0) continue;
            if (mate.state === 'fallen' || mate.state === 'tackle') continue;
            let target, speedMult = 1.0;
            if (theyAttack) {
                const dToBall = dist(mate, ball);
                if (i <= 4) {
                    if (dToBall < 300) { target = { x: ball.x + 80, y: ball.y }; speedMult = 1.0; }
                    else { target = { x: FIELD.w * 0.28 + (i - 2) * 60, y: mate.homeY }; speedMult = 0.9; }
                } else if (i <= 7) {
                    if (dToBall < 350) { target = { x: ball.x, y: ball.y }; speedMult = 1.0; }
                    else { target = { x: ball.x - 150, y: mate.homeY }; speedMult = 0.85; }
                } else {
                    if (dToBall < 400) { target = { x: ball.x, y: ball.y }; speedMult = 0.95; }
                    else { target = { x: FIELD.w * 0.35, y: mate.homeY }; speedMult = 0.75; }
                }
            } else if (weAttack2) {
                if (i <= 4) { target = { x: mate.homeX + 100, y: mate.homeY }; speedMult = 0.85; }
                else if (i <= 7) { target = { x: ball.x + 100 + (i - 6) * 60, y: ball.y + (i % 2 === 0 ? 130 : -130) }; speedMult = 0.95; }
                else { target = { x: Math.min(FIELD.w - 150, ball.x + 250), y: FIELD.h/2 + (i - 9) * 130 }; speedMult = 1.0; }
            } else {
                target = { x: mate.homeX, y: mate.homeY };
                speedMult = 0.9;
            }
            const dx = target.x - mate.x;
            const dy = target.y - mate.y;
            const d = Math.hypot(dx, dy) || 1;
            if (d > 10) updatePlayer(mate, dx/d, dy/d, 5.0 * speedMult);
            else { mate.vx *= 0.9; mate.vy *= 0.9; }
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
