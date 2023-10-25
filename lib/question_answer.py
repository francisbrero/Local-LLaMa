"""
This module contains the implementation of the question answering system.
"""
DEFAULT_MIN_SIMILARITY_SCORE = 0.5
DEFAULT_NUM_RELEVANT_DOCS = 4


def answer(
    question,
    vector_db,
    chain,
    min_similarity_score=DEFAULT_MIN_SIMILARITY_SCORE,
    num_relevant_docs=DEFAULT_NUM_RELEVANT_DOCS,
    verbose=False,
):
    """
    Answer a question using the given vector database and chain.

    Args:
        question (str): The question to answer.
        vector_db (VectorDB): The vector database.
        chain (LLMChain): The LLAMA chain for question answering.
        min_similarity_score (float): The minimum similarity score to consider a document relevant.
        num_relevant_docs (int): The number of relevant documents to consider.
        verbose (bool): Whether to print verbose information.

    Returns:
        Tuple[str, Set[str]]: The answer and the sources.
    """
    docs = vector_db.similarity_search_with_relevance_scores(
        question, k=num_relevant_docs
    )
    relevant_docs = [
        (doc, score) for doc, score in docs if score >= min_similarity_score
    ]

    if verbose:
        print()
        print("Relevant docs")
        for doc, score in relevant_docs:
            print("-" * 100)
            print(score)
            print(doc.page_content)
        print("#" * 100)

    print("Thinking...")

    context = " ".join([doc.page_content for doc, _ in relevant_docs])
    sources = set([doc.metadata["source"] for doc, _ in relevant_docs])

    return chain.run(context=context, question=question), sources
