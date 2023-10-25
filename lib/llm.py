"""
This module contains the model for question answering.
"""

from langchain import PromptTemplate, LLMChain
from langchain.llms import CTransformers
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


prompt_template = """[INST] <<SYS>>
You search for relevant information from the given information and answer the user's question. 
No need to give a long answer, just a short answer is enough.
If no relevant information is found, you can answer "I don't know" or "I don't know the answer to that question".
<</SYS>>

Find the answer for question '{question}' from the following pieces of information
{context} [/INST]
"""


def get_qa_chain():
    """
    Returns:
        The chain for question answering.
    """
    llm = CTransformers(
        model="TheBloke/Llama-2-7B-Chat-GGML",
        callbacks=[StreamingStdOutCallbackHandler()],
        # model_file="llama-2-7b.ggmlv3.q5_1.bin",
        model_file="llama-2-7b-chat.ggmlv3.q8_0.bin",
        model_type="llama",
        config={
            "temperature": 0,
            "top_p": 0.95,
            "top_k": 50,
            "context_length": 4096,
            "max_new_tokens": 256,
        },
    )

    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    return LLMChain(prompt=prompt, llm=llm)
