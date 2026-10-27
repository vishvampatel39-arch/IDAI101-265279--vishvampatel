"""Quick self-test for WaterBuddy. Run:  python test_waterbuddy.py   (needs streamlit installed)"""
from streamlit.testing.v1 import AppTest

at = AppTest.from_file("app.py", default_timeout=60).run()
checks = []
def check(name, ok): checks.append((name, bool(ok))); print("PASS" if ok else "FAIL", "-", name)

check("app starts with no errors", not at.exception)
for p in list(at.radio(key="page").options):          # every tab opens
    at.radio(key="page").set_value(p).run()
    check("page opens: " + p.strip()[-22:], not at.exception)

at.radio(key="page").set_value("Water Tracker").run()
for age, goal in [("6–12 years", 1600), ("13–18 years", 2000), ("19–50 years", 2500), ("65 years and above", 2000)]:
    at.selectbox(key="tr_age").set_value(age).run()
    check(f"age {age} suggests {goal} ml", at.session_state.goal == goal)
at.number_input(key="tr_goal").set_value(1000).run()
check("goal can be adjusted manually", at.session_state.goal == 1000)

for _ in range(2): at.button(key="tr_250").click().run()
total = sum(at.session_state.log)
check("two +250 ml entries = 500 ml", total == 500)
check("remaining = goal - total = 500", max(0, at.session_state.goal - total) == 500)
check("percentage = 50%", total / at.session_state.goal * 100 == 50)

at.number_input(key="custom_ml").set_value(300); at.button(key="tr_add").click().run()
check("custom amount adds 300 ml", sum(at.session_state.log) == 800)
at.button(key="tr_undo").click().run()
check("undo removes the last entry", sum(at.session_state.log) == 500)
for _ in range(2): at.button(key="tr_250").click().run()
check("over the goal: total 1000 ml, remaining stays 0", sum(at.session_state.log) == 1000 and max(0, 1000 - 1000) == 0)
check("Goal Reached achievement unlocked", "Goal Reached" in at.session_state.ach)
at.button(key="tr_reset").click().run()
check("reset clears everything", at.session_state.log == [] and not at.session_state.ach)

at.toggle(key="dark_sb").set_value(True).run()
check("dark mode switch turns dark mode on", at.session_state.dark is True and not at.exception)
at.toggle(key="dark_sb").set_value(False).run()
check("dark mode switch turns it off again", at.session_state.dark is False)

print(f"\n{sum(ok for _, ok in checks)} of {len(checks)} checks passed")
