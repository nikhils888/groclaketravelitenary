import os

#Loading env variables from a local .env file
from  dotenv import load_dotenv
from groclake.cataloglake import CatalogLake

#Loading env variables from a local .env file
load_dotenv()

"""
  os.environ is a mapping object that maps the user's environmental variables. 
  It returns a dictionary or table having the user's environmental variable as key and their values as value.

  os.environ behaves like a common dictionary, so operations like get and set can be performed. 
  We can also alter the python os environment, but the changes will be effective only for the current process where it was assigned 
  and will not permanently change the value.
"""
os.environ['GROCLAKE_API_KEY'] = os.getenv('GROCLAKE_API_KEY')
os.environ['GROCLAKE_ACCOUNT_ID'] = os.getenv('GROCLAKE_ACCOUNT_ID')

cataloglake = CatalogLake()


# The catalog.create() method in the CatalogLake library of GrocLake is used to create a new catalog entry in the system.
groclake_cat = cataloglake.create()
# print(groclake_cat)

product_create_request = {
    "product_name_hint": "NB",
    "category_name_hint": "NB",
    "provider_name_hint": "britannica",
    "images": [
        {
            "image_name": "Napoleon Bonaparte",
            "image_url": "https://cdn.britannica.com/93/115193-050-6FFE7E0F/First-Consul-Bonaparte-canvas-Antoine-Jean-Gros-Legion-1802.jpg"
        }
    ]
}

groclake_create_product = cataloglake.gen(product_create_request)
print("gen data", groclake_create_product)
