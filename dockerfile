FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl gnupg apt-transport-https ca-certificates unixodbc unixodbc-dev gcc && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc \
        | gpg --dearmor \
        | tee /etc/apt/keyrings/microsoft.gpg > /dev/null && \
    chmod +r /etc/apt/keyrings/microsoft.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
        > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


RUN pip install uv

COPY requirements.txt .

RUN uv pip install --system -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
