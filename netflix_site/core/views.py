# Importing necessary functions and classes from django to render pages, manage authentication, and display messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages 
from .models import Movie, MovieList
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import re

# View function to display the index page
@login_required(login_url = 'login')
def index(request):
    movies = Movie.objects.all()
    featured_movie = movies[len(movies) - 1]

    context = {
        'movies': movies,
        'featured_movie' : featured_movie,
    }
    # Rendering the index.html template for any request to the index view
    return render(request, 'index.html', context)

# View function to display details for a specific movie
@login_required(login_url = 'login')
def movie(request, pk):
    # Retrieving the unique identifier for the movie from the URL
    movie_uuid = pk
    # Fetching the movie details from the database using the unique identifier
    movie_details = Movie.objects.get(uu_id=movie_uuid)

    context = {
        'movie_details': movie_details
    }
    # Rendering the movie.html template, passing in the movie details
    return render(request, 'movie.html', context)

@login_required(login_url='login')
def search(request):
    # Process the search query if the method is POST
    if request.method == 'POST':
        # Retrieve the search term from the POST request
        search_term = request.POST['search_term']
        # Query the Movie model for movies that contain the search term in their title, case-insensitive
        movies = Movie.objects.filter(title__icontains=search_term)

        # Prepare the context with the search results and the search term
        context = {
            'movies': movies,
            'search_term': search_term,
        }
        # Render the search results page, passing in the context
        return render(request, 'search.html', context)
    else:
        # Redirect to the homepage if the request method is not POST, indicating an invalid search attempt
        return redirect('/')


@login_required(login_url='login')
def my_list(request):
    # Querying the MovieList model to get all movie list entries for the current user
    movie_list = MovieList.objects.filter(owner_user=request.user)
    user_movie_list = []

    # Iterating over the queryset to extract each movie object and add it to the user_movie_list
    for movie in movie_list:
        user_movie_list.append(movie.movie)

    # Preparing the context with the user's movie list to be passed to the template
    context = {
        'movies': user_movie_list
    }
    # Rendering the my_list.html template, passing in the context containing the user's movie list
    return render(request, 'my_list.html', context)


# View function to add a movie to the user's list
@login_required(login_url='login')
def add_to_list(request):
    # Only process POST requests to add movies to the user's list
    if request.method == 'POST':
        # Extract the movie ID from the POST request
        movie_url_id = request.POST.get('movie_id')
        # Use regular expression to validate and extract the UUID from the movie ID
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        match = re.search(uuid_pattern, movie_url_id)
        movie_id = match.group() if match else None

        # Fetch the movie from the database or return 404 if not found
        movie = get_object_or_404(Movie, uu_id=movie_id)
        # Attempt to add the movie to the user's list, creating a new list entry if necessary
        movie_list, created = MovieList.objects.get_or_create(owner_user=request.user, movie=movie)

        # Provide feedback based on whether a new list entry was created
        if created:
            response_data = {'status': 'success', 'message': 'Added ✓'}
        else:
            response_data = {'status': 'info', 'message': 'Movie already in list'}

        # Return a JsonResponse with the operation result
        return JsonResponse(response_data)
    else:
        # Return an error response if the request method is not POST
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


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

# View function to handle the logout
@login_required(login_url = 'login')
def logout(request):
    # Log out the current user
    auth.logout(request)
    # Redirect to the login page after successfully logging out
    return redirect('login')


# View function to handle the genres
@login_required(login_url='login')
def genre(request, pk):
    # Retrieving the genre identifier from the URL parameter
    movie_genre = pk
    # Querying the Movie model to get all movies that match the given genre
    movies = Movie.objects.filter(genre=movie_genre)

    # Preparing the context with the list of movies belonging to the specified genre
    context = {
        'movies': movies,
        'movie_genre': movie_genre,  # Passing the genre back to the template for display or further use
    }
    # Rendering the genre.html template, passing in the context with movies of the specified genre
    return render(request, 'genre.html', context)
