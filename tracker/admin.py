from django.contrib import admin
from .models import UserProfile, Workout, Meal

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'weight', 'height', 'fitness_goal', 'created_at']
    list_filter = ['fitness_goal']
    search_fields = ['user__username']

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise_name', 'sets', 'reps', 'calories_burned', 'date', 'created_at']
    list_filter = ['date', 'exercise_name']
    search_fields = ['user__username', 'exercise_name']
    date_hierarchy = 'date'

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['user', 'food_name', 'meal_type', 'calories', 'protein', 'carbs', 'fats', 'date', 'created_at']
    list_filter = ['date', 'meal_type']
    search_fields = ['user__username', 'food_name']
    date_hierarchy = 'date'