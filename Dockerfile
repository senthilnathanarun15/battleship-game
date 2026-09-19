FROM python:3.11-slim

WORKDIR /app

# Copy dependency definitions first for fast Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

EXPOSE 8501

# Run the Battleship Streamlit app
CMD ["streamlit", "run", "battleship_game_code.py", "--server.port=8501", "--server.address=0.0.0.0"]
