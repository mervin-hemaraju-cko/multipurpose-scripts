import boto3

def read_instances():

    with open("input/instance_ids.txt", "r") as file:
        instances = (file.read()).splitlines()
        return instances


instance_ids = read_instances()

print(f"Length: {len(instance_ids)}")

response = boto3.client('ec2').create_tags(
    Resources=instance_ids,
    Tags=[
        {
            'Key': 'EC2-Backup',
            'Value': 'Yes'
        },
    ]
)

print(f"Response: {response}")
