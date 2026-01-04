def decide_eligibility(explanation):
    """
    Deterministic eligibility decision based on structured explanation.
    No rules, no LLM.
    """

    details = explanation.get("details", [])
    relations = explanation.get("relations", [])
    confidence = explanation.get("confidence_score", 0)

    has_waiting_constraint = any(
        "waiting-period" in d["explanation"].lower()
        for d in details
    )

    has_treatment_clause = any(
        d["treatments"] for d in details
    )

    has_exception = any(
        "exception" in d["topics"] for d in details
    )

    # Decision logic (signal-based, not rule-based)
    if has_waiting_constraint and not has_exception:
        decision = "Rejected"
        reason = "A waiting-period constraint applies based on relevant policy clauses."

    elif has_treatment_clause and not has_waiting_constraint:
        decision = "Approved"
        reason = "The treatment is covered and no restricting conditions were identified."

    else:
        decision = "Needs Review"
        reason = (
            "The policy clauses provide mixed or insufficient signals to make a final determination."
        )

    evidence = [
        {
            "page": d["page"],
            "topics": d["topics"],
            "treatments": d["treatments"]
        }
        for d in details
    ]

    return {
        "decision": decision,
        "reason": reason,
        "confidence": confidence,
        "evidence": evidence
    }
