from django.db import models

# Create your models here.
class Feature(models.Model):
    title = models.CharField(verbose_name='Title', max_length=50, blank=False, null=False, default='')
    description = models.TextField(verbose_name="Description", null=False, blank=False)
    image = models.ImageField(upload_to="Features/", null=False, blank="False")
    added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Feature No {self.pk} added on {self.added_at}"
    
    @property
    def name(self):
        return f"Feature No {self.pk}"
    
    def getImage(self):
        try:
            url=self.image.url
        except Exception as e:
            url='default feature url'
        finally:
            return url
    
    class Meta:
        verbose_name="Feature"
        verbose_name_plural="Features"