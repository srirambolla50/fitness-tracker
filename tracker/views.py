from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import date, timedelta
from .models import Workout, Meal, UserProfile
from .forms import WorkoutForm, MealForm, UserProfileForm

# ==================== HOME & AUTH VIEWS ====================

def home(request):
    """Home page - shows dashboard if logged in"""
    context = {}
    if request.user.is_authenticated:
        # Get today's data
        today = date.today()
        
        # Today's workouts
        today_workouts = Workout.objects.filter(user=request.user, date=today)
        total_calories_burned = today_workouts.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
        
        # Today's meals
        today_meals = Meal.objects.filter(user=request.user, date=today)
        total_calories_consumed = today_meals.aggregate(Sum('calories'))['calories__sum'] or 0
        total_protein = today_meals.aggregate(Sum('protein'))['protein__sum'] or 0
        total_carbs = today_meals.aggregate(Sum('carbs'))['carbs__sum'] or 0
        total_fats = today_meals.aggregate(Sum('fats'))['fats__sum'] or 0
        
        # This week's stats
        week_ago = today - timedelta(days=7)
        week_workouts = Workout.objects.filter(user=request.user, date__gte=week_ago).count()
        week_meals = Meal.objects.filter(user=request.user, date__gte=week_ago).count()
        
        context = {
            'today_workouts': today_workouts,
            'today_meals': today_meals,
            'total_calories_burned': total_calories_burned,
            'total_calories_consumed': total_calories_consumed,
            'total_protein': round(total_protein, 1),
            'total_carbs': round(total_carbs, 1),
            'total_fats': round(total_fats, 1),
            'week_workouts': week_workouts,
            'week_meals': week_meals,
        }
    
    return render(request, 'tracker/home.html', context)


def register_view(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
        
        from django.contrib.auth.models import User
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        messages.success(request, f'Account created for {username}! You can now login.')
        return redirect('login')
    
    return render(request, 'tracker/register.html')


def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')
    
    return render(request, 'tracker/login.html')


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')


# ==================== WORKOUT VIEWS ====================

@login_required
def workout_list(request):
    """View all workouts"""
    workouts = Workout.objects.filter(user=request.user)
    return render(request, 'tracker/workout_list.html', {'workouts': workouts})


@login_required
def workout_add(request):
    """Add new workout"""
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            messages.success(request, 'Workout added successfully! 💪')
            return redirect('workout_list')
    else:
        form = WorkoutForm(initial={'date': date.today()})
    
    return render(request, 'tracker/workout_form.html', {'form': form, 'title': 'Add Workout'})


@login_required
def workout_delete(request, pk):
    """Delete workout"""
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    workout.delete()
    messages.success(request, 'Workout deleted successfully!')
    return redirect('workout_list')


# ==================== MEAL VIEWS ====================

@login_required
def meal_list(request):
    """View all meals"""
    meals = Meal.objects.filter(user=request.user)
    return render(request, 'tracker/meal_list.html', {'meals': meals})


@login_required
def meal_add(request):
    """Add new meal"""
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            messages.success(request, 'Meal logged successfully! 🍎')
            return redirect('meal_list')
    else:
        form = MealForm(initial={'date': date.today()})
    
    return render(request, 'tracker/meal_form.html', {'form': form, 'title': 'Log Meal'})


@login_required
def meal_delete(request, pk):
    """Delete meal"""
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    meal.delete()
    messages.success(request, 'Meal deleted successfully!')
    return redirect('meal_list')


# ==================== PROFILE VIEW ====================

@login_required
def profile_view(request):
    """User profile"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'tracker/profile.html', {'form': form, 'profile': profile})
@login_required
def quick_add_meal(request, meal_id):
    """Quick add Indian food template"""
    template_meal = get_object_or_404(Meal, pk=meal_id)
    
    # Create a copy for current user
    Meal.objects.create(
        user=request.user,
        food_name=template_meal.food_name,
        meal_type=template_meal.meal_type,
        calories=template_meal.calories,
        protein=template_meal.protein,
        carbs=template_meal.carbs,
        fats=template_meal.fats,
        quantity=template_meal.quantity,
        date=date.today()
    )
    
    messages.success(request, f'{template_meal.food_name} added! 🍽️')
    return redirect('meal_list')


@login_required
def indian_foods_list(request):
    """Show Indian food templates for quick adding"""
    from django.contrib.auth.models import User
    system_user = User.objects.get(username='system_foods')
    indian_foods = Meal.objects.filter(user=system_user).order_by('meal_type', 'food_name')
    
    # Group by meal type
    breakfast_foods = indian_foods.filter(meal_type='breakfast')
    lunch_foods = indian_foods.filter(meal_type='lunch')
    snack_foods = indian_foods.filter(meal_type='snack')
    
    context = {
        'breakfast_foods': breakfast_foods,
        'lunch_foods': lunch_foods,
        'snack_foods': snack_foods,
    }
    
    return render(request, 'tracker/indian_foods.html', context)
@login_required
def progress_view(request):
    """Show weekly/monthly progress with charts"""
    from datetime import timedelta
    from django.db.models import Sum, Count
    from django.db.models.functions import TruncDate
    
    # Get last 7 days data
    today = date.today()
    week_ago = today - timedelta(days=7)
    
    # Workouts by day
    workouts_by_day = Workout.objects.filter(
        user=request.user,
        date__gte=week_ago
    ).values('date').annotate(
        total_calories=Sum('calories_burned'),
        count=Count('id')
    ).order_by('date')
    
    # Meals by day
    meals_by_day = Meal.objects.filter(
        user=request.user,
        date__gte=week_ago
    ).values('date').annotate(
        total_calories=Sum('calories'),
        total_protein=Sum('protein'),
        total_carbs=Sum('carbs'),
        total_fats=Sum('fats'),
        count=Count('id')
    ).order_by('date')
    
    # Format data for Chart.js
    dates = [(week_ago + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(8)]
    workout_calories = [0] * 8
    meal_calories = [0] * 8
    protein_data = [0] * 8
    
    for workout in workouts_by_day:
        date_str = workout['date'].strftime('%Y-%m-%d')
        if date_str in dates:
            idx = dates.index(date_str)
            workout_calories[idx] = workout['total_calories'] or 0
    
    for meal in meals_by_day:
        date_str = meal['date'].strftime('%Y-%m-%d')
        if date_str in dates:
            idx = dates.index(date_str)
            meal_calories[idx] = meal['total_calories'] or 0
            protein_data[idx] = round(meal['total_protein'] or 0, 1)
    
    context = {
        'dates': dates,
        'workout_calories': workout_calories,
        'meal_calories': meal_calories,
        'protein_data': protein_data,
    }
    
    return render(request, 'tracker/progress.html', context)
@login_required
def recommendations_view(request):
    """AI-powered recommendations based on user data"""
    from datetime import timedelta
    from django.db.models import Avg, Sum
    
    # Get user profile
    profile = UserProfile.objects.filter(user=request.user).first()
    
    # Get last 7 days data
    today = date.today()
    week_ago = today - timedelta(days=7)
    
    # Calculate averages
    avg_calories_burned = Workout.objects.filter(
        user=request.user, date__gte=week_ago
    ).aggregate(Avg('calories_burned'))['calories_burned__avg'] or 0
    
    avg_calories_consumed = Meal.objects.filter(
        user=request.user, date__gte=week_ago
    ).aggregate(Avg('calories'))['calories__avg'] or 0
    
    avg_protein = Meal.objects.filter(
        user=request.user, date__gte=week_ago
    ).aggregate(Avg('protein'))['protein__avg'] or 0
    
    workout_count = Workout.objects.filter(
        user=request.user, date__gte=week_ago
    ).count()
    
    # Generate recommendations
    recommendations = []
    
    # Calorie recommendations
    if profile and profile.fitness_goal == 'lose_weight':
        target_deficit = 500
        if avg_calories_consumed - avg_calories_burned > target_deficit:
            recommendations.append({
                'type': 'warning',
                'icon': 'fa-fire',
                'title': 'Calorie Deficit Needed',
                'message': f'For weight loss, aim for 500 calorie deficit. Currently: {round(avg_calories_consumed - avg_calories_burned)} calories. Reduce intake by {round(avg_calories_consumed - avg_calories_burned - target_deficit)} calories.',
                'action': 'Reduce portion sizes or increase cardio'
            })
    
    elif profile and profile.fitness_goal == 'gain_muscle':
        target_surplus = 300
        if avg_calories_consumed - avg_calories_burned < target_surplus:
            recommendations.append({
                'type': 'info',
                'icon': 'fa-dumbbell',
                'title': 'Calorie Surplus Needed',
                'message': f'For muscle gain, aim for 300 calorie surplus. Currently: {round(avg_calories_consumed - avg_calories_burned)} calories. Increase intake by {round(target_surplus - (avg_calories_consumed - avg_calories_burned))} calories.',
                'action': 'Add protein-rich meals like eggs, chicken, paneer'
            })
    
    # Protein recommendations
    if profile and profile.weight:
        target_protein = profile.weight * 1.6  # 1.6g per kg bodyweight
        if avg_protein < target_protein:
            recommendations.append({
                'type': 'warning',
                'icon': 'fa-egg',
                'title': 'Low Protein Intake',
                'message': f'Target: {round(target_protein)}g/day. Current: {round(avg_protein)}g/day. Increase by {round(target_protein - avg_protein)}g.',
                'action': 'Add: Chicken breast (31g), Paneer (18g), Eggs (6g each)'
            })
    
    # Workout frequency
    if workout_count < 3:
        recommendations.append({
            'type': 'info',
            'icon': 'fa-running',
            'title': 'Increase Workout Frequency',
            'message': f'You worked out {workout_count} times this week. Aim for at least 3-4 sessions for better results.',
            'action': 'Schedule 3-4 workout days per week'
        })
    
    # If doing well
    if not recommendations:
        recommendations.append({
            'type': 'success',
            'icon': 'fa-trophy',
            'title': 'Great Job! Keep It Up! 🎉',
            'message': 'Your nutrition and workout routine look excellent! You\'re on track to reach your goals.',
            'action': 'Maintain current habits and stay consistent'
        })
    
    context = {
        'recommendations': recommendations,
        'avg_calories_burned': round(avg_calories_burned),
        'avg_calories_consumed': round(avg_calories_consumed),
        'avg_protein': round(avg_protein, 1),
        'workout_count': workout_count,
        'profile': profile
    }
    
    return render(request, 'tracker/recommendations.html', context)