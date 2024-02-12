# Import the path function from django.urls to define url paths, and import the views module from the current package
from django.urls import path
from . import views

# List of url patterns that Django will use to match browser URLs to the appropriate view function
urlpatterns = [
    # Define a URL pattern for the root URL ('') which maps to the 'index' view. 
    # When the site's root URL is accessed, Django will execute the views.index function.
    path('', views.index, name='index'),
    
    # Define a URL pattern for the 'login' path. 
    # When "/login" is accessed, Django will execute the views.login function.
    path('login', views.login, name='login'),

    # Define a URL pattern for the 'logout' path.
    # When "/logout" is accessed, Django will execute the views.logout function, allowing users to log out.
    path('logout', views.logout, name='logout'),
    
    # Define a URL pattern for the 'signup' path.
    # When "/signup" is accessed, Django will execute the views.signup function.
    path('signup', views.signup, name='signup'),

    # Define a URL pattern for individual movie details.
    # When "/movie/<str:pk>/" is accessed, Django will execute the views.movie function, passing the 'pk' as a parameter.
    path('movie/<str:pk>/', views.movie, name='movie'),
    
    # Define a URL pattern for accessing a user's personal list of movies.
    # When "/my-list" is accessed, Django will execute the views.my_list function, displaying the user's list of movies.
    path('my-list', views.my_list, name='my-list'),

    # Define a URL pattern for adding a movie to the user's personal list.
    # When "/add-to-list" is accessed, Django will execute the views.add_to_list function, allowing users to add movies to their list.
    path('add-to-list', views.add_to_list, name='add-to-list'),

    # Define a URL pattern for the search functionality.
    # When "/search" is accessed, Django will execute the views.search function, allowing users to search for movies.
    path('search', views.search, name='search'),

    # Define a URL pattern for accessing movies by genre.
    # When "/genre/<str:pk>/" is accessed, Django will execute the views.genre function, passing the 'pk' as a parameter.
    # This allows users to view movies filtered by a specific genre.
    path('genre/<str:pk>/', views.genre, name='genre'),
]

