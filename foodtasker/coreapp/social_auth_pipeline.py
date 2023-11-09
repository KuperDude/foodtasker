from .models import Customer, Driver, User 

def create_user_by_type(backend, user, response, *args, **kwargs):
    request = backend.strategy.request_data()

    if backend.name == 'vk-oauth2':
        avatar = response.get('photo', '')

        # print(user.id, avatar)

        # for x in User.objects.all():
        #     print(x.id)
        if request['user_type'] == 'driver':
            Driver.objects.get_or_create(user_id=user.id, avatar=avatar)
        elif request['user_type'] == 'customer':
            Customer.objects.get_or_create(user_id=user.id, avatar=avatar)
        


