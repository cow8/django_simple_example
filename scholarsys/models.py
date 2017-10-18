from django.db import models
from django.contrib.auth.models import User

scho_cate = ((0, 'National Scholarship'),
             (1, 'University Scholarship'),
             (2, 'School Academic Scholarship'),
             (3, 'School Athletic Scholarship'),
             (4, 'School Student Affair Scholarship'),
             (5, 'School Research Scholarship'),
             )
achi_cate=((0,'Basic Score'),
           (1,'Academic Score'),
           (2,'Athletic Score'),
           (3,'Student Affair Score'),
           (4,'Research Score')
           )

class Material(models.Model):
    description = models.TextField(null=True)
    evidence = models.ImageField(upload_to='media')
    achievement = models.ForeignKey('Achievement')

    def __str__(self):
        return self.description


class Achievement(models.Model):
    name = models.CharField(max_length=120)
    category = models.CharField(choices=achi_cate, max_length=30)
    score = models.IntegerField()
    student = models.ForeignKey('Student')
    status = models.BooleanField(choices=((0, '未通过'), (1, '通过')), default=0)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stu_id = models.CharField(max_length=20)
    scholarship = models.ManyToManyField('Scholarship')

    def __str__(self):
        return self.stu_id


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20)

    def __str__(self):
        return self.staff_id


class Scholarship(models.Model):
    category = models.CharField(choices=scho_cate, max_length=30)
    bonus = models.IntegerField()
    capacity = models.IntegerField()
    distributer = models.ForeignKey(Staff)
    is_active = models.BooleanField()

    def __str__(self):
        return self.category
