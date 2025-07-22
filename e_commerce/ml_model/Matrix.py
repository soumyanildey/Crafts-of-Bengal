import pickle
print(pickle.format_version)
import os
def matrix_factorization_recommendations(name):
    # Load dataset
    
    file_path1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'correlation_matrix.pkl')
    file_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'product_title')
    file_path3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'product_title_list')
    
    # Example logic to recommend based on factorization
    # Loading the numpy ndarray from the pickle file
    with open(file_path1, 'rb') as file1:
        corr = pickle.load(file1)

    with open(file_path2, 'rb') as file2:
        product_title_list = pickle.load(file2)

    with open(file_path3, 'rb') as file3:
        product_title = pickle.load(file3)
    
    coffey_hands = product_title_list.get_loc(name)
    corr_coffey_hands  = corr[coffey_hands]
    
    # Logic to return recommended items
    recommended_items = [product_title[i] for i in range(len(corr_coffey_hands)) if corr_coffey_hands[i] >= 0.75]
    
    # Return recommended items as a list
    return recommended_items




