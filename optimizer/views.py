from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated 

from .utils import carregar_melhorias
from .algorithms.genetic import algoritmo_genetico

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
        except (TypeError, ValueError):
            return Response({'erro': 'Parâmetros inválidos'}, status=400)

        melhor_individuo, fitness, evolucao = algoritmo_genetico(
            melhorias, orcamento, tamanho_populacao, geracoes
        )

        if melhor_individuo is None:
            return Response({'erro': 'Nenhuma solução viável encontrada com o orçamento fornecido.'}, status=400)

        resultado = {
            "fitness": fitness,
            "melhor_individuo": melhor_individuo,
            "evolucao": evolucao,
            "melhorias_escolhidas": [
                m for g, m in zip(melhor_individuo, melhorias) if g
            ]
        }

        return Response(resultado)