from django.db import models

class Grid(models.Model):
    row_number = models.IntegerField()
    text_field = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default='Pending')
    result = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Row {self.row_number}: {self.text_field}"
    
