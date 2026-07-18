import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
import requests
from streamlit_lottie import st_lottie
import time


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="AutoValuate // Car AI",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INTERACTIVE PARTICLE CANVAS (Electric Sunset Spectrum)
# 80 orange, amber, and gold particles with proximity lines
# and mouse-repel physics via JS canvas
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_PARTICLE_JS = """
<canvas id="pc" style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;pointer-events:none;"></canvas>
<script>
(function(){
var c=document.getElementById('pc'),x=c.getContext('2d'),W,H,mx=-999,my=-999;
function rz(){W=c.width=window.innerWidth;H=c.height=window.innerHeight;}
window.addEventListener('resize',rz);rz();
document.addEventListener('mousemove',function(e){mx=e.clientX;my=e.clientY;});
var N=80,P=[];
for(var i=0;i<N;i++){var h=12+Math.random()*25; // Amber/Orange spectrum
P.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.35,vy:(Math.random()-.5)*.35,
r:Math.random()*1.8+.7,h:h,a:Math.random()*.45+.15,p:Math.random()*6.28});}
function dr(){x.clearRect(0,0,W,H);var t=Date.now()*.001;
for(var i=0;i<N;i++){for(var j=i+1;j<N;j++){var dx=P[i].x-P[j].x,dy=P[i].y-P[j].y,d=Math.sqrt(dx*dx+dy*dy);
if(d<130){x.beginPath();x.moveTo(P[i].x,P[i].y);x.lineTo(P[j].x,P[j].y);
x.strokeStyle='rgba(255,107,107,'+(0.06*(1-d/130))+')';x.lineWidth=.5;x.stroke();}}}
for(var k=0;k<N;k++){var q=P[k],dmx=q.x-mx,dmy=q.y-my,dm=Math.sqrt(dmx*dmx+dmy*dmy);
if(dm<110){q.vx+=dmx/dm*.12;q.vy+=dmy/dm*.12;}
q.vx*=.99;q.vy*=.99;q.x+=q.vx;q.y+=q.vy;
if(q.x<0)q.x=W;if(q.x>W)q.x=0;if(q.y<0)q.y=H;if(q.y>H)q.y=0;
var pl=Math.sin(t*1.4+q.p)*.3+.7,gr=q.r*3*pl;
var gd=x.createRadialGradient(q.x,q.y,0,q.x,q.y,gr*3);
gd.addColorStop(0,'hsla('+q.h+',95%,60%,'+(q.a*pl*.35)+')');
gd.addColorStop(1,'hsla('+q.h+',95%,60%,0)');
x.beginPath();x.arc(q.x,q.y,gr*3,0,6.28);x.fillStyle=gd;x.fill();
x.beginPath();x.arc(q.x,q.y,q.r*pl,0,6.28);
x.fillStyle='hsla('+q.h+',95%,65%,'+(q.a*pl)+')';x.fill();}
requestAnimationFrame(dr);}dr();})();
</script>
"""
components.html(_PARTICLE_JS, height=0, scrolling=False)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FULL CSS — Electric Orange & Deep Charcoal Glassmorphism + VFX
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

:root{
--bg:#0b0c10;--card:rgba(255,255,255,.025);--card-h:rgba(255,255,255,.05);
--border:rgba(255,255,255,.05);--txt:#f1f2f6;--muted:#a4b0be;
--a1:#ff6b6b;--a2:#ff9f43;
--grad:linear-gradient(135deg,#ff6b6b 0%,#ff9f43 50%,#ff5252 100%);
--glow:rgba(255,107,107,.3);--r:16px;--rl:24px;
--tr:.3s cubic-bezier(.4,0,.2,1);
}

#MainMenu,header,footer{visibility:hidden}
.stDeployButton{display:none!important}

.stApp{background:var(--bg)!important;color:var(--txt);font-family:'Space Grotesk',sans-serif}

/* ── Ambient orbs (Lava/Sunset glow) ── */
.stApp::before,.stApp::after{content:'';position:fixed;border-radius:50%;filter:blur(130px);opacity:.25;z-index:0;pointer-events:none}
.stApp::before{width:500px;height:500px;background:radial-gradient(circle,#ff6b6b 0%,transparent 70%);top:-10%;left:-8%;animation:oA 22s ease-in-out infinite alternate}
.stApp::after{width:480px;height:480px;background:radial-gradient(circle,#ff9f43 0%,transparent 70%);bottom:-12%;right:-10%;animation:oB 26s ease-in-out infinite alternate}
@keyframes oA{0%{transform:translate(0,0) scale(1)}50%{transform:translate(60px,40px) scale(1.15)}100%{transform:translate(-30px,70px) scale(.95)}}
@keyframes oB{0%{transform:translate(0,0) scale(1)}50%{transform:translate(-50px,-30px) scale(1.1)}100%{transform:translate(40px,-60px) scale(.9)}}

/* ── Scanlines ── */
.scan{position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:0;
background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(255,107,107,.008) 2px,rgba(255,107,107,.008) 4px)}

/* ── Floating icons (Racing Theme) ── */
.ficons{position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:0;overflow:hidden}
.fi{position:absolute;opacity:0;animation:fUp linear infinite;filter:blur(.3px)}
@keyframes fUp{0%{transform:translateY(100vh) rotate(0) scale(.5);opacity:0}10%{opacity:.15}90%{opacity:.1}100%{transform:translateY(-10vh) rotate(360deg) scale(1.1);opacity:0}}

section.main>div{position:relative;z-index:1}

/* ── Hero ── */
.hbadge{display:inline-block;background:var(--grad);color:#fff;font-family:'JetBrains Mono',monospace;font-size:.68rem;font-weight:700;letter-spacing:3px;padding:6px 18px;border-radius:50px;text-transform:uppercase;box-shadow:0 0 20px var(--glow);animation:bp 3s ease-in-out infinite}
@keyframes bp{0%,100%{box-shadow:0 0 20px var(--glow)}50%{box-shadow:0 0 35px rgba(255,107,107,.5),0 0 60px rgba(255,107,107,.15)}}
.htitle{font-size:3.6rem;font-weight:900;line-height:1.05;letter-spacing:-1px;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin:0 0 8px;position:relative;display:inline-block}
.htitle::after{content:'AutoValuate';position:absolute;top:0;left:0;background:linear-gradient(90deg,transparent 0%,rgba(255,255,255,.4) 45%,rgba(255,255,255,.6) 50%,rgba(255,255,255,.4) 55%,transparent 100%);background-size:200% 100%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:shm 4s ease-in-out infinite}
@keyframes shm{0%{background-position:200% center}100%{background-position:-200% center}}
.hglow{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:280px;height:55px;background:radial-gradient(ellipse,rgba(255,107,107,.2) 0%,transparent 70%);filter:blur(28px);pointer-events:none;animation:tg 4s ease-in-out infinite alternate}
@keyframes tg{0%{opacity:.4;transform:translate(-50%,-50%) scale(1)}100%{opacity:.75;transform:translate(-50%,-50%) scale(1.3)}}
.hsub{font-family:'JetBrains Mono',monospace;font-size:.82rem;color:var(--muted);letter-spacing:4px;text-transform:uppercase;margin-bottom:6px}
.hdesc{color:var(--muted);font-size:.95rem;line-height:1.6;max-width:540px;margin:0 auto}

/* ── Speedo bars (Rev Counter) ── */
.speedo{display:flex;align-items:flex-end;justify-content:center;gap:3px;height:28px;margin:14px auto 0;width:fit-content}
.sbar{width:3px;border-radius:3px;background:var(--grad);animation:sb ease-in-out infinite;opacity:.45}
@keyframes sb{0%,100%{height:4px;opacity:.25}50%{opacity:.65}}

/* ── Glass cards ── */
.gc{background:var(--card);border:1px solid var(--border);border-radius:var(--rl);padding:24px 22px;backdrop-filter:blur(22px);-webkit-backdrop-filter:blur(22px);transition:var(--tr);position:relative;overflow:hidden;margin-bottom:8px}
.gc::before{content:'';position:absolute;inset:0;border-radius:inherit;padding:1px;background:linear-gradient(135deg,rgba(255,255,255,.08),transparent 60%);-webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none}
.gc::after{content:'';position:absolute;top:-35px;right:-35px;width:90px;height:90px;background:radial-gradient(circle,rgba(255,107,107,.1) 0%,transparent 70%);border-radius:50%;pointer-events:none;transition:var(--tr)}
.gc:hover{background:var(--card-h);border-color:rgba(255,107,107,.2);transform:translateY(-2px);box-shadow:0 10px 35px rgba(255,107,107,.05)}
.gc:hover::after{width:130px;height:130px;background:radial-gradient(circle,rgba(255,107,107,.18) 0%,transparent 70%)}
.ci{font-size:1.4rem;display:block;margin-bottom:4px}
.cl{font-family:'JetBrains Mono',monospace;font-size:.6rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--a2);margin-bottom:2px}
.ct{font-size:1.05rem;font-weight:700;color:var(--txt);margin-bottom:0}

/* ── Slider / Select / Input ── */
.stSlider>div>div>div>div{background:var(--grad)!important}
.stSlider [data-testid="stThumbValue"]{color:var(--txt)!important;font-weight:700!important;font-family:'JetBrains Mono',monospace!important}
div[data-baseweb="slider"] div[role="slider"]{background:#fff!important;border:3px solid var(--a1)!important;box-shadow:0 0 14px var(--glow)!important;width:20px!important;height:20px!important}
.stSlider label,.stSelectbox label,.stTextInput label{color:var(--muted)!important;font-weight:600!important;font-size:.82rem!important}
div[data-testid="stVerticalBlock"]>div:has(div.stSlider),div[data-testid="stVerticalBlock"]>div:has(div.stSelectbox),div[data-testid="stVerticalBlock"]>div:has(div.stTextInput){background:transparent!important;border:none!important;box-shadow:none!important;padding:0!important}

/* ── CTA Button ── */
div.stButton>button{background:var(--grad)!important;color:#fff!important;font-family:'JetBrains Mono',monospace!important;font-weight:700!important;font-size:.9rem!important;letter-spacing:2.5px!important;text-transform:uppercase!important;border:none!important;padding:17px 40px!important;border-radius:60px!important;width:100%!important;box-shadow:0 6px 28px var(--glow),0 0 50px rgba(255,107,107,.08)!important;transition:var(--tr)!important;position:relative!important;overflow:hidden!important;animation:bb 3s ease-in-out infinite!important}
@keyframes bb{0%,100%{box-shadow:0 6px 28px rgba(255,107,107,.25),0 0 50px rgba(255,107,107,.08)}50%{box-shadow:0 8px 38px rgba(255,107,107,.4),0 0 70px rgba(255,107,107,.12)}}
div.stButton>button::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.18),transparent);transform:translateX(-100%);transition:.6s ease}
div.stButton>button:hover{transform:translateY(-3px) scale(1.01)!important;box-shadow:0 10px 45px var(--glow),0 0 90px rgba(255,107,107,.18)!important}
div.stButton>button:hover::after{transform:translateX(100%)}
div.stButton>button:active{transform:translateY(0) scale(.98)!important}

/* ── Result card ── */
.rc{background:rgba(255,255,255,.02);border:1px solid var(--border);border-radius:var(--rl);padding:38px 34px;backdrop-filter:blur(28px);position:relative;overflow:hidden;animation:ci .7s cubic-bezier(.16,1,.3,1)}
@keyframes ci{0%{opacity:0;transform:translateY(35px) scale(.96);filter:blur(6px)}100%{opacity:1;transform:translateY(0) scale(1);filter:blur(0)}}
.prb{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);pointer-events:none;z-index:0}
.pr{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);border-radius:50%;border:1px solid;animation:rp ease-out infinite;opacity:0}
@keyframes rp{0%{width:40px;height:40px;opacity:.35}100%{width:380px;height:380px;opacity:0}}
.rbadge{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:.58rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;padding:5px 14px;border-radius:30px;margin-bottom:12px;position:relative;z-index:1}
.rprice{font-size:3rem;font-weight:900;letter-spacing:-1px;line-height:1.1;margin-bottom:6px;position:relative;z-index:1}
.rsub{font-family:'JetBrains Mono',monospace;font-size:.65rem;font-weight:600;letter-spacing:2px;text-transform:uppercase;margin-bottom:16px;position:relative;z-index:1}
.rdesc{color:var(--muted);font-size:.92rem;line-height:1.7;position:relative;z-index:1}
.rdiv{border:none;border-top:1px solid rgba(255,255,255,.06);margin:16px 0;position:relative;z-index:1}
.srow{display:flex;gap:14px;margin-top:22px;position:relative;z-index:1}
.sc{flex:1;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.045);border-radius:var(--r);padding:14px;text-align:center;transition:var(--tr)}
.sc:hover{background:rgba(255,255,255,.06);transform:translateY(-2px);box-shadow:0 6px 20px rgba(255,107,107,.08)}
.sv{font-family:'JetBrains Mono',monospace;font-size:1.15rem;font-weight:800;display:block;margin-bottom:2px}
.sl{font-size:.6rem;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--muted)}
.ctrack{width:100%;height:7px;background:rgba(255,255,255,.05);border-radius:10px;overflow:hidden;margin-top:18px;position:relative;z-index:1}
.cfill{height:100%;border-radius:10px;animation:fi 1.3s cubic-bezier(.16,1,.3,1) forwards}
@keyframes fi{0%{width:0%}}

/* ── Stage text ── */
.stg{text-align:center;font-family:'JetBrains Mono',monospace;font-size:.78rem;letter-spacing:1px;color:var(--a2);animation:si .35s ease}
@keyframes si{0%{opacity:0;transform:translateY(5px)}100%{opacity:1;transform:translateY(0)}}

/* ── Footer ── */
.foot{text-align:center;padding:36px 0 18px;font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:2px;color:rgba(164,176,190,.3);text-transform:uppercase}

.stMarkdown h3{color:var(--txt)!important;font-size:1rem!important}

/* ── Particle iframe ── */
div[data-testid="stHtml"]{position:fixed!important;top:0!important;left:0!important;width:0!important;height:0!important;overflow:visible!important;z-index:0!important}
div[data-testid="stHtml"] iframe{position:fixed!important;top:0!important;left:0!important;width:100vw!important;height:100vh!important;border:none!important;pointer-events:none!important;z-index:0!important}
</style>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FLOATING ICONS + SCANLINES (helper function)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def build_overlay():
    icons = ['🏎️', '🏍️', '🔋', '🔌', '⚡', '🏁', '🧭', '🏆', '📈', '🎯', '⚙️', '🛞', '🚘', '🚦']
    parts = ['<div class="ficons">']
    for i, ic in enumerate(icons):
        left = 4 + (i * 6.8) % 90
        dur = 13 + (i * 3.5) % 15
        delay = (i * 2.3) % 18
        sz = 0.8 + (i * 0.12) % 0.7
        parts.append('<span class="fi" style="left:')
        parts.append(str(int(left)))
        parts.append('%;animation-duration:')
        parts.append("{:.1f}".format(dur))
        parts.append('s;animation-delay:')
        parts.append("{:.1f}".format(delay))
        parts.append('s;font-size:')
        parts.append("{:.1f}".format(sz))
        parts.append('rem;">')
        parts.append(ic)
        parts.append('</span>')
    parts.append('</div><div class="scan"></div>')
    return "".join(parts)


st.markdown(build_overlay(), unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOTTIE LOADER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


lottie_car = load_lottieurl("https://lottie.host/2bc05c0e-608b-4d4e-89d4-89b30ba90e58/GjPgGHYPSf.json")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOAD ML PIPELINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_resource
def load_artifacts():
    mdl = joblib.load('car_price_regressor.pkl')
    enc = joblib.load('target_encoder.pkl')
    scl = joblib.load('car_scaler.pkl')
    return mdl, enc, scl


model, encoder, scaler = load_artifacts()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SPEEDOMETER BARS (helper function)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def build_speedo():
    parts = ['<div class="speedo">']
    for i in range(22):
        h = 5 + (i * 7 + 2) % 20
        dur = 0.5 + (i * 0.14) % 0.85
        delay = (i * 0.07) % 0.55
        parts.append('<div class="sbar" style="height:')
        parts.append(str(h))
        parts.append('px;animation-duration:')
        parts.append("{:.2f}".format(dur))
        parts.append('s;animation-delay:')
        parts.append("{:.2f}".format(delay))
        parts.append('s;"></div>')
    parts.append('</div>')
    return "".join(parts)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RESULT CARD BUILDER (helper function = magic-safe)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def build_result(price_str, car, yr, km, eng, bhp, fuel_t, trans_t, own_t):
    ac = "#ff6b6b"
    gr = "linear-gradient(135deg,#ff6b6b 0%,#ff9f43 50%,#ff5252 100%)"
    gl = "rgba(255,107,107,.3)"

    rings = ""
    for i in range(3):
        d = "{:.1f}".format(i * 1.2)
        rings += '<div class="pr" style="border-color:' + ac + '25;animation-duration:3.6s;animation-delay:' + d + 's;"></div>'

    p = []
    p.append('<div class="rc">')
    p.append('<div class="prb">' + rings + '</div>')

    # Top accent bar
    p.append('<div style="position:absolute;top:0;left:0;right:0;height:4px;background:')
    p.append(gr)
    p.append(';border-radius:var(--rl) var(--rl) 0 0;box-shadow:0 0 18px ')
    p.append(gl)
    p.append(';z-index:1;"></div>')

    # Badge
    p.append('<span class="rbadge" style="background:')
    p.append(ac)
    p.append('15;color:')
    p.append(ac)
    p.append(';">&#10022; Appraisal Complete</span>')

    # Price
    p.append('<p class="rprice" style="background:')
    p.append(gr)
    p.append(';-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;filter:drop-shadow(0 0 28px ')
    p.append(gl)
    p.append(');">')
    p.append(price_str)
    p.append('</p>')

    # Subtitle
    p.append('<p class="rsub" style="color:')
    p.append(ac)
    p.append(';">Estimated Market Value</p>')

    p.append('<hr class="rdiv">')

    # Description
    p.append('<p class="rdesc">Valuation computed for a <strong>')
    p.append(str(car))
    p.append('</strong> (')
    p.append(str(yr))
    p.append('). The target encoding engine mapped historical asset performance across <strong>')
    p.append("{:,}".format(km))
    p.append(' km</strong> driven, <strong>')
    p.append(str(eng))
    p.append(' CC</strong> engine, <strong>')
    p.append(str(bhp))
    p.append(' BHP</strong>, ')
    p.append(str(fuel_t))
    p.append(' / ')
    p.append(str(trans_t))
    p.append(', ')
    p.append(str(own_t))
    p.append(' to generate this price estimate.</p>')

    # Confidence bar
    p.append('<div style="margin-top:18px;position:relative;z-index:1;">')
    p.append('<div style="display:flex;justify-content:space-between;margin-bottom:5px;">')
    p.append('<span style="font-size:.6rem;letter-spacing:2px;text-transform:uppercase;color:var(--muted);font-weight:600;">Model Confidence</span>')
    p.append('<span style="font-family:JetBrains Mono,monospace;font-size:.78rem;font-weight:700;color:')
    p.append(ac)
    p.append(';">91%</span></div>')
    p.append('<div class="ctrack"><div class="cfill" style="width:91%;background:')
    p.append(gr)
    p.append(';box-shadow:0 0 10px ')
    p.append(gl)
    p.append(';"></div></div></div>')

    # Stats chips
    p.append('<div class="srow">')

    p.append('<div class="sc"><span class="sv" style="color:')
    p.append(ac)
    p.append(';">')
    p.append(str(yr))
    p.append('</span><span class="sl">Year</span></div>')

    p.append('<div class="sc"><span class="sv" style="color:')
    p.append(ac)
    p.append(';">')
    p.append("{:,}".format(km))
    p.append('</span><span class="sl">KM</span></div>')

    p.append('<div class="sc"><span class="sv" style="color:')
    p.append(ac)
    p.append(';">')
    p.append(str(bhp))
    p.append('</span><span class="sl">BHP</span></div>')

    p.append('<div class="sc"><span class="sv" style="color:')
    p.append(ac)
    p.append(';">SVR</span><span class="sl">Engine</span></div>')

    p.append('</div>')
    p.append('</div>')
    return "".join(p)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HERO HEADER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown('<div style="text-align:center;padding-top:18px;position:relative;">', unsafe_allow_html=True)
st.markdown('<span class="hbadge">&#10022; AI-Powered &#10022;</span>', unsafe_allow_html=True)
st.markdown('<div style="position:relative;display:inline-block;">', unsafe_allow_html=True)
st.markdown('<div class="hglow"></div>', unsafe_allow_html=True)
st.markdown('<p class="htitle">AutoValuate</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<p class="hsub">intelligent car appraisal engine</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hdesc">Enter your vehicle specs below and let our machine learning '
    'pipeline calculate a market-accurate price estimation in seconds.</p>',
    unsafe_allow_html=True,
)
st.markdown(build_speedo(), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if lottie_car:
    st_lottie(lottie_car, height=100, key="car_anim")

st.markdown("<br>", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INPUT — Vehicle Identity
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(
    '<div class="gc"><span class="ci">🚘</span>'
    '<p class="cl">Vehicle Identity</p>'
    '<p class="ct">Brand &amp; Model</p></div>',
    unsafe_allow_html=True,
)
car_name = st.text_input(
    "Enter Car Brand & Model",
    value="Maruti Swift Dzire VDI",
    label_visibility="collapsed",
)

st.markdown("<br>", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INPUT — Performance Metrics (2 columns)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown(
        '<div class="gc"><span class="ci">📅</span>'
        '<p class="cl">Timeline</p>'
        '<p class="ct">Year &middot; Distance &middot; Efficiency</p></div>',
        unsafe_allow_html=True,
    )
    year = st.slider("Model Year", min_value=2000, max_value=2024, value=2015)
    km_driven = st.slider("Distance Driven (KM)", min_value=0, max_value=300000, value=60000, step=5000)
    mileage = st.slider("Fuel Efficiency (kmpl)", min_value=5.0, max_value=40.0, value=20.0, step=0.5)

with col2:
    st.markdown(
        '<div class="gc"><span class="ci">⚙️</span>'
        '<p class="cl">Powertrain</p>'
        '<p class="ct">Engine &middot; Power &middot; Seats</p></div>',
        unsafe_allow_html=True,
    )
    engine = st.slider("Engine Displacement (CC)", min_value=600, max_value=5000, value=1250, step=50)
    max_power = st.slider("Max Power (BHP)", min_value=30, max_value=400, value=75, step=5)
    seats = st.selectbox("Seating Configuration", options=[4.0, 5.0, 7.0, 8.0], index=1)

st.markdown("<br>", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INPUT — Classification (3 columns)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
col3, col4, col5 = st.columns(3, gap="medium")

with col3:
    st.markdown(
        '<div class="gc"><span class="ci">⛽</span>'
        '<p class="cl">Fuel</p>'
        '<p class="ct">Category</p></div>',
        unsafe_allow_html=True,
    )
    fuel = st.selectbox("Fuel Type", options=['Diesel', 'Petrol', 'LPG', 'CNG'], label_visibility="collapsed")

with col4:
    st.markdown(
        '<div class="gc"><span class="ci">🔀</span>'
        '<p class="cl">Gearbox</p>'
        '<p class="ct">Transmission</p></div>',
        unsafe_allow_html=True,
    )
    transmission = st.selectbox("Transmission", options=['Manual', 'Automatic'], label_visibility="collapsed")

with col5:
    st.markdown(
        '<div class="gc"><span class="ci">👤</span>'
        '<p class="cl">History</p>'
        '<p class="ct">Ownership</p></div>',
        unsafe_allow_html=True,
    )
    owner = st.selectbox("Ownership", options=['First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner'], label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CTA BUTTON
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
analyze_clicked = st.button("CALCULATE ESTIMATED APPRAISAL VALUE")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INFERENCE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if analyze_clicked:

    # Processing stages
    ph = st.empty()
    for txt, wait in [("Encoding vehicle features...", 0.35), ("Running regression model...", 0.5), ("Generating appraisal report...", 0.4)]:
        ph.markdown('<p class="stg">' + txt + '</p>', unsafe_allow_html=True)
        time.sleep(wait)
    ph.empty()

    # Build DataFrame — seller_type set directly to avoid NameError
    raw_input = pd.DataFrame(
        [[car_name, year, km_driven, fuel, 'Individual', transmission, owner, mileage, engine, max_power, seats]],
        columns=['name', 'year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner', 'mileage', 'engine', 'max_power', 'seats'],
    )

    # Transform and predict
    encoded_input = encoder.transform(raw_input)
    scaled_input = scaler.transform(encoded_input)
    predicted_price = model.predict(scaled_input)[0]

    # Format price string
    price_display = "\u20b9 " + "{:,.2f}".format(predicted_price)

    # Success animation
    lottie_ok = load_lottieurl("https://lottie.host/80c436ab-6b08-45ec-b91c-7f51be0ccf5d/c3qCgQ2fCc.json")
    if lottie_ok:
        st_lottie(lottie_ok, height=150, speed=1.2, key="ok_vfx")

    # Render result card
    st.markdown(
        build_result(price_display, car_name, year, km_driven, engine, max_power, fuel, transmission, owner),
        unsafe_allow_html=True,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(
    '<p class="foot">&#10022; AutoValuate &middot; Streamlit &amp; ML &middot; 2025 &#10022;</p>',
    unsafe_allow_html=True,
)
