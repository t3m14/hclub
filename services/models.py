from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=255)
    service_type = models.ForeignKey('ServiceType', on_delete=models.CASCADE)
    description = models.TextField()
    price_from = models.DecimalField(max_digits=10, decimal_places=2)
    price_to = models.DecimalField(max_digits=10, decimal_places=2)
    main_images = models.JSONField(default=list)
    duration = models.DecimalField(max_digits=4, decimal_places=2)
    steps = models.JSONField(default=list)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class ServiceType(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
