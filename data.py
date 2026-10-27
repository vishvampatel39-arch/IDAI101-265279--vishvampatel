"""WaterBuddy content: age goals, page list, food data, ingredient cards, tips and quiz.
Edit this file to add foods, ingredients or tips; no other code needs to change."""

AGE_GOALS = {"6–12 years": 1600, "13–18 years": 2000,
             "19–50 years": 2500, "65 years and above": 2000}

CUP_ML = 240  # assumed US cup; a metric cup is 250 ml

PAGES = {"Dashboard": "🏠", "Water Tracker": "💧", "Drink Log": "📋", "My Progress": "📈", "Sip Planner": "⏰",
         "Hydration Tips": "💡", "Hydration Impact Checker": "🔍", "Infuse & Learn": "🍋",
         "Hydration Quiz": "🧠", "Unit Converter": "🔄",
         "Achievements": "🏅", "Profile & Daily Goal": "👤", "Settings": "⚙️"}

FDC = "https://fdc.nal.usda.gov/"

FOODS = {
    "Plain drinking water": (100.0, "Plain water is 100% water."),
    "Watermelon (raw)": (91.4, "Very water-rich fruit, with some natural sugar."),
    "Cucumber (raw, with peel)": (95.2, "One of the most water-rich foods."),
    "Tomato (raw)": (94.5, "Mostly water; also provides vitamin C."),
    "Coconut water": (94.5, "Mostly water with some natural sugar and potassium."),
    "Orange (raw)": (86.8, "Water-rich fruit that also gives vitamin C and fibre."),
    "Milk (whole)": (88.1, "A drink that contributes to fluid intake and gives protein and calcium."),
    "Yogurt (plain, whole milk)": (88.1, "Mostly water; also gives protein and calcium."),
    "Apple (raw, with skin)": (85.6, "Water-rich with fibre."),
    "Banana (raw)": (74.9, "Moderate water content; more energy-dense than melon."),
    "Almonds (raw)": (4.4, "Dry food: contributes little water directly but gives fats and protein."),
    "Potato chips (salted)": (1.9, "Dry, salty snack. Sodium can increase thirst, but this tool does not "
                                   "estimate any water loss."),
    "Soup (homemade, varies)": (None, "Water content depends on the recipe, so no single value is given."),
}

INGREDIENTS = {
    "Chia seeds": dict(hindi="Sabja-like (chia; not the same as sabja/basil seeds)", cat="Seeds", icon="🌱",
        desc="Tiny seeds that absorb liquid and form a gel.",
        nutrients="Fibre, plant omega-3 (ALA), protein.", taste="Mild, slightly nutty; gel-like texture.",
        use="Soak in water or milk for 15–20 minutes before drinking; do not swallow dry.",
        water="Adds nutrients, but the water comes from the drink itself.",
        claims=[("Chia seeds as a food provide fibre and plant omega-3 fats.", "Well supported"),
                ("Chia water helps with weight loss.", "Insufficient evidence"),
                ("Chia water clears skin.", "Insufficient evidence")],
        care="Always soak first (dry seeds can swell and cause choking). Ask a doctor if you have swallowing or digestive problems.",
        src=[("USDA FoodData Central", FDC)]),
    "Saunf (fennel seeds)": dict(hindi="Saunf", cat="Seeds & spices", icon="🌿",
        desc="Aromatic seeds used in Indian cooking and often eaten after meals.",
        nutrients="Small amounts of fibre and aromatic plant compounds.", taste="Sweet, anise-like.",
        use="Steep a teaspoon in warm or cool water; strain if you like.",
        water="No meaningful extra water; it flavours the drink.",
        claims=[("Saunf is a traditional digestive aid in India.", "Limited evidence"),
                ("Saunf water detoxifies the body.", "Insufficient evidence")],
        care="Tradition is not proof. People with allergies to celery/carrot family plants should be careful.",
        src=[("NCCIH (US NIH)", "https://www.nccih.nih.gov/"), ("USDA FoodData Central", FDC)]),
    "Jeera (cumin seeds)": dict(hindi="Jeera", cat="Seeds & spices", icon="🟤",
        desc="A common spice with a warm, earthy flavour.",
        nutrients="Small amounts of iron and plant compounds.", taste="Earthy, warm, slightly bitter.",
        use="Soaked or lightly boiled and cooled as a traditional drink.",
        water="No meaningful extra water.",
        claims=[("Jeera is a well-established cooking spice.", "Well supported"),
                ("Jeera water detoxifies or guarantees weight loss.", "Insufficient evidence"),
                ("Jeera water treats disease.", "Insufficient evidence")],
        care="Use ordinary culinary amounts, not concentrated extracts or supplements.",
        src=[("NCCIH (US NIH)", "https://www.nccih.nih.gov/"), ("USDA FoodData Central", FDC)]),
    "Lemon": dict(hindi="Nimbu", cat="Fruit", icon="🍋",
        desc="A citrus fruit that makes water more appealing.",
        nutrients="Vitamin C (mostly from the juice), citric acid.", taste="Sour and fresh.",
        use="Add slices or a small squeeze to cold water.",
        water="Juice is mostly water, but a squeeze adds very little.",
        claims=[("Lemon juice contains vitamin C.", "Well supported"),
                ("Flavoured water can help some people drink more.", "Limited evidence"),
                ("Lemon water removes toxins or improves skin.", "Insufficient evidence")],
        care="Acidic drinks can wear tooth enamel; rinse with plain water after.",
        src=[("USDA FoodData Central", FDC)]),
    "Mint": dict(hindi="Pudina", cat="Herb", icon="🌿",
        desc="A cooling, aromatic herb.", nutrients="Tiny amounts of vitamins at normal use.",
        taste="Cool and fresh.", use="Lightly crush a few leaves and add to cold water.",
        water="No meaningful extra water.",
        claims=[("Mint adds flavour that can make water more enjoyable.", "Well supported"),
                ("Mint water improves digestion or detoxifies.", "Insufficient evidence")],
        care="Wash leaves well. Mint can worsen heartburn for some people.",
        src=[("NCCIH (US NIH)", "https://www.nccih.nih.gov/")]),
    "Cucumber": dict(hindi="Kheera", cat="Vegetable", icon="🥒",
        desc="A crisp vegetable that is about 95% water.", nutrients="Water, small amounts of potassium and vitamin K.",
        taste="Mild and refreshing.", use="Slice thinly and chill in water for a spa-style drink.",
        water="Eating cucumber gives water; soaking slices adds almost none to the drink.",
        claims=[("Cucumber has very high water content.", "Well supported"),
                ("Cucumber-infused water has extra health effects beyond hydration.", "Insufficient evidence")],
        care="Wash well; refrigerate infused water and drink within a day.",
        src=[("USDA FoodData Central", FDC)]),
}

LABEL_HELP = {"Well supported": "Strong evidence for the specific claim.",
              "Limited evidence": "Some evidence, not enough for a confident conclusion.",
              "Insufficient evidence": "Evidence does not establish this claim."}

TIPS = [("Keep a bottle where you can see it.", "Visible cues make it easier to remember to drink."),
        ("Sip with meals.", "Linking drinking to routines builds habits."),
        ("Eat water-rich foods like cucumber or watermelon.", "Foods provide part of daily fluid intake."),
        ("Try a slice of lemon or mint if plain water feels boring.", "Taste can make drinking more pleasant."),
        ("Drink more when it is hot or you exercise.", "Needs vary with weather and activity."),
        ("Your urine colour can be a rough clue.", "Pale yellow is often fine; it is only a rough guide."),
        ("Spread drinks through the day.", "Small regular sips are easier than a lot at once."),
        ("Do not force very large amounts.", "Drinking far more than you need is not helpful.")]

QUIZ = [("Can foods count toward your daily fluid intake?", ["Yes, many foods contain water", "No, only drinks count"], 0,
         "Water-rich foods such as cucumber and watermelon add to your fluid intake."),
        ("Is there one daily water amount that suits everyone?", ["Yes", "No, needs vary"], 1,
         "Needs vary with age, activity, weather, diet and health."),
        ("Roughly how much of a cucumber is water?", ["About 5%", "About 50%", "About 95%"], 2,
         "Cucumber is about 95% water (see the Hydration Impact Checker)."),
        ("You are behind your goal this evening. What is a sensible approach?",
         ["Force down a huge amount at once", "Keep to comfortable sips and don't force it"], 1,
         "Drinking far more than you need isn't helpful. Goals are guides, not deadlines."),
        ("Does urine colour tell you exactly how hydrated you are?", ["Yes, exactly", "No, it is only a rough clue"], 1,
         "Colour is a rough clue and can be changed by foods, vitamins and medicines.")]
