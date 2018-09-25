def save_profile(backend, user, response, *args, **kwargs):
    user.is_reader = True
    user.save()