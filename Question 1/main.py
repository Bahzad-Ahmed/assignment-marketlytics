import requests 
import pandas as pd
import time

 
def get_rate_limit(headers):
    try:
        response = requests.get('https://api.github.com/rate_limit', headers=headers)
        remaining_rate_limit = int(response.headers.get('X-RateLimit-Remaining'))
        return response, remaining_rate_limit
    except Exception as e:
        print(f"Error getting rate limit: {str(e)}")
        return None, 0
    
    
def fetch_github_data(token, since_repo_id, count):
    num_repos = count
    repositories = [] 
    base_url = 'https://api.github.com/repositories'
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    while count > 0:
        params = {'since': since_repo_id, 'per_page': min(count, 100), 'languages': 'true'}

        try: 
            
            response, remaining_rate_limit = get_rate_limit(headers)
            print("Remaining rate limit is: {}".format(remaining_rate_limit))
            if remaining_rate_limit <= 2:
                reset_time = int(response.headers.get('X-RateLimit-Reset'))
                sleep_time = max(reset_time - time.time(), 0) + 10  # Wait for extra time
                print(f"Rate limit reached. Waiting for {sleep_time} seconds.")
                time.sleep(sleep_time)
                continue
            
            # Fetch a page of public repositories using the REST API 
            response = requests.get(base_url, headers=headers, params=params) 
            data = response.json() 
            
            for repo in data:
                
                repositories.append(repo)
                count -= 1
                since_repo_id = repo['id']
    
            # Print progress 
            print(f"Fetched {num_repos - count} of {num_repos}") 
                
            
        except Exception as e: 
            print(f"Error fetching page: {str(e)}") 
            
        
    return repositories


token = 'ADD-TOKEN-HERE'
since_repo_id = 0
repositories_count = 1000000

df = pd.DataFrame(fetch_github_data(token, since_repo_id, repositories_count)) 
df.to_csv("Question 1/public_repositories.csv", index=False) 
print("Data fetched and saved successfully.")