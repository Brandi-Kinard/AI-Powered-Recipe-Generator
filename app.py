# 'Flask' is imported to use the Flask framework for creating the web app.
# 'jsonify' is used to convert the Python dictionary into a JSON response.
from flask import Flask, jsonify, send_from_directory
# 'json' is used to load your JSON file.
import json
# importing 'render_template'
from flask import Flask, jsonify, render_template
# import the clustering function along with other functions from 'data_structures.py'
from data_structures import suggest_recipe, load_data, cluster_recipes
# importing the 'request' module object is part of the Flask framework and is used to ...
# ... handle data received in the HTTP request.
from flask import request 

app = Flask(__name__)

# Assuming load_data() loads your recipes data
_, recipes_data = load_data()
# Apply clustering to recipes data at startup
recipes_data, ingredient_clusters = cluster_recipes(recipes_data, n_clusters=5)  # Adjust n_clusters as needed

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ingredients')
def ingredients():
    try:
        with open('ingredients.json', 'r') as f:
            # 'json.load(f)' reads the JSON file and converts it into a Python dictionary.
            data = json.load(f)
        # 'jsonify(data)' converts the dictionary into a JSON-formatted response.
        return jsonify(data)
    # If the 'ingredients.json' file is not found, it returns an error message with a 404 status code.
    except FileNotFoundError:
        return jsonify({"error": "Ingredients database not found."}), 404

@app.route('/submit-ingredients', methods=['POST'])
def submit_ingredients():
    user_ingredients = request.json['selectedIngredients']
    suggested_recipes = suggest_recipe(user_ingredients, recipes_data)
    
    response_data = {
        "best_match": None,
        "additional_suggestions": [],
        "message": None
    }

    # Check if there are any suggested recipes (i.e., if suggested_recipes is not empty)
    if suggested_recipes:
        # If there are suggestions, retrieve the best match
        best_match = suggested_recipes[0]
        # Calculate the match percentage between the user's selected ingredients adn teh best match's ingredients
        match_percentage = len(set(best_match['ingredients']) & set(user_ingredients)) / len(set(best_match['ingredients']))
        
        # If the match percentage is less than 100%
        if match_percentage < 1.0:  # If not all user's ingredients are used
            # Set a message to inform the user that no recipe was found that uses all of their ingredients
            response_data['message'] = "Hmm, it seems we couldn't find a smoothie that uses all your chosen ingredients. But don't worry, we've still got something tasty for you! Here's a smoothie recipe that uses at least some of your selected ingredients. You might need to grab a few extra items next time you're out shopping, though. Keep it chill and remember, the perfect smoothie mix is just a few ticks away!"
        
        response_data['best_match'] = [best_match]
        
        # Find additional suggestions
        best_match_cluster = best_match['cluster']
        additional_suggestions = [recipe for recipe in recipes_data if recipe['cluster'] == best_match_cluster and recipe['name'] != best_match['name']]
        response_data['additional_suggestions'] = additional_suggestions[:5]  # Limit to 5 suggestions for simplicity
    else:
        response_data['message'] = "No matching recipes found. Please try different ingredients."
    
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)


