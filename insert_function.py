#!/usr/bin/env python3
import sys

with open('api/app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    new_lines.append(line)
    if line.strip().startswith('def get_meal_types_for_count'):
        # Find the end of the function (next line that starts with 'def' or empty line?)
        # We'll assume the function ends at the line before the next 'def' or end of file.
        # For safety, we'll insert after the entire block until an empty line followed by 'def'
        # But simpler: insert after the current line and before the next 'def'
        pass
    i += 1

# Instead, we'll just insert after the line number we know (line 501?)
# Let's do a simpler approach: find the line number of 'def generate_first_week_varied'
# and insert before it.
for idx, line in enumerate(lines):
    if line.strip().startswith('def generate_first_week_varied'):
        break
insert_idx = idx

new_function = '''
def get_calorie_distribution(target_calories, meals_per_day):
    """Distribuye calorías diarias entre los tipos de comida según porcentajes típicos."""
    meal_types = get_meal_types_for_count(meals_per_day)
    # Porcentajes basados en recomendaciones dietéticas (ajustables)
    if meals_per_day == 3:
        # desayuno 30%, comida 40%, cena 30%
        percentages = {'desayuno': 0.3, 'comida': 0.4, 'cena': 0.3}
    elif meals_per_day == 4:
        # desayuno 30%, comida 35%, merienda 10%, cena 25%
        percentages = {'desayuno': 0.3, 'comida': 0.35, 'merienda': 0.1, 'cena': 0.25}
    elif meals_per_day == 5:
        # desayuno 25%, almuerzo 10%, comida 35%, merienda 10%, cena 20%
        percentages = {'desayuno': 0.25, 'almuerzo': 0.1, 'comida': 0.35, 'merienda': 0.1, 'cena': 0.2}
    else:
        percentages = {meal_type: 1.0 / len(meal_types) for meal_type in meal_types}
    
    distribution = {}
    for meal_type in meal_types:
        distribution[meal_type] = round(percentages[meal_type] * target_calories)
    return distribution
'''

lines.insert(insert_idx, new_function + '\n')

with open('api/app.py', 'w') as f:
    f.writelines(lines)

print('Inserted new function before generate_first_week_varied')