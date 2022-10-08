import boto3

def read_instances():

    with open("input/instance_ids.txt", "r") as file:
        instances = (file.read()).splitlines()
        return instances

def get_instance_ids(instances):

    client = boto3.client("ec2")

    response = client.describe_instances(
        Filters=[
            {'Name':'tag:Name', 'Values':instances}
        ]
    )

    instance_ids = []

    for r in response["Reservations"]:
        for i in r['Instances']:
            instance_ids.append(i['InstanceId'])
    
    return instance_ids

def run_command(instance_ids, document_name, comment, commands):

    print('Creating client')
    client = boto3.client("ssm")
    
    print("Running command")
    response = client.send_command(
        InstanceIds=instance_ids,
        DocumentName=document_name,
        DocumentVersion='$LATEST',
        TimeoutSeconds=300,
        Comment=comment,
        Parameters={
            'commands': commands
        },
        MaxConcurrency='10',
        MaxErrors='5'
    )

    return response['Command']['CommandId']

def main():

    instances = read_instances()

    print(f'Instances: {instances}')

    instance_ids = get_instance_ids(instances)

    print(f"Instance IDs: {instance_ids}")
    print(f"Instance IDs: {len(instance_ids)}")
    
    command_id = run_command(
        instance_ids = instance_ids,
        document_name="AWS-RunPowerShellScript",
        comment="GatewayScript",
        commands=[
            "Write-Host 'Command ran successfully"
        ]
    )

    print(command_id)