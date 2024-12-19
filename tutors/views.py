from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .models import Tutor
from .forms import TutorForm

# def tutors_list(request):
#     tutors = Tutor.objects.all()
#     return render(request, 'tutors/tutors_list.html', {'tutors': tutors})

def tutors_list(request):
    tutors = Tutor.objects.select_related('user').all()  # Optimize query with select_related
    return render(request, 'tutors/tutors_list.html', {'tutors': tutors})

# def tutor_detail(request, tutor_id):
#     tutor = get_object_or_404(Tutor, id=tutor_id)
    
#     return render(request, 'tutors/tutor_detail.html', {'tutor': tutor})

def tutor_detail(request, tutor_id):
    tutor = get_object_or_404(Tutor.objects.select_related('user'), id=tutor_id)
    return render(request, 'tutors/tutor_detail.html', {'tutor': tutor})

# def tutor_add(request):
#     if request.method == 'POST':
#         form = TutorForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('tutors_list')
#     else:
#         form = TutorForm()
    
#     return render(request, 'tutors/tutors_add.html', {'form': form})

def tutor_add(request):
    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            tutor = form.save(commit=False)
            # Create and associate a User with the Tutor
            user = User.objects.create_user(
                username=form.cleaned_data['name'],  # Example: Use name as username
                password='defaultpassword'  # Set a default password (should be updated later)
            )
            tutor.user = user
            tutor.save()
            return redirect('tutors_list')
    else:
        form = TutorForm()
    return render(request, 'tutors/tutors_add.html', {'form': form})

# def tutor_edit(request, pk):
#     tutor = get_object_or_404(Tutor, pk=pk)
    
#     if request.method == 'POST':
#         form = TutorForm(request.POST, instance=tutor)
#         if form.is_valid():
#             form.save()
#             return redirect('tutors_list')
#     else:
#         form = TutorForm(instance=tutor)
#     return render(request, 'tutors/tutors_form.html', {'form': form})

def tutor_edit(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    if request.method == 'POST':
        form = TutorForm(request.POST, instance=tutor)
        if form.is_valid():
            tutor = form.save(commit=False)
            # Update associated User details
            user = tutor.user
            user.username = form.cleaned_data['name']  # Example: Update username to match email
            user.save()
            tutor.save()
            return redirect('tutors_list')
    else:
        form = TutorForm(instance=tutor)
    return render(request, 'tutors/tutors_form.html', {'form': form})

# def tutor_delete(request, pk):
#     tutor = get_object_or_404(Tutor, pk=pk)
#     if request.method == 'POST':
#         tutor.delete()
#         return redirect('tutors_list')
#     return render(request, 'tutors/tutors_confirm_delete.html', {'tutor': tutor})

def tutor_delete(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    if request.method == 'POST':
        # Optionally delete the associated User
        tutor.user.delete()
        tutor.delete()
        return redirect('tutors_list')
    return render(request, 'tutors/tutors_confirm_delete.html', {'tutor': tutor})