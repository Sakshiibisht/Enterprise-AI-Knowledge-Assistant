from transformers import pipeline

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-small"
)


def get_answer(vectorstore, query):

    docs = vectorstore.similarity_search(query)

    context = "\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
    Answer the question based on the context below.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    result = generator(
        prompt,
        max_length=256,
        do_sample=False
    )

    return result[0]["generated_text"]