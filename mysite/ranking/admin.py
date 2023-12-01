from django.contrib import admin
from .models import Student, Modify, History,Lesson,AttendanceHistory,Transfer

# Register your models here.

admin.site.register(Student)
admin.site.register(Modify)
admin.site.register(History)
admin.site.register(Lesson)
admin.site.register(Transfer)
admin.site.register(AttendanceHistory)


