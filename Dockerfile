# Use uma imagem base do Python
FROM python:3.10-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie os arquivos do projeto para o container
COPY . /app

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta 5000 para o Flask
EXPOSE 5000

# Comando para rodar o aplicativo usando Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "App:app"]
