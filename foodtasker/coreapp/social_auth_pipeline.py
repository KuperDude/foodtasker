from .models import Customer, Driver, User 

def create_user_by_type(backend, user, response, *args, **kwargs):
    request = backend.strategy.request_data()

    if backend.name == 'vk-oauth2' or backend.name == 'google-oauth2':
        avatar = response.get('photo', '')
        
        if request['user_type'] == 'driver':
            Driver.objects.get_or_create(user_id=user.id, avatar=avatar)
        elif request['user_type'] == 'customer':
            Customer.objects.get_or_create(user_id=user.id, avatar=avatar)
        


