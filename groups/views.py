from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Group
from .forms import GroupForm


def groups_list(request):
    groups = Group.objects.all()
    filters = {}

    name_query = request.GET.get('name')
    if name_query:
        groups = groups.filter(name__icontains=name_query)
        filters['name'] = name_query

    tutor_query = request.GET.get('tutor')
    if tutor_query:
        groups = groups.filter(tutor__name__icontains=tutor_query)  # Filter by tutor's name
        filters['tutor'] = tutor_query

    course_query = request.GET.get('course')
    if course_query:
        groups = groups.filter(course__name__icontains=course_query) # Filter by course's name
        filters['course'] = course_query

    return render(request, 'groups/groups_list.html', {'groups': groups, 'filters': filters})

def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'groups/group_detail.html', {'group': group})

@login_required
def group_add(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('groups_list')
        form = GroupForm()
    else:
        form = GroupForm()
    
    return render(request, 'groups/groups_add.html', {'form': form})

@login_required
def group_edit(request, pk):
    group = get_object_or_404(Group, pk=pk)
    
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('groups_list')
    else:
        form = GroupForm(instance=group)
    return render(request, 'groups/groups_form.html', {'form': form})

@login_required
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('groups_list')
    return render(request, 'groups/groups_confirm_delete.html', {'group': group})
