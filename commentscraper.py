import requests
import pandas as pd
import csv
import streamlit as st

st.set_page_config(page_title="Instragram Comment Scraper",
                   page_icon="📎",
                   layout="wide",
                   initial_sidebar_state="expanded")

st.title("""Instragram Comment Scraper""")
file = st.file_uploader("Upload a CSV file")


rapid_api_key = "524970b541msh85f0a580cda5de9p129a7ajsnc109631e2d31"

def get_post_comments_request(post_code, pagination_token=None):
    # Set the API endpoint URL, request parameters and RapidAPI headers
    url = "https://instagram-scraper-api2.p.rapidapi.com/v1/comments"
    querystring = {
        "code_or_id_or_url" : post_code,
        "pagination_token": pagination_token
    }
    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "instagram-scraper-api2.p.rapidapi.com"
    }

    comments = [] # list of posts retrieved
    next_token = None # pagination token retrieved for next page
    try:
        response = requests.get(url, headers=headers, params=querystring)
        status_code = response.status_code
        
        if status_code == 200: # success
            response_json = response.json()
            comments = response_json["data"]["items"]
            next_token = response_json["pagination_token"]
        elif status_code == 404:
            print("Account invalid or private")
        else:
            print("Error:", response.text)

    except Exception as e:
        print("Unexpected error:", e)
    
    return comments, next_token

def get_post_comments_all(post_code):
    # List to store all posts
    comments = []
    # Set no pagination for first request
    pagination_token = None
    
    while True:
        
        # Get one "page" of posts
        new_comments, next_token = get_post_comments_request(post_code, pagination_token=pagination_token)
        
        # update the list of posts and the pagination token
        comments += new_comments
        pagination_token = next_token
        
        print(f"Total comments after request: {len(comments)}")
        
        # No `pagination_token` = no more posts
        if pagination_token is None:
            break
    
    return comments
# Initialize an empty list to store dataframes
# all_comments_data = []
# columns_to_drop = ['created_at', 'created_at_utc','inline_composer_display_condition','is_covered','did_report_as_spam','did_report_as_spam']
# Open the CSV file
# with open(file, newline='') as csvfile:
#     # Create a CSV reader object
#     reader = csv.reader(csvfile)
#     # Iterate through each row in the CSV file
#     for row in reader:
#         # Assuming the post code is in the first column (index 0)
#         post_code = row[0]
#         # Retrieve comments for the current post code
#         comments_list = get_post_comments_all(post_code)
#         # Convert comments_list to a DataFrame
#         df = pd.DataFrame(comments_list)
#         # Add a new column 'Post_Code' to identify the post
#         df['Image_URL'] = post_code
#         # Append the DataFrame to the list
#         all_comments_data.append(df)

# # Concatenate all dataframes into a single dataframe
# all_comments_df = pd.concat(all_comments_data, ignore_index=True)
# all_comments_df.drop(columns=columns_to_drop, inplace=True)

# # Displaying the concatenated DataFrame
# print(all_comments_df)

# # Save the concatenated DataFrame to a CSV file
# all_comments_df.to_csv('all_comments_data4.csv', index=False)
