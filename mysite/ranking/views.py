from django.shortcuts import render #构建动态的 HTML 页面并将其呈现给用户
from django.shortcuts import redirect #用于将用户导航到另一个 URL
from django.views import View
from .models import Student, Modify, History,Lesson,AttendanceHistory,Transfer
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login ,logout
from django.http import request,HttpResponse
from django import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.db import transaction
from django.db.models import Q


class HomePageView(View):
    template_name = 'ranking/home.html'

    def get(self, request):
        students = Student.objects.all().order_by('-current_adcoins')
        return render(request, self.template_name, context = {'students': students})

class LoginPageView(View):
    template_name = 'ranking/login.html'

    def get(self, request):
        form = AuthenticationForm() #负责验证用户名和密码，您可以轻松使用 form.get_user() 获取已验证的用户。
        return render(request, self.template_name, {'form': form, 'error_message': None})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_staff:
                return redirect('staff')
            else:
                return redirect('staff') 
        else:
            error_message = 'Invalid username or password. Please try again.'
            return render(request, self.template_name, {'form': form, 'error_message': error_message})

@method_decorator(login_required(login_url='login'), name='dispatch')
class StaffPageView(View):
    template_name = 'ranking/staff.html'

    def get(self, request):
        # 获取当前登录用户
        user = request.user

        # 获取所有学生信息
        students = Student.objects.all().order_by('-current_adcoins')

        # 如果是学生，只显示当前学生的信息
        if not user.is_staff:
            student = Student.objects.get(name=user.username)
            context = {'students': students, 'student': student, 'user': user, 'is_staff': False}
        else:
            context = {'students': students, 'user': user, 'is_staff': True}

        return render(request, self.template_name, context)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
class StudentPageView(View):
    template_name = 'ranking/student.html'

    def get(self, request):
        students = Student.objects.all().order_by('-current_adcoins')
        return render(request, self.template_name, {'students': students})

    def post(self, request):
        # Handle the form submission for adding a new user
        new_name = request.POST.get('new_name')
        new_adcoins = int(request.POST.get('new_adcoins', 0))  # Convert to integer
        new_adstars = int(request.POST.get('new_adstars', 0))  # Convert to integer

        # Create a new student
        student = Student.objects.create(
            name=new_name,
            current_adcoins=new_adcoins,  # Set the received values
            adstars=new_adstars,
            highest_record_adcoins=new_adcoins  # Set initial highest record to the received value
        )

        # Redirect to the student page after adding a new user
        return redirect('student')
    
# class ModifyPageView(View):
#     template_name = 'ranking/modify.html'

#     def post(self, request):
#         # Handle the form submission for modification
#         student_id = request.POST.get('student_id')
#         adcoins_change = request.POST.get('adcoins_change')
#         remarks = request.POST.get('remarks')

#         # Create a new modification entry
#         student = Student.objects.get(id=student_id)
#         Modify.objects.create(student=student, adcoins_change=adcoins_change, remarks=remarks)

#         # Update the adcoins field of the student
#         student.current_adcoins += int(adcoins_change)
#         student.save()

#         # Redirect to the staff page after modification
#         return redirect('staff')

# class ModifyPageView(View):
#     template_name = 'ranking/modify.html'

#     def get(self, request):
#         students = Student.objects.all()
#         return render(request, self.template_name, {'students': students})

#     def post(self, request):
#         # Handle the form submission for modification
#         student_id = request.POST.get('student_id')
#         adcoins_change = request.POST.get('adcoins_change')
#         remarks = request.POST.get('remarks')

#         # Create a new modification entry
#         student = Student.objects.get(id=student_id)
#         Modify.objects.create(student=student, adcoins_change=adcoins_change, remarks=remarks)

#         # Update the adcoins field of the student
#         student.current_adcoins += int(adcoins_change)
#         student.save()

#         # Redirect to the staff page after modification
#         return redirect('staff')

# class HistoryPageView(View):
#     template_name = 'ranking/history.html'

#     def get(self, request):
#         name_filter = request.GET.get('name_filter', '')
#         if name_filter:
#             histories = History.objects.filter(student__name=name_filter)
#         else:
#             histories = History.objects.all()

#         students = Student.objects.all()
#         return render(request, self.template_name, {'histories': histories, 'students': students})

# class HistoryPageView(View):
#     template_name = 'ranking/history.html'

#     def get(self, request):
#         name_filter = request.GET.get('name_filter', 'All')
#         students = Student.objects.all()
        
#         # Fetch modify and history entries based on the selected filter
#         if name_filter == 'All':
#             modify_entries = Modify.objects.all()
#             history_entries = History.objects.all()
#         else:
#             student = Student.objects.get(name=name_filter)
#             modify_entries = Modify.objects.filter(student=student)
#             history_entries = History.objects.filter(student=student)

#         # Combine and sort modify and history entries based on timestamp
#         entries = sorted(
#             list(modify_entries) + list(history_entries),
#             key=lambda entry: entry.timestamp,
#             reverse=True
#         )

#         return render(request, self.template_name, {'entries': entries, 'students': students, 'name_filter': name_filter})
    
# class HistoryPageView(View):
#     template_name = 'ranking/history.html'

#     def get(self, request):
#         # Get the filter value from the request
#         filter_name = request.GET.get('filter_name')

#         # Fetch histories based on the filter
#         if filter_name and filter_name != 'All':
#             histories = History.objects.filter(student__name=filter_name)
#         else:
#             histories = History.objects.all()

#         # Fetch all student names for the filter dropdown
#         all_names = Student.objects.values_list('name', flat=True)

#         context = {
#             'histories': histories,
#             'all_names': all_names,
#             'filter_name': filter_name,
#         }

#         return render(request, self.template_name, context)
    
class ModifyPageView(View):
    template_name = 'ranking/modify.html'

    def get(self, request):
        students = Student.objects.all().order_by('-current_adcoins')
        return render(request, self.template_name, {'students': students})

    def post(self, request):
        # Handle the form submission for modification
        student_id = request.POST.get('student_id') #从 HTTP POST 请求中获取表单数据的方法，request.POST.get('key') 方法用于从这个字典中获取特定键（key）对应的值。
        adcoins_change_str = request.POST.get('adcoins_change')  # Get adcoins_change as string
        remarks = request.POST.get('remarks')

        # Convert adcoins_change to integer
        try:
            adcoins_change = int(adcoins_change_str)
        except ValueError:
            # Handle the case where adcoins_change is not a valid integer
            adcoins_change = 0  # or any default value

        # Create a new modification entry
        student = Student.objects.get(id=student_id)
        Modify.objects.create(student=student, adcoins_change=adcoins_change, remarks=remarks)

        # Update the adcoins field of the student
        student.current_adcoins += adcoins_change  # Use the converted integer value
        student.save()

        # Create a new history entry
        History.objects.create(student=student, adcoins_change=adcoins_change, remarks=remarks)

        # Redirect to the staff page after modification
        return redirect('staff')

    
class HistoryPageView(View):
    template_name = 'ranking/history.html'

    def get(self, request):
        # Get the filter value from the request
        filter_name = request.GET.get('filter_name')

        # Fetch histories based on the filter
        if filter_name and filter_name != 'All':
            histories = History.objects.filter(student__name=filter_name)
        else:
            histories = History.objects.all()

        # Fetch all student names for the filter dropdown
        all_names = Student.objects.values_list('name', flat=True) #使用 values_list 方法将它们放入一个列表中

        context = {
            'histories': histories,
            'all_names': all_names,
            'filter_name': filter_name,
        }

        return render(request, self.template_name, context)
    
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['lesson_no', 'title', 'pdf_file', 'reference_link']

class LessonView(View):
    template_name = 'ranking/lesson_view.html'

    def get(self, request):
        lessons = Lesson.objects.all().order_by('lesson_no')
        return render(request, self.template_name, {'lessons': lessons})

class LessonCreateView(View):
    template_name = 'ranking/lesson_create.html'

    def get(self, request):
        form = LessonForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('staff')
        return render(request, self.template_name, {'form': form})

    
@method_decorator(login_required(login_url='login'), name='dispatch')
class TransferPageView(View):
    template_name = 'ranking/transfer.html'

    def get(self, request):
        # Get the currently logged-in user
        user = request.user

        # Check if the user is staff
        is_staff = user.is_staff

        # Initialize sender to None for non-staff members
        sender = None

        # Get all students (excluding the sender for staff)
        students = Student.objects.exclude(name=user.username)

        # Get transfer history based on user role
        if is_staff:
            # If the user is staff, show all transfer history
            transfer_history = Transfer.objects.all()

            # Handling the filter form for staff
            student_filter = request.GET.get('student_filter')
            if student_filter:
                transfer_history = transfer_history.filter(sender__name=student_filter)
        else:
            # If the user is not staff, get the sender and their transfer history
            try:
                sender = Student.objects.get(name=user.username)
                transfer_history = Transfer.objects.filter(sender=sender)
            except Student.DoesNotExist:
                sender = None
                transfer_history = []

        return render(request, self.template_name, {'sender': sender, 'students': students, 'transfer_history': transfer_history, 'is_staff': is_staff})  

    def post(self, request):
        # Get the currently logged-in user
        user = request.user

        # Get form data
        recipient_id = request.POST.get('recipient_id')
        transfer_amount = int(request.POST.get('transfer_amount'))
        remark = request.POST.get('remark')

        # Get sender and recipient
        sender = Student.objects.get(name=user.username)
        recipient = Student.objects.get(id=recipient_id)

        # Check if the sender has enough adcoins for the transfer
        if sender.current_adcoins >= transfer_amount and transfer_amount > 0:
            try:
                with transaction.atomic():
                    # Update sender and recipient's adcoins
                    sender.current_adcoins -= transfer_amount
                    recipient.current_adcoins += transfer_amount

                    # Save updated data
                    sender.save()
                    recipient.save()

                    # Create a transfer record
                    Transfer.objects.create(sender=sender, recipient=recipient, transfer_amount=transfer_amount, remark=remark)

            except Exception as e:
                # Handle any exceptions that may occur during the transaction
                print(f"Error during transaction: {e}")
                # You can add more specific error handling here if needed

            # Redirect to staff page or another appropriate page
            return redirect('staff')
        else:
            # Handle transfer failure logic, you can return an error message to the user
            students = Student.objects.exclude(name=user.username)
            return render(request, self.template_name, {'sender': sender, 'students': students, 'error_message': 'Insufficient adcoins for transfer'})

class AttendanceMarkingView(View):
    template_name = 'ranking/attendance_marking.html'

    def get(self, request):
        # Get filter values from the request
        student_filter = request.GET.get('student_filter', '')
        date_filter = request.GET.get('date_filter', '')

        # Fetch all students for the filter dropdown
        students = Student.objects.all()
        lessons = Lesson.objects.all()

        # Fetch attendance history based on the filters
        attendance_history = AttendanceHistory.objects.all()

        if student_filter:
            attendance_history = attendance_history.filter(student__name=student_filter)

        if date_filter:
            attendance_history = attendance_history.filter(attendance_date=date_filter)

        # Other data retrieval and context setup...

        return render(request, self.template_name, {'lessons': lessons,'students': students, 'attendance_history': attendance_history, 'student_filter': student_filter, 'date_filter': date_filter})
    
    def post(self, request):
        # Handle form data directly
        student_id = request.POST.get('student_id')
        attendance_date = request.POST.get('attendance_date')
        attendance_time = request.POST.get('attendance_time')
        lesson_id = request.POST.get('lesson')

        # Perform any validation or processing as needed

        # Create AttendanceHistory entry
        student = Student.objects.get(id=student_id)
        lesson = Lesson.objects.get(id=lesson_id)
        AttendanceHistory.objects.create(
            student=student,
            lesson=lesson,
            attendance_date=attendance_date,
            attendance_time=attendance_time
        )

        # Get updated attendance history with filtering
        student_filter = request.POST.get('student_filter', '')  # Use POST instead of GET for consistency
        attendance_history = AttendanceHistory.objects.all()

        if student_filter:
            attendance_history = attendance_history.filter(student__name=student_filter)

        # Get updated lessons and students
        lessons = Lesson.objects.all()
        students = Student.objects.all()

        return render(request, self.template_name, {'lessons': lessons, 'students': students, 'attendance_history': attendance_history})

# GET 方法：

# 用于向用户呈现页面，获取信息。
# 通过 URL 参数传递信息，例如在查询字符串中。
# 不应该对数据进行修改或提交。

# POST 方法：

# 用于从用户获取信息，通常通过表单提交。
# 通过请求体传递信息，对于表单数据通常不可见。
# 通常用于提交、修改或处理数据。

#request.POST.get
#request.POST.get() 是 Django 中用于从 HTTP POST 请求中获取表单数据的方法。
#具体而言，request.POST 是一个类似字典的对象，它包含通过 POST 方法提交的所有表单数据。
#request.POST.get('key') 方法用于从这个字典中获取特定键（key）对应的值。