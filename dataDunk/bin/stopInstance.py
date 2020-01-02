import boto3

region = 'us-east-2'
instances = ['i-00e8ce7cef27934af']
ec2 = boto3.client('ec2', region_name=region)
ec2.sop_instances(InstanceIds=instances)
print('Started DataDunk EC2 instance: ' + str(instances))