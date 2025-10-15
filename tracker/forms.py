from django import forms
from .models import Workout, Meal, UserProfile

class WorkoutForm(forms.ModelForm):
    """
    Form for adding/editing workouts
    """
    class Meta:
        model = Workout
        fields = ['exercise_name', 'sets', 'reps', 'weight_used', 'calories_burned', 'duration', 'notes', 'date']
        widgets = {
            'exercise_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Push-ups, Bench Press, Running'
            }),
            'sets': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '3',
                'min': '1'
            }),
            'reps': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '12',
                'min': '1'
            }),
            'weight_used': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Weight in kg (optional)',
                'step': '0.5'
            }),
            'calories_burned': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Estimated calories',
                'min': '0'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duration in minutes',
                'min': '1'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any notes about this workout...',
                'rows': 3
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }


class MealForm(forms.ModelForm):
    """
    Form for adding/editing meals
    """
    class Meta:
        model = Meal
        fields = ['meal_type', 'food_name', 'calories', 'protein', 'carbs', 'fats', 'quantity', 'notes', 'date']
        widgets = {
            'meal_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'food_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Chicken Breast, Oatmeal, Apple'
            }),
            'calories': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Total calories',
                'min': '0'
            }),
            'protein': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Protein in grams',
                'step': '0.1',
                'min': '0'
            }),
            'carbs': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Carbs in grams',
                'step': '0.1',
                'min': '0'
            }),
            'fats': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fats in grams',
                'step': '0.1',
                'min': '0'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Serving size',
                'step': '0.1',
                'min': '0.1'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any notes about this meal...',
                'rows': 3
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }


class UserProfileForm(forms.ModelForm):
    """
    Form for user profile
    """
    class Meta:
        model = UserProfile
        fields = ['age', 'weight', 'height', 'fitness_goal']
        widgets = {
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your age',
                'min': '10',
                'max': '120'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Weight in kg',
                'step': '0.1',
                'min': '20'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Height in cm',
                'step': '0.1',
                'min': '50'
            }),
            'fitness_goal': forms.Select(attrs={
                'class': 'form-control'
            })
        }