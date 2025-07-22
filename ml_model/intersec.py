import pickle
from  . import Matrix
from . import Item


# Load the Matrix Factorization recommendations list
# with open('ml_model\MatFac.pkl', 'rb') as file:
#     matrix_factorization_results = pickle.load(file)

def load_model_results(name):
    # Find the intersection of the two lists
    matrix_factorization_results = Matrix.matrix_factorization_recommendations(name)
    item_based_results = Item.item_based_recommendations(name)
    
    intersection_items = list(set(matrix_factorization_results+item_based_results))
    
    # Print the intersection items to the console
    print("Intersection of Recommended Items:", intersection_items)
    
    return intersection_items

# Call the function and print the result
