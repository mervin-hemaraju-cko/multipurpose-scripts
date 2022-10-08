import boto3

def main():

    client = boto3.client('iam')

    response = client.list_policies(
        MaxItems=500,
    )

    policies_obtained = response['Policies']

    policies_deletable = [policy for policy in policies_obtained if policy['AttachmentCount'] == 0]

    print(f"Policies Obtained: {len(policies_obtained)}")
    print(f"Policies Deletable: {len(policies_deletable)}")

    for policy in policies_deletable:
        
        print(policy['PolicyName'])
        
        response = client.list_policy_versions(
            PolicyArn=policy['Arn']
        )
        
        version_ids = [version['VersionId'] for version in response['Versions'] if version['IsDefaultVersion'] == False]
        
        for version_id in version_ids:
            response = client.delete_policy_version(
                PolicyArn=policy['Arn'],
                VersionId=version_id
            )

        ####################
        ###### ENABLE ######
        ####################
        # client.delete_policy(
        #     PolicyArn=policy['Arn']
        # )

# * Call the main function
main()