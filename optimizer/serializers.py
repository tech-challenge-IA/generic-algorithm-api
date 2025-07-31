from rest_framework import serializers

class OtimizacaoRequestSerializer(serializers.Serializer):
    orcamento = serializers.FloatField()
    melhorias_path = serializers.CharField()

class MelhoramentoSerializer(serializers.Serializer):
    nome = serializers.CharField()
    custo = serializers.FloatField()
    valorizacao = serializers.FloatField()
