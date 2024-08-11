from django.db import models

# Create your models here.
class Todo(models.Model):
    STATUS = (
        ('todo','Todo'),
        ('in progress','In progress'),
        ('done','Done')
    )
    title = models.CharField(max_length=100,null=True)
    due_date = models.DateField(null=True)
    status = models.CharField(max_length=50,choices=STATUS,null=True)

    def __str__(self):
        return self.title