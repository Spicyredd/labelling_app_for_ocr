from django.db import models


class ValidLabelPair(models.Model):
    LABEL_STATUS_CHOICES = [
        ('valid', 'Valid'),
        ('not_checked', 'Not Checked'),
    ]

    label = models.CharField(max_length=255)
    image_path = models.CharField(max_length=500)
    label_status = models.CharField(
        max_length=20,
        choices=LABEL_STATUS_CHOICES,
        default='not_checked'
    )

    def __str__(self):
        return self.label


class RemovedLabelPair(models.Model):
    label = models.CharField(max_length=255)
    image_path = models.CharField(max_length=500)
    removed_reason = models.TextField()

    def __str__(self):
        return f"{self.label} (removed)"
