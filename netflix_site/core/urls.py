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

    path('logout', views.logout, name='logout'),
    
    # Define a URL pattern for the 'signup' path.
    # When "/signup" is accessed, Django will execute the views.signup function.
    path('signup', views.signup, name='signup'),

    # Define a URL pattern for individual movie details.
    # When "/movie/<str:pk>/" is accessed, Django will execute the views.movie function, passing the 'pk' as a parameter.
    path('movie/<str:pk>/', views.movie, name = 'movie'),
 


]
