from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, TaskUpdateForm,UserUpdateForm,ProfileUpdateForm
from .models import TaskData
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import CreateView ,DeleteView,UpdateView
from django.urls.base import reverse
import datetime, csv
from django.contrib.auth.models import User
from .filters import TaskDataFilter
from fpdf import FPDF

def send_mail(request):
	pass

def to_pdf(request):
	pass
	# task_qs=TaskData.objects.filter(is_complete=False,user=request.user)
	# tasks = TaskDataFilter(request.GET, queryset=task_qs)
	# pdf = FPDF()
	# pdf.add_page()
	# pdf.set_font("Arial", size = 15)

	# temp=request.META.get('HTTP_REFERER')
	# x = temp.split("taskdetail/")# http://127.0.0.1:8000/taskdetail/14/
	# y=x[1].split("/")

	# for task in tasks.qs:
		
	# 	if (int(y[0]))==task.task_id:
			
	# 		pdf.cell(200, 10, txt = task.task_name, ln = 1)
	# 		pdf.cell(200, 10, txt = task.task_details, ln = 2)
	# 		pdf.cell(200, 10, txt = str(task.task_created_date), ln = 3)
	# 		pdf.cell(200, 10, txt = str(task.task_end_date), ln = 4)
	# 		pdf.output("mohith.pdf")
	# 		messages.success(request, f'Your Pdf has been created!')

	# return redirect("todo-home") 
  

def to_csv(request):
	if request.META.get('HTTP_REFERER')=="http://127.0.0.1:8000/home/":
		bool1=False
		redirect_var="todo-home"
	else:
		bool1=True
		redirect_var="history-page"

	tasks = TaskDataFilter(request.GET, queryset=TaskData.objects.filter(is_complete=bool1,user=request.user))
	with open('mohit.csv', 'a', newline="") as csv_file:    
		fieldnames = ['task_name', 'task_details', 'task_created_date','task_end_date'] 
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)  
		writer.writeheader()

		for task in tasks.qs:
			writer.writerow({'task_name':task.task_name, 'task_details':task.task_details, 'task_created_date':task.task_created_date,'task_end_date':task.task_end_date})
	messages.success(request, f'Your csv file has been created!')		
	return redirect(redirect_var) 		



def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		print(form)
		if form.is_valid():
			form.save()
			# messages.success(request, f'Your account has been created! You are now able to log in')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'register.html', {'form': form})


def home(request):
	task_qs=TaskData.objects.filter(is_complete=False,user=request.user)
	tasks = TaskDataFilter(request.GET, queryset=task_qs)
	
	# tasks=TaskData.objects.filter(is_complete=False)
	x = datetime.datetime.now()
	tdate=x.date()
	
	colordic={}
	for task in tasks.qs:
		y=(task.task_end_date - datetime.timedelta(days=2))
		if(task.task_end_date>=tdate>=y):
			colordic[task] = "blue"
		elif(task.task_end_date<tdate):
			colordic[task] = "red"
		else:
			colordic[task] = "green"

	print(colordic)
	
	context = {
		'colordic': colordic,
		'filter': tasks,
	}
	if tasks.qs :
		pass
	else:
		messages.success(request, f'Plese enter your first task')
		return redirect('task-create')
	return render(request,'home.html',context)

def history(request):
	tasks = TaskDataFilter(request.GET, queryset=TaskData.objects.filter(is_complete=True,user=request.user))
	context = {
		'tasks': tasks.qs,
		'filter': tasks,
	}
	return render(request, 'history.html',context)

def status(request,pk):
	task = TaskData.objects.get(pk=pk)
	task.is_complete = True
	task.save()
	messages.success(request, f'Task completed. you can see in history!')
	return redirect('history-page')

# @login_required
# def taskdetail(request, pk):
#     data=TaskData.objects.get(pk=pk)
#     u_form = TaskUpdateForm(instance=data)
	   

#     context = {
#         'u_form': u_form,
#         'id': pk,
#     }

#     return render(request, 'taskdetail.html', context)

@login_required
def taskdetail(request,pk):
	if request.method == 'POST':
		# data=TaskData.objects.get(pk=pk)
		u_form = TaskUpdateForm(request.POST, instance=request.user)
	  
		if u_form.is_valid():
			u_form.save()
			
			messages.success(request, f'Your account has been updated!')
			return redirect('task-detail')

	else:
		
		data=TaskData.objects.get(pk=pk)
		
		u_form = TaskUpdateForm(instance=data)

	context = {
		'u_form': u_form,
		'id': pk,
	}

	return render(request, 'taskdetail.html', context)

@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST,
								request.FILES,
								instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')

	else:
		# u=request.user
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form': u_form,
		'p_form': p_form
	}

	return render(request, 'profile.html', context)


# def edit(request, todo_id):
#     if request.method == 'POST':
#         todo = Todo.objects.get(id=todo_id)
#         form = TodoForm(request.POST or None, instance=todo)

#         if form.is_valid():
#             form.save()
#             messages.success(request, ('Task has been edited!'))
#             return redirect('home')
#     else:
#         todo = Todo.objects.get(id=todo_id)
#         return render(request, 'todoapp/edit.html', {'todo': todo})
	
# @login_required
# def taskdelete(request, pk):
#     data=TaskData.objects.get(pk=pk)
#     data.delete()
#     return redirect('todo-home')

class TaskCreateView(LoginRequiredMixin, CreateView):
	success_url= "/home/"
	model = TaskData
	fields = ['task_id','task_name', 'task_details', 'task_end_date', 'task_end_time']

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


# class TaskDetailView(LoginRequiredMixin, DetailView):
class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = TaskData
	success_url = '/home/'

	def test_func(self):
		task = self.get_object()
		# print(task.user)
		# print(self.request.user)
		if self.request.user == task.user:
			return True
		return False

	
class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = TaskData
	fields = ['task_id','task_name', 'task_details', 'task_end_date', 'task_end_time']
	success_url = '/home/'

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

	def test_func(self):
		task = self.get_object()
		# print(task.user)
		# print(self.request.user)
		if self.request.user == task.user:
			return True
		return False


# def history(request):
# 	task = TO_DO_PROJECT.objects.filter(completed=True)
# 	return render(request, 'todoapp/home.html', {'todos': task})

