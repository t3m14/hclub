from django.db import models

class ServiceType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    client_types = models.JSONField(default=list)
    main_image = models.URLField(blank=True, null=True)
    benefits = models.JSONField(default=list)
    benefits_images = models.JSONField(default=list)
    target = models.CharField(max_length=100)
    products = models.JSONField(default=list)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
