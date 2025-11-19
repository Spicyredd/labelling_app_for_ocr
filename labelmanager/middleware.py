from django.http import HttpResponse

class IgnoreStreamlitRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the path starts with Streamlit's internal URL
        if request.path.startswith('/_stcore/'):
            # Return a "No Content" response, which is successful but has no body
            return HttpResponse(status=204)
        
        # If it's any other URL, let Django handle it normally
        response = self.get_response(request)
        return response


class LogRequestIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the client's IP address
        ip_address = request.META.get('REMOTE_ADDR')
        
        # Print the IP and the path it's requesting
        print(f"[Request Info] Path: {request.path}, Client IP: {ip_address}")
        
        response = self.get_response(request)
        return response