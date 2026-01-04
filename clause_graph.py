from collections import defaultdict
import itertools


def build_clause_graph(clauses):
    """
    Build a lightweight relationship graph between clauses.
    Returns adjacency list with edge labels.
    """

    graph = defaultdict(list)

    for c1, c2 in itertools.combinations(clauses, 2):
        relations = []

        # Relationship 1: shared treatment
        shared_treatments = set(c1["treatments"]) & set(c2["treatments"])
        if shared_treatments:
            relations.append({
                "type": "SHARES_TREATMENT",
                "value": list(shared_treatments)
            })

        # Relationship 2: shared topic
        shared_topics = set(c1["topics"]) & set(c2["topics"])
        if shared_topics:
            relations.append({
                "type": "SHARES_TOPIC",
                "value": list(shared_topics)
            })

        # Relationship 3: potential constraint relationship
        if (
            "waiting_period" in c1["topics"]
            and c2["mentions_treatment"]
        ) or (
            "waiting_period" in c2["topics"]
            and c1["mentions_treatment"]
        ):
            relations.append({
                "type": "POTENTIAL_CONSTRAINT",
                "value": "waiting_period"
            })

        if relations:
            graph[c1["page_number"]].append({
                "connected_to": c2["page_number"],
                "relations": relations
            })
            graph[c2["page_number"]].append({
                "connected_to": c1["page_number"],
                "relations": relations
            })

    return graph
