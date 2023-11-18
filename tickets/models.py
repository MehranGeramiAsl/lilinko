from django.db import models
from authentication.models import User

# Create your models here.


class Ticket(models.Model):
    TICKET_STATUS_CHOICES = [
    ("O", "Open"),
    ("OP", "On Progress"),
    ("A", "Answered"),
    ("C", "Closed"),
    ]

    title = models.CharField(max_length=255)
    status = models.CharField(max_length=2,choices=TICKET_STATUS_CHOICES,default="O")
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

