from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# Creating view function for sign up page
def signup_view(request):
    # Checking if request is POST
    if request.method == 'POST':
        # Crete new instance of User Creation Form and passing the POST data submitted
        form = UserCreationForm(request.POST)
        # Validate if the form is filled properly
        if form.is_valid():
            # Saving the user and logging in after that
            user = form.save()
            login(request, user)
        # After successful login we redirect user to Home page
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
