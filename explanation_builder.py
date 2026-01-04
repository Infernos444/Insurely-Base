def build_structured_explanation(reasoning_paths, clauses):
    """
    Build a structured, human-readable explanation from the top reasoning path.
    No decisions. No LLM.
    """

    if not reasoning_paths:
        return {
            "summary": "No sufficient clause relationships were found to explain the policy impact.",
            "details": []
        }

    # Use the top-ranked path
    top_path = reasoning_paths[0]

    # Index clauses by page for lookup
    clause_by_page = {c["page_number"]: c for c in clauses}

    details = []

    for page in [c["page"] for c in top_path["clauses"]]:
        clause = clause_by_page.get(page)
        if not clause:
            continue

        explanation = {
            "page": page,
            "topics": clause["topics"],
            "treatments": clause["treatments"],
            "explanation": generate_clause_explanation(clause)
        }
        details.append(explanation)

    summary = generate_summary(details)

    return {
        "summary": summary,
        "details": details,
        "relations": top_path["relations"],
        "confidence_score": top_path["score"]
    }


def generate_clause_explanation(clause):
    """
    Deterministic explanation based on clause semantics.
    """

    topics = clause["topics"]
    treatments = clause["treatments"]

    if "waiting_period" in topics:
        return "This clause introduces a waiting-period condition that may restrict eligibility until a specified duration is met."

    if treatments:
        return "This clause refers to procedures related to the queried treatment category."

    if "coverage" in topics:
        return "This clause outlines general coverage provisions applicable to medical procedures."

    if "exclusion" in topics:
        return "This clause describes exclusions that may limit policy applicability."

    return "This clause provides contextual policy information relevant to the procedure."


def generate_summary(details):
    """
    High-level explanation summary.
    """

    has_waiting = any("waiting-period" in d["explanation"] for d in details)

    if has_waiting:
        return (
            "The policy clauses jointly indicate that the queried treatment "
            "is subject to procedural conditions, including a waiting-period constraint."
        )

    return (
        "The policy clauses collectively provide procedural and coverage context "
        "relevant to the queried treatment."
    )
