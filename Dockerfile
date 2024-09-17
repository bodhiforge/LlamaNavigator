FROM --platform=$BUILDPLATFORM python:3.9-slim AS base

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ARG TARGETPLATFORM

RUN if [ "$TARGETPLATFORM" = "linux/arm64" ]; then \
      pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu; \
    elif [ "$TARGETPLATFORM" = "linux/amd64" ]; then \
      pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu; \
    else \
      echo "Unsupported architecture: $TARGETPLATFORM"; exit 1; \
    fi

COPY . .

EXPOSE 7860

CMD ["python", "rag_qa_system.py"]