from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    skills = models.JSONField()  # Store skills as a list
    availability = models.CharField(max_length=20, default='Available')
    email = models.EmailField(default='no-reply@example.com')

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    priority = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="Pending")
    progress = models.IntegerField(default=0)
    feedback = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    estimated_time = models.IntegerField(default=0)  # Estimated time in hours

    def __str__(self):
        return self.title


