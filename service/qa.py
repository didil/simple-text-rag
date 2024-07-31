from grpc_gen import qa_pb2, qa_pb2_grpc
import logging
from processing.pipeline import Pipeline


class QAServiceServicer(qa_pb2_grpc.QAServiceServicer):

    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline

    def check_collection_name_valid(self, collection_name: str) -> bool:
        return all(c.isalnum() or c == '_' for c in collection_name)

    def CreateCollection(self, request, context):
        logging.info(f"Received CreateCollection request {request.name} , file_url {request.file_url}")

        if not self.check_collection_name_valid(request.name):
            raise ValueError(f"Invalid collection name: {request.name}")

        document_text = self.pipeline.download_text(request.file_url)
        chunks = self.pipeline.load_and_split_text(document_text)
        self.pipeline.create_vectorstore(request.name, chunks)

        return qa_pb2.CreateCollectionResponse()

    def GetAnswer(self, request, context):
        logging.info(
            f"Received GetAnswer request collection_name {request.collection_name}, question: {request.question}")

        if not self.check_collection_name_valid(request.collection_name):
            raise ValueError(f"Invalid collection name: {request.collection_name}")

        vectorstore = self.pipeline.load_vectorstore(request.collection_name)
        qa_chain = self.pipeline.setup_qa_chain(vectorstore)
        answer = qa_chain.invoke(request.question)
        answer_result = answer.get('result', '')
        return qa_pb2.Answer(text=answer_result)
