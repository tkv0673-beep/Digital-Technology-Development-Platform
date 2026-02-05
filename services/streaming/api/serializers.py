"""
Serializers for streaming service
"""
from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    """Serializer for video"""
    video_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Video
        fields = ('id', 'title', 'description', 'video_url', 'thumbnail_url', 'duration', 'lesson_id', 'created_at')
        read_only_fields = ('id', 'created_at')
    
    def get_video_url(self, obj):
        """Get video URL"""
        if obj.video_file:
            return obj.video_file.url
        return None
    
    def get_thumbnail_url(self, obj):
        """Get thumbnail URL"""
        if obj.thumbnail:
            return obj.thumbnail.url
        return None

