from rest_framework import serializers

from project_module.models import Project,Module


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("project_name",)


class ModuleSerializer(serializers.ModelSerializer):
    quiz_count = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ['id', 'module_name', 'status', 'body','quiz_count']

    # For time being, count of modules is used. Later it will be replaced with quiz count.
    def get_quiz_count(self, obj):
        return Module.objects.count()
