from django.core.management.base import BaseCommand
from tracker.models import Meal
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Loads common Indian foods into database as templates'

    def handle(self, *args, **kwargs):
        # Get or create a system user for template foods
        system_user, created = User.objects.get_or_create(
            username='system_foods',
            defaults={'email': 'system@fitnesstracker.com'}
        )
        
        # Indian foods database with accurate macros
        indian_foods = [
            # Breakfast Items
            {'name': 'Plain Dosa (1 piece)', 'calories': 133, 'protein': 2.6, 'carbs': 24, 'fats': 2.5, 'type': 'breakfast'},
            {'name': 'Masala Dosa (1 piece)', 'calories': 250, 'protein': 5, 'carbs': 40, 'fats': 7, 'type': 'breakfast'},
            {'name': 'Idli (2 pieces)', 'calories': 78, 'protein': 2, 'carbs': 17, 'fats': 0.2, 'type': 'breakfast'},
            {'name': 'Vada (2 pieces)', 'calories': 200, 'protein': 4, 'carbs': 20, 'fats': 12, 'type': 'breakfast'},
            {'name': 'Poha (1 bowl)', 'calories': 180, 'protein': 3, 'carbs': 35, 'fats': 3, 'type': 'breakfast'},
            {'name': 'Upma (1 bowl)', 'calories': 190, 'protein': 5, 'carbs': 35, 'fats': 4, 'type': 'breakfast'},
            {'name': 'Paratha (1 piece)', 'calories': 230, 'protein': 4, 'carbs': 30, 'fats': 10, 'type': 'breakfast'},
            {'name': 'Aloo Paratha (1 piece)', 'calories': 300, 'protein': 6, 'carbs': 40, 'fats': 12, 'type': 'breakfast'},
            
            # Rice Items
            {'name': 'Plain Rice (1 bowl)', 'calories': 206, 'protein': 4.3, 'carbs': 45, 'fats': 0.4, 'type': 'lunch'},
            {'name': 'Jeera Rice (1 bowl)', 'calories': 250, 'protein': 5, 'carbs': 45, 'fats': 5, 'type': 'lunch'},
            {'name': 'Biryani - Chicken (1 plate)', 'calories': 450, 'protein': 25, 'carbs': 55, 'fats': 15, 'type': 'lunch'},
            {'name': 'Biryani - Veg (1 plate)', 'calories': 350, 'protein': 10, 'carbs': 60, 'fats': 10, 'type': 'lunch'},
            {'name': 'Curd Rice (1 bowl)', 'calories': 220, 'protein': 6, 'carbs': 40, 'fats': 4, 'type': 'lunch'},
            
            # Roti/Bread
            {'name': 'Roti (1 piece)', 'calories': 71, 'protein': 3, 'carbs': 15, 'fats': 0.4, 'type': 'lunch'},
            {'name': 'Naan (1 piece)', 'calories': 262, 'protein': 9, 'carbs': 45, 'fats': 5, 'type': 'lunch'},
            {'name': 'Chapati (1 piece)', 'calories': 104, 'protein': 3.5, 'carbs': 18, 'fats': 2, 'type': 'lunch'},
            
            # Curries/Side Dishes
            {'name': 'Dal Tadka (1 bowl)', 'calories': 150, 'protein': 9, 'carbs': 20, 'fats': 4, 'type': 'lunch'},
            {'name': 'Rajma (1 bowl)', 'calories': 180, 'protein': 10, 'carbs': 25, 'fats': 5, 'type': 'lunch'},
            {'name': 'Chole (1 bowl)', 'calories': 200, 'protein': 10, 'carbs': 30, 'fats': 5, 'type': 'lunch'},
            {'name': 'Paneer Butter Masala (1 bowl)', 'calories': 350, 'protein': 15, 'carbs': 15, 'fats': 25, 'type': 'lunch'},
            {'name': 'Chicken Curry (1 bowl)', 'calories': 280, 'protein': 25, 'carbs': 10, 'fats': 15, 'type': 'lunch'},
            {'name': 'Sambar (1 bowl)', 'calories': 100, 'protein': 5, 'carbs': 15, 'fats': 2, 'type': 'lunch'},
            
            # Snacks
            {'name': 'Samosa (2 pieces)', 'calories': 308, 'protein': 6, 'carbs': 40, 'fats': 14, 'type': 'snack'},
            {'name': 'Pakora (5 pieces)', 'calories': 250, 'protein': 5, 'carbs': 30, 'fats': 12, 'type': 'snack'},
            {'name': 'Bhel Puri (1 plate)', 'calories': 180, 'protein': 4, 'carbs': 30, 'fats': 5, 'type': 'snack'},
            {'name': 'Pani Puri (6 pieces)', 'calories': 150, 'protein': 3, 'carbs': 25, 'fats': 4, 'type': 'snack'},
            
            # Sweets
            {'name': 'Gulab Jamun (2 pieces)', 'calories': 300, 'protein': 3, 'carbs': 50, 'fats': 10, 'type': 'snack'},
            {'name': 'Jalebi (2 pieces)', 'calories': 150, 'protein': 1, 'carbs': 30, 'fats': 3, 'type': 'snack'},
            {'name': 'Rasgulla (2 pieces)', 'calories': 186, 'protein': 4, 'carbs': 40, 'fats': 1, 'type': 'snack'},
            
            # Beverages & Others
            {'name': 'Chai (1 cup)', 'calories': 60, 'protein': 2, 'carbs': 8, 'fats': 2, 'type': 'snack'},
            {'name': 'Coffee (1 cup)', 'calories': 50, 'protein': 2, 'carbs': 6, 'fats': 2, 'type': 'snack'},
            {'name': 'Lassi (1 glass)', 'calories': 150, 'protein': 6, 'carbs': 20, 'fats': 5, 'type': 'snack'},
            
            # Protein Items
            {'name': 'Boiled Egg (1 piece)', 'calories': 68, 'protein': 6, 'carbs': 0.6, 'fats': 4.8, 'type': 'snack'},
            {'name': 'Egg Omelette (2 eggs)', 'calories': 154, 'protein': 13, 'carbs': 1, 'fats': 11, 'type': 'breakfast'},
            {'name': 'Chicken Breast (100g)', 'calories': 165, 'protein': 31, 'carbs': 0, 'fats': 3.6, 'type': 'lunch'},
            {'name': 'Paneer (100g)', 'calories': 265, 'protein': 18, 'carbs': 1.2, 'fats': 20, 'type': 'lunch'},
        ]
        
        self.stdout.write(self.style.SUCCESS('Loading Indian foods...'))
        
        count = 0
        for food in indian_foods:
            # Check if food already exists
            if not Meal.objects.filter(user=system_user, food_name=food['name']).exists():
                Meal.objects.create(
                    user=system_user,
                    food_name=food['name'],
                    meal_type=food['type'],
                    calories=food['calories'],
                    protein=food['protein'],
                    carbs=food['carbs'],
                    fats=food['fats'],
                    quantity=1,
                    notes='Template food (Indian database)'
                )
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} Indian foods!'))