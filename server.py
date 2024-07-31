from dotenv import load_dotenv
# Load environment variables
load_dotenv()

import logging
import grpc
from grpc_gen import qa_pb2_grpc
from service.qa import QAServiceServicer
from processing.pipeline import Pipeline

from concurrent import futures
import os


def main() -> None:
    FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    serve()


def serve():
    grpc_max_workers_str = os.getenv('GRPC_MAX_WORKERS', None)
    grpc_max_workers = int(grpc_max_workers_str) if grpc_max_workers_str else 4

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=grpc_max_workers))

    persist_directory = "chroma_db"

    pipeline = Pipeline(persist_directory)

    qa_pb2_grpc.add_QAServiceServicer_to_server(QAServiceServicer(pipeline), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
