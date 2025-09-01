from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('dollo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultat',
            name='evaluation',
            field=models.ForeignKey(
                to='dollo.Evaluation',  # attention à la majuscule E
                on_delete=models.CASCADE,
                null=True,
                blank=True,
                related_name='resultats'
            ),
        ),
    ]
