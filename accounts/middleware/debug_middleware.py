# accounts/middleware/debug_middleware.py
class DebugAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("🧩 user:", request.user)
        print("🛡️ is_authenticated:", request.user.is_authenticated)
        return self.get_response(request)
