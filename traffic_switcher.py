import boto3



def main():

    r53_client = boto3.client('route53')

    response = r53_client.list_hosted_zones_by_name(
        DNSName=HOSTED_ZONE
    )

    required_zones = [zone for zone in response['HostedZones'] if zone['Name'] == f"{HOSTED_ZONE}."]

    if len(required_zones) == 0:
        raise Exception("Could not retrieve this hosted zone")
    
    
    response = r53_client.list_resource_record_sets(
        HostedZoneId=required_zones[0]['Id'],
        StartRecordName=TOP_DOMAIN+HOSTED_ZONE
    )


    print(response['ResourceRecordSets'][0])

if __name__ == "__main__":
    main()