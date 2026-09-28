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
    "Fácil":   {"speed": 2.4},
    "Normal":  {"speed": 2.8},
    "Difícil": {"speed": 3.2},
    "Leyenda": {"speed": 3.6},
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
        "difSpeed": d["speed"],
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
#debug { position:absolute; top:8px; right:8px; color:#00ffc8; font-size:10px;
         background:rgba(0,0,0,0.6); padding:4px 8px; border-radius:6px;
         pointer-events:none; z-index:20; }
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
    <div id="debug">--</div>
</div>
<script>
const CFG = __DATA__;
const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const W = canvas.width, H = canvas.height;

const ISO = {
    fieldW: 2000, fieldH: 1200,
    camX: 1000, camY: 600,
    targetCamX: 1000, targetCamY: 600,
    scale: 1.6,
    tiltY: 0.55,
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
    ISO.targetCamX = ball.x;
    ISO.targetCamY = ball.y;
    ISO.camX += (ISO.targetCamX - ISO.camX) * 0.08;
    ISO.camY += (ISO.targetCamY - ISO.camY) * 0.08;
}

const CESPEDES = {
    "Clásico": { dark:"#3d8a2b", light:"#4a9e35", line:"#ffffff" },
    "Mojado":  { dark:"#2e6b20", light:"#3a7d28", line:"#e8e8e8" },
    "Seco":    { dark:"#7a8a3a", light:"#8a9a4a", line:"#f0e8c0" },
    "Nieve":   { dark:"#d8e0e8", light:"#eef2f6", line:"#4a5a6a" },
};

const SPRITES = {
    idle_down: [
        "........HHHHHHHH........",".......HHHHHHHHHH.......",
        "......HHHHHHHHHHHH......","......HHssssssssHH......",
        "......HssSSSSSSssH......","......HsS@SSSS@SsH......",
        "......HsSSSSSSSSsH......",".......SSSSSSSSSS.......",
        ".......SSS/SS/SSS.......","........SSSSSSSS........",
        "........SSSSSSSS........",".......JJJJJJJJJJ.......",
        "......JJccJJJJccJJ......",".....JJJJcNNNNcJJJJ.....",
        ".....JJJJcNNNNcJJJJ.....","....JJJJJcNNNNcJJJJJ....",
        "....JJJJJcNNNNcJJJJJ....","...KJJJJJJJJJJJJJJJJK...",
        "...KJJJJJJJJJJJJJJJJK...","...KJJJJJJJJJJJJJJJJK...",
        "....JJJJJJJJJJJJJJJJ....","....JJJJJJJJJJJJJJJJ....",
        ".....JJJJJJJJJJJJJJ.....",".....PPPPPPPPPPPPPP.....",
        ".....PPPPPPPPPPPPPP.....",".....PPPPPPPPPPPPPP.....",
        ".....PPPPPPPPPPPPPP.....",".....PPPP..PPPPPP.......",
        ".....PPPP..PPPPPP.......",".....BBBB..BBBBBB.......",
        ".....BBBB..BBBBBB.......","........................",
    ],
    run1_down: [
        "........HHHHHHHH........",".......HHHHHHHHHH.......",
        "......HHHHHHHHHHHH......","......HHssssssssHH......",
        "......HssSSSSSSssH......","......HsS@SSSS@SsH......",
        "......HsSSSSSSSSsH......",".......SSSSSSSSSS.......",
        ".......SSS/SS/SSS.......","........SSSSSSSS........",
        "........SSSSSSSS........",".......JJJJJJJJJJ.......",
        "......JJccJJJJccJJ......",".....JJJJcNNNNcJJJJ.....",
        ".....JJJJcNNNNcJJJJ.....","....JJJJJcNNNNcJJJJJ....",
        "...KJJJJJcNNNNcJJJJJK...","...KJJJJJJJJJJJJJJJJK...",
        "....JJJJJJJJJJJJJJJJ....","....JJJJJJJJJJJJJJJJ....",
        ".....JJJJJJJJJJJJJJ.....",".....PPPPPPPPPPPPPP.....",
        ".....PPPPPPPPPPPPPP.....",".....PPPPPPPPPPPPP......",
        "....PPPPPP...PPPPP......","....PPPP......PPPP......",
        "....BBB.......PPPP......","....BBB.......BBBB......",
        "..............BBBB......","..............BBB.......",
        "........................","........................",
    ],
    run2_down: [
        "........HHHHHHHH........",".......HHHHHHHHHH.......",
        "......HHHHHHHHHHHH......","......HHssssssssHH......",
        "......HssSSSSSSssH......","......HsS@SSSS@SsH......",
        "......HsSSSSSSSSsH......",".......SSSSSSSSSS.......",
        ".......SSS/SS/SSS.......","........SSSSSSSS........",
        "........SSSSSSSS........",".......JJJJJJJJJJ.......",
        "......JJccJJJJccJJ......",".....JJJJcNNNNcJJJJ.....",
        ".....JJJJcNNNNcJJJJ.....","....JJJJJcNNNNcJJJJJ....",
        "...KJJJJJcNNNNcJJJJJK...","...KJJJJJJJJJJJJJJJJK...",
        "....JJJJJJJJJJJJJJJJ....","....JJJJJJJJJJJJJJJJ....",
        ".....JJJJJJJJJJJJJJ.....",".....PPPPPPPPPPPPPP.....",
        ".....PPPPPPPPPPPPPP.....","......PPPPPPPPPPPPP.....",
        "......PPPPP...PPPPPP....","......PPPP......PPPP....",
        "......PPPP.......BBB....","......BBBB.......BBB....",
        "......BBBB..............",".......BBB..............",
        "........................","........................",
    ],
    idle_up: [
        "........HHHHHHHH........",".......HHHHHHHHHH.......",
        "......HHHHHHHHHHHH......","......HHHHHHHHHHHH......",
        "......HHHHHHHHHHHH......","......HHHHHHHHHHHH......",
        "......HHHHHHHHHHHH......","......HHHHHHHHHHHH......",
        ".......HHHHHHHHHH.......","........ssssssss........",
        "........SSSSSSSS........",".......JJJJJJJJJJ.......",
        "......JJccJJJJccJJ......",".....JJJJcNNNNcJJJJ.....",
        ".....JJJJcNNNNcJJJJ.....","....JJJJJcNNNNcJJJJJ....",
        "....JJJJJcNNNNcJJJJJ....","...KJJJJJJJJJJJJJJJJK...",
        "...KJJJJJJJJJJJJJJJJK...","...KJJJJJJJJJJJJJJJJK...",
        "....JJJJJJJJJJJJJJJJ....","....JJJJJJJJJJJJJJJJ....",
        ".....JJJJJJJJJJJJJJ.....",".....PPPPPPPPPPPPPP.....",
        ".....PPPPPPPPPPPPPP.....",".....PPPPPPPPPPPPPP.....",
        ".....PPPPPPPPPPPPPP.....",".....PPPP..PPPPPP.......",
        ".....PPPP..PPPPPP.......",".....BBBB..BBBBBB.......",
        ".....BBBB..BBBBBB.......","........................",
    ],
    run1_up: [
        "........HHHHHHHH........",".......HHHHHHHHHH.......",
        "......HHHHHHHHHHHH......","......HHHHHHHHHHHH......",
        "......HHHHHHHHHHHH......","......HHHHHHHHHHHH......",
        "......HHHHHHHHHHHH......","......HHHHHHHHHHHH......",
        ".......HHHHHHHHHH.......","........ssssssss........",
        "........SSSSSSSS........",".......JJJJJJJJJJ.......",
        "......JJccJJJJccJJ......",".....JJJJcNNNNcJJJJ.....",
        ".....JJJJcNNNNcJJJJ.....","....JJJJJcNNNNcJJJJJ....",
        "...KJJJJJcNNNNcJJJJJK...","...KJJJJJJJJJJJJJJJJK...",
        "....JJJJJJJJJJJJJJJJ....","....JJJJJJJJJJJJJJJJ....",
        ".....JJJJJJJJJJJJJJ.....",".....PPPPPPPPPPPPPP.....",
        ".....PPPPPPPPPPPPPP.....",".....PPPPPPPPPPPPP......",
        "....PPPPPP...PPPPP......","....PPPP......PPPP......",
        "....BBB.......PPPP......","....BBB.......BBBB......",
        "..............BBBB......","..............BBB.......",
        "........................","........................",
    ],
    run2_up: [
        "........HHHHHHHH........",".......HHHHHHHHHH.......",
        "......HHHHHHHHHHHH......","......HHHHHHHHHHHH......",
        "......HHHHHHHHHHHH......","......HHHHHHHHHHHH......",
        "......HHHHHHHHHHHH......","......HHHHHHHHHHHH......",
        ".......HHHHHHHHHH.......","........ssssssss........",
        "........SSSSSSSS........",".......JJJJJJJJJJ.......",
        "......JJccJJJJccJJ......",".....JJJJcNNNNcJJJJ.....",
        ".....JJJJcNNNNcJJJJ.....","....JJJJJcNNNNcJJJJJ....",
        "...KJJJJJcNNNNcJJJJJK...","...KJJJJJJJJJJJJJJJJK...",
        "....JJJJJJJJJJJJJJJJ....","....JJJJJJJJJJJJJJJJ....",
        ".....JJJJJJJJJJJJJJ.....",".....PPPPPPPPPPPPPP.....",
        ".....PPPPPPPPPPPPPP.....","......PPPPPPPPPPPPP.....",
        "......PPPPP...PPPPPP....","......PPPP......PPPP....",
        "......PPPP.......BBB....","......BBBB.......BBB....",
        "......BBBB..............",".......BBB..............",
        "........................","........................",
    ],
    idle_right: [
        "........HHHHHHHH........",".......HHHHHHHHHH.......",
        ".......HHHHHHHHHH.......","......HHHHHHHHHHH.......",
        "......HHHssssssHH.......","......HHsSSSSSsH........",
        "......HHsS@SSSss........","......HHsSSSSSs.........",
        ".......HSsssssS.........",".......SSS/SSS..........",
        "........SSSSSS..........","........SSSSSS..........",
        ".......JJJJJJJJ.........","......JJJJJJJJJJ........",
        ".....JJJJcNNNcJJJ.......","....JJJJJcNNNcJJJJ......",
        "....JJJJJcNNNcJJJJ......","...KJJJJJcNNNcJJJJK.....",
        "...KJJJJJJJJJJJJJJK.....","....JJJJJJJJJJJJJJ......",
        "....JJJJJJJJJJJJJJ......",".....JJJJJJJJJJJJ.......",
        ".....PPPPPPPPPPP........",".....PPPPPPPPPPP........",
        ".....PPPPPPPPPPP........",".....PPPPPPPPPPP........",
        ".....PPPP.PPPPPP........",".....PPPP.PPPPPP........",
        ".....BBBB.BBBBBB........",".....BBBB.BBBBBB........",
        "........................","........................",
    ],
    run1_right: [
        "........HHHHHHHH........",".......HHHHHHHHHH.......",
        ".......HHHHHHHHHH.......","......HHHHHHHHHHH.......",
        "......HHHssssssHH.......","......HHsSSSSSsH........",
        "......HHsS@SSSss........","......HHsSSSSSs.........",
        ".......HSsssssS.........",".......SSS/SSS..........",
        "........SSSSSS..........","........SSSSSS..........",
        ".......JJJJJJJJ.........","......JJJJJJJJJJ........",
        ".....JJJJcNNNcJJJ.......","....JJJJJcNNNcJJJJ......",
        "....JJJJJcNNNcJJJJ......","...KJJJJJcNNNcJJJJK.....",
        "...KJJJJJJJJJJJJJJK.....","....JJJJJJJJJJJJJJ......",
        ".....JJJJJJJJJJJJ.......",".....PPPPPPPPPPP........",
        ".....PPPPPPPPPPP........",".....PPPPPPPPPPP........",
        "....PPPPPP..PPP.........","....PPPP.....PP.........",
        "....BBB......PPP........","....BBB......BBBB.......",
        ".............BBBB.......",".............BBB........",
        "........................","........................",
    ],
    run2_right: [
        "........HHHHHHHH........",".......HHHHHHHHHH.......",
        ".......HHHHHHHHHH.......","......HHHHHHHHHHH.......",
        "......HHHssssssHH.......","......HHsSSSSSsH........",
        "......HHsS@SSSss........","......HHsSSSSSs.........",
        ".......HSsssssS.........",".......SSS/SSS..........",
        "........SSSSSS..........","........SSSSSS..........",
        ".......JJJJJJJJ.........","......JJJJJJJJJJ........",
        ".....JJJJcNNNcJJJ.......","....JJJJJcNNNcJJJJ......",
        "....JJJJJcNNNcJJJJ......","...KJJJJJcNNNcJJJJK.....",
        "...KJJJJJJJJJJJJJJK.....","....JJJJJJJJJJJJJJ......",
        ".....JJJJJJJJJJJJ.......",".....PPPPPPPPPPP........",
        ".....PPPPPPPPPPP........","......PPPPPPPPPP........",
        "......PPPPP.PPPP........","......PPPP...PPP........",
        "......PPPP...BBB........","......BBBB...BBB........",
        "......BBBB..............",".......BBB..............",
        "........................","........................",
    ],
    shoot: [
        "........HHHHHHHH........",".......HHHHHHHHHH.......",
        "......HHHHHHHHHHHH......","......HHssssssssHH......",
        "......HssSSSSSSssH......","......HsS@SSSS@SsH......",
        "......HsSSSSSSSSsH......",".......SSSSSSSSSS.......",
        ".......SSS/SS/SSS.......","........SSSSSSSS........",
        "........SSSSSSSS........",".......JJJJJJJJJJ.......",
        "......JJccJJJJccJJ......",".....JJJJcNNNNcJJJJ.....",
        ".....JJJJcNNNNcJJJJ.....","....JJJJJcNNNNcJJJJJ....",
        "....JJJJJcNNNNcJJJJJ....","...KJJJJJJJJJJJJJJJJK...",
        "...KJJJJJJJJJJJJJJJJK...","...KJJJJJJJJJJJJJJJJK...",
        "....JJJJJJJJJJJJJJJJ....","....JJJJJJJJJJJJJJJJ....",
        ".....JJJJJJJJJJJJJJ.....",".....PPPPPPPPPPPPPP.....",
        ".....PPPPPPPPPPPPPP.....",".....PPPPPPPPPPPPPP.....",
        ".....PPPPPPPPPPPPPP.....",".....PPPP..PPPPPP.......",
        ".....PPPP..PPPPPP.......",".....BBBB..BBBBBB.......",
        ".....BBBB..BBBBBB.......","........................",
    ],
    celebrate: [
        "..SS....HHHHHHHH....SS..","..SS...HHHHHHHHHH...SS..",
        "..SS...HHHHHHHHHH...SS..","..SS...HHHHHHHHHH...SS..",
        "..SS...HHssssssssHH.SS..","..SS...HssSSSSSSssH.SS..",
        "..SS...HsS@SSSS@SsH.SS..","..SS...HsSSSSSSSSsH.SS..",
        "..SS....SSSSSSSSSS..SS..","..SS....SSS/SS/SSS..SS..",
        "...S....SSSSSSSS....S...","........SSSSSSSS........",
        ".......JJJJJJJJJJ.......","......JJccJJJJccJJ......",
        ".....JJJJcNNNNcJJJJ.....",".....JJJJcNNNNcJJJJ.....",
        "....JJJJJcNNNNcJJJJJ....","....JJJJJcNNNNcJJJJJ....",
        "...KJJJJJJJJJJJJJJJJK...","...KJJJJJJJJJJJJJJJJK...",
        "...KJJJJJJJJJJJJJJJJK...","....JJJJJJJJJJJJJJJJ....",
        "....JJJJJJJJJJJJJJJJ....",".....JJJJJJJJJJJJJJ.....",
        ".....PPPPPPPPPPPPPP.....",".....PPPPPPPPPPPPPP.....",
        ".....PPPPPPPPPPPPPP.....",".....PPPPPPPPPPPPPP.....",
        ".....PPPP..PPPPPP.......",".....PPPP..PPPPPP.......",
        ".....BBBB..BBBBBB.......",".....BBBB..BBBBBB.......",
    ],
    fallen: [
        "........................","........................",
        "........................","........................",
        "........................","........................",
        "........................","................HHHHHHHH",
        "...............HHHHHHHHH","..............HHHHHHHHHH",
        "..............HHsssssssH","..............HssSSSSssH",
        "..............HsS@SS@SsH","...............SSSSSSSS.",
        "...............SSS/SS/SS","................SSSSSSSS",
        "......JJJJJJJJJJJJJJJJJ.",".....JJJJccJJJJccJJJJJJ.",
        "....JJJJcNNNNNNNNcJJJJJ.","...JJJJJcNNNNNNNNcJJJJJ.",
        "..JJJJJJcNNNNNNNNcJJJJJ.","..KJJJJJJJJJJJJJJJJJJJJ.",
        "..KJJJJJJJJJJJJJJJJJJJJ.","...JJJJJJJJJJJJJJJJJJJJ.",
        "....JJJJJJJJJJJJJJJJJJ..","....PPPPPPPPPPPPPPPPP...",
        "...PPPPPPPPPPPPPPPPPPP..",".BBBB...............BBB.",
        ".BBBB...............BBB.","........................",
        "........................","........................",
        "........................",
    ],
};

function drawPixelSprite(sprite, x, y, pixelSize, color1, color2, dorsal, isControlled, flipX) {
    const h = sprite.length;
    const w = sprite[0].length;
    const offsetX = -w * pixelSize / 2;
    const offsetY = -h * pixelSize;
    
    ctx.fillStyle = 'rgba(0,0,0,0.4)';
    ctx.beginPath();
    ctx.ellipse(x, y + 4, w * pixelSize * 0.4, h * pixelSize * 0.1, 0, 0, Math.PI * 2);
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
    
    ctx.font = `bold ${Math.round(pixelSize * 4)}px Courier New`;
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.strokeStyle = 'rgba(0,0,0,0.9)';
    ctx.lineWidth = 3;
    ctx.fillStyle = '#ffffff';
    const dorsalY = y - h * pixelSize * 0.5;
    ctx.strokeText(dorsal, x, dorsalY);
    ctx.fillText(dorsal, x, dorsalY);
    
    if (isControlled) {
        const arrowY = y - h * pixelSize - 14;
        const bounce = Math.sin(animTimer * 0.15) * 2;
        ctx.fillStyle = '#00ffc8';
        ctx.beginPath();
        ctx.moveTo(x - 6, arrowY + bounce);
        ctx.lineTo(x + 6, arrowY + bounce);
        ctx.lineTo(x, arrowY + 10 + bounce);
        ctx.closePath();
        ctx.fill();
        ctx.strokeStyle = '#00ffc8';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.ellipse(x, y + 2, w * pixelSize * 0.5, h * pixelSize * 0.1, 0, 0, Math.PI * 2);
        ctx.stroke();
    }
    ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
}

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

function drawCrowd() {
    ctx.fillStyle = '#0a1a0a';
    ctx.fillRect(0, 0, W, H);
    
    const tl = toScreen(0, 0);
    const tr = toScreen(ISO.fieldW, 0);
    const bl = toScreen(0, ISO.fieldH);
    const br = toScreen(ISO.fieldW, ISO.fieldH);
    
    const colores = ['#e8b890', '#c84040', '#4060c8', '#f0d040', '#40a040', '#e060a0'];
    const bandaGrosor = 90;
    
    // Superior
    const topDirX = tr.sx - tl.sx, topDirY = tr.sy - tl.sy;
    const topLen = Math.hypot(topDirX, topDirY);
    const topPerpX = -topDirY / topLen, topPerpY = topDirX / topLen;
    for (let fila = 0; fila < 12; fila++) {
        const t = (fila + 1) / 13;
        for (let i = 0; i < 50; i++) {
            const s = i / 49;
            const bx = tl.sx + topDirX * s, by = tl.sy + topDirY * s;
            const px = bx + topPerpX * bandaGrosor * t;
            const py = by + topPerpY * bandaGrosor * t;
            const idx = (fila + i * 3) % colores.length;
            ctx.fillStyle = colores[idx];
            ctx.fillRect(px, py, 4, 4);
            ctx.fillStyle = '#e8b890';
            ctx.fillRect(px + 1, py - 1, 2, 2);
        }
    }
    
    // Inferior
    const botDirX = br.sx - bl.sx, botDirY = br.sy - bl.sy;
    const botLen = Math.hypot(botDirX, botDirY);
    const botPerpX = botDirY / botLen, botPerpY = -botDirX / botLen;
    for (let fila = 0; fila < 12; fila++) {
        const t = (fila + 1) / 13;
        for (let i = 0; i < 50; i++) {
            const s = i / 49;
            const bx = bl.sx + botDirX * s, by = bl.sy + botDirY * s;
            const px = bx + botPerpX * bandaGrosor * t;
            const py = by + botPerpY * bandaGrosor * t;
            const idx = (fila + i * 5) % colores.length;
            ctx.fillStyle = colores[idx];
            ctx.fillRect(px, py, 4, 4);
            ctx.fillStyle = '#e8b890';
            ctx.fillRect(px + 1, py - 1, 2, 2);
        }
    }
    
    // Izquierda
    const leftDirX = bl.sx - tl.sx, leftDirY = bl.sy - tl.sy;
    const leftLen = Math.hypot(leftDirX, leftDirY);
    const leftPerpX = -leftDirY / leftLen, leftPerpY = leftDirX / leftLen;
    for (let fila = 0; fila < 12; fila++) {
        const t = (fila + 1) / 13;
        for (let i = 0; i < 30; i++) {
            const s = i / 29;
            const bx = tl.sx + leftDirX * s, by = tl.sy + leftDirY * s;
            const px = bx + leftPerpX * bandaGrosor * t;
            const py = by + leftPerpY * bandaGrosor * t;
            const idx = (fila + i * 7) % colores.length;
            ctx.fillStyle = colores[idx];
            ctx.fillRect(px, py, 4, 4);
            ctx.fillStyle = '#e8b890';
            ctx.fillRect(px + 1, py - 1, 2, 2);
        }
    }
    
    // Derecha
    const rightDirX = br.sx - tr.sx, rightDirY = br.sy - tr.sy;
    const rightLen = Math.hypot(rightDirX, rightDirY);
    const rightPerpX = rightDirY / rightLen, rightPerpY = -rightDirX / rightLen;
    for (let fila = 0; fila < 12; fila++) {
        const t = (fila + 1) / 13;
        for (let i = 0; i < 30; i++) {
            const s = i / 29;
            const bx = tr.sx + rightDirX * s, by = tr.sy + rightDirY * s;
            const px = bx + rightPerpX * bandaGrosor * t;
            const py = by + rightPerpY * bandaGrosor * t;
            const idx = (fila + i * 9) % colores.length;
            ctx.fillStyle = colores[idx];
            ctx.fillRect(px, py, 4, 4);
            ctx.fillStyle = '#e8b890';
            ctx.fillRect(px + 1, py - 1, 2, 2);
        }
    }
    
    // Carteles
    ctx.strokeStyle = '#00d4a8';
    ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.moveTo(tl.sx + topPerpX * 12, tl.sy + topPerpY * 12);
    ctx.lineTo(tr.sx + topPerpX * 12, tr.sy + topPerpY * 12);
    ctx.stroke();
    
    ctx.fillStyle = '#00d4a8';
    ctx.font = 'bold 11px Courier New';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    const textos = ['· FIFA TOTAL ·', '· RETRO LIGA ·', '· SOUNDSNIP ·', '· FIFA 96 ·', '· LIGA PRO ·'];
    for (let i = 0; i < 8; i++) {
        const s = (i + 0.5) / 8;
        const bx = tl.sx + topDirX * s + topPerpX * 6;
        const by = tl.sy + topDirY * s + topPerpY * 6;
        ctx.fillText(textos[i % textos.length], bx, by);
    }
    
    ctx.strokeStyle = '#ff9f43';
    ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.moveTo(bl.sx + botPerpX * 12, bl.sy + botPerpY * 12);
    ctx.lineTo(br.sx + botPerpX * 12, br.sy + botPerpY * 12);
    ctx.stroke();
    
    ctx.fillStyle = '#ff9f43';
    for (let i = 0; i < 8; i++) {
        const s = (i + 0.5) / 8;
        const bx = bl.sx + botDirX * s + botPerpX * 6;
        const by = bl.sy + botDirY * s + botPerpY * 6;
        ctx.fillText('· FIFA TOTAL ·', bx, by);
    }
    
    ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
}

function drawGoal(goalX, side, c) {
    const GOAL_H = 100, GOAL_DEPTH = 45;
    const dir = side === 'left' ? -1 : 1;
    
    const frontTop = toScreen(goalX, ISO.centerY - GOAL_H);
    const frontBot = toScreen(goalX, ISO.centerY + GOAL_H);
    const backTop = toScreen(goalX + dir * GOAL_DEPTH, ISO.centerY - GOAL_H);
    const backBot = toScreen(goalX + dir * GOAL_DEPTH, ISO.centerY + GOAL_H);
    
    ctx.fillStyle = 'rgba(0,0,0,0.55)';
    ctx.beginPath();
    ctx.moveTo(frontTop.sx, frontTop.sy);
    ctx.lineTo(frontBot.sx, frontBot.sy);
    ctx.lineTo(backBot.sx, backBot.sy);
    ctx.lineTo(backTop.sx, backTop.sy);
    ctx.closePath();
    ctx.fill();
    
    ctx.strokeStyle = 'rgba(255,255,255,0.65)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 8; i++) {
        const t = i / 8;
        const x1 = frontTop.sx + (frontBot.sx - frontTop.sx) * t;
        const y1 = frontTop.sy + (frontBot.sy - frontTop.sy) * t;
        const x2 = backTop.sx + (backBot.sx - backTop.sx) * t;
        const y2 = backTop.sy + (backBot.sy - backTop.sy) * t;
        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    }
    for (let i = 0; i <= 10; i++) {
        const t = i / 10;
        const x1 = frontTop.sx + (backTop.sx - frontTop.sx) * t;
        const y1 = frontTop.sy + (backTop.sy - frontTop.sy) * t;
        const x2 = frontBot.sx + (backBot.sx - frontBot.sx) * t;
        const y2 = frontBot.sy + (backBot.sy - frontBot.sy) * t;
        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    }
    
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(frontTop.sx, frontTop.sy); ctx.lineTo(backTop.sx, backTop.sy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(frontBot.sx, frontBot.sy); ctx.lineTo(backBot.sx, backBot.sy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(backTop.sx, backTop.sy); ctx.lineTo(backBot.sx, backBot.sy); ctx.stroke();
    
    ctx.strokeStyle = 'rgba(255,255,255,0.5)';
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(frontTop.sx, frontTop.sy); ctx.lineTo(frontBot.sx, frontBot.sy); ctx.stroke();
    ctx.lineCap = 'butt';
}

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
    
    ctx.strokeStyle = c.line;
    ctx.lineWidth = 2;
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
    
    drawGoal(0, 'left', c);
    drawGoal(ISO.fieldW, 'right', c);
}

function drawScoreboard(score, time) {
    const x = 20, y = 20;
    ctx.fillStyle = 'rgba(0,0,0,0.85)';
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
        setControlledIndex(next);
        return;
    }
}
function autoSwitchToNearestToBall() {
    let best = controlledIndex, bestDist = Infinity;
    for (let i = 1; i < you.players.length; i++) {
        const p = you.players[i];
        if (p.x < 0) continue;
        const d = Math.hypot(p.x - ball.x, p.y - ball.y);
        if (d < bestDist) { bestDist = d; best = i; }
    }
    if (best !== controlledIndex) setControlledIndex(best);
}

function dist(a, b) { return Math.hypot(a.x - b.x, a.y - b.y); }
function clampToField(o, r) {
    o.x = Math.max(r, Math.min(FIELD.w - r, o.x));
    o.y = Math.max(r, Math.min(FIELD.h - r, o.y));
}

function movePlayer(p, dx, dy, baseSpeed) {
    if (p.state === 'fallen' || p.state === 'tackle') return;
    const boost = 0.7 + (p.vel / 100) * 0.6;
    const speed = baseSpeed * boost;
    const len = Math.hypot(dx, dy);
    if (len > 0) {
        p.vx = (dx / len) * speed;
        p.vy = (dy / len) * speed;
        if (Math.abs(dx) > Math.abs(dy) * 1.3) p.facing = dx > 0 ? 'right' : 'left';
        else if (Math.abs(dy) > Math.abs(dx) * 1.3) p.facing = dy > 0 ? 'down' : 'up';
        else p.facing = dx > 0 ? 'right' : 'left';
    } else {
        p.vx *= 0.85;
        p.vy *= 0.85;
    }
    p.x += p.vx;
    p.y += p.vy;
    clampToField(p, PR);
}

function showBigAlert(text, color) {
    const a = document.getElementById('bigAlert');
    a.textContent = text; a.style.color = color; a.style.opacity = '1';
    setTimeout(() => a.style.opacity = '0', 1200);
}

function attemptDribble() {
    const p = you.players[controlledIndex];
    if (!p) return;
    dribbleCooldown = 60;
    let nearest = null, nd = 999;
    for (const r of rival.players) {
        const d = dist(p, r);
        if (d < nd) { nd = d; nearest = r; }
    }
    if (!nearest || nd > 80) { p.vx *= 1.6; p.vy *= 1.6; showBigAlert("💨 SPRINT", "#00ffc8"); return; }
    const isGood = p.reg >= 80;
    const isElite = p.reg >= 88;
    let skillOptions = ['bicicleta'];
    if (isGood) { skillOptions.push('ruleta'); skillOptions.push('sombrero'); }
    if (isElite) skillOptions.push('cano'); skillOptions.push('elastica');
    const skill = skillOptions[Math.floor(Math.random() * skillOptions.length)];
    const baseProb = 0.5 + (p.reg - nearest.def) / 150 + (p.vel - nearest.vel) / 250;
    let prob = Math.max(0.15, Math.min(0.92, baseProb));
    const success = Math.random() < prob;
    if (success) {
        const angle = Math.atan2(ball.y - p.y, ball.x - p.x);
        const power = { 'bicicleta': 40, 'ruleta': 55, 'sombrero': 60, 'cano': 65, 'elastica': 80 }[skill] || 50;
        p.x += Math.cos(angle) * power;
        p.y += Math.sin(angle) * power;
        clampToField(p, PR);
        nearest.vx *= 0.4; nearest.vy *= 0.4;
        const info = {
            'bicicleta': { text: '¡BICICLETA!', color: '#00ffc8' },
            'ruleta':    { text: '¡RULETA!',    color: '#ffdd00' },
            'sombrero':  { text: '¡SOMBRERO!',  color: '#00b8ff' },
            'cano':      { text: '¡CAÑO!',      color: '#ff5c9f' },
            'elastica':  { text: '¡ELÁSTICA!',  color: '#ff9f43' },
        }[skill];
        showBigAlert(info.text, info.color);
    } else {
        p.vx *= 0.3; p.vy *= 0.3;
        showBigAlert("❌ PERDIDO", "#ff3b5c");
    }
}

function findBallOwner() {
    let owner = null, minDist = 999;
    const all = [...you.players, ...rival.players];
    for (const p of all) {
        const d = Math.hypot(p.x - ball.x, p.y - ball.y);
        if (d < minDist && d < PR + BR + 6) { minDist = d; owner = p; }
    }
    return owner;
}

function checkBounds() {
    let out = false;
    if (ball.y - BR < 0 || ball.y + BR > FIELD.h) {
        ball.y = ball.y < FIELD.h/2 ? BR + 5 : FIELD.h - BR - 5;
        ball.x = Math.max(50, Math.min(FIELD.w - 50, ball.x));
        ball.vx = 0; ball.vy = 0;
        out = true;
        showBigAlert("SAQUE DE BANDA", "#00d4a8");
        playWhistle();
    } else if (ball.x - BR < 0 || ball.x + BR > FIELD.w) {
        const gTop = FIELD.h/2 - 100, gBot = FIELD.h/2 + 100;
        if (ball.y > gTop && ball.y < gBot) {
            if (ball.x < FIELD.w/2) { score.rival++; showBigAlert("GOL RIVAL", "#ff3b5c"); }
            else { score.you++; showBigAlert("¡GOOOL!", "#00ffc8"); }
            playGoal();
            resetPositions();
        } else {
            ball.x = ball.x < FIELD.w/2 ? 100 : FIELD.w - 100;
            ball.y = FIELD.h/2;
            ball.vx = 0; ball.vy = 0;
            out = true;
            showBigAlert("SAQUE", "#ffdd00");
            playWhistle();
        }
    }
    if (out) { freezeTimer = 60; gameState = "pause"; }
}

function resetPositions() {
    ball.x = FIELD.w/2; ball.y = FIELD.h/2;
    ball.vx = 0; ball.vy = 0;
    you.players.forEach((p, i) => {
        p.x = CFG.formJug[i][0] * FIELD.w;
        p.y = CFG.formJug[i][1] * FIELD.h;
        p.state = 'idle'; p.stateTimer = 0;
        p.vx = 0; p.vy = 0;
    });
    rival.players.forEach((p, i) => {
        p.x = FIELD.w - CFG.formRiv[i][0] * FIELD.w;
        p.y = CFG.formRiv[i][1] * FIELD.h;
        p.state = 'idle'; p.stateTimer = 0;
        p.vx = 0; p.vy = 0;
    });
    gameState = "play"; freezeTimer = 0;
}

function updateControlled() {
    const p = you.players[controlledIndex];
    if (!p) return;
    let dx = 0, dy = 0;
    if (keys['up']) dy -= 1;
    if (keys['down']) dy += 1;
    if (keys['left']) dx -= 1;
    if (keys['right']) dx += 1;
    movePlayer(p, dx, dy, 4.5);
    
    if (keys['shoot'] && dist(p, ball) < PR + BR + 12) {
        const dirX = p.facing === 'right' ? 1 : p.facing === 'left' ? -1 : 0;
        const dirY = p.facing === 'down' ? 1 : p.facing === 'up' ? -1 : 0;
        const angle = (dirX === 0 && dirY === 0) 
            ? Math.atan2(FIELD.h/2 - ball.y, FIELD.w - ball.x) 
            : Math.atan2(dirY, dirX);
        ball.vx = Math.cos(angle) * 18;
        ball.vy = Math.sin(angle) * 18;
        keys['shoot'] = false;
        p.state = 'shoot'; p.stateTimer = 12;
        lastBallToucher = p;
        playKick();
    }
    
    if (keys['action'] && dist(p, ball) < PR + BR + 12) {
        let best = null, bestScore = -Infinity;
        for (let i = 0; i < you.players.length; i++) {
            if (i === controlledIndex) continue;
            const mate = you.players[i];
            const fwd = mate.x - p.x;
            if (fwd > 0 && fwd < 600) {
                const s = fwd - Math.abs(mate.y - p.y) * 0.5;
                if (s > bestScore) { bestScore = s; best = mate; }
            }
        }
        if (best) {
            const angle = Math.atan2(best.y - ball.y, best.x - ball.x);
            ball.vx = Math.cos(angle) * 12;
            ball.vy = Math.sin(angle) * 12;
            keys['action'] = false;
            p.state = 'shoot'; p.stateTimer = 10;
            lastBallToucher = p;
            playKick();
        }
    }
}

function updateRival() {
    for (let i = 0; i < rival.players.length; i++) {
        const p = rival.players[i];
        if (p.state === 'fallen' || p.state === 'tackle') continue;
        
        let target;
        if (i === 0) {
            target = { x: FIELD.w - 40, y: Math.max(FIELD.h/2 - 100, Math.min(FIELD.h/2 + 100, ball.y)) };
        } else if (i <= 4) {
            if (Math.abs(ball.x - p.x) < 400) target = { x: ball.x, y: ball.y };
            else target = { x: FIELD.w * 0.6, y: FIELD.h/2 + (i - 2.5) * 120 };
        } else if (i <= 7) {
            if (Math.abs(ball.x - p.x) < 500) target = { x: ball.x, y: ball.y };
            else target = { x: FIELD.w * 0.55, y: FIELD.h/2 + (i - 6) * 100 };
        } else {
            target = { x: ball.x + 100, y: ball.y };
        }
        
        const dx = target.x - p.x;
        const dy = target.y - p.y;
        const d = Math.hypot(dx, dy) || 1;
        const speed = i === 0 ? CFG.difSpeed * 0.5 : CFG.difSpeed;
        if (d > 4) movePlayer(p, dx/d, dy/d, speed);
        else { p.vx *= 0.85; p.vy *= 0.85; }
    }
}

function updateAllies() {
    const owner = findBallOwner();
    const weAttack = owner && owner.side === 'you';
    
    for (let i = 0; i < you.players.length; i++) {
        if (i === controlledIndex) continue;
        if (i === 0) continue;
        const p = you.players[i];
        if (p.state === 'fallen' || p.state === 'tackle') continue;
        
        let target;
        if (weAttack) {
            if (i <= 4) target = { x: p.homeX + 150, y: p.homeY };
            else if (i <= 7) target = { x: ball.x + 150, y: ball.y + (i % 2 === 0 ? 120 : -120) };
            else target = { x: Math.min(FIELD.w - 150, ball.x + 250), y: FIELD.h/2 + (i - 9) * 150 };
        } else {
            target = { x: p.homeX, y: p.homeY };
        }
        
        const dx = target.x - p.x;
        const dy = target.y - p.y;
        const d = Math.hypot(dx, dy) || 1;
        if (d > 10) movePlayer(p, dx/d, dy/d, 4.0);
        else { p.vx *= 0.85; p.vy *= 0.85; }
    }
}

function updateBall() {
    const owner = findBallOwner();
    if (owner) {
        const angle = owner.facing === 'right' ? 0 :
                      owner.facing === 'left' ? Math.PI :
                      owner.facing === 'down' ? Math.PI/2 : -Math.PI/2;
        const offset = PR + 5;
        const targetX = owner.x + Math.cos(angle) * offset;
        const targetY = owner.y + Math.sin(angle) * offset;
        ball.x += (targetX - ball.x) * 0.5;
        ball.y += (targetY - ball.y) * 0.5;
        ball.vx *= 0.5; ball.vy *= 0.5;
        lastBallToucher = owner;
        return;
    }
    
    ball.x += ball.vx;
    ball.y += ball.vy;
    ball.vx *= 0.96;
    ball.vy *= 0.96;
    
    const all = [...you.players, ...rival.players];
    for (const p of all) {
        if (p.state === 'fallen') continue;
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
    
    checkBounds();
}

function getSpriteKey(p) {
    if (p.state === 'celebrate') return 'celebrate';
    if (p.state === 'fallen') return 'fallen';
    if (p.state === 'shoot') return 'shoot';
    const speed = Math.hypot(p.vx, p.vy);
    const moving = speed > 0.3;
    const dir = p.facing;
    if (moving) {
        const frame = (Math.floor(animTimer / 5) % 2 === 0) ? 'run1' : 'run2';
        return `${frame}_${dir}`;
    }
    return `idle_${dir}`;
}

function drawAll() {
    ctx.fillStyle = '#05070b';
    ctx.fillRect(0, 0, W, H);
    
    drawCrowd();
    drawField();
    
    const all = [...rival.players, ...you.players];
    all.sort((a, b) => a.y - b.y);
    
    for (const p of all) {
        const scr = toScreen(p.x, p.y);
        const spriteKey = getSpriteKey(p);
        const sprite = SPRITES[spriteKey] || SPRITES.idle_down;
        const depthScale = 0.9 + (p.y / FIELD.h) * 0.2;
        const pxSize = 1.4 * depthScale;
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
    
    const all = [...you.players, ...rival.players];
    for (const p of all) {
        if (p.stateTimer > 0) p.stateTimer--;
        if (p.stateTimer === 0 && p.state !== 'idle') p.state = 'idle';
    }
    
    const dbg = document.getElementById('debug');
    if (dbg) dbg.textContent = `state:${gameState} freeze:${freezeTimer} t:${Math.floor(matchTime)}`;

    if (gameState === "play") {
        const ownerCheck = findBallOwner();
        if (ownerCheck && ownerCheck.side === 'rival' && animTimer % 30 === 0) autoSwitchToNearestToBall();
        
        updateCamera();
        updateControlled();
        updateAllies();
        updateRival();
        updateBall();
    } else if (gameState === "pause") {
        if (freezeTimer > 0) freezeTimer--;
        if (freezeTimer === 0) gameState = "play";
    }
    
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
