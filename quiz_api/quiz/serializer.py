from rest_framework import serializers


class AnswerEvaluationSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_answers = serializers.ListField(child=serializers.CharField(), allow_empty=False)
