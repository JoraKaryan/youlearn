from django.shortcuts import get_object_or_404, render, redirect
from .models import Group
from .forms import GroupForm


def groups_list(request):
    groups = Group.objects.all()
    return render(request, 'groups/groups_list.html', {'groups': groups})

def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'groups/group_detail.html', {'group': group})


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

def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('groups_list')
    return render(request, 'groups/groups_confirm_delete.html', {'group': group})
