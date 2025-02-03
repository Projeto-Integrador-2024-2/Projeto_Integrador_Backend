# Projeto Integrador - Backend

Este projeto é uma integração entre o backend em Django e o frontend em JavaScript/React. Siga as instruções abaixo para configurar e executar o projeto em sua máquina.

## Como Usar

### Configuração do Backend

1. **Instale as dependências do Django:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Execute o servidor de desenvolvimento do Django:**
    ```bash
    py manage.py runserver
    ```

### Migrações do Banco de Dados

Para configurar e aplicar as migrações do banco de dados:

1. **Crie as migrações:**
    ```bash
    py manage.py makemigrations
    ```

2. **Aplique as migrações:**
    ```bash
    py manage.py migrate
    ```

### Entrar na ambiente virtual

1. **Entre na pasta venv:**
    ```bash
    cd venv
    ```

2. **Ative o ambiente**
    ```bash
    source bin/activate
    ```

3. **Sair do ambiente**
    ```bash
    deactivate
    ```