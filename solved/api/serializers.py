from rest_framework import serializers
from problems.models import Problem, User



class ProblemSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    class Meta:
        model = Problem
        fields = '__all__'
