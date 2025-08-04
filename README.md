# Projeto API de Otimização com Algoritmo Genético

Este projeto é uma API RESTful construída com Django e Django REST Framework para resolver problemas de otimização usando um algoritmo genético. A API recebe um arquivo CSV com melhorias, um orçamento e parâmetros do algoritmo, e retorna a melhor combinação de melhorias para maximizar a valorização respeitando o orçamento.

Além disso, pode gerar um gráfico da evolução do fitness do algoritmo em PDF codificado em base64 para download.

---

# Deixei um arquivo de teste do insomnia para teste na raiz do arquivo, para testes da API.


## Tecnologias Utilizadas

- Python 3.13+
- Django 5.2.4
- Django REST Framework
- drf-yasg (Swagger / OpenAPI)
- Matplotlib (para geração de gráficos)
- NumPy (cálculos numéricos)
- CSV (processamento de arquivos CSV)

---

## Estrutura do Projeto

- `optimizer/views.py`: Endpoint principal para receber o arquivo CSV e parâmetros, retornando a solução.
- `optimizer/utils.py`: Função para carregar melhorias do CSV.
- `optimizer/algorithms/genetic.py`: Implementação do algoritmo genético, avaliação, mutação, crossover, e geração do gráfico.
- `requirements.txt`: Lista de dependências.
- Configurações padrão do Django.

---

## Instalação

### 1. Clone o repositório


git clone https://github.com/tech-challenge-IA/generic-algorithm-api
cd generic-algorithm-api

## Windows:

- python -m venv .venv
- .\.venv\Scripts\activate

## Linux / MacOS:


- python3 -m venv .venv
- source .venv/bin/activate


## pip install -r requirements.txt


## 4 Configuração e Execução
- Configure o Django
- Certifique-se de que o app optimizer está listado em INSTALLED_APPS no settings.py.

- Ajuste URLs e middleware se necessário.

## 5. Execute as migrations
- python manage.py migrate

- A API estará disponível em http://127.0.0.1:8000/


## Criar superusuário
- No terminal, dentro do ambiente virtual, execute:


```
python manage.py createsuperuser
Siga as instruções para definir:

username

email (opcional)

senha

``` 

## Após criar o usuário, você poderá fazer login e autenticar suas requisições usando as credenciais criadas.

## Como usar a API com Insomnia (ou Postman)
## Endpoint principal

## POST http://127.0.0.1:8000/api/optimizer/
- Parâmetros esperados (multipart/form-data)
- Campo	Tipo	Descrição	Exemplo
- melhorias_path	arquivo	Arquivo CSV contendo as melhorias	melhorias.csv
- orcamento	float	Orçamento disponível para as melhorias	5000
- tamanho_populacao	int	(Opcional) Tamanho da população do algoritmo genético	50
- geracoes	int	(Opcional) Número de gerações para execução	100
- gerar_grafico	bool	(Opcional) Se deseja receber o gráfico em PDF base64	false/true

## Passos para testar no Insomnia
## Defina método POST e URL http://127.0.0.1:8000/api/optimizer/.

- Em Body, selecione Multipart Form.

- Adicione o arquivo CSV no campo melhorias_path.

- Adicione os demais campos (orcamento, tamanho_populacao, geracoes, gerar_grafico).

- Envie a requisição.

- Resposta da API Se gerar_grafico for false ou não informado:

``` json

{
  "fitness": 123.45,
  "melhor_individuo": [1, 0, 1, 0],
  "evolucao": [10, 20, 30, 40, ...],
  "melhorias_escolhidas": [
    {
      "nome": "Melhoria 1",
      "custo": 1500,
      "valorizacao": 4000
    },
    ...
  ]
} 

```
Se gerar_grafico for true:

``` json

{
  "fitness": 123.45,
  "melhor_individuo": [...],
  "evolucao": [...],
  "melhorias_escolhidas": [...],
  "grafico_pdf_base64": "JVBERi0xLjQKJcfs..."
}

```
- Você pode salvar o conteúdo do campo grafico_pdf_base64 em um arquivo .pdf para visualizar o gráfico gerado.

- Como salvar o PDF base64 no Insomnia
- Copie o valor da resposta no campo grafico_pdf_base64.

- Salve em um arquivo com extensão .pdf usando seu editor de texto favorito, por exemplo, grafico.pdf.

- Abra o arquivo em qualquer visualizador de PDF.

## Erros comuns e dicas
## CSV não enviado: Verifique o campo de arquivo na requisição.

## Parâmetros inválidos: Confirme que orcamento, tamanho_populacao e geracoes são números válidos.

## Nenhuma solução viável encontrada: O orçamento pode ser insuficiente para as melhorias disponíveis.




