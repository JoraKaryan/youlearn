from django.shortcuts import get_object_or_404, render, redirect
from .models import Tutor
from .forms import TutorForm

def tutors_list(request):
    tutors = Tutor.objects.all()
    return render(request, 'tutors/tutors_list.html', {'tutors': tutors})

def tutor_detail(request, tutor_id):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    
    return render(request, 'tutors/tutor_detail.html', {'tutor': tutor})

def tutor_add(request):
    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tutors_list')
    else:
        form = TutorForm()
    
    return render(request, 'tutors/tutors_add.html', {'form': form})

def tutor_edit(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    
    if request.method == 'POST':
        form = TutorForm(request.POST, instance=tutor)
        if form.is_valid():
            form.save()
            return redirect('tutors_list')
    else:
        form = TutorForm(instance=tutor)
    return render(request, 'tutors/tutors_form.html', {'form': form})

def tutor_delete(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    if request.method == 'POST':
        tutor.delete()
        return redirect('tutors_list')
    return render(request, 'tutors/tutors_confirm_delete.html', {'tutor': tutor})
