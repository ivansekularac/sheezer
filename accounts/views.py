from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages

# Creating view function for sign up page
def signup_view(request):
    # Checking if request is POST
    if request.method == 'POST':
        # Crete new instance of User Creation Form and passing the POST data submitted
        form = UserCreationForm(request.POST)
        # Validate if the form is filled properly
        if form.is_valid():
            # Saving the user and logging in after that
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for { username }')            
            return redirect('home')
    else:
        # If request method is not POST we just return form instance
        form = UserCreationForm()
    # Render new page template and pass the form data to it
    return render(request, 'accounts/signup.html', { 'form': form })

# Creating login view function for login page
def login_view(request):
    # Checking if request is POST
    if request.method == 'POST':
        # Crete new instance of User Creation Form and passing the POST data submitted
        form = AuthenticationForm(data = request.POST)
        # Validate if the form is filled properly
        if form.is_valid():
            # If form is filled properly we are using get_user method to fetch the user from db and logging it in
            user = form.get_user()
            login(request, user)
            # If there is next key in POST data we redirect user to value of the key and if not redirect to home
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('home')
    else:
        # If request method is not POST we just return form instance
        form = AuthenticationForm()
    # Render new page template and pass the form data to it
    return render(request, 'accounts/login.html', { 'form': form })

# Creating logout view which does not have a template page
def logout_view(request):
    # Checking if request is POST
    if request.method == 'POST':
        # We don't need any other data to logout the user except request itself
        logout(request)
        # Redirect to login page after success
        return redirect('accounts:login')


# Creating User Profile view for Profile page
def profile_view(request):
    # Check if request is POST method
    if request.method == "POST":
        # Instantiate two forms we created and imported from forms.py
        user_form = UserUpdateForm(request.POST, instance = request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        # If both of the forms are valid perform save and redirect to profile url
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:profile')
    else:
        # Else we just create new forms
        user_form = UserUpdateForm(instance = request.user)
        profile_form = ProfileUpdateForm(instance = request.user.profile)

    # Save forms to dictionary and send them to template
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    # Render template and return it
    return render(request, 'accounts/profile.html', context)
