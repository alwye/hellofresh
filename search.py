import os
import json
from shutil import copyfile, rmtree


def clean_search_results():
    for filename in os.listdir(search_results_path):
        file_path = os.path.join(search_results_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


recipes_path = os.path.join(os.getcwd(), "output")
search_results_path = os.path.join(os.getcwd(), "search_results")
recipe_file = 'recipe.json'
recipe_card_file = 'recipe.pdf'

clean_search_results()

for subdir, dirs, files in os.walk(recipes_path):
    if recipe_card_file in files:
        if recipe_file in files:
            json_path = os.path.join(subdir, recipe_file)
            with open(json_path, 'r') as f:
                recipe = json.load(f)
                average_rating = recipe.get('averageRating', 0)
                tags = [tag['name'] for tag in recipe['tags']]
                #if isinstance(average_rating, int) and average_rating > 3.3:
                if 'Healthy' in tags:
                    card_path = os.path.join(subdir, recipe_card_file)
                    dst_file = os.path.join(os.getcwd(), "search_results", recipe['id'] + '.pdf')
                    copyfile(card_path, dst_file)
