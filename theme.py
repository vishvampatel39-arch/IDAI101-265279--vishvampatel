"""WaterBuddy look and feel: CSS, dark-mode CSS and the small JavaScript helpers (sound, scroll,
mountain background, sidebar arrow). Kept apart from app.py so the Python logic stays easy to read."""
import json

BUBBLES = '''<span class="wbbub" style="left:6%;width:14px;height:14px;animation-duration:17s;animation-delay:-3s"></span><span class="wbbub" style="left:17%;width:22px;height:22px;animation-duration:23s;animation-delay:-10s"></span><span class="wbbub" style="left:30%;width:10px;height:10px;animation-duration:15s;animation-delay:-6s"></span><span class="wbbub" style="left:46%;width:18px;height:18px;animation-duration:20s;animation-delay:-13s"></span><span class="wbbub" style="left:60%;width:12px;height:12px;animation-duration:16s;animation-delay:-1s"></span><span class="wbbub" style="left:72%;width:26px;height:26px;animation-duration:26s;animation-delay:-8s"></span><span class="wbbub" style="left:84%;width:14px;height:14px;animation-duration:18s;animation-delay:-15s"></span><span class="wbbub" style="left:94%;width:20px;height:20px;animation-duration:22s;animation-delay:-5s"></span>'''

HERO_VIDEO = "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260815_034306_b4af8200-cdba-4dc8-b46d-ba7eb9c68c44.mp4"

CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Urbanist:opsz,wght@9..144,600;9..144,800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap');
:root { color-scheme: light; }
html, body, [class*="css"], .stApp { font-family:'Urbanist',sans-serif; }
.stApp { background:linear-gradient(135deg,#f7fbff 0%,#eff8ff 48%,#f6fffc 100%); color:#203047; }
[data-testid="stHeader"] { background:rgba(247,251,255,.88); }
[data-testid="stSidebar"] { display:block!important; background:radial-gradient(circle at 10% 10%,rgba(63,220,221,.24),transparent 30%),linear-gradient(165deg,#087e9b 0%,#056783 48%,#073b68 100%); border-right:1px solid #0d7189; box-shadow:8px 0 30px rgba(3,80,112,.12); min-width:265px; }
[data-testid="stSidebar"] > div { padding:1.25rem .9rem; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#d5f6fb!important; }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color:#c0e8f2!important; }
[data-testid="stSidebar"] [data-testid="stRadio"] > label { color:#e5fbff!important; font-weight:700; font-size:.8rem; }
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] { gap:7px; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { padding:10px 12px; border-radius:12px; border:1px solid transparent; transition:all .18s ease; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background:rgba(255,255,255,.14); border-color:rgba(180,245,255,.35); }
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) { background:linear-gradient(100deg,#e4fbff,#c8f7f0); border-color:#a4f1ee; box-shadow:0 5px 18px rgba(0,0,0,.14); }
[data-testid="stSidebar"] [data-testid="stRadio"] label p { color:#f0fdff!important; font-weight:600; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p { color:#056b83!important; font-weight:800; }
[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child { display:flex!important; }
[data-testid="stSidebar"] [data-testid="stSidebarContent"] { padding-top:1rem; }
h1,h2,h3 { font-family:'Urbanist',serif!important; color:#17344b!important; letter-spacing:-.02em; }
h1 { font-size:2.2rem!important; }
.block-container { max-width:1350px; padding-top:1.7rem; padding-bottom:3rem; animation:fadeUp .55s cubic-bezier(.2,.7,.2,1) both; }
[data-testid="stPlotlyChart"], [data-testid="stVegaLiteChart"], [data-testid="stArrowVegaLiteChart"] { animation:chartRise .7s ease both; }
@keyframes chartRise { from{opacity:0;transform:translateY(12px) scale(.985)} to{opacity:1;transform:translateY(0) scale(1)} }
@keyframes fadeUp { from {opacity:0;transform:translateY(8px)} to {opacity:1;transform:none} }
@keyframes bob { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-5px)} }
@keyframes shine { from{background-position:-200% 0} to{background-position:200% 0} }
.topbar { display:flex; align-items:center; gap:10px; padding:8px 4px 16px; border-bottom:1px solid #dceaf2; margin-bottom:20px; }
.brand { display:flex; align-items:center; gap:10px; font-family:'Urbanist',serif; font-size:1.45rem; font-weight:800; color:#f2fdff; }
.brand .dot { width:38px;height:38px;border-radius:13px;background:rgba(255,255,255,.16);border:1px solid rgba(200,250,255,.3);display:flex;align-items:center;justify-content:center;box-shadow:0 5px 14px rgba(31,148,177,.10);animation:bob 4s ease-in-out infinite; }
.hero { position:relative;overflow:hidden;display:flex;align-items:center;gap:26px;border-radius:24px;padding:30px 32px;margin-bottom:20px;background:linear-gradient(115deg,#ffffff 0%,#e8f8ff 60%,#e6fbf5 100%);border:1px solid #d6edf5;box-shadow:0 14px 40px rgba(52,112,145,.09); }
.hero::after { content:"";position:absolute;top:-90px;right:-40px;width:300px;height:300px;border-radius:50%;background:rgba(79,205,218,.16);filter:blur(30px); }
.hero h1 { margin:6px 0 0;font-size:2.7rem!important;line-height:1.08; }
.hero p { margin:.7rem 0 0;color:#526a7e;max-width:540px;position:relative;z-index:1; }
.hero svg { animation:bob 4.5s ease-in-out infinite;flex-shrink:0;position:relative;z-index:1; }
.badge { font-family:'Urbanist',monospace;font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;color:#087f9b;background:#d9f7fb;border:1px solid #b9eaf2;border-radius:8px;padding:5px 10px; }
.grad { background:linear-gradient(90deg,#0891b2,#0f9f91,#38a6c7);background-size:200% auto;-webkit-background-clip:text;background-clip:text;color:transparent;animation:shine 6s linear infinite; }
.eye { transform-origin:center;transform-box:fill-box; }
.section-kicker {font-size:.69rem;font-weight:800;letter-spacing:.13em;color:#0a91a7;margin-bottom:5px;}
.wb-card { background:rgba(255,255,255,.92);border:1px solid #deebf2;border-radius:16px;padding:15px 13px;text-align:left;box-shadow:0 6px 20px rgba(44,94,124,.055);transition:transform .2s,border-color .2s,box-shadow .2s;height:100%; }
.wb-card:hover { transform:translateY(-3px);border-color:#a9dfe9;box-shadow:0 12px 25px rgba(44,130,155,.10); }
.wb-card .l { font-family:'Urbanist',monospace;font-size:.65rem;color:#71869a;text-transform:uppercase;letter-spacing:.05em; }
.wb-card .v { font-family:'Urbanist',serif;font-size:1.3rem;font-weight:800;color:#0785a2;margin-top:5px;overflow-wrap:anywhere; }
.bottle { width:120px;height:240px;border:3px solid #8bdbe8;border-radius:22px 22px 34px 34px;position:relative;overflow:hidden;background:#edfaff;margin:auto;box-shadow:0 8px 24px rgba(25,155,190,.12),inset 0 0 18px rgba(34,211,238,.1); }
.fill { position:absolute;bottom:0;left:0;width:100%;background:linear-gradient(#70dce9,#26a9d0);transition:height 1s cubic-bezier(.2,.8,.2,1); }
.fill svg { position:absolute;top:-9px;left:0;width:200%;height:10px; }
.mascot { display:flex;gap:14px;align-items:center;background:#f0fbff;border:1px solid #d6eef5;border-radius:16px;padding:13px 16px;color:#31556b; }
.stButton>button { border-radius:12px;border:1px solid #c8e4ee;font-weight:700;background:#fff;color:#24546b;transition:transform .18s,box-shadow .18s,background .18s; }
.stButton>button:hover { transform:translateY(-1px);background:#effbff;border-color:#8fd5e5;color:#087f9b;box-shadow:0 7px 16px rgba(35,135,165,.10); }
.stButton>button[kind="primary"] { background:linear-gradient(100deg,#0e9fbd,#24b9b0);color:#fff;border-color:transparent;box-shadow:0 6px 16px rgba(20,160,180,.17); }
.stProgress>div>div>div>div { background:linear-gradient(90deg,#18b4ce,#39c6aa); }
.tag { display:inline-block;padding:3px 10px;border-radius:12px;background:#e0f8f5;color:#087f78;font-size:.8rem; }
div[data-testid="stAlert"] { border-radius:12px; }
div[data-testid="stExpander"] { background:rgba(255,255,255,.72);border:1px solid #deebf2;border-radius:14px; }
[data-testid="stMetric"] { background:#fff;border:1px solid #deebf2;padding:14px;border-radius:14px; }
hr { border-color:#dceaf2!important; }
@media(max-width:700px) { .hero{flex-direction:column;text-align:center;padding:24px}.hero h1{font-size:2rem!important}.block-container{padding-top:1rem} }

/* Premium visual polish: richer colour, depth, spacing and interaction */
.stApp { background: radial-gradient(ellipse at 82% 4%, rgba(66,211,211,.16), transparent 27%), radial-gradient(ellipse at 15% 60%, rgba(69,169,255,.10), transparent 32%), linear-gradient(135deg,#f7fbff 0%,#edf8ff 48%,#f1fffb 100%) !important; }
[data-testid="stSidebar"] { background: radial-gradient(ellipse at 15% 8%,rgba(83,244,226,.30),transparent 32%), radial-gradient(ellipse at 85% 70%,rgba(29,154,221,.30),transparent 30%), linear-gradient(160deg,#087e9b 0%,#056783 42%,#07345f 100%) !important; min-width:285px; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { padding:12px 13px!important; border-radius:14px!important; margin:2px 0!important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) { background:linear-gradient(105deg,#f0ffff,#bdf5ec)!important; box-shadow:0 8px 24px rgba(1,33,62,.22),inset 0 0 0 1px rgba(255,255,255,.75)!important; transform:translateX(3px); }
.block-container { max-width:1480px!important; padding-top:1.25rem!important; }
.hero { min-height:230px; padding:34px 38px!important; border-radius:28px!important; background:linear-gradient(115deg,rgba(255,255,255,.98),rgba(224,247,255,.95) 58%,rgba(218,255,245,.96))!important; border:1px solid rgba(151,218,235,.65)!important; box-shadow:0 18px 45px rgba(36,112,151,.12),inset 0 1px 0 #fff!important; }
.hero h1 { font-size:clamp(2.6rem,4vw,3.6rem)!important; letter-spacing:-.055em!important; }
.hero p { font-size:1.04rem; line-height:1.7; }
.wb-card { padding:19px 18px!important; border-radius:20px!important; background:linear-gradient(145deg,rgba(255,255,255,.98),rgba(241,251,255,.94))!important; border:1px solid #d7edf5!important; box-shadow:0 9px 25px rgba(35,103,137,.08),inset 0 1px 0 white!important; }
.wb-card .v { font-size:1.65rem!important; letter-spacing:-.035em; }
.wb-card .l { font-size:.7rem!important; }
[data-testid="stPlotlyChart"], [data-testid="stVegaLiteChart"] { background:rgba(255,255,255,.78); border:1px solid #d9edf5; border-radius:20px; padding:10px; box-shadow:0 8px 22px rgba(35,103,137,.06); }
[data-testid="stMetric"] { background:linear-gradient(145deg,#fff,#effaff); padding:17px 18px; border:1px solid #d9edf5; border-radius:18px; box-shadow:0 7px 20px rgba(35,103,137,.06); }
[data-testid="stMetricValue"] { color:#0785a2!important; font-weight:800!important; }
.stButton>button { min-height:43px; border-radius:14px!important; padding:.55rem 1rem!important; }
.stButton>button[kind="primary"] { background:linear-gradient(110deg,#078db5,#14b8a6)!important; box-shadow:0 8px 20px rgba(8,157,180,.25)!important; }
.stButton>button[kind="primary"]:hover { box-shadow:0 12px 26px rgba(8,157,180,.32)!important; transform:translateY(-2px) scale(1.01)!important; }
.stProgress>div { height:12px!important; border-radius:20px!important; background:#dceff5!important; }
.stProgress>div>div>div>div { border-radius:20px!important; background:linear-gradient(90deg,#0ea5e9,#14b8a6,#5eead4)!important; }
[data-testid="stExpander"] { border:1px solid #d9edf5!important; border-radius:16px!important; background:rgba(255,255,255,.72)!important; }
[data-testid="stAlert"] { border-radius:16px!important; box-shadow:0 5px 16px rgba(35,103,137,.05); }
hr { border-color:#d7eaf2!important; }
@media (prefers-reduced-motion:no-preference) { .hero { animation:fadeUp .55s ease both; } .wb-card { animation:fadeUp .45s ease both; } .stButton>button:active { transform:scale(.98); } }


@property --n{syntax:'<integer>';initial-value:0;inherits:false}
@keyframes countUp{to{--n:var(--to)}}
.cnt{animation:countUp 1.1s cubic-bezier(.2,.8,.2,1) forwards;counter-reset:n var(--n)}
.cnt::after{content:counter(n)}
@keyframes pop{0%{transform:scale(.6);opacity:0}60%{transform:scale(1.08)}100%{transform:scale(1);opacity:1}}
@keyframes sloshG{0%,100%{filter:brightness(1)}50%{filter:brightness(1.15)}}
.glrow{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0 4px}
.gl{width:34px;height:52px;border:2px solid #0e9fbd;border-radius:6px 6px 12px 12px;position:relative;overflow:hidden;
 background:rgba(14,159,189,.07);animation:pop .55s cubic-bezier(.2,.9,.3,1.3) both;transition:transform .25s}
.gl:hover{transform:translateY(-5px) rotate(-4deg)}
.gf{position:absolute;bottom:0;width:100%;background:linear-gradient(#5ccfe6,#0e9fbd);transition:height .9s cubic-bezier(.2,.8,.2,1);animation:sloshG 3s ease-in-out infinite}
.glcap{font-size:.78rem;opacity:.7;margin-bottom:6px}
.nm{display:inline-block;margin:8px 0;padding:8px 16px;border-radius:999px;border:1px dashed #0e9fbd;animation:fadeUp .6s ease both}

.sx{--p:0;position:relative;height:80vh;min-height:460px;border-radius:30px;overflow:hidden;margin-bottom:20px;
 background:linear-gradient(180deg,#25aacb,#0e7da3);box-shadow:0 24px 50px -24px rgba(6,42,61,.7);isolation:isolate}
.sx-bg{position:absolute;inset:0;opacity:calc(1 - var(--p));z-index:0}
.sx-bg i{position:absolute;left:-25%;width:150%;height:60%;bottom:calc(-30% + var(--p)*-20%);border-radius:42%;
 background:rgba(92,207,230,.16);animation:swell 11s ease-in-out infinite}
.sx-bg i:nth-child(2){background:rgba(34,211,238,.14);animation-duration:15s;animation-direction:reverse;bottom:-38%}
.sx-bg i:nth-child(3){background:rgba(224,242,254,.08);animation-duration:19s;bottom:-44%}
@keyframes swell{0%,100%{transform:translateX(0) rotate(0)}50%{transform:translateX(6%) rotate(4deg)}}
.sx-media{position:absolute;z-index:1;top:50%;left:50%;transform:translate(-50%,-50%);
 width:calc(260px + (100% - 260px)*var(--p));height:calc(58% + 42%*var(--p));overflow:hidden;
 border-radius:calc(26px*(1 - var(--p)));box-shadow:0 0 50px rgba(0,0,0,.35);background:linear-gradient(160deg,#4bcbe4,#1393b6)}
.sx-media video{width:100%;height:100%;object-fit:cover;opacity:.85}
.sx-shade{position:absolute;inset:0;background:rgba(4,60,85,calc(.18 - var(--p)*.1))}
.sx-mascot{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:calc(1 - var(--p)*1.6)}
.sx-mascot svg{animation:bob 4.5s ease-in-out infinite}
.sx-title{position:absolute;inset:0;z-index:2;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;pointer-events:none;text-align:center}
.sx-title h2{margin:0;color:#e0f2fe!important;font-size:clamp(2.2rem,6vw,4.4rem);line-height:1;text-shadow:0 4px 24px rgba(0,0,0,.45)}
.sx-title .l{transform:translateX(calc(var(--p)*-42vw))}
.sx-title .r{transform:translateX(calc(var(--p)*42vw))}
.sx-title .badge{margin-bottom:12px;opacity:calc(1 - var(--p)*2)}
.sx-hint{position:absolute;z-index:2;bottom:18px;left:0;right:0;text-align:center;color:#bfe9f4;font-size:.8rem;letter-spacing:.14em;
 text-transform:uppercase;opacity:calc(1 - var(--p)*4);animation:nudge 1.8s ease-in-out infinite}
@keyframes nudge{50%{transform:translateY(6px)}}
@media(prefers-reduced-motion:reduce){.sx-bg i,.sx-mascot svg,.sx-hint{animation:none}}

/* ===== full-page living background (every tab) ===== */
.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"],[data-testid="stHeader"]{background:transparent!important}
.stApp{background:#d4edf5!important}
.wbbg{--p:0;position:fixed;inset:0;z-index:0;overflow:hidden;pointer-events:none;background:linear-gradient(170deg,#e4f6fb,#c9eaf4 60%,#b4e0ee)}
.wbbg video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.28;
 transform:scale(calc(1 + var(--p)*.18));transition:transform .2s linear}
.wbwash{position:absolute;inset:0;background:linear-gradient(180deg,rgba(240,251,254,calc(.86 + var(--p)*.06)),rgba(219,243,250,calc(.9 + var(--p)*.05)))}
.wbwaves i{position:absolute;left:-30%;width:160%;height:55%;border-radius:44%;background:rgba(14,159,189,.13);
 bottom:calc(-34% + var(--p)*14%);animation:swell 13s ease-in-out infinite}
.wbwaves i:nth-child(2){background:rgba(92,207,230,.16);animation-duration:18s;animation-direction:reverse;bottom:calc(-42% + var(--p)*10%)}
.wbwaves i:nth-child(3){background:rgba(11,37,69,.07);animation-duration:23s;bottom:calc(-48% + var(--p)*6%)}
.wbbub{position:absolute;bottom:-40px;border-radius:50%;border:1px solid rgba(14,159,189,.4);background:rgba(255,255,255,.35);
 animation:riseB linear infinite}
@keyframes riseB{0%{transform:translateY(0) scale(.5);opacity:0}15%,80%{opacity:.7}100%{transform:translateY(-112vh) scale(1.15);opacity:0}}
.block-container{position:relative;z-index:2}
.block-container{background:rgba(255,255,255,.55);backdrop-filter:blur(6px);border-radius:30px;margin-top:.6rem;margin-bottom:1rem}
.wb-card,.mascot,.nm{background:rgba(255,255,255,.78)!important;backdrop-filter:blur(8px)}
@media(prefers-reduced-motion:reduce){.wbwaves i,.wbbub{animation:none}}

@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Urbanist:wght@400;500;600;700&family=DM+Mono:wght@500&display=swap');
html,body,[class*="css"],.stApp{font-family:'Urbanist',sans-serif!important}
h1,h2,h3,.brand,.wb-card .v,.sx-title h2,.sbx-name{font-family:'Urbanist',sans-serif!important;letter-spacing:-.025em}
h1{font-weight:800!important;position:relative;padding-bottom:10px}
h1::after{content:"";position:absolute;left:0;bottom:0;height:4px;width:0;border-radius:4px;background:linear-gradient(90deg,#0e9fbd,#5ccfe6);animation:draw .9s .2s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes draw{to{width:90px}}
.badge,.wb-card .l,.sbx-card .t{font-family:'Urbanist',monospace!important}
/* sidebar */
[data-testid="stSidebar"] [data-testid="stRadio"] label>div:first-child{display:none!important}
[data-testid="stSidebar"] [role="radiogroup"]{gap:3px!important}
[data-testid="stSidebar"] [role="radiogroup"] label{position:relative;opacity:0;animation:slideIn .5s cubic-bezier(.2,.8,.2,1) forwards;
 overflow:visible!important;padding:10px 14px!important;transition:background .25s,transform .25s,box-shadow .25s,padding-left .25s}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{padding-left:20px!important;transform:none}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){box-shadow:0 8px 22px -10px rgba(92,235,255,.7)!important}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked)::before{content:"";position:absolute;left:-10px;top:22%;height:56%;width:4px;border-radius:4px;background:#5ccfe6;box-shadow:0 0 12px #5ccfe6;animation:grow .35s ease both}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(1),[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(6),[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(11){margin-top:26px!important}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(1)::after,[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(6)::after,[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(11)::after{
 position:absolute;top:-20px;left:6px;font-family:'Urbanist',monospace;font-size:.62rem;letter-spacing:.18em;color:#8fdcec;opacity:.85}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(1)::after{content:"TRACK"}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(6)::after{content:"LEARN"}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(11)::after{content:"YOU"}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(1){animation-delay:0.04s}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(2){animation-delay:0.08s}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(3){animation-delay:0.12s}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(4){animation-delay:0.16s}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(5){animation-delay:0.20s}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(6){animation-delay:0.24s}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(7){animation-delay:0.28s}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(8){animation-delay:0.32s}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(9){animation-delay:0.36s}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(10){animation-delay:0.40s}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(11){animation-delay:0.44s}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(12){animation-delay:0.48s}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(13){animation-delay:0.52s}
@keyframes slideIn{from{opacity:0;transform:translateX(-20px)}to{opacity:1;transform:none}}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes shine{from{background-position:-200% 0}to{background-position:200% 0}}
@keyframes drift{0%,100%{transform:translateY(0) rotate(-4deg)}50%{transform:translateY(-6px) rotate(4deg)}}
.sbx-brand{display:flex;align-items:center;gap:12px;padding:4px 4px 14px;border-bottom:1px solid rgba(255,255,255,.14)}
.sbx-logo{display:flex;width:48px;height:48px;align-items:center;justify-content:center;border-radius:16px;background:rgba(255,255,255,.12);
 border:1px solid rgba(255,255,255,.25);box-shadow:0 0 22px rgba(92,235,255,.35);animation:drift 4.5s ease-in-out infinite}
.sbx-name{font-size:1.4rem;font-weight:800;color:#fff;line-height:1}
.sbx-tag{font-size:.7rem;letter-spacing:.09em;text-transform:uppercase;margin-top:5px;background:linear-gradient(90deg,#9ff0ff 20%,#fff 50%,#9ff0ff 80%);
 background-size:200% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;animation:shine 5s linear infinite}
.sbx-card{margin-top:22px;padding:14px;border-radius:18px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);backdrop-filter:blur(8px)}
.sbx-card .t{font-size:.62rem;letter-spacing:.14em;text-transform:uppercase;color:#9fe3f2}
.sbx-card .n{font-family:'Urbanist',sans-serif;font-size:1.3rem;font-weight:700;color:#fff;margin:2px 0 9px}
.sbx-card .bar{height:7px;border-radius:9px;background:rgba(255,255,255,.18);overflow:hidden}
.sbx-card .bar i{display:block;height:100%;border-radius:9px;background:linear-gradient(90deg,#5ccfe6,#d6fbff);transition:width 1s cubic-bezier(.2,.8,.2,1)}
.sbx-card .note{font-size:.8rem;color:#d5f6fb;margin-top:10px;font-style:italic}
.sbx-foot{font-size:.68rem;color:#9fcfdc;text-align:center;margin-top:14px}
/* main-area motion */
.block-container [data-testid="stElementContainer"]{animation:fadeUp .6s cubic-bezier(.2,.8,.2,1) both}
.block-container [data-testid="stElementContainer"]:nth-child(2){animation-delay:.05s}
.block-container [data-testid="stElementContainer"]:nth-child(3){animation-delay:.1s}
.block-container [data-testid="stElementContainer"]:nth-child(4){animation-delay:.15s}
.block-container [data-testid="stElementContainer"]:nth-child(5){animation-delay:.2s}
.stButton>button[kind="primary"]{position:relative;overflow:hidden}
.stButton>button[kind="primary"]::after{content:"";position:absolute;top:0;left:-60%;width:40%;height:100%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.55),transparent);transform:skewX(-20deg);animation:sweep 3.2s ease-in-out infinite}
@keyframes sweep{0%,60%{left:-60%}100%{left:130%}}
.tlrow{display:flex;flex-wrap:wrap;gap:10px;margin:10px 0}
.tl{min-width:92px;padding:10px 12px;border-radius:14px;border:1px solid #bfe3ee;background:rgba(255,255,255,.75);text-align:center;animation:pop .5s cubic-bezier(.2,.9,.3,1.3) both;transition:transform .25s}
.tl:hover{transform:translateY(-4px)}
.tl b{display:block;font-family:'Urbanist',sans-serif;font-size:1.05rem;color:#0b2545}
.tl span{font-size:.75rem;color:#4d6b80}
.tl.done{background:linear-gradient(160deg,#5ccfe6,#0e9fbd);border-color:#0e9fbd}
.tl.done b,.tl.done span{color:#fff}

/* ===== bolder type ===== */
.stApp p,.stApp li,.stApp label,.stApp [data-testid="stMarkdownContainer"]{font-weight:500}
.stApp strong,.stApp b{font-weight:800}
h1,h2,h3{font-weight:800!important;line-height:1.02!important;letter-spacing:-.045em!important}
h1{font-size:clamp(2.3rem,4.6vw,3.7rem)!important;padding-bottom:14px!important}
h2,h3{font-size:clamp(1.5rem,2.6vw,2rem)!important}
h1::after{height:6px!important}
.pw{display:inline-block;margin-right:.24em;opacity:0;animation:pull .7s cubic-bezier(.16,1,.3,1) forwards}
.pw:last-child{margin-right:0}
@keyframes pull{from{transform:translateY(.5em);opacity:0}to{transform:none;opacity:1}}
.sx-title h2{font-size:clamp(2.6rem,7.2vw,5.8rem)!important;font-weight:800!important;letter-spacing:-.065em!important;line-height:.88!important}
.wb-card .v{font-size:1.6rem!important;font-weight:800!important;letter-spacing:-.03em}
.wb-card .l{font-weight:700;font-size:.68rem!important}
.badge{font-weight:700}
.sbx-name{font-size:1.55rem!important;font-weight:800!important;letter-spacing:-.05em!important}
[data-testid="stSidebar"] [role="radiogroup"] label p{font-weight:700!important;font-size:.98rem!important;letter-spacing:-.01em}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p{font-weight:800!important}
.stButton>button{font-weight:800!important;letter-spacing:-.01em}
.tl b{font-weight:800}
@media(prefers-reduced-motion:reduce){.pw{animation:none;opacity:1}}

.sx-sub{position:absolute;z-index:2;left:50%;bottom:64px;transform:translateX(-50%);width:min(560px,86%);margin:0;text-align:center;
 color:#effcff;font-weight:600;font-size:1.02rem;line-height:1.4;text-shadow:0 2px 14px rgba(3,50,72,.55);
 opacity:calc(1 - var(--p)*3);animation:fadeUp .8s .9s ease both}

/* ===== blue dotted background (replaces the plain pale wash) ===== */
.stApp{background:#bfe2f6!important}
.wbbg{background:linear-gradient(160deg,#d9effc 0%,#bfe2f6 55%,#a6d5f0 100%)!important}
.wbbg video,.wbwash,.wbwaves{display:none!important}
.wbbg::before{content:"";position:absolute;left:-60px;right:-60px;bottom:-60px;top:calc(-60px + var(--p)*-50px);
 background-image:radial-gradient(circle,rgba(22,108,188,.42) 1.8px,transparent 2.2px),radial-gradient(circle,rgba(255,255,255,.85) 1.3px,transparent 1.7px);
 background-size:26px 26px;background-position:0 0,13px 13px;animation:dotsDrift 36s linear infinite}
.wbbg::after{content:"";position:absolute;inset:0;
 background:radial-gradient(ellipse at 18% 0%,rgba(255,255,255,.65),transparent 52%),radial-gradient(ellipse at 92% 100%,rgba(30,140,220,.28),transparent 55%)}
@keyframes dotsDrift{to{transform:translate(26px,26px)}}
.wbbub{z-index:1}
.block-container{background:rgba(255,255,255,.3)!important;backdrop-filter:blur(2px)!important}
@media(prefers-reduced-motion:reduce){.wbbg::before{animation:none}}

@import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@500;700;800&family=Public+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap');
/* ===== calmer, flatter styling ===== */
.stApp{background:#c6e3f5!important}
.wbbg{background:#c6e3f5!important}
.wbbg::before{animation:none!important;background-image:radial-gradient(circle,rgba(22,100,170,.28) 1.4px,transparent 1.8px)!important;background-size:24px 24px!important;background-position:0 0!important;left:0;right:0;bottom:0}
.wbbg::after,.wbbub{display:none!important}
.block-container{background:transparent!important;backdrop-filter:none!important;border-radius:0!important}
h1::after{background:#0b5fa5!important;animation:none!important;width:56px!important;height:4px!important}
h1{font-size:clamp(2rem,3.8vw,3rem)!important;letter-spacing:-.04em!important}
.wb-card,.mascot,.nm,.tl{background:#fff!important;border:1px solid #a9c8dd!important;border-radius:10px!important;box-shadow:none!important;backdrop-filter:none!important}
.nm{border-style:solid!important}
.wb-card:hover,.tl:hover,.gl:hover{transform:none!important;border-color:#0b5fa5!important;box-shadow:none!important}
.wb-card .v{color:#0b3a66!important}
.badge{background:#0b3a66!important;color:#e6f3fb!important;border:0!important;border-radius:4px!important}
.grad{animation:none!important;background:none!important;color:inherit!important;-webkit-text-fill-color:inherit!important}
.stButton>button{border-radius:8px!important;box-shadow:none!important}
.stButton>button[kind="primary"]{animation:none!important;background:#0b5fa5!important;color:#fff!important;border-color:#0b5fa5!important}
.stButton>button[kind="primary"]::after{display:none!important}
.stButton>button:hover{transform:none!important;box-shadow:none!important;background:#e3f1fa!important;color:#0b3a66!important}
.stButton>button[kind="primary"]:hover{background:#094a82!important;color:#fff!important}
.bottle{box-shadow:none!important;border-radius:14px 14px 22px 22px!important}
/* sidebar */
[data-testid="stSidebar"]{background:#0f2a43!important;border-right:0!important}
[data-testid="stSidebar"] [role="radiogroup"] label{animation:none!important;opacity:1!important;border-radius:6px!important;padding:9px 12px!important;border:0!important}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{background:rgba(255,255,255,.07)!important;padding-left:12px!important}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){background:#1b4a73!important;box-shadow:none!important}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked)::before{left:0!important;top:0!important;height:100%!important;width:3px!important;border-radius:0!important;box-shadow:none!important;background:#7cc8ee!important;animation:none!important}
[data-testid="stSidebar"] [role="radiogroup"] label p{font-family:'Urbanist',monospace!important;font-size:.82rem!important;font-weight:500!important;letter-spacing:0!important;white-space:pre}
.sbx-logo{animation:none!important;box-shadow:none!important;border-radius:10px!important;background:rgba(255,255,255,.08)!important}
.sbx-tag{animation:none!important;background:none!important;-webkit-text-fill-color:#8fb8d3!important;color:#8fb8d3!important}
.sbx-card{background:rgba(255,255,255,.06)!important;border-radius:8px!important;backdrop-filter:none!important}
/* hero */
.sx{border-radius:14px!important;box-shadow:none!important;background:#1479b8!important}
.sx-bg i{display:none!important}
.sx-media{background:#3aa5d6!important}
.sx-mascot svg,.sx-hint{animation:none!important}
.sx-title h2{font-size:clamp(2.4rem,6vw,4.8rem)!important;letter-spacing:-.045em!important}
.hero svg{animation:none!important}

/* ===== dithered water-range background (drawn by canvas, see DITHER_JS) ===== */
.wbbg{display:none!important}
.stApp{background:linear-gradient(180deg,#e4f2fb 0%,#cfe6f5 100%)!important}
.stApp>canvas#wb-dither{z-index:0}

@import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@300;400;500;600;700&display=swap');
/* ===== Gilroy-style type (Urbanist) + blur-reveal motion ===== */
html,body,[class*="css"],.stApp,.stApp button,.stApp input,.stApp textarea{font-family:'Urbanist',sans-serif!important}
.stApp p,.stApp li,.stApp label,.stApp [data-testid="stMarkdownContainer"]{font-weight:500}
h1,h2,h3,.brand,.sbx-name,.wb-card .v,.tl b,.sbx-card .n{font-family:'Urbanist',sans-serif!important;font-weight:600!important;letter-spacing:-.025em!important}
h1{font-size:clamp(2.2rem,4.2vw,3.4rem)!important;line-height:1.05!important}
.sx-title h2{font-weight:600!important;letter-spacing:-.04em!important}
.wb-card .v{font-size:1.7rem!important}
.wb-card .l,.badge,.sbx-card .t,.sbx-tag{font-family:'Urbanist',sans-serif!important;font-weight:600!important;letter-spacing:.1em!important}
.stButton>button{font-weight:600!important;letter-spacing:0!important}
[data-testid="stSidebar"] [role="radiogroup"] label p{font-family:'Urbanist',sans-serif!important;font-size:1rem!important;font-weight:600!important}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p{font-weight:700!important}
.pw{animation:blurIn 1s cubic-bezier(.4,0,.2,1) forwards!important}
@keyframes blurIn{from{opacity:0;filter:blur(10px);transform:translateY(20%)}to{opacity:1;filter:blur(0);transform:none}}
@keyframes blurSoft{from{opacity:0;filter:blur(6px);transform:translateY(10px)}to{opacity:1;filter:blur(0);transform:none}}
.block-container [data-testid="stElementContainer"]{animation:blurSoft .9s cubic-bezier(.4,0,.2,1) both!important}
@media(prefers-reduced-motion:reduce){.pw,.block-container [data-testid="stElementContainer"]{animation:none!important;opacity:1;filter:none}}

/* ===== dashboard motion ===== */
.sx-wave{position:absolute;z-index:1;left:0;bottom:0;width:200%;height:46px;animation:wave 9s linear infinite;opacity:calc(1 - var(--p)*1.5)}
.sx-wave.w2{animation-duration:6s;animation-direction:reverse;height:34px}
.bottle{animation:sway 6s ease-in-out infinite;transform-origin:50% 100%}
@keyframes sway{0%,100%{transform:rotate(-1.4deg)}50%{transform:rotate(1.4deg)}}
.bb{position:absolute;z-index:2;bottom:6px;width:9px;height:9px;border-radius:50%;border:1.5px solid rgba(255,255,255,.85);background:rgba(255,255,255,.25);animation:bubUp 4.2s ease-in infinite;opacity:0}
@keyframes bubUp{0%{transform:translateY(0) scale(.5);opacity:0}15%{opacity:.9}100%{transform:translateY(-200px) scale(1.1);opacity:0}}
.gl.new .gf{animation:flash 1.3s ease-out}
.gl.new{animation:pop .55s cubic-bezier(.2,.9,.3,1.3) both,nudgeG 2.6s 1s ease-in-out infinite}
@keyframes flash{0%{filter:brightness(1.9)}100%{filter:brightness(1)}}
@keyframes nudgeG{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
.nm::before{content:"";display:inline-block;width:8px;height:8px;margin-right:10px;border-radius:50%;background:#0e9fbd;animation:ping 1.8s ease-out infinite}
@keyframes ping{0%{box-shadow:0 0 0 0 rgba(14,159,189,.6)}100%{box-shadow:0 0 0 10px rgba(14,159,189,0)}}
.wb-card .v{transition:transform .3s}
.wb-card:hover .v{transform:scale(1.06)}
.stProgress>div>div>div>div{background-size:200% 100%;background-image:linear-gradient(90deg,#0e9fbd,#5ccfe6,#0e9fbd)!important;animation:shine 2.8s linear infinite}
@media(prefers-reduced-motion:reduce){.sx-wave,.bottle,.bb,.gl.new,.gl.new .gf,.nm::before,.stProgress>div>div>div>div{animation:none!important}}

.tspiral{width:100%;max-width:300px;display:block;margin:auto}
.tspiral polyline{stroke-dasharray:1;stroke-dashoffset:1;animation:drawSp 2s cubic-bezier(.4,0,.2,1) forwards}
@keyframes drawSp{to{stroke-dashoffset:0}}

.eod{padding:22px 26px;border:1px solid #a9c8dd;border-radius:10px;background:#fff;animation:pop .6s cubic-bezier(.2,.9,.3,1.3) both;margin:8px 0}
.eodh{font-size:1.5rem;font-weight:700;margin-bottom:4px}
.eodn{font-size:2.6rem;font-weight:700;color:#0b5fa5;line-height:1.1}
.eodm{margin-top:8px;font-weight:600}

.sx-scene{position:absolute;inset:0;width:100%;height:100%;z-index:0}
.sx-media video{position:absolute!important;inset:0;z-index:1}
.sx-shade{z-index:2}
.sx-mascot{z-index:3}
</style>"""

SOUND_JS = """<script>
const P=window.parent;
if(!P.__wb){const wb=P.__wb={on:true,ctx:null};
const ac=()=>{if(!wb.ctx)wb.ctx=new(P.AudioContext||P.webkitAudioContext)();if(wb.ctx.state==='suspended')wb.ctx.resume();return wb.ctx};
const tone=(f1,f2,d,v,ty,dl)=>{const c=ac(),o=c.createOscillator(),g=c.createGain(),t=c.currentTime+(dl||0);o.type=ty||'sine';
o.frequency.setValueAtTime(f1,t);o.frequency.exponentialRampToValueAtTime(f2,t+d*.45);o.frequency.exponentialRampToValueAtTime(f1*.8,t+d);
g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(v,t+.02);g.gain.exponentialRampToValueAtTime(.001,t+d);
o.connect(g);g.connect(c.destination);o.start(t);o.stop(t+d+.05)};
wb.drop=()=>tone(400,860,.22,.16);
wb.pour=()=>[0,.09,.18].forEach((d,i)=>tone(380+i*60,820+i*80,.2,.14,'sine',d));
wb.splash=(x,y)=>{if(P.matchMedia&&P.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
for(let i=0;i<12;i++){const d=P.document.createElement('i'),a=(-Math.PI/2)+(Math.random()-.5)*2.2,v=50+Math.random()*70,s=4+Math.random()*5;
d.style.cssText='position:fixed;z-index:99999;pointer-events:none;border-radius:50%;background:#4aaee0;opacity:.9;left:'+x+'px;top:'+y+'px;width:'+s+'px;height:'+s+'px';
P.document.body.appendChild(d);
d.animate([{transform:'translate(0,0)',opacity:.9},{transform:'translate('+Math.cos(a)*v+'px,'+(Math.sin(a)*v)+'px)',opacity:.9,offset:.5},{transform:'translate('+Math.cos(a)*v*1.2+'px,'+(Math.sin(a)*v+70)+'px)',opacity:0}],{duration:800,easing:'cubic-bezier(.3,.6,.4,1)'}).onfinish=()=>d.remove()}};
wb.tick=()=>tone(700,500,.08,.07,'triangle');
wb.chime=()=>[523,659,784,1047].forEach((f,i)=>tone(f,f*1.01,.5,.16,'sine',i*.12));
wb.confetti=()=>{const d=P.document,c=d.createElement('canvas');c.width=P.innerWidth;c.height=P.innerHeight;
c.style.cssText='position:fixed;inset:0;z-index:99999;pointer-events:none';d.body.appendChild(c);const x=c.getContext('2d');
const cols=['#22d3ee','#67e8f9','#5eead4','#e0f2fe','#38bdf8'];
const ps=Array.from({length:140},()=>({x:c.width/2,y:c.height*.35,vx:(Math.random()-.5)*14,vy:Math.random()*-12-3,s:Math.random()*7+3,c:cols[Math.random()*5|0],r:Math.random()*6}));
let f=0;(function a(){x.clearRect(0,0,c.width,c.height);ps.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.vy+=.28;p.r+=.2;x.save();x.translate(p.x,p.y);x.rotate(p.r);x.fillStyle=p.c;x.fillRect(-p.s/2,-p.s/2,p.s,p.s*.6);x.restore()});
if(++f<150)P.requestAnimationFrame(a);else c.remove()})()};
P.document.addEventListener('click',e=>{if(!wb.on)return;const b=e.target.closest('button,label');if(!b)return;
const t=(b.innerText||'').toLowerCase();try{if(t.includes('+250')||t.includes('add custom')){wb.pour();wb.splash(e.clientX,e.clientY)}
else if(b.closest('[data-testid="stRadio"]'))wb.drop();else wb.tick()}catch(_){}},true)}
P.__wb.on=__ON__;
</script>"""

SCROLL_JS = """<script>
(function(){const P=window.parent;if(P.__wbScroll)return;P.__wbScroll=true;
if(P.matchMedia&&P.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
const seen=new WeakMap();
(function loop(){const d=P.document,sc=d.querySelector('[data-testid="stMain"]')||d.querySelector('.main')||d.scrollingElement;
if(sc){const p=Math.min(1,Math.max(0,sc.scrollTop/(P.innerHeight*0.6))).toFixed(3);
d.querySelectorAll('.sx,.wbbg').forEach(el=>{if(seen.get(el)!==p){el.style.setProperty('--p',p);seen.set(el,p)}})}
P.requestAnimationFrame(loop)})()})();
</script>"""

DITHER_JS = "(function(){\nif(window.__wbDither)return;window.__wbDither=1;\nconst D=document,W=window,TONES=[\"#e8f4fb\", \"#cfe6f6\", \"#b0d5ef\", \"#8bbfe5\", \"#63a4d6\", \"#3d84c2\", \"#235f9f\", \"#123f78\"],PX=3,LAY=7,SEED=11;\nconst hx=h=>[parseInt(h.slice(1,3),16),parseInt(h.slice(3,5),16),parseInt(h.slice(5,7),16)];\nconst PK=TONES.map(t=>{const c=hx(t);return(c[2]<<16)|(c[1]<<8)|c[0]}),N=PK.length,PKD=['#0a1a2c','#17426a','#21598a','#2f73a8','#4690c4','#62aedb','#8ccbe9','#c4e8f6'].map(t=>{const c=hx(t);return(c[2]<<16)|(c[1]<<8)|c[0]});\nfunction bm(n){if(n===1)return[[0]];const m=bm(n/2),s=m.length,r=[],A=[[0,2],[3,1]];\nfor(let y=0;y<2*s;y++){r[y]=[];for(let x=0;x<2*s;x++)r[y][x]=m[y%s][x%s]*4+A[(y/s)|0][(x/s)|0]}return r}\nconst B=bm(8),BF=new Float32Array(64);for(let y=0;y<8;y++)for(let x=0;x<8;x++)BF[y*8+x]=(B[y][x]+.5)/64;\nconst hash=(x,y,s)=>{let h=Math.imul(x|0,374761393)+Math.imul(y|0,668265263)+Math.imul(s|0,1442695041);h=Math.imul(h^(h>>>13),1274126177);h^=h>>>16;return(h>>>0)/4294967296};\nconst noise=(x,y,s)=>{const xi=Math.floor(x),yi=Math.floor(y),xf=x-xi,yf=y-yi,u=xf*xf*(3-2*xf),v=yf*yf*(3-2*yf),a=hash(xi,yi,s),b=hash(xi+1,yi,s),c=hash(xi,yi+1,s),d=hash(xi+1,yi+1,s);return a+(b-a)*u+(c-a)*v+(a-b-c+d)*u*v};\nconst fbm=(x,y,s,o)=>{let sum=0,amp=.5,nm=0;for(let i=0;i<o;i++){sum+=noise(x,y,s+i*31)*amp;nm+=amp;x*=2.03;y*=2.03;amp*=.5}return sum/nm};\nconst sm=(a,b,x)=>{const t=Math.min(1,Math.max(0,(x-a)/(b-a)));return t*t*(3-2*t)};\nconst ease=t=>{const c=t<0?0:t>1?1:t;return 1-Math.pow(1-c,3)};\nfunction ridge(cols,rows,i,L,seed,mg){const k=L>1?i/(L-1):1,n=cols+mg*2,out=new Float32Array(n);\nconst base=rows*(.38+.66*Math.pow(k,1.4)),amp=rows*(.2+.24*k),freq=6-3.8*k;\nconst fl=rows*.5*k*k*k*(.55+.6*hash(i,11,seed)),fr=rows*.5*k*k*k*(.55+.6*hash(i,13,seed));\nconst ceil=rows*.2,tilt=(hash(i,7,seed)-.5)*rows*.34*(.4+k),s=seed*13+i*101;\nfor(let x=0;x<n;x++){const u=(x-mg)/cols;\nconst r1=1-Math.abs(noise(u*freq+i*3.7,.5,s)*2-1),r2=1-Math.abs(noise(u*freq*2.3,3.5,s+1)*2-1),f=fbm(u*freq*4.1,9.5,s+2,3);\nconst h=r1*r1*.62+r2*.24+f*.14,e=Math.min(1.2,Math.abs(u*2-1));\nconst y=base-h*amp+tilt*(u-.5)*2-(u<.5?fl:fr)*e*e*Math.sqrt(e);out[x]=y<ceil?ceil-(ceil-y)*.25:y}return out}\nconst RED=W.matchMedia&&W.matchMedia('(prefers-reduced-motion: reduce)').matches;\nconst cv=D.createElement('canvas'),cx=cv.getContext('2d');cv.id='wb-dither';cv.setAttribute('aria-hidden','true');\ncv.style.cssText='position:fixed;left:0;bottom:0;z-index:0;pointer-events:none;image-rendering:pixelated;max-width:none';\nlet cols,rows,mg,img,buf,tops,pools,cT,cS,cP,fog,fw,fh,ex=-1e4,ey=-1e4,clear=0,inside=false,pt=0,pe=0,wV=0,wX=0,last=0,lastT=0;\nconst t0=performance.now();\nfunction layout(){const w=W.innerWidth,h=Math.round(Math.min(W.innerHeight*.72,760));\ncols=Math.ceil(w/PX);rows=Math.ceil(h/PX);cv.width=cols;cv.height=rows;cv.style.width=cols*PX+'px';cv.style.height=rows*PX+'px';\nimg=cx.createImageData(cols,rows);buf=new Uint32Array(img.data.buffer);mg=Math.ceil(cols*.045)+3;tops=[];pools=[];\nfor(let i=0;i<LAY;i++){const t=ridge(cols,rows,i,LAY,SEED,mg),p=new Float32Array(t.length);\nfor(let x=0;x<t.length;x++)p[x]=.45+1.1*fbm(((x-mg)/cols)*4,i*5.3,SEED+9,2);tops.push(t);pools.push(p)}\ncT=new Float32Array(LAY*cols);cS=new Float32Array(LAY*cols);cP=new Float32Array(LAY*cols);fw=(cols>>1)+2;fh=(rows>>1)+2;fog=new Float32Array(fw*fh)}\nfunction draw(now){const PKX=D.body.classList.contains('wb-dark')?PKD:PK;const dt=Math.min(64,now-lastT||16);lastT=now;\nconst e1=1-Math.pow(.82,dt/16.7),e2=1-Math.pow(.93,dt/16.7);\nclear+=((inside?1:0)-clear)*e2;pe+=((RED?0:pt)-pe)*e2;wV*=Math.pow(.965,dt/16.7);wX+=wV*dt/1000;\nconst sc=D.querySelector('[data-testid=\"stMain\"]'),sy=sc?Math.min(sc.scrollTop,900)/PX:0;\nconst age=now-t0,fT=(RED?0:now/1000*.045)+wX;\nfor(let gy=0;gy<fh;gy++)for(let gx=0;gx<fw;gx++){const nx=gx*9/cols+fT,ny=gy*4.4/rows,wp=noise(nx*.45-fT*.6,ny*.8,77)*.6;\nfog[gy*fw+gx]=sm(.3,.74,fbm(nx+wp,ny+wp*.4,31,3))}\nconst rev=new Float32Array(LAY),k=new Float32Array(LAY),tb=new Float32Array(LAY);\nfor(let i=0;i<LAY;i++){k[i]=i/(LAY-1);rev[i]=RED?1:ease((age-200-i*150)/1200);tb[i]=.1+.88*Math.pow(k[i],1.25);\nconst rise=(1-rev[i])*rows*.09+sy*(.12+.5*k[i]),sh=Math.round(pe*(.25+k[i])*.75*(mg-3)),t=tops[i],lastI=t.length-1,dp=rows*(.08+.42*k[i]);\nfor(let x=0;x<cols;x++){const at=x+mg+sh;cT[i*cols+x]=t[at]+rise;cS[i*cols+x]=t[Math.min(lastI,at+2)]-t[Math.max(0,at-2)];cP[i*cols+x]=dp*pools[i][at]}}\nconst T=RED?0:now/1000,lift=RED?0:1-ease((age-700)/1800),r=120/PX,r2=r*r,fadeTo=rows*.42;\nfor(let y=0;y<rows;y++){const fade=sm(0,fadeTo,y),fr=(y>>1)*fw,by=(y&7)*8,dy=(y-ey)*1.5,a=Math.round(fade*235)<<24;\nfor(let x=0;x<cols;x++){let L=-1;for(let i=LAY-1;i>=0;i--){if(y>=cT[i*cols+x]){L=i;break}}\nlet tone=0,mk=.3;\nif(L>=0){const kk=k[L],d=y-cT[L*cols+x],dp=cP[L*cols+x];tone=tb[L]*(1-sm(0,dp,d)*(.88-.45*kk));\nconst sl=cS[L*cols+x]*.06;tone+=(sl<-.2?-.2:sl>.2?.2:sl)*(1-sm(0,dp*.5,d));\ntone+=(hash(x+Math.round(cT[L*cols+x]*7),d|0,L)-.5)*.07*kk;tone+=(1-sm(0,2.2,d))*.2*(.4+kk)+kk*.05*Math.sin(d*.42-T*1.1+x*.035)*sm(1,6,d);tone*=rev[L];mk=.95-.5*kk}\nlet m=fog[fr+(x>>1)]*.55*mk;\nif(clear>.01){const dx=x-ex,q=(dx*dx+dy*dy)/r2;if(q<4){const c=clear*Math.exp(-q);m*=1-c*.92;if(L>=0)tone+=c*.14*rev[L]}}\nif(tone>.97)tone=.97;m+=lift*.55;if(m>1)m=1;tone*=1-m*.9;\nlet v=Math.floor(tone*(N-1)+BF[by+(x&7)]);if(v>N-1)v=N-1;\nbuf[y*cols+x]=v<=0?0:((a|PKX[v])>>>0)}}\ncx.putImageData(img,0,0)}\nfunction mount(){const app=D.querySelector('.stApp')||D.body;app.insertBefore(cv,app.firstChild)}\nfunction loop(now){if(!cv.isConnected)mount();if(now-last>33){draw(now);last=now}W.requestAnimationFrame(loop)}\nD.addEventListener('pointermove',e=>{pt=e.clientX/W.innerWidth*2-1;ex=e.clientX/PX;ey=(e.clientY-(W.innerHeight-rows*PX))/PX;inside=ey>=0&&ey<rows});\nD.addEventListener('pointerleave',()=>{inside=false;pt=0});\nD.addEventListener('pointerdown',e=>{if(inside&&!e.target.closest('a,button,input,label,[role=radio]'))wV+=ex<cols/2?1.4:-1.4});\nlet rt=0;W.addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(()=>{layout();draw(performance.now())},120)});\nlayout();mount();draw(performance.now());if(!RED)W.requestAnimationFrame(loop);\n})();\n"

DITHER_BOOT = ("<script>(function(){const P=window.parent;if(P.__wbDitherBoot)return;P.__wbDitherBoot=1;"
              "const s=P.document.createElement('script');s.textContent=" + json.dumps(DITHER_JS) + ";P.document.head.appendChild(s)})();</script>")

SIDE_JS = "(function(){\nif(window.__wbSide)return;window.__wbSide=1;\nconst D=document,B=D.body,KEY='wb-side-off';\nconst st=D.createElement('style');st.textContent=`\nbody.wb-side-off [data-testid=\"stSidebar\"]{display:none!important}\n#wb-side-btn{position:fixed;top:16px;z-index:1000002;width:34px;height:34px;border-radius:50%;border:1px solid #0b5fa5;background:#fff;color:#0b3a66;cursor:pointer;display:grid;place-items:center;padding:0;box-shadow:0 2px 8px rgba(11,58,102,.25);transition:left .3s cubic-bezier(.2,.8,.2,1),background .2s,color .2s,transform .2s}\n#wb-side-btn:hover{background:#0b5fa5;color:#fff;transform:scale(1.08)}\n#wb-side-btn svg{width:16px;height:16px;transition:transform .3s}\nbody.wb-side-off #wb-side-btn svg{transform:rotate(180deg)}`;\nD.head.appendChild(st);\nconst b=D.createElement('button');b.id='wb-side-btn';b.type='button';\nb.innerHTML='<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.4\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M15 5l-7 7 7 7\"/></svg>';\nconst sb=()=>D.querySelector('[data-testid=\"stSidebar\"]');\nconst collapsedNative=()=>{const s=sb();return !!s&&s.getAttribute('aria-expanded')==='false'};\nfunction sync(){const off=B.classList.contains('wb-side-off')||collapsedNative(),s=sb();\nb.setAttribute('aria-label',off?'Open sidebar':'Close sidebar');b.title=off?'Open sidebar':'Close sidebar';\nb.classList.toggle('x',off);\nb.style.left=(off||!s)?'14px':Math.max(8,s.getBoundingClientRect().right-17)+'px';\nB.classList.toggle('wb-side-flip',off)}\ntry{if(localStorage.getItem(KEY)==='1')B.classList.add('wb-side-off')}catch(e){}\nb.addEventListener('click',()=>{\nif(collapsedNative()&&!B.classList.contains('wb-side-off')){const n=D.querySelector('[data-testid=\"stExpandSidebarButton\"],[data-testid=\"collapsedControl\"] button,[data-testid=\"stSidebarCollapsedControl\"] button');if(n){n.click();sync();return}}\nB.classList.toggle('wb-side-off');\ntry{localStorage.setItem(KEY,B.classList.contains('wb-side-off')?'1':'0')}catch(e){}sync()});\nB.appendChild(b);sync();\nsetInterval(()=>{if(!b.isConnected)B.appendChild(b);sync()},400);\nwindow.addEventListener('resize',sync);\n})();\n"

SIDE_BOOT = ("<script>(function(){const P=window.parent;if(P.__wbSideBoot)return;P.__wbSideBoot=1;"
             "const s=P.document.createElement('script');s.textContent=" + json.dumps(SIDE_JS) + ";P.document.head.appendChild(s)})();</script>")

DARK_CSS = """<style>
.stApp{background:linear-gradient(180deg,#0a1a2c,#0e2a44)!important}
.stApp{transition:color .5s}
.stApp,.stApp p,.stApp li,.stApp label,.stApp span,.stApp [data-testid="stMarkdownContainer"]{color:#e3eff8}
h1,h2,h3,.pw{color:#fff!important}
.wb-card,.mascot,.nm,.tl,.eod{background:#12304a!important;border-color:#2a5578!important;color:#e3eff8!important}
.wb-card .v,.tl b{color:#7fd0ee!important}
.wb-card .l,.glcap,.tl span{color:#9bbbd1!important}
.stButton>button{background:#12304a!important;color:#e3eff8!important;border-color:#3a6a92!important}
.stButton>button[kind="primary"]{background:#2b8fd0!important;color:#fff!important}
[data-baseweb="input"],[data-baseweb="select"]>div,[data-baseweb="base-input"],.stNumberInput input,.stTextInput input{background:#12304a!important;color:#e3eff8!important}
[data-testid="stDataFrame"]{filter:invert(.9) hue-rotate(180deg)}
.gl{border-color:#5bb6dc}
</style>"""


# The sound and scroll scripts used to run inside the small hidden iframe that Streamlit makes for
# components.html. Every time dark mode (or sound) was switched, that iframe was rebuilt and its
# scripts died, so the scroll animation stopped. Now they are injected into the page itself,
# once, like the mountain background and the sidebar arrow, so they survive reruns.
def _boot(code, flag):
    return ("<script>(function(){const P=window.parent;if(P." + flag + ")return;P." + flag + "=1;"
            "const s=P.document.createElement('script');s.textContent=" + json.dumps(code) +
            ";P.document.head.appendChild(s)})();</script>")


def _inner(js):
    return (js.replace("<script>", "").replace("</script>", "")
              .replace("window.parent", "window").replace("P.__wb.on=__ON__;", ""))


SOUND_BOOT = _boot(_inner(SOUND_JS), "__wbSoundBoot")
SCROLL_BOOT = _boot(_inner(SCROLL_JS), "__wbScrollBoot")
