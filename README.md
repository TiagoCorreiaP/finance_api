📘 Documentação da API - Controle Financeiro

  Esta API gerencia usuários, transações financeiras e geração de relatórios em PDF.
  
  Base URL: http://localhost:8000
  
  Documentação Interativa (Swagger): http://localhost:8000/docs


🔐 Autenticação

  A API utiliza OAuth2 com JWT (JSON Web Tokens). Para acessar rotas protegidas, envie o token no Header de cada requisição:
  
    Authorization: Bearer <seu_token>
  
  1. Registro de Usuário
     
     Rota: POST /users/
     
     Corpo (JSON):
       {
          "username": "usuario",
          "email": "email@exemplo.com",
          "password": "sua_senha_forte"
        }
     
  3. Login (Obter Token)
     
     Rota: POST /token
     
     Formato: Content-Type: application/x-www-form-urlencoded
     
     Campos: username e password.
     
     Retorno: {"access_token": "...", "token_type": "bearer"}

     
💰 Transações

  Todas as rotas abaixo exigem autenticação.
  
  1. Listar Transações
     
     Rota: GET /transactions/
     
     Descrição: Retorna todas as transações do usuário logado.
     
  3. Criar Transação
     
     Rota: POST /transactions/
     
     Corpo (JSON):
       {
          "description": "Aluguel",
          "amount": 1200.00,
          "type": "Saída",
          "category": "Moradia",
          "date": "2024-05-20"
        }
     
     Nota: O campo type deve ser "Entrada" ou "Saída".
     
     Categorias Sugeridas: Moradia, Alimentação, Transporte, Renda, Lazer.
     
  5. Deletar Transação
     
     Rota: DELETE /transactions/{transaction_id}

     
📄 Relatórios

  1. Gerar PDF
     
     Rota: GET /export/pdf
     
     Descrição: Gera e retorna um arquivo .pdf com o resumo financeiro e a lista de todas as transações do usuário.

     
🛠️ Como Rodar o Projeto (Local)

  Certifique-se de ter o Docker instalado.
  
  Clone o repositório.
  
  Configure o arquivo .env (Já incluso no repositório privado).
  
  Suba os containers:
  
    docker-compose up --build -d
    
  Acesse a API: http://localhost:8000/docs

  
🗄️ Estrutura do Banco de Dados (MySQL)

  Tabelas e Campos Principais
  
    Users	                  id, username, email, hashed_password
    Transactions            id, description, amount, type, category, date, user_id

    
⚠️ Observações para o Front-end (C# e Web)

  CORS: A API está configurada para aceitar requisições de localhost.
  
  Erros: Caso algo dê errado, a API retornará um JSON com o campo detail explicando o erro (ex: 401 para Não Autorizado, 404 para Não Encontrado).
