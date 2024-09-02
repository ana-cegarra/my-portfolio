from rest_framework import serializers
from .models import Employee, Task

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        
class AssignmentReportSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='assigned_to.name')
    employee_skills = serializers.JSONField(source='assigned_to.skills')

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'status', 'progress', 'estimated_time', 'employee_name', 'employee_skills']
        
class AssignTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'estimated_time', 'required_skills', 'employee']