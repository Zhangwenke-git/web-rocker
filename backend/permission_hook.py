def my_own_data(request):
    print('---------------')
    if str(request.user.id) == request.GET.get('consultant'):
        print(request.user.id)
        return True
    else:
        return False