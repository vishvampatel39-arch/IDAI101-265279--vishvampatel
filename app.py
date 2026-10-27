"""WaterBuddy - Your Daily Hydration Companion (educational student project, not medical advice).

How the code is organised
  data.py   : content (age goals, foods, ingredients, tips, quiz)
  theme.py  : CSS and JavaScript for the look and feel
  app.py    : logic and pages
      State        init_state, add_water, undo, reset, new_day      (all data lives in st.session_state)
      Calculations total, remaining, percent                         (live maths used by every page)
      Feedback     mascot_message, milestone_note, progress_visual   (bottle, bar and mascot react to progress)
      Pages        page_dashboard ... page_settings                  (one function per tab)
Run with:  streamlit run app.py
"""
import datetime
import json
import re
import math
import random
import time
import streamlit as st
from data import AGE_GOALS, CUP_ML, PAGES, FDC, FOODS, INGREDIENTS, LABEL_HELP, TIPS, QUIZ
from theme import (CSS, DARK_CSS, SOUND_BOOT, SCROLL_BOOT, DITHER_BOOT, SIDE_BOOT,
                   BUBBLES, HERO_VIDEO)

st.set_page_config(page_title="WaterBuddy", page_icon="💧", layout="wide")

# ---------------------------------------------------------------- DATA
# Example goals from the assignment (1600 children, 2500 adults); the other
# two values are illustrative. NOT medical recommendations.
# Order matters: the sidebar shows section headings at items 1 (Track), 6 (Learn) and 11 (You).

# water % = approximate USDA FoodData Central values (rounded). None = unavailable.
# Please re-check each value on FoodData Central before submitting.





# ---------------------------------------------------------------- STATE
def init_state():
    d = {"page": "Dashboard", "age": "19–50 years", "goal": 2500, "log": [],
         "tip_i": 0, "ach": set(), "flash": None, "sound_on": True, "celebrate": False, "times": []}
    for k, v in d.items():
        st.session_state.setdefault(k, v)

def total(): return sum(st.session_state.log)
def remaining(): return max(0, st.session_state.goal - total())
def percent():
    g = st.session_state.goal
    return total() / g * 100 if g > 0 else 0.0

def update_achievements():
    p, a = percent(), st.session_state.ach
    if st.session_state.log: a.add("First Log")
    for name, t in [("Quarter Way", 25), ("Halfway There", 50), ("Almost There", 75), ("Goal Reached", 100)]:
        if p >= t: a.add(name)

def add_water(ml):
    try:
        ml = int(ml)
    except (TypeError, ValueError):
        ml = 0
    if ml <= 0 or ml > 2000:
        st.session_state.flash = ("error", "Please enter a whole amount from 1 to 2000 ml.")
        return
    before = percent()
    st.session_state.log.append(ml)
    st.session_state.times.append(time.time())
    if before < 100 <= percent(): st.session_state.celebrate = True
    update_achievements()
    st.session_state.flash = ("success", f"Logged {ml} ml.")

def add_custom(): add_water(st.session_state.get("custom_ml", 0))
def new_day():
    reset()
    st.session_state.eod = False

def undo():
    if st.session_state.log:
        st.session_state.log.pop()
        if st.session_state.times: st.session_state.times.pop()
        st.session_state.flash = ("info", "Last entry removed.")
def reset():
    st.session_state.log = []
    st.session_state.times = []
    st.session_state.ach = set()
    st.session_state.flash = ("info", "Everything has been reset.")
def goto(p): st.session_state.page = p
def on_age(key):
    """Apply the selected age-group goal and keep the visible goal widget in sync."""
    st.session_state.age = st.session_state[key]
    suggested_goal = AGE_GOALS[st.session_state.age]
    st.session_state.goal = suggested_goal
    # Each page has its own goal input key. Update it in the callback, before
    # widgets are created on the next rerun, so the displayed value cannot go stale.
    prefix = key.rsplit("_", 1)[0]
    goal_widget_key = f"{prefix}_goal"
    if goal_widget_key in st.session_state:
        st.session_state[goal_widget_key] = suggested_goal
    update_achievements()
def on_goal(key):
    st.session_state.goal = int(st.session_state[key])
    update_achievements()

# ---------------------------------------------------------------- UI HELPERS

def drop_svg(size=70, mood=None):
    """Water-drop mascot; the mouth changes with progress."""
    p = percent() if mood is None else mood
    mouth = ("M40 66 h20" if not st.session_state.log else "M38 63 Q50 80 62 63 Z" if p >= 75
             else "M40 65 Q50 75 60 65")
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100"><path d="M50 6 C50 6 18 44 18 64 '
            f'A32 32 0 0 0 82 64 C82 44 50 6 50 6Z" fill="#8fe3f2" stroke="#fff" stroke-width="3"/>'
            f'<ellipse class="eye" cx="40" cy="55" rx="4" ry="5" fill="#0b2545"/>'
            f'<ellipse class="eye" cx="60" cy="55" rx="4" ry="5" fill="#0b2545"/>'
            f'<path d="{mouth}" fill="#0b2545" stroke="#0b2545" stroke-width="2.5" stroke-linecap="round"/>'
            f'<circle cx="32" cy="64" r="4" fill="#ff9db0" opacity=".6"/><circle cx="68" cy="64" r="4" fill="#ff9db0" opacity=".6"/></svg>')

def pull(text, start=0.0):
    """Split text into words that rise into place one after another."""
    return "".join(f'<span class="pw" style="animation-delay:{start + i*0.1:.2f}s">{w}</span>'
                   for i, w in enumerate(text.split()))

def page_title(text):
    text = re.sub(r"^[^A-Za-z0-9]+", "", text)  # drop leading emoji
    st.markdown(f'<h1 class="pu">{pull(text)}</h1>', unsafe_allow_html=True)

def card(label, value, num=None, unit="", i=0):
    v = f'<span class="cnt" style="--to:{int(num)}"></span>{unit}' if num is not None else value
    st.markdown(f'<div class="wb-card" style="animation-delay:{i*0.07:.2f}s"><div class="v">{v}</div>'
                f'<div class="l">{label}</div></div>', unsafe_allow_html=True)

AGE_VOICE = {"6–12 years": "You're a hydration hero!", "13–18 years": "Nice and easy, keep going.",
             "19–50 years": "", "65 years and above": "Gentle and steady is just right."}

def mascot_message():
    msg = _mascot_core()
    tail = AGE_VOICE.get(st.session_state.age, "")
    return f"{msg} {tail}".strip() if st.session_state.log and tail else msg

def _mascot_core():
    p = percent()
    if not st.session_state.log: return "😐 Drip: Ready when you are. One small sip is a great start!"
    if p > 100: return "😮 Drip: Goal exceeded! Great job. You don't need to drink more today."
    if p >= 100: return "🎉 Drip: You reached your goal! Lovely work."
    if p >= 75: return "😄 Drip: 75%! Almost there."
    if p >= 50: return "😊 Drip: Halfway there. Keep going at your own pace."
    if p >= 25: return "🙂 Drip: Quarter way! Nice start."
    return "💧 Drip: Every sip counts. Good start!"

def milestone_note():
    p = percent()
    if p > 100: return "Goal exceeded."
    for t in (100, 75, 50, 25):
        if p >= t: return f"Milestone reached: {t}%"
    return "No milestone yet. Small sips add up."

def show_flash():
    f = st.session_state.flash
    if f:
        getattr(st, f[0])(f[1])
        st.session_state.flash = None

def progress_visual():
    p = percent()
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f'<div class="bottle"><i class="bb" style="left:22%;animation-delay:0s"></i><i class="bb" style="left:48%;animation-delay:1.3s"></i><i class="bb" style="left:70%;animation-delay:2.4s"></i><i class="bb" style="left:36%;animation-delay:3.3s"></i><div class="fill" style="height:{min(p,100):.0f}%"><svg viewBox="0 0 200 10" preserveAspectRatio="none"><path d="M0 5 Q25 0 50 5 T100 5 T150 5 T200 5 V10 H0Z" fill="#4cc3e0"/></svg></div></div>',
                    unsafe_allow_html=True)
    with c2:
        st.progress(min(max(p, 0.0), 100.0) / 100)
        st.write(f"**{p:.0f}%** of your goal · {milestone_note()}")
        st.markdown(f'<div class="mascot">{drop_svg(46)}<div>{mascot_message()}</div></div>', unsafe_allow_html=True)

def stats_cards():
    cols = st.columns(6)
    items = [("Age group", st.session_state.age, None, ""), ("Suggested goal", "", AGE_GOALS[st.session_state.age], " ml"),
             ("Your goal", "", st.session_state.goal, " ml"), ("Logged", "", total(), " ml"),
             ("Remaining", "", remaining(), " ml"), ("Achieved", "", round(percent()), "%")]
    for i, (c, (l, v, n, u)) in enumerate(zip(cols, items)):
        with c: card(l, v, n, u, i)

def turtle_svg(pct):
    """Turtle-graphics style spiral: forward d, turn 59 degrees, lengthen d. More water = more steps."""
    steps = round(min(pct, 100) * 0.9)
    x = y = ang = 0.0
    d = 3.0
    pts = [(x, y)]
    for _ in range(steps):
        x += d * math.cos(math.radians(ang))
        y += d * math.sin(math.radians(ang))
        ang += 59
        d += 1.4
        pts.append((x, y))
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    w, h = max(xs) - min(xs) or 1, max(ys) - min(ys) or 1
    k = 260 / max(w, h)
    path = " ".join(f"{(px - min(xs)) * k + 20:.1f},{(py - min(ys)) * k + 20:.1f}" for px, py in pts)
    ex, ey = path.split()[-1].split(",")
    return (f'<svg class="tspiral" viewBox="0 0 300 300"><polyline points="{path}" pathLength="1" fill="none" stroke="#0e9fbd" '
            f'stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/><circle cx="{ex}" cy="{ey}" r="6" fill="#0b3a66"/></svg>')

def glasses():
    """Row of 250 ml glasses that fill as you log water."""
    n = max(1, min(16, math.ceil(st.session_state.goal / 250)))
    full = total() / 250
    out = []
    for i in range(n):
        f = max(0.0, min(1.0, full - i))
        newest = min(n - 1, math.ceil(full) - 1) if full > 0 else -1
        out.append(f'<div class="gl{" new" if i == newest else ""}" style="animation-delay:{i*0.06:.2f}s"><div class="gf" style="height:{f*100:.0f}%"></div></div>')
    st.markdown('<div class="glrow">' + "".join(out) + '</div>'
                f'<div class="glcap">Each glass = 250 ml · {n} glasses make up your goal</div>', unsafe_allow_html=True)

def next_milestone():
    p = percent()
    nxt = next((t for t in (25, 50, 75, 100) if p < t), None)
    if nxt is None:
        st.markdown('<div class="nm">All milestones reached today. Nicely done.</div>', unsafe_allow_html=True)
        return
    need = max(0, math.ceil(st.session_state.goal * nxt / 100 - total()))
    st.markdown(f'<div class="nm">Next milestone <b>{nxt}%</b> · about <b>{need} ml</b> to go</div>', unsafe_allow_html=True)

def log_controls(prefix):
    c1, c2, c3 = st.columns([1, 2, 1])
    c1.button("+250 ml", key=f"{prefix}_250", on_click=add_water, args=(250,), type="primary")
    c2.number_input("Custom amount (ml)", 1, 2000, 100, 50, key="custom_ml") if prefix == "tr" else None
    if prefix == "tr":
        c3.button("Add custom", key="tr_add", on_click=add_custom)

def goal_controls(prefix):
    ages = list(AGE_GOALS)
    st.selectbox("Age group", ages, index=ages.index(st.session_state.age), key=f"{prefix}_age",
                 on_change=on_age, args=(f"{prefix}_age",))
    st.number_input("Daily goal (ml)", 500, 6000, int(st.session_state.goal), 50, key=f"{prefix}_goal",
                    on_change=on_goal, args=(f"{prefix}_goal",))
    st.caption("Goals are examples for this project, not medical advice. Needs vary with the person, "
               "activity, weather, diet and health.")

# ---------------------------------------------------------------- PAGES
def page_dashboard():
    st.markdown(f'''<div class="sx"><div class="sx-bg"><i></i><i></i><i></i></div>
<div class="sx-media"><svg class="sx-scene" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice"><defs><linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fdcf0"/><stop offset="1" stop-color="#1479b8"/></linearGradient></defs><rect width="400" height="300" fill="url(#sg)"/><circle cx="300" cy="80" r="34" fill="#fff6d6" opacity=".9"/><path d="M0 190 Q60 160 120 190 T240 190 T400 170 V300 H0Z" fill="#3aa5d6" opacity=".85"/><path d="M0 220 Q70 195 140 220 T280 220 T400 205 V300 H0Z" fill="#1d89c4"/><path d="M0 255 Q80 235 160 255 T320 255 T400 245 V300 H0Z" fill="#0e6fa6"/></svg><video autoplay loop muted playsinline src="{HERO_VIDEO}"></video><div class="sx-shade"></div>
<div class="sx-mascot">{drop_svg(110)}</div></div>
<div class="sx-title"><span class="badge">Today · goal {st.session_state.goal} ml</span>
<h2 class="l">{pull("Stay fresh,", .1)}</h2><h2 class="r">{pull("one sip at a time.", .45)}</h2></div>
<svg class="sx-wave" viewBox="0 0 400 40" preserveAspectRatio="none"><path d="M0 20 Q50 0 100 20 T200 20 T300 20 T400 20 V40 H0Z" fill="rgba(255,255,255,.16)"/></svg><svg class="sx-wave w2" viewBox="0 0 400 40" preserveAspectRatio="none"><path d="M0 22 Q50 40 100 22 T200 22 T300 22 T400 22 V40 H0Z" fill="rgba(255,255,255,.22)"/></svg><p class="sx-sub">Track your water, learn what is in your food and drinks, and build a routine that feels easy.</p><div class="sx-hint">Scroll to dive in</div></div>''', unsafe_allow_html=True)
    stats_cards()
    st.write("")
    show_flash()
    st.button("+250 ml", key="dash_250", on_click=add_water, args=(250,), type="primary")
    progress_visual()
    next_milestone()
    glasses()
    st.subheader("Quick links")
    c = st.columns(4)
    for col, p in zip(c, ["Water Tracker", "Hydration Impact Checker", "Infuse & Learn", "Hydration Tips"]):
        col.button(p, key=f"q_{p}", on_click=goto, args=(p,))

def page_tracker():
    page_title("💧 Water Tracker")
    goal_controls("tr")
    st.divider()
    show_flash()
    log_controls("tr")
    b1, b2 = st.columns(2)
    b1.button("Undo last entry", key="tr_undo", on_click=undo)
    b2.button("Reset today", key="tr_reset", on_click=reset)
    stats_cards()
    progress_visual()
    next_milestone()
    glasses()
    st.caption("Your records are kept for this browser session only.")

def page_progress():
    page_title("📈 My Progress")
    stats_cards()
    progress_visual()
    st.subheader("Today's hydration breakdown")
    logged = total()
    remaining_ml = max(0, st.session_state.goal - logged)
    ratio = min(logged / st.session_state.goal, 1.0) if st.session_state.goal else 0.0
    circumference = 2 * 3.14159 * 43
    dash = circumference * ratio
    pie_svg = f'''<div style="display:flex;justify-content:center;align-items:center;min-height:245px;animation:fadeUp .6s ease both"><svg viewBox="0 0 180 180" width="205" role="img" aria-label="Hydration goal progress"><circle cx="90" cy="90" r="43" fill="none" stroke="#dceef5" stroke-width="18"/><circle cx="90" cy="90" r="43" fill="none" stroke="#08a6b7" stroke-width="18" stroke-linecap="round" stroke-dasharray="{dash:.1f} {circumference:.1f}" transform="rotate(-90 90 90)" style="transition:stroke-dasharray 1s ease"/><text x="90" y="85" text-anchor="middle" font-size="22" font-weight="800" fill="#17344b">{ratio*100:.0f}%</text><text x="90" y="105" text-anchor="middle" font-size="10" fill="#526a7e">of goal</text></svg></div>'''
    left, right = st.columns([1, 2])
    with left:
        st.markdown(pie_svg, unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;color:#526a7e;font-size:.9rem'><b style='color:#0785a2'>{logged:,} ml logged</b><br>{remaining_ml:,} ml remaining</div>", unsafe_allow_html=True)
        # A real, data-driven pie chart complements the animated progress ring.
        # The remaining slice becomes zero once the goal is reached.
        pie_data = {"Status": ["Completed", "Remaining"],
                    "Water (ml)": [min(logged, st.session_state.goal), remaining_ml]}
        st.vega_lite_chart(
            pie_data,
            {
                "mark": {"type": "arc", "innerRadius": 48, "cornerRadius": 5},
                "encoding": {
                    "theta": {"field": "Water (ml)", "type": "quantitative"},
                    "color": {"field": "Status", "type": "nominal",
                              "scale": {"domain": ["Completed", "Remaining"],
                                        "range": ["#0e9fbd", "#dceef5"]},
                              "legend": {"orient": "bottom"}},
                    "tooltip": [{"field": "Status"}, {"field": "Water (ml)", "type": "quantitative"}]
                },
                "view": {"stroke": None}
            },
            use_container_width=True
        )
        st.caption("Do not force fluids just to hit a number.")
    with right:
        if st.session_state.log:
            cum, running = [], 0
            for x in st.session_state.log:
                running += x
                cum.append(running)
            st.subheader("Intake across today's entries")
            st.line_chart({"Cumulative intake (ml)": cum}, height=220)
            st.bar_chart({"Each drink (ml)": st.session_state.log}, height=180)
            st.caption("Each point/bar represents a water log from this session.")
        else:
            st.info("Log your first drink to bring your charts to life.")
    st.subheader("You vs the standard target")
    std = AGE_GOALS[st.session_state.age]
    st.vega_lite_chart([{"Bar": "Logged today", "ml": total()}, {"Bar": "Your goal", "ml": st.session_state.goal},
                        {"Bar": f"Standard ({st.session_state.age})", "ml": std}], {
        "mark": {"type": "bar", "cornerRadiusEnd": 6},
        "encoding": {"y": {"field": "Bar", "type": "nominal", "sort": None, "title": None},
                     "x": {"field": "ml", "type": "quantitative", "title": "ml"},
                     "color": {"field": "Bar", "type": "nominal", "legend": None,
                               "scale": {"range": ["#0e9fbd", "#0b3a66", "#8bbfe5"]}},
                     "tooltip": [{"field": "Bar"}, {"field": "ml"}]}}, use_container_width=True)
    st.subheader("End of day")
    if st.session_state.get("eod"):
        p = percent()
        note = ("Goal reached. Lovely work today." if p >= 100 else "Over halfway. A good day." if p >= 50
                else "A start is a start. Tomorrow is a fresh page.")
        avg = round(total() / len(st.session_state.log)) if st.session_state.log else 0
        st.markdown(f'<div class="eod"><div class="eodh">Great job today!</div><div class="eodn"><span class="cnt" style="--to:{total()}"></span> ml</div>'
                    f'<div>{round(p)}% of your {st.session_state.goal} ml goal · {len(st.session_state.log)} entries · average {avg} ml</div>'
                    f'<div class="eodm">{note}</div></div>', unsafe_allow_html=True)
        st.button("Start a new day", key="eod_new", on_click=new_day)
    else:
        st.button("Finish my day", key="eod_btn", on_click=lambda: st.session_state.update(eod=True))
    st.subheader("Your hydration spiral")
    t1, t2 = st.columns([1, 2])
    t1.markdown(turtle_svg(percent()), unsafe_allow_html=True)
    t2.write("A Turtle-graphics style drawing built with a Python loop: go forward, turn 59°, go a little further, repeat. "
             "The more of your goal you reach, the more steps the turtle takes, and the dark dot marks where it is now.")
    st.subheader("Deeper look")
    g1, g2 = st.columns(2)
    pct = percent()
    with g1:
        st.markdown("**Milestone journey**")
        st.vega_lite_chart([{"Milestone": f"{t}%", "Reached": min(pct, t) / t * 100} for t in (25, 50, 75, 100)], {
            "mark": {"type": "bar", "cornerRadiusEnd": 6, "color": "#0e9fbd"},
            "encoding": {"y": {"field": "Milestone", "type": "ordinal", "sort": None, "title": None},
                         "x": {"field": "Reached", "type": "quantitative", "scale": {"domain": [0, 100]},
                               "title": "% of each milestone completed"},
                         "tooltip": [{"field": "Milestone"}, {"field": "Reached", "format": ".0f"}]}},
            use_container_width=True)
    with g2:
        st.markdown("**Where your water came from**")
        if st.session_state.log:
            sizes = {}
            for x in st.session_state.log: sizes[f"{x} ml"] = sizes.get(f"{x} ml", 0) + x
            st.vega_lite_chart([{"Drink": k, "Water (ml)": v} for k, v in sizes.items()], {
                "mark": {"type": "arc", "innerRadius": 45, "cornerRadius": 4},
                "encoding": {"theta": {"field": "Water (ml)", "type": "quantitative"},
                             "color": {"field": "Drink", "type": "nominal",
                                       "scale": {"range": ["#0e9fbd", "#5ccfe6", "#0b2545", "#7bc6d9", "#2f6f8f"]},
                                       "legend": {"orient": "bottom"}},
                             "tooltip": [{"field": "Drink"}, {"field": "Water (ml)"}]},
                "view": {"stroke": None}}, use_container_width=True)
        else:
            st.info("Your drink sizes will appear here.")
    if len(st.session_state.times) == len(st.session_state.log) and st.session_state.log:
        t0, run, rows = st.session_state.times[0], 0, []
        for t, x in zip(st.session_state.times, st.session_state.log):
            run += x
            rows.append({"Minutes since first sip": round((t - t0) / 60, 1), "Total (ml)": run})
        st.markdown("**Pace through your session** (dashed line = your goal)")
        st.vega_lite_chart(rows, {"layer": [
            {"mark": {"type": "area", "line": {"color": "#0e9fbd"}, "color": "#0e9fbd", "opacity": 0.25,
                      "interpolate": "step-after", "point": True},
             "encoding": {"x": {"field": "Minutes since first sip", "type": "quantitative"},
                          "y": {"field": "Total (ml)", "type": "quantitative"}}},
            {"mark": {"type": "rule", "strokeDash": [6, 4], "color": "#0b2545"},
             "encoding": {"y": {"datum": st.session_state.goal}}}]}, use_container_width=True)
    st.caption("Session-only data: no weekly history is stored, so these charts do not invent past-day data.")

def page_log():
    page_title("📋 Drink Log")
    show_flash()
    if not st.session_state.log:
        st.info("Nothing logged yet. Add water from the Dashboard or Water Tracker.")
        return
    t0 = st.session_state.times[0] if len(st.session_state.times) == len(st.session_state.log) else None
    rows, run = [], 0
    for i, ml in enumerate(st.session_state.log):
        run += ml
        mins = round((st.session_state.times[i] - t0) / 60, 1) if t0 else None
        rows.append({"Entry": i + 1, "Water (ml)": ml, "Running total (ml)": run, "Minutes after first sip": mins})
    st.dataframe(rows, hide_index=True)
    c1, c2 = st.columns(2)
    c1.button("Undo last entry", key="log_undo", on_click=undo)
    csv = "entry,ml,running_total_ml\n" + "\n".join(f"{r['Entry']},{r['Water (ml)']},{r['Running total (ml)']}" for r in rows)
    c2.download_button("Download as CSV", csv, "waterbuddy_log.csv", "text/csv", key="log_dl")
    st.caption("Session-only log. It disappears when you close the page unless you download it.")

def page_planner():
    page_title("⏰ Sip Planner")
    st.write("Spread your goal across your day in small, comfortable sips. This is a planning aid; "
             "the app cannot send reminders.")
    c1, c2, c3 = st.columns(3)
    wake = c1.time_input("Wake-up time", datetime.time(7, 0), key="sp_wake")
    sleep = c2.time_input("Bedtime", datetime.time(22, 0), key="sp_sleep")
    size = c3.number_input("Sip size (ml)", 100, 500, 250, 50, key="sp_size")
    awake = (sleep.hour * 60 + sleep.minute) - (wake.hour * 60 + wake.minute)
    if awake < 120:
        st.error("Please choose a bedtime at least 2 hours after you wake up.")
        return
    slots = max(1, min(24, math.ceil(st.session_state.goal / size)))
    gap = awake / slots
    done = int(total() // size)
    items = []
    for i in range(slots):
        m = wake.hour * 60 + wake.minute + gap * (i + 0.5)
        state = "done" if i < done else "todo"
        items.append(f'<div class="tl {state}" style="animation-delay:{i*0.05:.2f}s"><b>{int(m//60):02d}:{int(m%60):02d}</b>'
                     f'<span>{size} ml</span></div>')
    st.markdown(f'<div class="tlrow">{"".join(items)}</div>', unsafe_allow_html=True)
    st.caption(f"{slots} sips of {size} ml ≈ one every {gap:.0f} minutes. Filled slots match what you've logged. "
               "Skip, shift or shrink them to suit your day.")

def reset_quiz():
    st.session_state.quiz_checked = False
    for i in range(len(QUIZ)): st.session_state[f"qz{i}"] = None
def check_quiz(): st.session_state.quiz_checked = True

def page_quiz():
    page_title("🧠 Hydration Quiz")
    st.write("Five quick questions. No pressure; it's just for learning.")
    checked = st.session_state.get("quiz_checked", False)
    score = 0
    for i, (q, opts, ans, why) in enumerate(QUIZ):
        pick = st.radio(f"{i+1}. {q}", opts, index=None, key=f"qz{i}", disabled=checked)
        if checked:
            ok = pick == opts[ans]
            score += ok
            (st.success if ok else st.warning)(("Correct. " if ok else f"Answer: {opts[ans]}. ") + why)
    if checked:
        st.markdown(f'<div class="nm">You scored <b>{score} / {len(QUIZ)}</b></div>', unsafe_allow_html=True)
        st.button("Try again", key="qz_again", on_click=reset_quiz)
    else:
        ready = all(st.session_state.get(f"qz{i}") for i in range(len(QUIZ)))
        st.button("Check answers", key="qz_check", on_click=check_quiz, disabled=not ready, type="primary")

def next_tip():
    """Pick a different random tip from the TIPS list."""
    choices = [i for i in range(len(TIPS)) if i != st.session_state.tip_i % len(TIPS)]
    st.session_state.tip_i = random.choice(choices)

def page_tips():
    page_title("💡 Hydration Tips")
    tip, why = TIPS[st.session_state.tip_i % len(TIPS)]
    st.markdown(f'<div class="mascot"><b>{tip}</b><br>{why}</div>', unsafe_allow_html=True)
    st.button("Show another tip", on_click=next_tip)
    st.caption("General guidance only. Sources: [USDA](https://fdc.nal.usda.gov/) · "
               "[NIH](https://www.nih.gov/) · [WHO](https://www.who.int/)")

def page_checker():
    page_title("🔍 Hydration Impact Checker")
    st.write("Find out how much water is in a food or drink. This is an educational tool, not a "
             "dehydration or medical calculator.")
    q = st.text_input("Search food or drink", key="food_q")
    names = [n for n in FOODS if q.lower() in n.lower()] if q else list(FOODS)
    if not names:
        st.warning("No match in this small starter database.")
        return
    # Search changes the selectbox options. Clear a now-invalid selection before
    # Streamlit instantiates the widget, avoiding stale widget-state errors.
    if st.session_state.get("food_sel") not in names:
        st.session_state["food_sel"] = names[0]
    c1, c2, c3 = st.columns([2, 1, 1])
    food = c1.selectbox("Food", names, key="food_sel")
    unit = c3.selectbox("Unit", ["grams", "millilitres"], key="food_unit")
    amt = c2.number_input("Serving size", 1.0, 5000.0, 200.0, 10.0, key="food_amt")
    pct, note = FOODS[food]
    with st.container(border=True):
        st.subheader(food)
        st.write(f"Serving: {amt:g} {'g' if unit == 'grams' else 'ml'}")
        if pct is None:
            st.write("Water percentage: **Data unavailable**")
        else:
            w = amt * pct / 100
            cat = ("Very high" if pct >= 90 else "High" if pct >= 75 else "Moderate" if pct >= 40 else "Low")
            st.write(f"Water percentage: **{pct}%** · category: **{cat} water content**")
            st.write(f"Estimated water: **{w:.0f} ml** ({amt:g} × {pct} ÷ 100 = {w:.0f} g ≈ {w:.0f} ml)")
        st.write(note)
        st.caption("Categories: ≥90% very high, 75–89% high, 40–74% moderate, <40% low (our own simple "
                   "ranges). Water in food is not the same as water the body keeps. 1 g water ≈ 1 ml; "
                   "milk and other drinks are treated the same way for simplicity. "
                   f"Values are approximate, from [USDA FoodData Central]({FDC}); the database here is a "
                   "small local list, not a live service. Educational only.")
    st.markdown("**How your pick compares** (water % in the starter database)")
    rows = [{"Food": n, "Water %": v[0], "Selected": n == food} for n, v in FOODS.items() if v[0] is not None]
    st.vega_lite_chart(rows, {"mark": {"type": "bar", "cornerRadiusEnd": 5},
        "encoding": {"y": {"field": "Food", "type": "nominal", "sort": "-x", "title": None},
                     "x": {"field": "Water %", "type": "quantitative", "scale": {"domain": [0, 100]}},
                     "color": {"condition": {"test": "datum.Selected", "value": "#0b2545"}, "value": "#0e9fbd"},
                     "tooltip": [{"field": "Food"}, {"field": "Water %"}]}}, use_container_width=True)

def page_infuse():
    page_title("🍋 Infuse & Learn")
    st.write("Educational guide: normal hydration supports health, but adding an ingredient does not "
             "automatically give extra, measurable benefits. Always check with a doctor for health concerns.")
    st.subheader("Build a refreshing drink — evidence first")
    st.caption("For most everyday situations, plain safe drinking water is an excellent choice. Add-ins are mainly for taste; they are not detoxes or treatments.")
    ideas = [
        ("🍋 Lemon + mint", "A few washed lemon slices and mint leaves", "Adds flavour; vitamin C in a few slices is modest. Acidic lemon can affect tooth enamel, so avoid sipping acidic water all day."),
        ("🥒 Cucumber + mint", "A few cucumber slices and washed mint", "A refreshing, low-sugar flavour option. Infusing does not transfer the cucumber's full nutrients into the water."),
        ("🍊 Orange + cinnamon", "One orange slice and a small cinnamon stick", "Adds aroma and flavour without needing syrup. Use culinary amounts; avoid concentrated extracts."),
        ("🫚 Ginger + lemon", "A thin slice of fresh ginger and a little lemon", "Strong flavour may make water more appealing; it is not a proven detox or disease treatment. Ginger may bother some stomachs."),
        ("🧂 Electrolytes — only when useful", "Use a properly labelled oral rehydration solution (ORS) when indicated, following its packet directions", "Electrolytes can matter during significant fluid loss, such as diarrhoea or vomiting. Do not casually add salt to daily water; ask a trusted adult/health professional if unwell.")
    ]
    for title, ingredients, science in ideas:
        with st.expander(title):
            st.write(f"**Try:** {ingredients}")
            st.write(f"**Science note:** {science}")
    st.warning("Avoid adding salt, large amounts of sugar, supplements, or essential oils to routine drinking water. Do not use infused water as a replacement for meals or medical care. Wash produce and refrigerate infused water; make a fresh batch daily.")
    with st.expander("What do the evidence labels mean?"):
        for k, v in LABEL_HELP.items(): st.write(f"**{k}:** {v}")
    cats = ["All"] + sorted({v["cat"] for v in INGREDIENTS.values()})
    c1, c2 = st.columns(2)
    q = c1.text_input("Search ingredients", key="ing_q")
    cat = c2.selectbox("Category", cats, key="ing_cat")
    for n, d in INGREDIENTS.items():
        if (q and q.lower() not in n.lower()) or (cat != "All" and d["cat"] != cat): continue
        with st.expander(f'{d["icon"]} {n}  ·  {d["hindi"]}'):
            st.write(d["desc"])
            st.write(f"**Nutrients:** {d['nutrients']}  \n**Taste:** {d['taste']}  \n**How it's used:** {d['use']}")
            st.write(f"**Water contribution:** {d['water']}")
            for cl, lab in d["claims"]: st.write(f"- {cl} — <span class='tag'>{lab}</span>", unsafe_allow_html=True)
            st.write(f"**Precautions:** {d['care']}")
            st.caption("Sources: " + " · ".join(f"[{t}]({u})" for t, u in d["src"]) +
                       ". Links go to the organisation's website; evidence labels are our simplified summary.")
    st.subheader("Compare two ingredients")
    a, b = st.columns(2)
    x = a.selectbox("First", list(INGREDIENTS), key="cmp_a")
    y = b.selectbox("Second", list(INGREDIENTS), index=1, key="cmp_b")
    for col, n in ((a, x), (b, y)):
        d = INGREDIENTS[n]
        with col:
            st.markdown(f"**{n}**")
            st.write(f"Nutrients: {d['nutrients']}\n\nWater: {d['water']}\n\nTaste: {d['taste']}\n\nPrecautions: {d['care']}")
            for cl, lab in d["claims"]: st.write(f"- {cl} ({lab})")
    st.caption("No ingredient is 'the healthiest': it depends on your diet, needs and tastes.")

def page_converter():
    page_title("🔄 Unit Converter")
    st.caption(f"Assumed cup size: {CUP_ML} ml (a US cup; a metric cup is 250 ml).")
    mode = st.selectbox("Conversion", ["ml → litres", "litres → ml", "cups → ml", "ml → cups"], key="conv_m")
    v = st.number_input("Value", 0.0, 1_000_000.0, 250.0, key="conv_v")
    r = {"ml → litres": (v / 1000, "L"), "litres → ml": (v * 1000, "ml"),
         "cups → ml": (v * CUP_ML, "ml"), "ml → cups": (v / CUP_ML, "cups")}[mode]
    st.success(f"{v:g} → **{r[0]:.3g} {r[1]}**")

def page_ach():
    page_title("🏅 Achievements")
    for n, d in [("First Log", "Record your first entry"), ("Quarter Way", "Reach 25%"),
                 ("Halfway There", "Reach 50%"), ("Almost There", "Reach 75%"), ("Goal Reached", "Reach 100%")]:
        st.write(("✅ " if n in st.session_state.ach else "🔒 ") + f"**{n}**: {d}")
    st.caption("Achievements are for fun. Never drink more than you need to unlock one.")

def page_profile():
    page_title("👤 Profile & Daily Goal")
    goal_controls("pr")
    st.info("Changing the age group sets the suggested goal; you can then adjust it yourself.")

def page_settings():
    page_title("⚙️ Settings")
    show_flash()
    st.write("Dark mode: use the switch in the sidebar.")
    st.button("Reset all water records", key="set_reset", on_click=reset)
    st.subheader("Privacy")
    st.write("WaterBuddy collects no personal information. Your entries live only in this browser "
             "session (`st.session_state`) and are lost when you close or refresh the page.")
    st.caption("This is an educational student project, not medical advice.")

# ---------------------------------------------------------------- MAIN
import streamlit.components.v1 as components





init_state()
st.markdown(CSS, unsafe_allow_html=True)
if st.session_state.get("dark"):
    st.markdown(DARK_CSS, unsafe_allow_html=True)
st.markdown(f'''<div class="wbbg"><video autoplay loop muted playsinline src="{HERO_VIDEO}"></video><div class="wbwash"></div>
<div class="wbwaves"><i></i><i></i><i></i></div>{BUBBLES}</div>''', unsafe_allow_html=True)
# Sidebar navigation: keep the menu visible and easy to scan.
NOTES = ["Small sips add up.", "One glass at a time.", "Steady beats rushed.", "Sip, smile, repeat.", "Be kind to yourself."]
with st.sidebar:
    st.markdown(f'<div class="sbx-brand"><span class="sbx-logo">{drop_svg(40, 50)}</span><div><div class="sbx-name">WaterBuddy</div>'
                '<div class="sbx-tag">Small sips. Better habits.</div></div></div>', unsafe_allow_html=True)
    st.radio("Navigate", list(PAGES), key="page", format_func=lambda p: f"{list(PAGES).index(p)+1:02d}   {p}", label_visibility="collapsed")
    st.toggle("Dark mode", value=st.session_state.get("dark", False), key="dark_sb",
              on_change=lambda: st.session_state.update(dark=st.session_state.dark_sb))
    st.markdown(f'<div class="sbx-card"><div class="t">Today</div><div class="n">{total()} / {st.session_state.goal} ml</div>'
                f'<div class="bar"><i style="width:{min(percent(), 100):.0f}%"></i></div>'
                f'<div class="note">Tip of the day: {TIPS[datetime.date.today().toordinal() % len(TIPS)][0]}</div></div>'
                '<div class="sbx-foot">Educational project · not medical advice</div>', unsafe_allow_html=True)

c1, c2 = st.columns([5, 1])
with c1:
    st.markdown('<div class="topbar"><div><div style="font-size:.78rem;color:#7890a2;font-weight:700;letter-spacing:.08em;text-transform:uppercase">WATERBUDDY</div><div style="font-size:1.15rem;font-weight:800;color:#24465b">Your hydration, at a glance</div></div></div>', unsafe_allow_html=True)
with c2:
    st.toggle("Sound", key="sound_on")
js = SOUND_BOOT + SCROLL_BOOT + DITHER_BOOT + SIDE_BOOT          # injected once into the page
js += "<script>window.parent.__wb.on=" + ("true" if st.session_state.sound_on else "false") + ";</script>"
if st.session_state.celebrate:
    js += "<script>if(window.parent.__wb.on){window.parent.__wb.chime();window.parent.__wb.confetti();}</script>"
    st.session_state.celebrate = False
js += "<script>window.parent.document.body.classList.toggle('wb-dark'," + ("true" if st.session_state.get("dark") else "false") + ")</script>"
components.html(js, height=0)
{"Dashboard": page_dashboard, "Water Tracker": page_tracker, "Drink Log": page_log, "My Progress": page_progress, "Sip Planner": page_planner, "Hydration Quiz": page_quiz,
 "Hydration Tips": page_tips, "Hydration Impact Checker": page_checker, "Infuse & Learn": page_infuse,
 "Unit Converter": page_converter, "Achievements": page_ach, "Profile & Daily Goal": page_profile,
 "Settings": page_settings}[st.session_state.page]()
