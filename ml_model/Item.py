
import pickle
import pandas as pd
import os
def item_based_recommendations(name):
    # Load dataset
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'user_product_df.pkl')

    with open(file_path, 'rb') as file:
        user_product_df = pickle.load(file)
    
    # Compute product correlation matrix
    product_name = name
    product_name = user_product_df[product_name]
    suggestions=user_product_df.corrwith(product_name).sort_values(ascending=False)
    sugg_df=pd.Series.to_frame(suggestions)
    sugg_df=sugg_df[sugg_df[0]>0.75]
    
    
    return sugg_df.index.to_list()



