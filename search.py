import os
import json

output_path = os.path.join(os.getcwd(), "output")
recipe_file = 'recipe.json'

for subdir, dirs, files in os.walk(output_path):
    if recipe_file in files:
        json_path = os.path.join(subdir, recipe_file)
        with open(json_path, 'r') as f:
            recipe = json.load(f)



