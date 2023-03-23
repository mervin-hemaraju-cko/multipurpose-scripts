import boto3, os, pandas as pd

def export_to_excel(file_name, schema):

    df = pd.DataFrame(schema)
    df.to_excel (file_name, index = False, header=True)

def read_patch_groups():

    with open("input/patch_groups.txt", "r") as file:
        return  (file.read()).splitlines()
    
# * Get patch groups list
patch_groups = read_patch_groups()

# * Define empty schema
instance_mappings = []
    
# * Create an EC2 client
client = boto3.client("ec2", region_name = os.environ['AWS_REGION'])

for patch_group in patch_groups:
    
    # * Make API Call 
    response = client.describe_instances(
        Filters=[
            {
                'Name': f'tag:PatchGroup', 
                'Values': [patch_group]
            }
        ]
    )

    # * Iterate through reservations and get instances
    instances = [i for r in response["Reservations"] for i in r['Instances']]
    
    instance_mappings.append(
        (patch_group, [instance['InstanceId'] for instance in instances])
    )

schema = {
    "Patch Groups": [entry[0] for entry in instance_mappings],
    "Instance Ids": [", ".join(entry[1]) for entry in instance_mappings],
}

print(schema)

export_to_excel(
    file_name="prod-legacy.xlsx",
    schema=schema
)