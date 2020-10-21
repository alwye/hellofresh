import json
import os
import config as c
from hellofresh import HelloFresh

hf = HelloFresh(c.username, c.password)


def save_recipe(id, recipe_json, card):
    recipe_dir_path = os.path.join(os.getcwd(), "output", id)

    if not os.path.exists(recipe_dir_path):
        os.mkdir(recipe_dir_path)

    # create recipe JSON
    recipe_json_path = os.path.join(recipe_dir_path, "recipe.json")
    with open(recipe_json_path, "w") as fw:
        fw.write(recipe_json)

    # save the PDF card
    if card is not False:
        recipe_pdf_path = os.path.join(recipe_dir_path, "recipe.pdf")
        with open(recipe_pdf_path, "wb") as fw:
            fw.write(card)


for recipe in hf.get_recipes():
    recipe_id = recipe['id']
    card_link = recipe['cardLink']
    recipe_str = json.dumps(recipe, sort_keys=True, indent=4)
    recipe_card = hf.download_card(card_link)
    save_recipe(recipe_id, recipe_str, recipe_card)
    print(recipe_id)
