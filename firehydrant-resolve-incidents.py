import json, requests, os

# Define a headers block
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ['FH_API_TOKEN']}"
}

# Define a starting page number
starting_page_number = 1

# Define the list incidents url
list_incidents_url = "https://api.firehydrant.io/v1/incidents?current_milestones=resolved&severities=SEV3,SEV4,RETROSPECTIVE&start_date=01/01/2021&end_date=18/04/2022&page={}"

# Get all incidents
incidents_response = requests.get(
    url=list_incidents_url.format(starting_page_number),
    headers=headers
)

# Load the response
incidents_response = json.loads(incidents_response.content)

total_pages = incidents_response['pagination']['pages']
incidents = incidents_response['data']

# Iterate over each pages and bulk update incidents
for page in range(1, total_pages):
    
    # Get all incidents
    incidents_response = requests.get(
        url=list_incidents_url.format(page),
        headers=headers
    )
    
    # Load the response
    incidents_response = json.loads(incidents_response.content)
    
    # Iterate over each incidents
    for incident in incidents_response['data']:
        
        # Get the incident id
        incident_id = incident['id']
        incident_name = incident['name']
        
        print(f"Processing incident {incident_name} with id {incident_id}")
        
        # Start post-mortem
        post_mortem_response = requests.post(
            url=f"https://api.firehydrant.io/v1/post_mortems/reports",
            headers=headers,
            data=json.dumps(
                {
                    "incident_id": incident_id,
                    "name": incident_name
                }
            )
        )
        
        print(f"Post Mortem Started status: {post_mortem_response.status_code}")
        
        # Build the body for update
        update_body = {
            "milestone": "postmortem_completed",
            "impact": [
                {
                    "type": impact['type'],
                    "id": impact['impact']['id'],
                    "condition_id": "6ba555f3-103c-4f42-b208-c7793df304da"
                }
                for impact in incident['impacts']
            ],
            "status_pages": [
                {
                    "id": "a87d9596-2b5a-4f05-b8b0-8152a1ac8810",
                    "integration_slug": "nunc"
                }
            ]
        }
        
        # Send request to update incident
        incident_update_response = requests.put(
            url=f"https://api.firehydrant.io/v1/incidents/{incident_id}/impact",
            headers=headers,
            data=json.dumps(update_body)
        )
        
        print(f"Update status: {incident_update_response.status_code}")
        print(f"Update content: {incident_update_response.content}")
        
        print(f"==========================================================")


