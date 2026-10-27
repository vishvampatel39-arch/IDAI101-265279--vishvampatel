"""Tests for WaterBuddy. Run with:  pytest -v"""

from streamlit.testing.v1 import AppTest

from logic import (
    classify_food_hydration,
    compute_hydration_metrics,
    get_milestone_info,
    get_unlocked_achievements,
    validate_amount,
)

NAV = "nav_page_radio"


# ------------------------------------------------------------------ pure logic
def test_core_hydration_maths_and_zero_goal():
    m = compute_hydration_metrics([{"amount": 500}, {"amount": 250}], 2000)
    assert m["total"] == 750
    assert m["remaining"] == 1250
    assert m["percentage"] == 37.5
    assert m["visual_pct"] == 37.5

    # Over the goal: percentage can pass 100, the visual bar stops at 100
    m_over = compute_hydration_metrics([{"amount": 1800}], 1600)
    assert m_over["total"] == 1800
    assert m_over["remaining"] == 0
    assert m_over["percentage"] == 112.5
    assert m_over["visual_pct"] == 100.0

    # Zero goal must not crash
    m_zero = compute_hydration_metrics([{"amount": 250}], 0)
    assert m_zero["total"] == 250
    assert m_zero["remaining"] == 0
    assert m_zero["percentage"] == 0.0
    assert m_zero["visual_pct"] == 0.0


def test_milestone_and_goal_exceeded_messages():
    assert "25%" in get_milestone_info(25.0, 400)[0]
    assert "50%" in get_milestone_info(50.0, 800)[0]
    assert "75%" in get_milestone_info(75.0, 1200)[0]
    assert "100%" in get_milestone_info(100.0, 1600)[0]

    title_over, msg_over, _ = get_milestone_info(115.0, 1840)
    assert "Exceeded" in title_over
    assert "no need to drink extra" in msg_over.lower()


def test_food_categories_and_missing_data():
    assert classify_food_hydration(95.0)[0] == "Very High (≥90%)"
    assert classify_food_hydration(85.0)[0] == "High (75–89%)"
    assert classify_food_hydration(68.0)[0] == "Moderate (40–74%)"
    assert classify_food_hydration(2.0)[0] == "Low (<40%)"
    assert classify_food_hydration(None)[0] == "Data unavailable"


def test_no_false_goal_reached_when_short():
    logs = [{"amount": 1999}]
    m = compute_hydration_metrics(logs, 2000)
    assert m["remaining"] == 1
    assert m["percentage"] < 100.0

    title, _, _ = get_milestone_info(m["percentage"], m["total"])
    assert "Goal Reached" not in title

    unlocked = {a["id"]: a["unlocked"] for a in get_unlocked_achievements(logs, m["percentage"])}
    assert unlocked["almost_there"] is True
    assert unlocked["goal_reached"] is False


def test_goal_reached_exactly_at_goal():
    logs = [{"amount": 2000}]
    m = compute_hydration_metrics(logs, 2000)
    assert m["percentage"] == 100.0
    assert "Goal Reached" in get_milestone_info(m["percentage"], m["total"])[0]
    unlocked = {a["id"]: a["unlocked"] for a in get_unlocked_achievements(logs, m["percentage"])}
    assert unlocked["goal_reached"] is True


def test_validate_amount():
    assert validate_amount(250) == (250, None)
    assert validate_amount("500") == (500, None)
    assert validate_amount(1)[1] is None
    assert validate_amount(2000)[1] is None
    assert validate_amount(0)[0] is None
    assert validate_amount(2001)[0] is None
    assert validate_amount("abc")[0] is None
    assert validate_amount(None)[0] is None


# ------------------------------------------------------------------ app flow
def new_app():
    return AppTest.from_file("app.py", default_timeout=15).run()


def test_apptest_dashboard_and_navigation_persistence():
    at = new_app()
    assert not at.exception

    at.button(key="dash_add_250_btn").click().run()
    assert len(at.session_state["logs"]) == 1
    assert at.session_state["logs"][0]["amount"] == 250

    at.radio(key=NAV).set_value("Water Tracker").run()
    assert not at.exception
    assert len(at.session_state["logs"]) == 1

    at.number_input(key="custom_amount_input").set_value(500).run()
    at.button(key="tracker_add_custom_btn").click().run()
    assert len(at.session_state["logs"]) == 2
    assert sum(x["amount"] for x in at.session_state["logs"]) == 750

    at.button(key="tracker_undo_btn").click().run()
    assert len(at.session_state["logs"]) == 1

    for page in [
        "My Progress",
        "Hydration Tips",
        "Hydration Impact Checker",
        "Infuse & Learn",
        "Unit Converter",
        "Achievements",
        "Profile & Daily Goal",
        "Settings",
    ]:
        at.radio(key=NAV).set_value(page).run()
        assert not at.exception, page


def test_name_and_settings_survive_page_switch():
    at = new_app()

    at.radio(key=NAV).set_value("Profile & Daily Goal").run()
    at.text_input(key="user_name").set_value("Asha").run()

    at.radio(key=NAV).set_value("Settings").run()
    at.checkbox(key="Show_Math_Formulas").uncheck().run()

    at.radio(key=NAV).set_value("Dashboard").run()
    assert at.session_state["user_name"] == "Asha"
    assert at.session_state["Show_Math_Formulas"] is False


def test_age_preset_updates_goal_and_slider():
    at = new_app()
    at.radio(key=NAV).set_value("Profile & Daily Goal").run()

    at.selectbox(key="profile_age_selector").set_value("19–64 years (Adults)").run()
    at.button(key="apply_age_goal_btn").click().run()

    assert at.session_state["daily_goal"] == 2500
    assert at.session_state["manual_goal_slider"] == 2500
    assert not at.exception


def test_reset_clears_logs():
    at = new_app()
    at.button(key="dash_add_250_btn").click().run()
    at.button(key="dash_add_250_btn").click().run()
    assert len(at.session_state["logs"]) == 2

    at.button(key="dash_reset_btn").click().run()
    assert at.session_state["logs"] == []
    assert at.session_state["next_log_id"] == 1
