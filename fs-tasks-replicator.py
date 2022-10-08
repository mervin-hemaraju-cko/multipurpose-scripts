import requests,json,os

def main():
    
    api_key = os.environ['FRESHSERVICE_API_KEY_B64']
    change_number = "16334"
    new_change_number = "17879"
    
    header = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {api_key}"
    }
    
    response = requests.get(
        f"https://{os.environ['FRESHSERVICE_DOMAIN']}/api/v2/changes/{change_number}/tasks",
        headers=header,
        verify=False
    )
    
    response_content = json.loads(response.content)
    
    for task in response_content['tasks']:
        
        new_task = {
            #"agent_id": float(task['agent_id']),
            "status": 1,
            "due_date": "2022-09-27T10:00:00Z",
            "notify_before": 0,
            "title": task['title'],
            "description": task['description']
        }
        
        print(new_task)
        
        new_response = requests.post(
            f"https://{os.environ['FRESHSERVICE_DOMAIN']}/api/v2/changes/{new_change_number}/tasks",
            headers=header,
            data=json.dumps(new_task),
            verify=False
        )
        
        print(json.loads(new_response.content))
    

if __name__ == "__main__":
    main()
    
    
    