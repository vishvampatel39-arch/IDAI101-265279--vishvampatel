"""WaterBuddy – pure hydration logic.

Nothing in this file imports Streamlit, so it can be imported and tested
anywhere (for example by pytest) without starting the app.
"""

MIN_ENTRY_ML = 1
MAX_ENTRY_ML = 2000


def compute_hydration_metrics(logs, goal):
    """Return the core hydration numbers.

    - total      = sum of all logged amounts (ml)
    - remaining  = max(0, goal - total)
    - percentage = total / goal * 100, rounded DOWN to 1 decimal place
                   (rounding down means 1999 of 2000 ml shows 99.9%, never 100.0%)
    - visual_pct = percentage limited to the range 0-100 (used for bars)
    """
    total = int(sum(int(item["amount"]) for item in logs))
    safe_goal = int(goal) if goal is not None else 0
    remaining = max(0, safe_goal - total)

    if safe_goal <= 0:
        percentage = 0.0
    else:
        # Integer arithmetic avoids floating-point surprises such as 29.999999.
        percentage = (total * 1000 // safe_goal) / 10

    visual_pct = min(100.0, max(0.0, percentage))
    return {
        "total": total,
        "goal": safe_goal,
        "remaining": remaining,
        "percentage": percentage,
        "visual_pct": visual_pct,
    }


def validate_amount(amount):
    """Check a water amount. Returns (value, error_message); one of them is None."""
    try:
        value = int(amount)
    except (ValueError, TypeError):
        return None, "Please enter a valid whole number in ml."

    if value < MIN_ENTRY_ML or value > MAX_ENTRY_ML:
        return None, (
            f"Validated range: Please enter an amount between "
            f"{MIN_ENTRY_ML} ml and {MAX_ENTRY_ML} ml."
        )
    return value, None


def get_milestone_info(percentage, total):
    """Return (badge title, message, colour) for the current progress.

    Milestones at 25 / 50 / 75 / 100 %, plus a separate 'goal exceeded'
    message (>100 %) that does NOT encourage drinking more.
    """
    if total == 0:
        return (
            "Ready to Begin",
            "Take your first small sip today whenever you feel ready. Every drop counts!",
            "#0e7c9b",
        )
    if percentage > 100.0:
        return (
            "Daily Goal Exceeded",
            "You have moved past 100% of your planned daily goal. Listen to your body's "
            "natural thirst cues—there is no need to drink extra water just for numbers.",
            "#0b2545",
        )
    if percentage == 100.0:
        return (
            "100% Milestone – Goal Reached!",
            "Wonderful consistency! You have reached 100% of your daily hydration target.",
            "#0e7c9b",
        )
    if percentage >= 75.0:
        return (
            "75% Milestone – Almost There!",
            "You are three-quarters of the way through your daily goal. Steady and comfortable!",
            "#0e7c9b",
        )
    if percentage >= 50.0:
        return (
            "50% Milestone – Halfway There!",
            "Great rhythm! You have reached the halfway mark for today's hydration goal.",
            "#0e7c9b",
        )
    if percentage >= 25.0:
        return (
            "25% Milestone – Quarter Way!",
            "Nice start! You are one-quarter of the way to your daily goal. Keep a steady pace.",
            "#0e7c9b",
        )
    return (
        "Off to a Good Start",
        "You have logged your first sips today. Small sips build better habits!",
        "#0e7c9b",
    )


def classify_food_hydration(water_pct):
    """Return (label, colour) for a food's water percentage."""
    if water_pct is None:
        return "Data unavailable", "#64748b"
    if water_pct >= 90.0:
        return "Very High (≥90%)", "#0d9488"
    if water_pct >= 75.0:
        return "High (75–89%)", "#0e7c9b"
    if water_pct >= 40.0:
        return "Moderate (40–74%)", "#d97706"
    return "Low (<40%)", "#64748b"


def get_unlocked_achievements(logs, percentage):
    """Work out the 5 achievements from real session data only."""
    has_logs = len(logs) > 0
    return [
        {
            "id": "first_log",
            "title": "First Log",
            "desc": "Record your very first water entry of the session.",
            "rule": "At least 1 logged entry",
            "unlocked": has_logs,
        },
        {
            "id": "quarter_way",
            "title": "Quarter Way",
            "desc": "Reach at least 25% of your daily hydration target.",
            "rule": "Progress ≥ 25%",
            "unlocked": has_logs and percentage >= 25.0,
        },
        {
            "id": "halfway_there",
            "title": "Halfway There",
            "desc": "Reach 50% of your daily hydration target.",
            "rule": "Progress ≥ 50%",
            "unlocked": has_logs and percentage >= 50.0,
        },
        {
            "id": "almost_there",
            "title": "Almost There",
            "desc": "Reach 75% of your daily hydration target.",
            "rule": "Progress ≥ 75%",
            "unlocked": has_logs and percentage >= 75.0,
        },
        {
            "id": "goal_reached",
            "title": "Goal Reached",
            "desc": "Complete 100% of your daily hydration target.",
            "rule": "Progress ≥ 100%",
            "unlocked": has_logs and percentage >= 100.0,
        },
    ]
