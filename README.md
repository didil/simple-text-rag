# Simple Text RAG

Simple Text RAG Python application that allows adding a document then asking questions about it. Uses:
- LangChain
- Groq API
- ChromaDB Vector Store
- gRPC API

*This is a demo app. The code is not production ready*

The companion article can be found on [Adil's Backend & Cloud Engineering Blog](https://open.substack.com/pub/didil/p/simple-text-rag?r=63gj&utm_campaign=post&utm_medium=web)

## Development Setup

### Create Virtual Env
```bash
python3 -m venv .venv
```

### Install requirements
```bash
make requirements
make requirements-dev
```

### Setup .env file
```bash
cp .env.example .env
```

### Regenerate Protobuf output files
Only needed if making changes to the proto files
```bash
make gen-protos
```

### Run linter
```bash
make lint
```

### Run server
```bash
make server
```