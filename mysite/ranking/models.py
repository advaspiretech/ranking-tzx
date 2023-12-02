from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import F
from django.contrib.auth.models import User
from django import forms

class Student(models.Model):
    name = models.CharField(max_length=50)
    current_adcoins = models.IntegerField(default=0)
    adstars = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    highest_record_adcoins = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Update highest_record_adcoins based on changes in current_adcoins
        if self.current_adcoins > self.highest_record_adcoins:
            self.highest_record_adcoins = self.current_adcoins

        super().save(*args, **kwargs)

        # Check if a user with the same username already exists
        existing_user = User.objects.filter(username=self.name).first()

        # Only create a new user if it doesn't exist
        if not existing_user:
            user = User.objects.create_user(username=self.name, password=self.name)

    def __str__(self):
        return self.name

class Modify(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE) #父删除子也会被删除
    adcoins_change = models.IntegerField()
    remarks = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Update student's current_adcoins using F() expression
        Student.objects.filter(id=self.student.id).update(  #filter就是要找特定的student id 如何.update就是要更新这一个学生的资料
            current_adcoins=F('current_adcoins') + self.adcoins_change #这里是要让当前的钱加上要加或者减的钱
        )

        super().save(*args, **kwargs) #把它save起来


class History(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE) #父删除子也会被删除
    adcoins_change = models.IntegerField()
    remarks = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Lesson(models.Model):
    lesson_no = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True)
    reference_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Lesson {self.lesson_no}: {self.title}"
    
class AttendanceHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    attendance_time = models.TimeField()

class Transfer(models.Model):
    sender = models.ForeignKey(Student, related_name='transfers_sent', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Student, related_name='transfers_received', on_delete=models.CASCADE)
    transfer_amount = models.IntegerField()
    remark = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
