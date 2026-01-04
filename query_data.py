import argparse
from langchain_community.vectorstores import Chroma
from clause_semantics import tag_clause_semantics
from clause_graph import build_clause_graph
from reasoning_paths import extract_reasoning_paths


from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()

    clauses = retrieve_clauses(args.query_text)

    print("\nRelevant Policy Clauses (Semantic-Tagged)")
    print("=" * 65)

    for i, clause in enumerate(clauses, 1):
        print(f"\nClause {i}")
        print(f"Page Number : {clause['page_number']}")
        print(f"Similarity  : {clause['similarity_score']}")
        print(f"Topics      : {clause['topics']}")
        print(f"Treatments  : {clause['treatments']}")
        print(f"Mentions Tx : {clause['mentions_treatment']}")
        print("Clause Text :")
        print(clause["clause_text"][:900])
        print("-" * 65)

    graph = build_clause_graph(clauses)

    print("\nClause Relationship Graph")
    print("=" * 65)

    for node, edges in graph.items():
        print(f"\nClause (Page {node}) is related to:")
        for edge in edges:
            print(
                f"  → Clause (Page {edge['connected_to']}) | Relations: {edge['relations']}"
        )
            
    paths = extract_reasoning_paths(clauses, graph)

    print("\nReasoning Paths (Ranked)")
    print("=" * 65)

    for i, p in enumerate(paths[:5], 1):  # show top 5
        print(f"\nPath {i} | Score: {p['score']}")
        for c in p["clauses"]:
            print(
                f"  Clause Page {c['page']} | Topics: {c['topics']} | Treatments: {c['treatments']}"
            )
        print(f"  Relations: {p['relations']}")
        print("-" * 65)




def retrieve_clauses(query_text: str, top_k: int = 5):
    embedding_function = get_embedding_function()

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function
    )

    results = db.similarity_search_with_score(query_text, k=top_k)

    structured_clauses = []

    for doc, score in results:
        semantics = tag_clause_semantics(doc.page_content)

        structured_clauses.append({
            "clause_text": doc.page_content.strip(),
            "page_number": doc.metadata.get("page", "unknown"),
            "source": doc.metadata.get("source", "policy"),
            "similarity_score": round(score, 4),
            "topics": semantics["topics"],
            "treatments": semantics["treatments"],
            "mentions_treatment": semantics["mentions_treatment"]
        })

    return structured_clauses



if __name__ == "__main__":
    main()
