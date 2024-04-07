import boto3

s3_client = boto3.client('s3')
# s3_client.upload_file('/Users/caherita/Desktop/SWE/Estilo_calico/videos/HombreLobo.mp4', 'estilocalico-bucket', 'new_video.mp4')
# bucket = s3_client.list_objects_v2(Bucket='estilocalico-bucket')
# for obj in bucket['Contents']:
#     print(obj['Key'])

video = s3_client.get_object(Bucket='estilocalico-bucket', Key='sample_video.mp4')
print(video)