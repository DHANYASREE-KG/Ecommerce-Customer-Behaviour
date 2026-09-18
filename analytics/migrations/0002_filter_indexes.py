from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("analytics", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="category",
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="order",
            name="state",
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="rfmsegment",
            name="segment",
            field=models.CharField(db_index=True, max_length=50),
        ),
    ]