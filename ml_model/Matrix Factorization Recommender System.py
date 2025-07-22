import pandas as pd
import pickle

def matrix_factorization_recommendations():
    # Load dataset
    df = pd.read_csv('d:/project/Django/myproject/Final/FINAL_YEAR_PROJECT/e_commerce/ml_model/DATASET.csv')
    
    # Example logic to recommend based on factorization
    product_ratingCount = (df.groupby(by=['Product Name'])['Rating'].count().reset_index().rename(columns={'Rating': 'totalRatingCount'}))
    
    # Logic to return recommended items
    recommended_items = product_ratingCount[product_ratingCount['totalRatingCount'] > 10]['Product Name'].tolist()
    
    # Return recommended items as a list
    return recommended_items

# Saving the model (if necessary)
with open('MatFac.pkl', 'wb') as file:
    pickle.dump(matrix_factorization_recommendations, file)
