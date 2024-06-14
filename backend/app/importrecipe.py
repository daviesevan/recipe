import sqlite3
from app.models import db, Recipe

def transfer_data():
    conn = sqlite3.connect('recipes.db')
    print("Connected<<<<<<<")
    cursor = conn.cursor()

    
    cursor.execute('SELECT * FROM recipes')
    print("Data read<<<<")
    recipes = cursor.fetchall()


    for recipe in recipes:
        new_recipe = Recipe(
            id = recipe[0],
            title=recipe[1],
            ingredients=recipe[2],
            instructions=recipe[3]
        )
        db.session.add(new_recipe)
    db.session.commit()
    cursor.close()




