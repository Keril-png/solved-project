from django.core.paginator import Paginator
from django.http.response import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required 
from .forms import ProblemForm
from .models import Problem, User
from django.urls import reverse
import os

def index(request):
    problem_list = Problem.objects.order_by('-pub_date').all()
    
    paginator = Paginator(problem_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  'problems/index.html',
                  {
                        'page': page,
                        'paginator': paginator,
                        'problems': problem_list,
                        
                  }
                )
    
    
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
@login_required
def new_problem(request):
    
    if request.method == 'POST':
        
        form = ProblemForm(
            request.POST,
            files=request.FILES or None
            )
        if form.is_valid():
            new = form.save(commit=False) 
            new.author = request.user 
            # handle_uploaded_file(request.FILES['file'])
            new.save() 
            return redirect('index')
        
        
        return render(request, 'problems/problem_create_form.html', {'form': form})
        
    form = ProblemForm()
    
    return render(request, 'problems/problem_create_form.html', {'form': form})


@login_required()
def edit_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    
    if request.user != problem.author: 
        return redirect("problem_detail", problem_id=problem_id)
    
    form = ProblemForm(request.POST or None, files=request.FILES or None, instance = problem)   
    
    if form.is_valid():
        form.save()
        return redirect('index')
    
    
    return render(request, 'problems/problem_create_form.html', {'form': form,
                                                                 'problem':problem,
                                                                'is_edit': True,
                                                             }
                  )
    
@login_required()
def delete_problem(request, problem_id):
    recipe = get_object_or_404(Problem, id=problem_id)

    if recipe.author == request.user:
        recipe.delete()
    return redirect(reverse('index'))
    

def profile(request, username):
    user = get_object_or_404(User, username=username)
    problem_list = Problem.objects.filter(author=user).order_by('-pub_date')
    
    paginator = Paginator(problem_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    return render(
        request,
        'problems/profile.html',
        {
            'user': user,
            'page': page,
            
            
        }
    )
    
def problem_detail(request, problem_id):
    
    problem = get_object_or_404(Problem, id = problem_id)
    
    return render(
        request,
        'problems/problem_detail.html',
        {
            'problem': problem,
            
        }
    )

def download_file(request, problem_id):
    problem = get_object_or_404(Problem, id = problem_id)
    
    filename = os.path.basename(problem.file.name)
    response = HttpResponse(problem.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response
              