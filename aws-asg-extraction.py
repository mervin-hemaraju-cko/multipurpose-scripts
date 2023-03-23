import boto3, os
import pandas as pd

CONST_NOT_APPLICABLE = "N/A"

def export_to_excel(file_name, schema):

    df = pd.DataFrame(schema)
    df.to_excel (file_name, index = False, header=True)

def get_auto_scaling_groups(client):
    response = client.describe_auto_scaling_groups()
    return response['AutoScalingGroups']

def get_ami_details(client, image_id):
    response = client.describe_images(
        ImageIds = [image_id]
    )
    return response["Images"]

# * Define boto3 clients
client_autoscaling = boto3.client('autoscaling', region_name = os.environ['AWS_REGION'])
client_ec2 = boto3.client('ec2', region_name = os.environ['AWS_REGION'])

# * Get all autoscaling groups in use
asgs = get_auto_scaling_groups(client=client_autoscaling)

# * Get launch configuration names
launch_config_names = [
    asg_config["LaunchConfigurationName"] if "LaunchConfigurationName" in asg_config else CONST_NOT_APPLICABLE
    for asg_config in asgs
]

# * Get launch template names
launch_template_names = []

for asg_config in asgs:

    if "LaunchTemplate" in asg_config:
        launch_template_names.append(
            {
                "LaunchTemplateName": asg_config['LaunchTemplate']['LaunchTemplateName'],
                "Version": asg_config['LaunchTemplate']['Version']
            }
        )
    elif "MixedInstancesPolicy" in asg_config:
        launch_template_names.append(
            {
                "LaunchTemplateName": asg_config['MixedInstancesPolicy']['LaunchTemplate']["LaunchTemplateSpecification"]['LaunchTemplateName'],
                "Version": asg_config['MixedInstancesPolicy']['LaunchTemplate']["LaunchTemplateSpecification"]['Version']
            }
        )
    else:
        launch_template_names.append(CONST_NOT_APPLICABLE)


# * Define an empty list of amis
ami_ids = []

# * Iterate through launch templates and configurations
for lc, lt in zip(launch_config_names, launch_template_names):
    print(f"{lc}: {lt}")
    # * If launch configuration is valid
    if lc != CONST_NOT_APPLICABLE:

        # * Describe the launch confgiuration to get the image id
        launch_config_response = client_autoscaling.describe_launch_configurations(
            LaunchConfigurationNames=[lc]
        )

        # * Append AMIs
        ami_ids += [ami['ImageId'] for ami in launch_config_response['LaunchConfigurations'] if 'ImageId' in ami]

    # * If launch template is valid
    if lt != CONST_NOT_APPLICABLE:

        # * Describe the launch template version to get the image id
        response = client_ec2.describe_launch_template_versions(
            LaunchTemplateName=lt["LaunchTemplateName"],
            Versions=[
                lt["Version"]
            ]
        )

        ami_ids += [
            ami['LaunchTemplateData']['ImageId']
            for ami in response['LaunchTemplateVersions']
        ]

# * Define an empty list of ami descriptions
amis = []

# * Determine ami description
for ami in ami_ids:

    try:
        amis += get_ami_details(client=client_ec2, image_id=ami)
    except:
        amis.append(CONST_NOT_APPLICABLE)
    
# * Define data
autoscaling_names = [asg['AutoScalingGroupName'] for asg in asgs]
autoscaling_instances = [",".join([instance['InstanceId'] for instance in asg['Instances']]) if(len(asg['Instances']) > 0) else "None" for asg in asgs]
autoscaling_usage = ["In Use" if(len(asg['Instances']) > 0) else "Not in Use" for asg in asgs]
autoscaling_instance_count = [str(len(asg['Instances'])) for asg in asgs]

# * Define Schema
schema = {
    "Autoscaling Groups": autoscaling_names,
    "Launch Template Name": [lt["LaunchTemplateName"] if lt != CONST_NOT_APPLICABLE else CONST_NOT_APPLICABLE for lt in launch_template_names],
    "Launch Configuration Name": launch_config_names,
    "Autoscaling Instances": autoscaling_instance_count,
    "Usage": autoscaling_usage,
    "Instance Ids": autoscaling_instances,
    "AMI": ami_ids,
    "AMI Description": [ami['Description'] if 'Description' in ami else CONST_NOT_APPLICABLE for ami in amis],
    "ECS Optimized": ["No" if ami == CONST_NOT_APPLICABLE or 'ecs' not in ami["Name"].lower() else "Yes" for ami in amis],
}

for k,v in schema.items():
    print(f"{k}: {len(v)}")

# * Export to excel
export_to_excel(
    file_name="mgmt.xlsx",
    schema=schema
)

