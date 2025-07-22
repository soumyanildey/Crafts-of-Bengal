import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity

def item_based_recommendations():
    # Load dataset
    df = pd.read_csv('d:/project/Django/myproject/Final/FINAL_YEAR_PROJECT/e_commerce/ml_model/DATASET.csv')
    
    # Create user-product matrix
    user_product_df = df.pivot_table(index=["User_id"], columns=["Product Name"], values="Rating").fillna(0)
    
    # Compute cosine similarity matrix
    product_similarity = cosine_similarity(user_product_df.T)
    
    # Store product names
    product_names = list(user_product_df.columns)
    
    # Example recommendation logic
    recommended_items = [product for product in product_names if product_similarity[0][product_names.index(product)] > 0.5]
    
    # Return recommended items as a list
    return recommended_items

# Saving the model (if necessary)
with open('ItemBase.pkl', 'wb') as file:
    pickle.dump(item_based_recommendations, file)
