"""
Proxy views - routes requests to appropriate microservices
"""
import requests
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView


class ProxyViewSet(viewsets.ViewSet):
    """
    API Gateway viewset that proxies requests to microservices
    """
    permission_classes = [AllowAny]
    
    def _proxy_request(self, service_url, path, method='GET', data=None, headers=None):
        """Helper method to proxy requests to microservices"""
        url = f"{service_url}{path}"
        request_headers = {'Content-Type': 'application/json'}
        
        if headers:
            request_headers.update(headers)
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=request_headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=request_headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=request_headers, timeout=10)
            elif method == 'PATCH':
                response = requests.patch(url, json=data, headers=request_headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=request_headers, timeout=10)
            else:
                return Response(
                    {'error': 'Method not allowed'},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED
                )
            
            return Response(
                response.json() if response.content else {},
                status=response.status_code
            )
        except requests.RequestException as e:
            return Response(
                {'error': f'Service unavailable: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class BaseAuthProxyView(APIView):
    """Base proxy view for authentication requests"""
    permission_classes = [AllowAny]
    
    def _proxy(self, path, method='POST', data=None):
        headers = {}
        if hasattr(self.request, 'META') and 'HTTP_AUTHORIZATION' in self.request.META:
            headers['Authorization'] = self.request.META['HTTP_AUTHORIZATION']
        
        url = f"{settings.TOKENS_SERVICE_URL}/api/auth/{path}"
        try:
            if method == 'POST':
                response = requests.post(url, json=data or {}, headers=headers, timeout=10)
            elif method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            
            return Response(
                response.json() if response.content else {},
                status=response.status_code
            )
        except requests.RequestException as e:
            return Response(
                {'error': f'Authentication service unavailable: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class RegisterProxyView(BaseAuthProxyView):
    """Proxy for registration"""
    def post(self, request):
        return self._proxy('register/', data=request.data)


class LoginProxyView(BaseAuthProxyView):
    """Proxy for login"""
    def post(self, request):
        return self._proxy('login/', data=request.data)


class RefreshProxyView(BaseAuthProxyView):
    """Proxy for token refresh"""
    def post(self, request):
        return self._proxy('refresh/', data=request.data)


class LogoutProxyView(BaseAuthProxyView):
    """Proxy for logout"""
    def post(self, request):
        return self._proxy('logout/', data=request.data)


class BaseCoursesProxyView(APIView):
    """Base proxy view for courses requests"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def _proxy(self, path, method='GET', data=None):
        headers = {'Authorization': self.request.META.get('HTTP_AUTHORIZATION', '')}
        url = f"{settings.COURSES_SERVICE_URL}/api/courses/{path}"
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data or {}, headers=headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data or {}, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            
            return Response(
                response.json() if response.content else {},
                status=response.status_code
            )
        except requests.RequestException as e:
            return Response(
                {'error': f'Courses service unavailable: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class CoursesListProxyView(BaseCoursesProxyView):
    """Proxy for courses list and create"""
    def get(self, request):
        return self._proxy('')
    
    def post(self, request):
        return self._proxy('', method='POST', data=request.data)


class CoursesDetailProxyView(BaseCoursesProxyView):
    """Proxy for course detail, update and delete"""
    def get(self, request, pk):
        return self._proxy(f'{pk}/')
    
    def put(self, request, pk):
        return self._proxy(f'{pk}/', method='PUT', data=request.data)
    
    def delete(self, request, pk):
        return self._proxy(f'{pk}/', method='DELETE')


class CoursesLessonsProxyView(BaseCoursesProxyView):
    """Proxy for course lessons"""
    def get(self, request, pk):
        return self._proxy(f'{pk}/lessons/')


class CoursesEnrollProxyView(BaseCoursesProxyView):
    """Proxy for course enrollment"""
    def post(self, request, pk):
        return self._proxy(f'{pk}/enroll/', method='POST', data=request.data)


class CoursesProgressProxyView(BaseCoursesProxyView):
    """Proxy for course progress"""
    def get(self, request, pk):
        return self._proxy(f'{pk}/progress/')


class BaseStreamingProxyView(APIView):
    """Base proxy view for streaming requests"""
    permission_classes = [IsAuthenticated]


class StreamingVideoProxyView(BaseStreamingProxyView):
    """Proxy for video streaming"""
    def get(self, request, video_id):
        headers = {'Authorization': self.request.META.get('HTTP_AUTHORIZATION', '')}
        url = f"{settings.STREAMING_SERVICE_URL}/api/streaming/video/{video_id}/"
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            return Response(
                response.content,
                status=response.status_code,
                content_type=response.headers.get('Content-Type', 'video/mp4')
            )
        except requests.RequestException as e:
            return Response(
                {'error': f'Streaming service unavailable: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class StreamingVideoInfoProxyView(BaseStreamingProxyView):
    """Proxy for video info"""
    def get(self, request, video_id):
        headers = {'Authorization': self.request.META.get('HTTP_AUTHORIZATION', '')}
        url = f"{settings.STREAMING_SERVICE_URL}/api/streaming/video/{video_id}/info/"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            return Response(
                response.json() if response.content else {},
                status=response.status_code
            )
        except requests.RequestException as e:
            return Response(
                {'error': f'Streaming service unavailable: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class BaseChatBotProxyView(APIView):
    """Base proxy view for chatbot requests"""
    permission_classes = [IsAuthenticated]


class ChatBotMessageProxyView(BaseChatBotProxyView):
    """Proxy for chatbot messages"""
    def post(self, request):
        headers = {'Authorization': self.request.META.get('HTTP_AUTHORIZATION', '')}
        url = f"{settings.CHATBOT_SERVICE_URL}/api/chatbot/message/"
        try:
            # Get data from request - ensure it's a dict
            if hasattr(request, 'data'):
                data = dict(request.data)
            else:
                import json
                try:
                    data = json.loads(request.body.decode('utf-8'))
                except:
                    data = {}
            
            # Ensure proper JSON encoding
            import json
            json_data = json.dumps(data, ensure_ascii=False)
            
            headers['Content-Type'] = 'application/json; charset=utf-8'
            response = requests.post(
                url, 
                data=json_data.encode('utf-8'),
                headers=headers, 
                timeout=30
            )
            
            if response.content:
                try:
                    response.encoding = 'utf-8'
                    return Response(
                        response.json(),
                        status=response.status_code
                    )
                except (ValueError, UnicodeDecodeError) as e:
                    return Response(
                        {'error': f'Invalid response from chatbot service: {str(e)}'},
                        status=status.HTTP_502_BAD_GATEWAY
                    )
            return Response({}, status=response.status_code)
        except requests.RequestException as e:
            return Response(
                {'error': f'Chatbot service unavailable: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class ChatBotContextProxyView(BaseChatBotProxyView):
    """Proxy for chatbot context"""
    def get(self, request, lesson_id):
        headers = {'Authorization': self.request.META.get('HTTP_AUTHORIZATION', '')}
        url = f"{settings.CHATBOT_SERVICE_URL}/api/chatbot/context/{lesson_id}/"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            return Response(
                response.json() if response.content else {},
                status=response.status_code
            )
        except requests.RequestException as e:
            return Response(
                {'error': f'Chatbot service unavailable: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

