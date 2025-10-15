from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    """
    Extended user profile with fitness information
    """
    GOAL_CHOICES = [
        ('lose_weight', 'Lose Weight'),
        ('maintain', 'Maintain Weight'),
        ('gain_muscle', 'Gain Muscle'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(help_text="Weight in kg", null=True, blank=True)
    height = models.FloatField(help_text="Height in cm", null=True, blank=True)
    fitness_goal = models.CharField(max_length=20, choices=GOAL_CHOICES, default='maintain')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def bmi(self):
        """Calculate BMI"""
        if self.weight and self.height:
            height_m = self.height / 100  # convert cm to meters
            return round(self.weight / (height_m ** 2), 2)
        return None


class Workout(models.Model):
    """
    Workout log for tracking exercises
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=200)
    sets = models.IntegerField(default=1)
    reps = models.IntegerField(default=1)
    weight_used = models.FloatField(help_text="Weight in kg", null=True, blank=True)
    calories_burned = models.IntegerField(default=0)
    duration = models.IntegerField(help_text="Duration in minutes", default=30)
    notes = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.exercise_name} on {self.date}"


class Meal(models.Model):
    """
    Meal log for tracking nutrition
    """
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES, default='breakfast')
    food_name = models.CharField(max_length=200)
    calories = models.IntegerField(default=0)
    protein = models.FloatField(help_text="Protein in grams", default=0)
    carbs = models.FloatField(help_text="Carbohydrates in grams", default=0)
    fats = models.FloatField(help_text="Fats in grams", default=0)
    quantity = models.FloatField(default=1, help_text="Serving size")
    notes = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.food_name} ({self.meal_type}) on {self.date}"