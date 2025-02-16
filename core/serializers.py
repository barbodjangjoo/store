from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer

class UserCreationSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']