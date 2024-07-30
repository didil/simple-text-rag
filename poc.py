# Proof of concept using a gutenberg book.

from dotenv import load_dotenv
# Load environment variables
load_dotenv()

from processing.pipeline import download_text, load_and_split_text, create_or_load_vectorstore, setup_qa_chain


def main() -> None:

    # Download a Project Gutenberg book (e.g., Pride and Prejudice)
    document_url = "https://www.gutenberg.org/files/1342/1342-0.txt"
    collection_name = "pride_and_prejudice"
    persist_directory = "chroma_db"

    document_text = download_text(document_url)
    chunks = load_and_split_text(document_text)
    vectorstore = create_or_load_vectorstore(persist_directory,
                                             collection_name, chunks)
    qa_chain = setup_qa_chain(vectorstore)

    # Interactive Q&A loop
    while True:
        question = input(
            "Ask a question about the document (or type 'quit' to exit): ")
        if question.lower() == 'quit':
            break
        answer = qa_chain.invoke(question)
        print(f"Answer: {answer}\n")


if __name__ == "__main__":
    main()
