from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
import os

from .utils import carregar_melhorias
from .algorithms.genetic import algoritmo_genetico, plotar_evolucao_fitness

class OtimizacaoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        arquivo = request.FILES.get('melhorias_path')
        if not arquivo:
            return Response({'erro': 'Arquivo CSV não enviado'}, status=400)

        try:
            melhorias = carregar_melhorias(arquivo)
        except Exception as e:
            return Response({'erro': f'Erro ao processar CSV: {str(e)}'}, status=400)

        try:
            orcamento = float(request.data.get('orcamento'))
            tamanho_populacao = int(request.data.get('tamanho_populacao', 50))
            geracoes = int(request.data.get('geracoes', 100))
            gerar_grafico = request.data.get('gerar_grafico', 'true').lower() == 'true'
        except (TypeError, ValueError):
            return Response({'erro': 'Parâmetros inválidos'}, status=400)

        melhor_individuo, fitness, evolucao = algoritmo_genetico(
            melhorias, orcamento, tamanho_populacao, geracoes
        )

        if melhor_individuo is None:
            return Response({'erro': 'Nenhuma solução viável encontrada com o orçamento fornecido.'}, status=400)

        if gerar_grafico:
            caminho_pdf = plotar_evolucao_fitness(evolucao)

            if not os.path.exists(caminho_pdf):
                return Response({'erro': 'Erro ao gerar o gráfico PDF.'}, status=500)

            return FileResponse(
                open(caminho_pdf, 'rb'),
                content_type='application/pdf',
                as_attachment=True,
                filename=os.path.basename(caminho_pdf)
            )
        else:
            melhorias_selecionadas = []
            custo_total = 0
            valorizacao_total = 0

            for gene, melhoria in zip(melhor_individuo, melhorias):
                if gene:
                    melhorias_selecionadas.append(melhoria)
                    custo_total += melhoria['custo']
                    valorizacao_total += melhoria['valorizacao']

            return Response({
                'melhor_fitness': fitness,
                'custo_total': custo_total,
                'valorizacao_total': valorizacao_total,
                'melhorias_selecionadas': melhorias_selecionadas,
                'evolucao_fitness': evolucao,
            })
