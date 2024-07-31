lint:
	ruff check .

requirements:
	pip install -r requirements.txt

requirements-dev:
	pip install -r requirements-dev.txt

gen-proto:
	python -m grpc_tools.protoc -Igrpc_gen=protos --python_out=. --pyi_out=. --grpc_python_out=. protos/*.proto

server:
	python server.py