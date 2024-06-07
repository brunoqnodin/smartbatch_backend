# Documentação de Software

## SmartBatch - Alyne - Backend

### Visão Geral

Desenvolvimento de sistema de gestão de processo produtivo por batelada.

### Desenvolvimento

#### Ambiente
- VS Code 16.11.5
- Node.JS v14.21.3
- Python 3.10.12

#### Pacotes Necessários
- Flask: 2.2.5
- Cursor: 1.3.5
- Flask-MySQLdb: 1.0.1
- Werkzeug: 3.0.1

#### Estrutura de pastas
```
- apialyne_flask -> Aplicação de rotas para post no SmartBatch e encadeamento para o Sankhya
- apialyne_node -> Relay do Flask
```

### Instalação  do Executável

A aplicação deve ser instalado em ambiente com nodejs e python previamente instalado, baseado nas premissas de desenvolvimento. Os pacotes de instalação Flask são instalados via pip. O arquivo de execução é o execute.sh.

### Configuração do Projeto

- Clonar o projeto utilizando o comando abaixo:
```sh
git clone https://github.com/brunoqnodin/smartbatch_backend.git
```
- Entrar no diretório do projeto clonado e executar o seguinte comando:
```sh
./execute.sh
``` 

### Histórico de Versões

#### Versões Disponíveis
- **Versão 1.0.0** -> 07/02/2024