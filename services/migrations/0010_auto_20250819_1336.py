from django.db import migrations
import json

def fix_json_data(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    for service in Service.objects.all():
        for field in ['target', 'client_types']:
            value = getattr(service, field)
            if isinstance(value, str) and not value.startswith('['):
                setattr(service, field, [value])
        service.save()

class Migration(migrations.Migration):
    dependencies = [
        ('services', '0008_alter_service_slug'),
    ]
    operations = [migrations.RunPython(fix_json_data)]