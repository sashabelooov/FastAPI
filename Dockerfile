FROM python:3.10-slim

WORKDIR /app

# Install uv via pip (avoids dependency on ghcr.io registry)
RUN pip install uv

# Install dependencies before copying app code (better layer caching)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
