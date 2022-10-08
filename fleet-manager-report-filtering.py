import json

def main():
    
    with open('report-fleetmanager-cko-prod-legacy.json', 'r') as file:
        
        json_file = json.loads(file.read())
        
        for instance in json_file['data']:
            
            if instance['AgentVersion'] < "3.1.1045.0":
                print(f"Instance ID: {instance['InstanceId']}")
                print(f"Instance Name: {instance['Name']}")
                print(f"Agent Version: {instance['AgentVersion']}")
                print('==========================')
    
if __name__ == "__main__":
    main()
    