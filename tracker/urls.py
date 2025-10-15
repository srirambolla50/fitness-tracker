from django.urls import path
from . import views

urlpatterns = [
    # Home & Auth
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Workouts
    path('workouts/', views.workout_list, name='workout_list'),
    path('workouts/add/', views.workout_add, name='workout_add'),
    path('workouts/delete/<int:pk>/', views.workout_delete, name='workout_delete'),
    
    # Meals
    path('meals/', views.meal_list, name='meal_list'),
    path('meals/add/', views.meal_add, name='meal_add'),
    path('meals/delete/<int:pk>/', views.meal_delete, name='meal_delete'),
    
    # Profile
    path('profile/', views.profile_view, name='profile'),
    
    # Indian Foods
    path('indian-foods/', views.indian_foods_list, name='indian_foods'),
    path('quick-add/<int:meal_id>/', views.quick_add_meal, name='quick_add_meal'),
    # Progress
    path('progress/', views.progress_view, name='progress'),
    # Recommendations
    path('recommendations/', views.recommendations_view, name='recommendations'),
]