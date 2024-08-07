from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q
from django.forms import ModelForm

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', 'index'))  # Redirect to the next page or 'index'
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def all_emp(request):
    emps = Employee.objects.all()
    context = {'emps': emps}
    return render(request, 'view_all_emp.html', context)

@login_required
def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        salary_str = request.POST.get('salary', '')
        bonus_str = request.POST.get('bonus', '')
        phone_number = request.POST.get('phone_number', '')
        dept_id_str = request.POST.get('dept', '')
        role_id_str = request.POST.get('role', '')
        hire_date_str = request.POST.get('hire_date', '')

        # Check if any required fields are missing
        if not first_name or not last_name or not salary_str or not bonus_str or not phone_number or not dept_id_str or not role_id_str or not hire_date_str:
            messages.error(request, "All fields are required.")
            return render(request, 'add_emp.html', {
                'departments': Department.objects.all(),
                'roles': Role.objects.all(),
                'first_name': first_name,
                'last_name': last_name,
                'salary': salary_str,
                'bonus': bonus_str,
                'phone_number': phone_number,
                'dept': dept_id_str,
                'role': role_id_str,
                'hire_date': hire_date_str
            })

        # Validate numeric fields and hire date
        try:
            salary = int(salary_str)
            bonus = int(bonus_str)
            dept = int(dept_id_str)
            role = int(role_id_str)
            hire_date = datetime.strptime(hire_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid salary, bonus, department, role, or hire date.")
            return render(request, 'add_emp.html', {
                'departments': Department.objects.all(),
                'roles': Role.objects.all(),
                'first_name': first_name,
                'last_name': last_name,
                'salary': salary_str,
                'bonus': bonus_str,
                'phone_number': phone_number,
                'dept': dept_id_str,
                'role': role_id_str,
                'hire_date': hire_date_str
            })

        # Create and save new employee
        new_emp = Employee(
            first_name=first_name, last_name=last_name, salary=salary,
            bonus=bonus, phone=phone_number, dept_id=dept, role_id=role,
            hire_date=hire_date
        )
        new_emp.save()
        messages.success(request, "Employee added successfully.")
        return redirect('index')

    elif request.method == 'GET':
        context = {
            'departments': Department.objects.all(),
            'roles': Role.objects.all()
        }
        return render(request, 'add_emp.html', context)

    else:
        return HttpResponse("An Exception Occurred! Employee Has Not Been Added")

@login_required
def remove_emp(request, emp_id=None):
    if emp_id:
        try:
            emp_to_be_removed = get_object_or_404(Employee, id=emp_id)
            emp_to_be_removed.delete()
            messages.success(request, "Employee removed successfully.")
            return redirect('index')  # Redirect to the index page after successful removal
        except:
            messages.error(request, "Please Enter A Valid EMP ID")
            return redirect('remove_emp')  # Redirect back to the remove_emp page if an exception occurs
    
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'remove_emp.html', context)

@login_required
def filter_emp(request):
    if request.method == 'POST':
        # Retrieve filter values from POST request
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        dept = request.POST.get('dept', '')
        role = request.POST.get('role', '')
        hire_date_from = request.POST.get('hire_date_from', '')
        hire_date_to = request.POST.get('hire_date_to', '')
        
        # Filter employees based on form input
        employees = Employee.objects.all()
        if first_name:
            employees = employees.filter(first_name__icontains=first_name)
        if last_name:
            employees = employees.filter(last_name__icontains=last_name)
        if dept:
            employees = employees.filter(department_id=dept)
        if role:
            employees = employees.filter(role_id=role)
        if hire_date_from:
            employees = employees.filter(hire_date__gte=hire_date_from)
        if hire_date_to:
            employees = employees.filter(hire_date__lte=hire_date_to)
        
        # Get departments and roles for the form
        departments = Department.objects.all()
        roles = Role.objects.all()
        
        context = {
            'employees': employees,
            'departments': departments,
            'roles': roles,
            'first_name': first_name,
            'last_name': last_name,
            'dept': dept,
            'role': role,
            'hire_date_from': hire_date_from,
            'hire_date_to': hire_date_to,
        }
        
        return render(request, 'filter_emp.html', context)
    
    # Handle GET request to display the form
    departments = Department.objects.all()
    roles = Role.objects.all()
    
    context = {
        'departments': departments,
        'roles': roles,
    }
    
    return render(request, 'filter_emp.html', context)


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'dept', 'salary', 'bonus', 'role', 'hire_date']

@login_required
def update_emp(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', emp.first_name)
        last_name = request.POST.get('last_name', emp.last_name)
        salary_str = request.POST.get('salary', emp.salary)
        bonus_str = request.POST.get('bonus', emp.bonus)
        dept_id_str = request.POST.get('dept', emp.dept.id)
        role_id_str = request.POST.get('role', emp.role.id)
        phone_number = request.POST.get('phone_number', emp.phone)
        hire_date_str = request.POST.get('hire_date', emp.hire_date.strftime('%Y-%m-%d'))

        if not first_name or not last_name or not phone_number or not salary_str or not bonus_str or not dept_id_str or not role_id_str or not hire_date_str:
            messages.error(request, "All fields are required.")
            return render(request, 'update_emp.html', {
                'emp': emp,
                'departments': Department.objects.all(),
                'roles': Role.objects.all(),
                'phone_number': phone_number,
                'hire_date': hire_date_str
            })

        try:
            emp.first_name = first_name
            emp.last_name = last_name
            emp.salary = int(salary_str)
            emp.bonus = int(bonus_str)
            emp.dept_id = int(dept_id_str)
            emp.role_id = int(role_id_str)
            emp.phone = phone_number
            emp.hire_date = datetime.strptime(hire_date_str, '%Y-%m-%d').date()
            emp.save()
            messages.success(request, "Employee details updated successfully.")
            return redirect('all_emp')  # Redirect to the 'all_emp' page
        except ValueError:
            messages.error(request, "Invalid input. Please check your entries.")
            return render(request, 'update_emp.html', {
                'emp': emp,
                'departments': Department.objects.all(),
                'roles': Role.objects.all(),
                'phone_number': phone_number,
                'hire_date': hire_date_str
            })
    else:
        context = {
            'emp': emp,
            'departments': Department.objects.all(),
            'roles': Role.objects.all(),
            'phone_number': emp.phone,
            'hire_date': emp.hire_date.strftime('%Y-%m-%d')
        }
        return render(request, 'update_emp.html', context)


