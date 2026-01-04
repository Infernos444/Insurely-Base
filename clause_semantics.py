import re

# Lightweight vocab (can expand later)
TOPIC_KEYWORDS = {
    "waiting_period": [
        "waiting period", "wait period", "pre-existing", "time-bound exclusion"
    ],
    "exclusion": [
        "not covered", "excluded", "exclusion", "shall not be covered", "no cover"
    ],
    "coverage": [
        "covered", "coverage", "benefit", "eligible"
    ],
    "procedure_list": [
        "surgery", "procedure", "treatment"
    ]
}

TREATMENT_KEYWORDS = {
    "cataract": ["cataract"],
    "eye_treatment": ["eye", "ophthalm", "laser eye"],
    "joint_replacement": ["joint replacement", "knee replacement", "hip replacement"],
    "accident": ["accident", "injury", "trauma"]
}


def tag_clause_semantics(text: str):
    text_l = text.lower()
    topics = set()
    treatments = set()

    for topic, kws in TOPIC_KEYWORDS.items():
        if any(kw in text_l for kw in kws):
            topics.add(topic)

    for treatment, kws in TREATMENT_KEYWORDS.items():
        if any(kw in text_l for kw in kws):
            treatments.add(treatment)

    return {
        "topics": sorted(list(topics)),
        "treatments": sorted(list(treatments)),
        "mentions_treatment": len(treatments) > 0
    }
