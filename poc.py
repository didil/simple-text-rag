# Proof of concept using a gutenberg book.

from dotenv import load_dotenv
# Load environment variables
load_dotenv()

from processing.pipeline import Pipeline


def main() -> None:
    persist_base_directory = "chroma_db"
    pipeline = Pipeline(persist_base_directory)

    # Download a Project Gutenberg book (e.g., Pride and Prejudice)
    document_url = "https://www.gutenberg.org/files/1342/1342-0.txt"
    collection_name = "pride_and_prejudice"

    document_text = pipeline.download_text(document_url)
    chunks = pipeline.load_and_split_text(document_text)
    vectorstore = pipeline.create_vectorstore(collection_name, chunks)
    qa_chain = pipeline.setup_qa_chain(vectorstore)

    # Interactive Q&A loop
    while True:
        question = input("Ask a question about the document (or type 'quit' to exit): ")
        if question.lower() == 'quit':
            break
        answer = qa_chain.invoke(question)
        print(f"Answer: {answer}\n")


if __name__ == "__main__":
    main()
