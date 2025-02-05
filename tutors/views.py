from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Tutor
from .forms import TutorForm

@login_required
def tutors_list(request):
    tutors = Tutor.objects.select_related('user').all()
    filters = {}

    name_query = request.GET.get('name')
    if name_query:
        tutors = tutors.filter(name__icontains=name_query)
        filters['name'] = name_query

    surname_query = request.GET.get('surname')
    if surname_query:
        tutors = tutors.filter(surname__icontains=surname_query)
        filters['surname'] = surname_query

    email_query = request.GET.get('email')
    if email_query:
        tutors = tutors.filter(user__email__icontains=email_query)  # Use user__email for related email
        filters['email'] = email_query

    experience_query = request.GET.get('experience')
    if experience_query:
        tutors = tutors.filter(experience__icontains=experience_query)
        filters['experience'] = experience_query

    information_query = request.GET.get('information')
    if information_query:
        tutors = tutors.filter(information__icontains=information_query)
        filters['information'] = information_query


    return render(request, 'tutors/tutors_list.html', {'tutors': tutors, 'filters': filters})


@login_required
def tutor_detail(request, tutor_id):
    tutor = get_object_or_404(Tutor.objects.select_related('user'), id=tutor_id)
    return render(request, 'tutors/tutor_detail.html', {'tutor': tutor})

User = get_user_model()  # Get the custom user model

@login_required
def tutor_add(request):
    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            try:
                # Step 1: Use transaction to ensure both user and tutor are saved correctly
                with transaction.atomic():
                    # Step 2: Create and save the CustomUser first
                    user = User.objects.create_user(
                        email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['name'],
                        last_name=form.cleaned_data['surname'],
                        password='defaultpassword',  # Set a default password (should be updated later)
                        username=form.cleaned_data['email'],  # Assuming email is used as username
                        role='tutor'
                    )
                    user.save()  # Ensure the user is saved before creating the tutor

                    # Step 3: Create the Tutor instance and associate it with the user
                    tutor = form.save(commit=False)  # Don't save the tutor yet
                    tutor.user = user  # Associate the created user with the tutor
                    tutor.save()  # Save the tutor

                return redirect('tutors_list')  # Redirect to the tutors list or desired page
            except Exception as e:
                # Handle any exceptions that occur during the transaction
                print(f"Error: {e}")
                return render(request, 'tutors/tutors_add.html', {'form': form, 'error': str(e)})

    else:
        form = TutorForm()

    return render(request, 'tutors/tutors_add.html', {'form': form})

@login_required
def tutor_edit(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    if request.method == 'POST':
        form = TutorForm(request.POST, instance=tutor)
        if form.is_valid():
            tutor = form.save(commit=False)
            # Update associated User details
            user = tutor.user
            user.email = form.cleaned_data['email']  # Example: Update username to match email
            user.username = user.email
            user.save()
            tutor.save()
            return redirect('tutors_list')
    else:
        initial_data = {'email': tutor.user.email if tutor.user else ''}
        form = TutorForm(instance=tutor, initial=initial_data)
    return render(request, 'tutors/tutors_form.html', {'form': form})

def tutor_delete(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    if request.method == 'POST':
        # Optionally delete the associated User
        tutor.user.delete()
        tutor.delete()
        return redirect('tutors_list')
    return render(request, 'tutors/tutors_confirm_delete.html', {'tutor': tutor})

@login_required
def tutor_dashboard(request):
    if not request.user.is_tutor():
        return redirect('home')  # Prevent access if not a tutor
    return render(request, 'tutors/dashboard.html')