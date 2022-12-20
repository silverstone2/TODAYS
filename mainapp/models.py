from django.db import models

# Create your models here.
class Members(models.Model):
    name = models.CharField(max_length=50, db_collation='utf8mb4_general_ci')
    id = models.CharField(primary_key=True, max_length=50, db_collation='utf8mb4_general_ci')
    pw1 = models.CharField(max_length=50, db_collation='utf8mb4_general_ci')
    pw2 = models.CharField(max_length=50, db_collation='utf8mb4_general_ci')
    email = models.CharField(max_length=50, db_collation='utf8mb3_general_ci')
    regdate = models.DateField()

    class Meta:
        managed = False
        db_table = 'members'


class Notice(models.Model):
    number = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    writer = models.CharField(max_length=50)
    regdate = models.DateField()
    views = models.IntegerField()
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'notice'