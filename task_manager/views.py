from django.shortcuts import render
from rest_framework import generics
from .models import Task, Employee
from .serializers import TaskSerializer, EmployeeSerializer, AssignmentReportSerializer
from django.core.mail import send_mail
from django.utils.dateparse import parse_date

# Task Views
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# Employee Views
class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

# Assign Task to Employee
from rest_framework.response import Response
from rest_framework import status

class AssignTaskView(generics.GenericAPIView):
    serializer_class = TaskSerializer

    def post(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs['pk'])
        employee = Employee.objects.get(id=request.data['employeeId'])
        task.assigned_to = employee
        task.save()
        return Response({"message": "Task assigned successfully"}, status=status.HTTP_200_OK)

class UpdateTaskView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    # task_manager/views.py

class AssignTaskView(generics.GenericAPIView):
    serializer_class = TaskSerializer

    def post(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs['pk'])
        employee = Employee.objects.get(id=request.data['employeeId'])
        task.assigned_to = employee
        task.save()

        # Send email notification
        send_mail(
            'New Task Assignment',
            f'You have been assigned a new task: {task.title}',
            'from@example.com',
            [employee.email],
            fail_silently=False,
        )

        return Response({"message": "Task assigned successfully"}, status=status.HTTP_200_OK)

from .serializers import AssignmentReportSerializer  # Import the serializer

# task_manager/views.py

from rest_framework import generics
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from .models import Task
from .serializers import AssignmentReportSerializer

# task_manager/views.py

from rest_framework import generics
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from .models import Task
from .serializers import AssignmentReportSerializer

class AssignmentReportView(generics.ListAPIView):
    serializer_class = AssignmentReportSerializer

    def get_queryset(self):
        date = self.request.query_params.get('date')
        if date:
            parsed_date = parse_date(date)
            return Task.objects.filter(deadline=parsed_date)
        return Task.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        employee_summary = {}

        for task in serializer.data:
            employee_name = task['employee_name']
            if employee_name not in employee_summary:
                employee_summary[employee_name] = {
                    'tasks': [],
                    'total_time': 0,
                    'skills_used': []
                }
            employee_summary[employee_name]['tasks'].append(task['title'])
            employee_summary[employee_name]['total_time'] += task['estimated_time']
            employee_summary[employee_name]['skills_used'].extend(task['employee_skills'])

        for employee, summary in employee_summary.items():
            summary['skills_used'] = list(set(summary['skills_used']))

        return Response(employee_summary)
