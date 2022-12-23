from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Members(models.Model):
    name = models.CharField(max_length=50, db_collation='utf8mb4_general_ci')
    id = models.CharField(primary_key=True, max_length=50, db_collation='utf8mb4_general_ci')
    pw1 = models.CharField(max_length=100, db_collation='utf8mb4_general_ci')
    pw2 = models.CharField(max_length=100, db_collation='utf8mb4_general_ci')
    email = models.CharField(max_length=50, db_collation='utf8mb3_general_ci')
    regdate = models.DateField(db_column='regdate', auto_now_add=True)
    #regdate = models.DateField()

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
        
class CafeList(models.Model):
    cafename = models.CharField(max_length=50)
    gu = models.CharField(primary_key=True, max_length=50)
    dong = models.CharField(max_length=50)
    review = models.CharField(max_length=50)
    bookmark = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'cafe_list'


class Mylike(models.Model):
    userid = models.CharField(max_length=50)
    cafename = models.CharField(max_length=50)
    addr = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    review = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'mylike'


class Mybookmark(models.Model):
    id = models.CharField(primary_key=True, max_length=50, db_collation='utf8mb4_general_ci')
    cafename = models.CharField(max_length=50, db_collation='utf8mb4_general_ci')
    addr = models.CharField(max_length=50, db_collation='utf8mb4_general_ci')
    category = models.CharField(max_length=50, db_collation='utf8mb4_general_ci')
    memo = models.CharField(max_length=250, db_collation='utf8mb4_general_ci')
    class Meta:
        managed = False
        db_table = 'mybookmark'



