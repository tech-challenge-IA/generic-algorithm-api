import os
import csv
import random
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

TAXA_MUTACAO = 0.01
TAXA_CROSSOVER = 0.8

def carregar_melhorias(nome_arquivo):
    melhorias = []
    with open(nome_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        reader.fieldnames = [campo.strip() for campo in reader.fieldnames]
        for row in reader:
            melhorias.append({
                'nome': row['nome'].strip(),
                'custo': float(row['custo'].replace(',', '.')),
                'valorizacao': float(row['valorizacao'].replace(',', '.'))
            })
    return melhorias

def inicializar_populacao(num_individuos, num_melhorias):
    return [[random.randint(0, 1) for _ in range(num_melhorias)] for _ in range(num_individuos)]

def avaliar_fitness(individuo, melhorias, orcamento):
    custo_total = sum(m['custo'] for m, v in zip(melhorias, individuo) if v)
    if custo_total > orcamento:
        return 0
    return sum(m['valorizacao'] for m, v in zip(melhorias, individuo) if v)

def selecao_roleta(populacao, fitnesses):
    total_fitness = sum(fitnesses)
    if total_fitness == 0:
        return random.choice(populacao)
    pick = random.uniform(0, total_fitness)
    atual = 0
    for individuo, fitness in zip(populacao, fitnesses):
        atual += fitness
        if atual > pick:
            return individuo
    return populacao[-1]

def crossover(pai1, pai2):
    if random.random() < TAXA_CROSSOVER:
        ponto = random.randint(1, len(pai1) - 1)
        filho1 = pai1[:ponto] + pai2[ponto:]
        filho2 = pai2[:ponto] + pai1[ponto:]
        return filho1, filho2
    return pai1[:], pai2[:]

def mutacao(individuo):
    return [1 - g if random.random() < TAXA_MUTACAO else g for g in individuo]


def algoritmo_genetico(melhorias, orcamento, tamanho_populacao=50, num_geracoes=100):
    num_melhorias = len(melhorias)
    populacao = inicializar_populacao(tamanho_populacao, num_melhorias)
    melhor_individuo = None
    melhor_fitness = 0
    evolucao_fitness = []

    for geracao in range(num_geracoes):
        fitnesses = [avaliar_fitness(i, melhorias, orcamento) for i in populacao]
        geracao_melhor_fitness = max(fitnesses)
        evolucao_fitness.append(geracao_melhor_fitness)

        for individuo, fit in zip(populacao, fitnesses):
            if fit > melhor_fitness:
                melhor_individuo = individuo[:]
                melhor_fitness = fit

        nova_populacao = []
        while len(nova_populacao) < tamanho_populacao:
            pai1 = selecao_roleta(populacao, fitnesses)
            pai2 = selecao_roleta(populacao, fitnesses)
            filho1, filho2 = crossover(pai1, pai2)
            filho1 = mutacao(filho1)
            filho2 = mutacao(filho2)
            nova_populacao.extend([filho1, filho2])

        populacao = nova_populacao[:tamanho_populacao]
        print(f"Geração {geracao+1}: Melhor fitness = {melhor_fitness}")

    return melhor_individuo, melhor_fitness, evolucao_fitness


def exibir_solucao(individuo, melhorias):
    print("\nMelhor combinação de melhorias encontrada:")
    custo_total = 0
    valorizacao_total = 0
    for gene, melhoria in zip(individuo, melhorias):
        if gene:
            print(f"- {melhoria['nome']} (Custo: {melhoria['custo']}, Valorização: {melhoria['valorizacao']})")
            custo_total += melhoria['custo']
            valorizacao_total += melhoria['valorizacao']
    print(f"\nCusto total: {custo_total}")
    print(f"Valorização total: {valorizacao_total}")

def plotar_evolucao_fitness(evolucao_fitness, nome_projeto='Tech Challenge Fase 2'):
    os.makedirs('resultados', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    nome_arquivo_base = f"resultados/evolucao_fitness_{timestamp}"

    plt.figure(figsize=(13, 7))
    cor_principal = "#005caa"

    plt.plot(
        range(1, len(evolucao_fitness)+1),
        evolucao_fitness,
        marker='o',
        linestyle='-',
        linewidth=2.5,
        markersize=7,
        label='Melhor Fitness',
        color=cor_principal
    )

    if len(evolucao_fitness) > 5:
        janela = 5
        media_movel = np.convolve(evolucao_fitness, np.ones(janela)/janela, mode='valid')
        plt.plot(range(janela, len(evolucao_fitness)+1), media_movel,
                 label='Média Móvel (5 gerações)', linestyle='--', color='#f28500', linewidth=2)

    plt.title(f'Evolução do Melhor Fitness por Geração\n{nome_projeto}', fontsize=17, fontweight='bold', color='#222')
    plt.xlabel('Geração', fontsize=14, fontweight='bold')
    plt.ylabel('Melhor Fitness', fontsize=14, fontweight='bold')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(visible=True, linestyle=':', alpha=0.55)
    plt.legend(fontsize=13, loc='best', frameon=True, shadow=True)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_linewidth(1.2)
    plt.gca().spines['bottom'].set_linewidth(1.2)

    plt.figtext(0.99, 0.01, 'Tech Challenge Fase 2 - FIAP', fontsize=11, color='#aaa',
                ha='right', va='bottom', alpha=0.8)

    idx_max = np.argmax(evolucao_fitness)
    idx_min = np.argmin(evolucao_fitness)

    plt.annotate(f'Máx: {max(evolucao_fitness):.2f}',
                xy=(idx_max + 1, evolucao_fitness[idx_max]),
                xytext=(-60, -30), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color='green'),
                fontsize=12, color='green', fontweight='bold')

    plt.annotate(f'Mín: {min(evolucao_fitness):.2f}',
                xy=(idx_min + 1, evolucao_fitness[idx_min]),
                xytext=(20, 10), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=12, color='red', fontweight='bold')

    plt.tight_layout()
    plt.savefig(f"{nome_arquivo_base}.png", dpi=180)
    plt.savefig(f"{nome_arquivo_base}.pdf")
    plt.show()
