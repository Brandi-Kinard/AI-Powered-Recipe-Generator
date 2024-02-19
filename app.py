# 'Flask' is imported to use the Flask framework for creating the web app.
# 'jsonify' is used to convert the Python dictionary into a JSON response.
from flask import Flask, jsonify, send_from_directory
# 'json' is used to load your JSON file.
import json
# importing 'render_template'
from flask import Flask, jsonify, render_template
from data_structures import suggest_recipe, load_data
# importing the 'request' module object is part of the Flask framework and is used to ...
# ... handle data received in the HTTP request.
from flask import request 

app = Flask(__name__)

# Assuming load_data() loads your recipes data
_, recipes_data = load_data()

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
    # Get the list of ingredients from the request JSON
    user_ingredients = request.json['selectedIngredients']
    # Use the suggest_recipe function to find matching recipes
    suggested_recipes = suggest_recipe(user_ingredients, recipes_data)
    # Return the suggestions as JSON
    return jsonify(suggested_recipes)

if __name__ == "__main__":
    app.run(debug=True)


