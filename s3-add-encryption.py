import boto3

def main():
    
    # Boto3 Client
    client = boto3.client('s3')

    # Define results files
    results = open("input/results.txt", "w")
    errors = open("output/errors.txt", "w")

    # Read text file
    with open("files/buckets.txt", "r") as output:

        for line in output.readlines():

            bucket_name = line.strip()

            print(f"Processing bucket {bucket_name}")

            try:
                response = client.put_bucket_encryption(
                        Bucket=bucket_name,
                        ServerSideEncryptionConfiguration={
                            'Rules': [
                                {
                                    'ApplyServerSideEncryptionByDefault': {
                                        'SSEAlgorithm': 'AES256'
                                    }
                                },
                            ]
                        }
                    )
                
                results.write(f"Results for {bucket_name}:\n\n")
                results.write(f"{str(response)}\n\n")
                results.write("====================================\n\n\n")
            except:
                errors.write(f"Error for {bucket_name}:\n\n")



if __name__ == "__main__":
    main()