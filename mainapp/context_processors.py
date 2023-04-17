def global_context_processor(request):
    return {
                'MEDIA_URL': 'media',
            }

def auth_context_processor(request):
    return { "logged_in": request.user.is_authenticated }