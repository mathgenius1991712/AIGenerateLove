from .models import CustomUser

class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.user.is_authenticated:
             user = CustomUser.objects.get(email = request.user.email)
             print("authenticated user")
             user.is_online = True
             user.save()
        # Do something before the view is called
        response = self.get_response(request)
        # Do something after the view is called
        print("middleware")
        return response
