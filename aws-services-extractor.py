import boto3, os
import pandas as pd

def export_to_excel(file_name, schema):

    df = pd.DataFrame(schema)

    df.to_excel (f'out/{file_name}', index = False, header=True)

def main():
    
    # * Create the resource client
    client = boto3.client("lambda", region_name = os.environ["AWS_REGION"])

    # * Define empty list of resources and fields
    resources = []
    creators = []
    teams = []

    # * Make the API call to the service
    list_response = client.list_functions(
    )

    # * Get the resources
    resources += list_response['Functions']

    while("NextMarker" in list_response):

        # * Make the API call to the service
        list_response = client.list_functions(
            Marker=list_response['NextMarker'],
        )

        # * Get the resources
        resources += list_response['Functions']

        # * Print count of resources obtained
        print(f"Current count: {len(resources)}")

        for resource in resources:
            print(f"Processing {resource['FunctionName']}")

            # * Extra API call for more details
            get_response = client.get_function(FunctionName=resource['FunctionName'])

            if 'Tags' in get_response:
                print(f"Tags obtained for {resource['FunctionName']} : {get_response['Tags']}")

                if 'Creator' in get_response['Tags']:
                    creators.append(get_response['Tags']['Creator'])
                elif 'creator' in get_response["Tags"]:
                    creators.append(get_response['Tags']['creator'])
                else:
                    creators.append('Unknown')
            else:
                creators.append('Unknown')
            
            if 'Tags' in get_response:
                if 'Team' in get_response['Tags']:
                    teams.append(get_response['Tags']['Team'])
                elif 'team' in get_response["Tags"]:
                    teams.append(get_response['Tags']['team'])
                else:
                    teams.append('Unknown')
            else:
                teams.append('Unknown')


    schema = {
        "Name": [field['FunctionName'] for field in resources],
        "ARN": [field['FunctionArn'] for field in resources],
        "Runtime": [field['Runtime'] for field in resources],
        "Description": [field['Description'] for field in resources],
        "Creator": creators,
        "Team": teams,
    }

    # * Export the schema into excel
    export_to_excel(
        file_name="lambdas_prod_legacy.xlsx",
        schema=schema,
    )