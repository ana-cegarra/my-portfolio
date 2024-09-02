from django.urls import path
from .views import TaskListCreateView, TaskDetailView, EmployeeListCreateView, EmployeeDetailView, AssignTaskView, AssignmentReportView  # Ensure this import is correct

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('assign/', AssignTaskView.as_view(), name='assign-task'),
    path('report/', AssignmentReportView.as_view(), name='assignment-report'),  # Ensure the view is correctly referenced
]
