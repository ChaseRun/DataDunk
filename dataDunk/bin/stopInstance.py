import boto3

region = 'us-east-2'
instances = ['i-09ca26937edc091c7']
ec2 = boto3.client('ec2', 
                   region_name=region,
                   aws_access_key_id='AKIAWJCHVF5ZXWVEQBGI',
                   aws_secret_access_key='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')

ec2.stop_instances(InstanceIds=instances)
print('Stopped DataDunk EC2 instance: ' + str(instances))