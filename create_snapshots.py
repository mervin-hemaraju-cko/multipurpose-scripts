import boto3

def read_volume_ids():

    with open("input/volume_ids.txt", "r") as file:
        ids = (file.read()).splitlines()
        return ids

def get_volume_attributes(client, volume_ids):

    return client.describe_volumes(
        VolumeIds=volume_ids
    )['Volumes']

def main():

    # * Get volume_ids
    volume_ids = read_volume_ids()

    # * Create ec2 client
    client = boto3.client('ec2')

    # * Get volume attributes
    volume_attr = get_volume_attributes(
        client, volume_ids
    )

    # * Iterate through volume IDs
    for volume_id in volume_ids:

        # * Get the instance ID
        v_attr = [attr for attr in volume_attr if attr['VolumeId'] == volume_id][0]
        instance_id = v_attr['Attachments'][0]['InstanceId']

        # * Take snapshots
        response = client.create_snapshot(
            Description=f'snapshot_for_{instance_id}',
            VolumeId=volume_id,
            TagSpecifications=[
                {
                    'ResourceType': 'snapshot',
                    'Tags': [
                        {
                            'Key': 'Creator',
                            'Value': 'mervin.hemaraju'
                        },
                        {
                            'Key': 'Retention',
                            'Value': '5'
                        },
                        {
                            'Key': 'Instance ID',
                            'Value': instance_id
                        },
                    ]
                },
            ]
        )

        print(f"Snapshot response for {volume_id}: {response}")

main()