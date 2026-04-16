# Usa uma imagem leve do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /code

# Copia o arquivo de dependências
COPY ./requirements.txt /code/requirements.txt

# Instala as dependências
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia o restante do código da pasta app
COPY ./app /code/app

# Comando para rodar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]