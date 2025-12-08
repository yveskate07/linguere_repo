from django.db import models

# Create your models here.
class Feature(models.Model):
    description = models.TextField(verbose_name="Description", null=False, blank=False)
    image = models.ImageField(upload_to="Features/", null=False, blank="False")
    added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Feature No {self.pk} added on {self.added_at}"
    
    @property
    def name(self):
        return f"Feature No {self.pk}"
    
    class Meta:
        verbose_name="Feature"
        verbose_name_plural="Features"