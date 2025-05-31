from django.shortcuts import render, redirect
import boto3
from botocore.client import Config
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.conf import settings

def home(request):
    return render(request, "home.html")

def media_proxy(request):
    key = request.GET.get('key')
    if not key:
        return HttpResponseBadRequest("Missing key")

    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        config=Config(signature_version='s3v4'),
        region_name=settings.AWS_S3_REGION_NAME,
    )

    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': key},
        ExpiresIn=settings.MEDIA_PROXY_EXPIRES_IN,  # valid 1 jam
    )

    return HttpResponseRedirect(url)