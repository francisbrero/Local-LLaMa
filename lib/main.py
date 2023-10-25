"""
This is the entry point for the question answering system.
"""
import time

import data_loader
import llm
import question_answer

vector_db = data_loader.get_vector_db()
chain = llm.get_qa_chain()

question = ""
STOP = "STOP"
while question != STOP:
    question = input("Ask me any question: \n")

    now = time.time()

    answer, sources = question_answer.answer(
        question, vector_db, chain, verbose=True
    )

    print()
    print()
    print("Sources for answering the question:")
    for source in sources:
        print("-", source)
    print("Elapsed time", time.time() - now, " seconds")
