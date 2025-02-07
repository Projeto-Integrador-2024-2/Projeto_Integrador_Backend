# Projeto Integrador - Backend

Este projeto é uma integração entre o backend em Django e o frontend em JavaScript/React. Siga as instruções abaixo para configurar e executar o projeto em sua máquina.

## Como Usar

### Entrar na ambiente virtual

**Criando ambiente no linux**
```bash
virtualenv -p python3 venv/
```

1. **Ative o ambiente no linux**
    ```bash
    source myenv/bin/activate
    ```

2. **Ative o ambiente no windows**
    ```bash
    myenv\Scripts\activate
    ```

3. **Sair do ambiente**
    ```bash
    deactivate
    ```

### Configuração do Backend

1. **Instale as dependências do Django:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Execute o servidor de desenvolvimento do Django:**
    ```bash
    py manage.py runserver
    ```

3. **Execute o servidor de desenvolvimento do Django em uma porta expecifica:**
    ```bash
    python3 manage.py runserver 65535
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