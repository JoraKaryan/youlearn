from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Course
from .forms import CourseForm

def courses_list(request):
    courses = Course.objects.all()
    filters = {}

    name_query = request.GET.get('name')
    if name_query:
        courses = courses.filter(name__icontains=name_query)
        filters['name'] = name_query

    description_query = request.GET.get('description')
    if description_query:
        courses = courses.filter(description__icontains=description_query)
        filters['description'] = description_query

    duration_query = request.GET.get('duration')
    if duration_query:
        courses = courses.filter(duration__icontains=duration_query)  # Or exact match: duration=duration_query
        filters['duration'] = duration_query

    price_query = request.GET.get('price')
    if price_query:
        try:
            price = float(price_query) #try to convert to float
            courses = courses.filter(price=price) #if it is number filter by number
            filters['price'] = price_query
        except ValueError:
            pass #if not number do not filter by price


    return render(request, 'courses/courses_list.html', {'courses': courses, 'filters': filters})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})

@login_required
def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses_list')
        form = CourseForm()
    else:
        form = CourseForm()
    
    return render(request, 'courses/courses_add.html', {'form': form})

@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/courses_form.html', {'form': form})

@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('courses_list')
    return render(request, 'courses/courses_confirm_delete.html', {'course': course})
