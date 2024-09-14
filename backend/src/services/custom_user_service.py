from src.models.custom_user import CustomUser, CustomUserSerializer


def create_custom_user(data: dict) -> dict:
    CustomUserSerializer(data=data).is_valid(raise_exception=True)
    user = CustomUser.objects.create(user=data)
    user.save()  # salva no BD
    return CustomUserSerializer(user).data
