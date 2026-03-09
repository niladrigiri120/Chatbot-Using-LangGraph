# -------- Base Image --------
FROM python:3.11-slim

# -------- Environment --------
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# -------- Work Directory --------
WORKDIR /app

# -------- Upgrade pip --------
RUN pip install --upgrade pip

# -------- Copy requirements --------
COPY requirements.txt .

# -------- Install dependencies --------
RUN pip install --no-cache-dir -r requirements.txt

# -------- Copy project --------
COPY . .

# -------- Expose Streamlit port --------
EXPOSE 8501

# -------- Start Streamlit (Render Compatible) --------
CMD sh -c "streamlit run app.py --server.address=0.0.0.0 --server.port=${PORT:-8501}"