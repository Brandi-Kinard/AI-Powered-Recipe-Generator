import json

# Load ingredients and recipes data
# The 'load_data' function reads both 'ingredients.json' and 'recipes.json' files and returns their data.
def load_data():
    with open('ingredients.json', 'r') as file:
        ingredients_data = json.load(file)

    with open('recipes.json', 'r') as file:
        recipes_data = json.load(file)

    return ingredients_data, recipes_data


def suggest_recipe(user_ingredients, recipes_data):
    user_ingredients_set = set(user_ingredients)

    suggested_recipes = []
    for recipe in recipes_data:
        recipe_ingredients_set = set(recipe['ingredients'])
        common_ingredients = recipe_ingredients_set & user_ingredients_set
        # Calculate match score based on the number of common ingredients
        # divided by the total number of ingredients in the recipe
        match_score = len(common_ingredients) / len(recipe_ingredients_set)
        # Add the match score to the recipe data
        recipe['match_score'] = match_score
        if match_score > 0:  # if there is at least one matching ingredient
            suggested_recipes.append(recipe)

    # Sort suggested recipes by their match score, highest first
    suggested_recipes.sort(key=lambda x: x['match_score'], reverse=True)

    # Return only the match recipe instead of all
    if suggested_recipes:
        return [suggested_recipes[0]]
    else:
        return []

'''
# CHECKS FOR A SUBSET, CALCULATE THE MATCH SCORE (this was replaced by the code above)

# Matching function to suggest recipes based on selected ingredients
# The 'suggest_recipe' function:
# • Takes user-selected ingredients and recipes data as input.
# • Uses sets to efficiently find recipes where the recipe ingredients are a subset of the user's ingredients.
# • Sorts the suggested recipes by the number of ingredients matching the user's selection, with recipes having more matching ingredients listed first.
# • Returns a list of suggested recipes.
def suggest_recipe(user_ingredients, recipes_data):
    # Convert user ingredients to a set for faster lookups
    user_ingredients_set = set(user_ingredients)
    
    suggested_recipes = []
    for recipe in recipes_data:
        recipe_ingredients_set = set(recipe['ingredients'])  # Use simplified ingredient list for matching
        if recipe_ingredients_set.issubset(user_ingredients_set):
            suggested_recipes.append(recipe)
    
    # Sort suggested recipes by the number of matching ingredients (more matches higher up)
    suggested_recipes.sort(key=lambda x: len(set(x['ingredients']) & user_ingredients_set), reverse=True)
    
    return suggested_recipes

'''
