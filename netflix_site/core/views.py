# Importing necessary functions and classes from django to render pages, manage authentication, and display messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages 

# View function to display the index page
def index(request):
    # Rendering the index.html template for any request to the index view
    return render(request, 'index.html')

# View function to display the login page and handle login functionality
def login(request):
    # Check if the current request is a POST request, which indicates form submission
    if request.method == 'POST':
        # Retrieve the username and password from the submitted form data
        username = request.POST['username']
        password = request.POST['password']
        
        # Use Django's authentication system to verify the credentials
        user = auth.authenticate(username=username, password=password)
        
        # If the authentication is successful and a user object is returned
        if user is not None:
            # Log the user in, which sets up the session for the user
            auth.login(request, user)
            # Redirect to the homepage (or any other page) after successful login
            return redirect('/')
        else:
            # If authentication fails, inform the user that the credentials are invalid
            messages.info(request, 'Credentials Invalid')
            # Redirect back to the login page to allow the user to try again
            return redirect('login')
    
    # If the request method is not POST (e.g., GET), display the login page without any authentication attempt
    # This handles the case where the user initially navigates to the login page
    return render(request, 'login.html')


# View function to handle the signup process
def signup(request):
    # Checking if the request method is POST (form submission)
    if request.method == 'POST':
        # Extracting form data sent by the user
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Checking if the two entered passwords match
        if password == password2:
            # Checking if an user with the same email already exists
            if User.objects.filter(email=email).exists():
                # Informing the user that the email is already taken
                messages.info(request, 'Email taken')
                # Redirecting back to the signup page
                return redirect('signup')
            # Checking if an user with the same username already exists
            elif User.objects.filter(username=username).exists():
                # Informing the user that the username is already taken
                messages.info(request, 'Username taken')
                # Redirecting back to the signup page
                return redirect('signup')
            else:
                # Creating a new user with the provided credentials
                user = User.objects.create_user(username=username, email=email, password=password)
                # Saving the user to the database
                user.save()
                # Authenticating the user automatically after registration
                user_login = auth.authenticate(username=username, password=password)
                # Logging the user in
                auth.login(request, user_login)
                # Redirecting to the home page after successful signup and login
                return redirect('/')
        else:
            # Informing the user if the passwords do not match
            messages.info(request, 'Password not matching')
            # Redirecting back to the signup page for correction
            return redirect('signup')
    else:
        # If the request method is not POST, simply render the signup page template
        return render(request, 'signup.html')
