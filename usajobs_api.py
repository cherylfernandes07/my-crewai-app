# contains your function to fetch job postings from the USAJobs API. 
# In one of the tasks in this project, 
# you’ll define a function that takes in search parameters 
# and returns a list of job results.

from job_hunt_assistant.utils.config import USAJOBS_API_KEY
import requests

BASE_URL = "https://data.usajobs.gov/api/search"

# Import the requests module and USAJOBS_API_KEY from the config file.


#Accept three parameters: keyword, location, 
# and results_per_page, with "remote" and 5 as default values for the latter two.
def fetch_usajobs(keyword, location="remote", results_per_page=5):
    message = f"Fetching for, {keyword}, {location}, and number: {results_per_page}"
    print(message)

    #Define a headers dictionary containing authentication keys and metadata required by the API.
    headers = {
        "Authorization-Key": USAJOBS_API_KEY,
        "Host": "data.usajobs.gov",
        "User-Agent": "cherylfernandes07@gmail.com",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }
    #Add a params dictionary that includes the job keyword, location, and number of results to fetch.
    # Define your search values
    params = {
        "Keyword": keyword,
        "LocationName": location,
        "ResultsPerPage": results_per_page
    }

    #Construct the API URL using the keyword and location values.
    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        #Parse the JSON response and return the list of job items if the call is successful.
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('SearchResult', {}).get('SearchResultItems', [])
            print("JSON successfully parsed")
            print(jobs)
            return jobs
        else:
            print(f"Server returned an error status: {response.status_code}")
    except requests.exceptions.JSONDecodeError:
        print("Error: The response exists, but it is not in JSON format")
    except requests.exceptions.RequestException as e:
        print(f"Network error occured: {e}")
    return []

if __name__ == "__main__":
    # Test the function by fetching jobs
    jobs = fetch_usajobs("business analyst", location="New York", results_per_page=10)
    
    for job in jobs:
        title = job.get('MatchedObjectDescriptor', {}).get('PositionTitle', 'N/A')
        agency = job.get('MatchedObjectDescriptor', {}).get('OrganizationName', 'N/A')
        print(f"{title} at {agency}")
