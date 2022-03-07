from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doghelp', '0008_alter_case_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to='doghelp.video'),
        )
    ]
