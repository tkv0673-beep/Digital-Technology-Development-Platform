"""
Views for streaming service
"""
import os
from django.http import StreamingHttpResponse, HttpResponse
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Video
from .serializers import VideoSerializer
import boto3
from botocore.config import Config


class VideoViewSet(viewsets.ModelViewSet):
    """
    Video streaming endpoints
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def stream(self, request, pk=None):
        """Stream video file"""
        try:
            video = self.get_object()
            
            # Get video file from S3
            s3_client = boto3.client(
                's3',
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                config=Config(signature_version='s3v4')
            )
            
            # Generate presigned URL for streaming
            video_key = video.video_file.name
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': video_key},
                ExpiresIn=3600
            )
            
            # Redirect to presigned URL
            return Response({'stream_url': presigned_url})
            
        except Exception as e:
            return Response(
                {'error': f'Error streaming video: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def info(self, request, pk=None):
        """Get video info"""
        video = self.get_object()
        serializer = self.get_serializer(video)
        return Response(serializer.data)

