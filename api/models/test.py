from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tests"  # Explicitly set the table name