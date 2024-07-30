import os
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from chromadb.config import Settings
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
import logging


class Pipeline:

    def __init__(self, persist_base_directory: str) -> None:
        self.persist_base_directory = persist_base_directory
        self.embeddings = HuggingFaceEmbeddings()

    def download_text(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def load_and_split_text(self, document_text: str) -> list[str]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                       chunk_overlap=200,
                                                       length_function=len)
        chunks = text_splitter.split_text(document_text)
        return chunks

    def create_vectorstore(self, collection_name: str,
                           chunks: list[str]) -> Chroma:

        persist_directory = os.path.join(self.persist_base_directory,
                                         collection_name)
        logging.info(
            f"Using chroma persistence directory: {persist_directory}")

        logging.info(
            f"Creating new Chroma vector store for collection {collection_name} ..."
        )
        vectorstore = Chroma.from_texts(
            chunks,
            self.embeddings,
            collection_name=collection_name,
            client_settings=Settings(anonymized_telemetry=False,
                                     is_persistent=True,
                                     persist_directory=persist_directory))

        return vectorstore

    def load_vectorstore(self, collection_name: str) -> Chroma:
        persist_directory = os.path.join(self.persist_base_directory,
                                         collection_name)
        logging.info(
            f"Using chroma persistence directory: {persist_directory}")
        if not os.path.exists(persist_directory):
            logging.error(
                f"Chroma vector store not found for collection {collection_name} ..."
            )
            raise ValueError("Chroma vector store not found")

        logging.info(
            f"Loading existing Chroma vector store for collection {collection_name} ..."
        )
        vectorstore = Chroma(persist_directory=persist_directory,
                             embedding_function=self.embeddings,
                             collection_name=collection_name,
                             client_settings=Settings(
                                 anonymized_telemetry=False,
                                 is_persistent=True,
                                 persist_directory=persist_directory))

        return vectorstore

    def setup_qa_chain(self, vectorstore: Chroma) -> RetrievalQA:
        llm_temp_str = os.environ.get('LLM_MODEL_TEMPERATURE')
        llm_temp = float(llm_temp_str) if llm_temp_str else 0.5

        llm_max_tokens_str = os.environ.get('LLM_MAX_TOKENS')
        llm_max_tokens = int(llm_max_tokens_str) if llm_max_tokens_str else 512

        llm = ChatGroq(model=os.environ.get('LLM_MODEL_NAME',
                                            'llama-3.1-70b-versatile'),
                       temperature=llm_temp,
                       max_tokens=llm_max_tokens,
                       stop_sequences=None)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())
        return qa_chain
