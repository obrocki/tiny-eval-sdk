from django.db import models

# Create your models here.
class PromptParam(models.Model):
    row_number = models.IntegerField()
    eval_query = models.CharField(max_length=255)
    eval_response = models.CharField(max_length=255)
    ground_truth = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default='Pending')
    result = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Row {self.row_number}: {self.text_field}"