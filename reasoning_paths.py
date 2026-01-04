from collections import deque

PRIORITY_RELATIONS = {
    "POTENTIAL_CONSTRAINT": 3,
    "SHARES_TREATMENT": 2,
    "SHARES_TOPIC": 1
}

def extract_reasoning_paths(clauses, graph, max_depth=2):
    """
    Extract short, high-signal reasoning paths from the clause graph.
    Returns a list of paths with explanations.
    """

    # Index clauses by page for quick lookup
    clause_by_page = {c["page_number"]: c for c in clauses}

    # Start from clauses that mention the treatment
    start_pages = [
        c["page_number"] for c in clauses if c.get("mentions_treatment")
    ]

    paths = []

    for start in start_pages:
        queue = deque()
        queue.append((start, [start], []))  # (current_page, path_pages, path_relations)

        while queue:
            current, path_pages, path_relations = queue.popleft()

            # Save path if it includes any meaningful relation
            if path_relations:
                paths.append({
                    "path": path_pages.copy(),
                    "relations": path_relations.copy(),
                    "score": sum(PRIORITY_RELATIONS[r["type"]] for r in path_relations)
                })

            # Stop expanding if max depth reached
            if len(path_pages) - 1 >= max_depth:
                continue

            for edge in graph.get(current, []):
                next_page = edge["connected_to"]
                if next_page in path_pages:
                    continue  # avoid cycles

                for rel in edge["relations"]:
                    queue.append((
                        next_page,
                        path_pages + [next_page],
                        path_relations + [rel]
                    ))

    # Sort paths by score (higher = more important)
    paths.sort(key=lambda x: x["score"], reverse=True)

    # Enrich paths with clause details
    enriched_paths = []
    for p in paths:
        enriched_paths.append({
            "score": p["score"],
            "clauses": [
                {
                    "page": pg,
                    "topics": clause_by_page[pg]["topics"],
                    "treatments": clause_by_page[pg]["treatments"]
                }
                for pg in p["path"]
            ],
            "relations": p["relations"]
        })

    return enriched_paths
