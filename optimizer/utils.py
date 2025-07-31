import csv
import random

def carregar_melhorias(arquivo):
    """
    Lê o arquivo CSV enviado via upload e retorna uma lista de melhorias
    arquivo: UploadedFile (objeto vindo do request.FILES)
    """
    melhorias = []
    reader = csv.DictReader(
        (line.decode('utf-8') for line in arquivo),
        delimiter=';'
    )
    for row in reader:
        melhorias.append({
            'nome': row['nome'].strip(),
            'custo': float(row['custo'].replace(',', '.')),
            'valorizacao': float(row['valorizacao'].replace(',', '.'))
        })
    return melhorias

def avaliar_fitness(individuo, melhorias, orcamento):
    custo_total = sum(m['custo'] for i, m in enumerate(melhorias) if individuo[i])
    if custo_total > orcamento:
        return 0
    return sum(m['valorizacao'] for i, m in enumerate(melhorias) if individuo[i])

def crossover(pai1, pai2):
    ponto = random.randint(1, len(pai1) - 1)
    return pai1[:ponto] + pai2[ponto:]

def mutacao(individuo, taxa_mutacao=0.01):
    return [not gene if random.random() < taxa_mutacao else gene for gene in individuo]

def selecao_roleta(populacao, fitnesses):
    total = sum(fitnesses)
    if total == 0:
        return random.choice(populacao)
    pick = random.uniform(0, total)
    atual = 0
    for individuo, fit in zip(populacao, fitnesses):
        atual += fit
        if atual >= pick:
            return individuo

def inicializar_populacao(tamanho_populacao, tamanho_individuo):
    return [[random.choice([True, False]) for _ in range(tamanho_individuo)] for _ in range(tamanho_populacao)]
