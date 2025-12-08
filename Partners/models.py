from django.db import models

# Create your models here.
class Partner(models.Model):
    name = models.CharField(verbose_name="Name", max_length=50, null=False, blank=False)
    image = models.ImageField(upload_to="Partners/",verbose_name="Image", null=False, blank=False)
    added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Partner No {self.pk} added on {self.added_at}"
    
    class Meta:
        verbose_name="Partner"
        verbose_name_plural="Partners"