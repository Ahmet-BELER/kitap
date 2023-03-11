from rest_framework import serializers 
from kitaplar.models import Kitap,Yorum
from django.contrib.auth.models import User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

 
class YorumSerializers(serializers.ModelSerializer):
    yorum_sahibi = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Yorum
        #fields = '__all__'
        
        exclude = ['kitap']
        
class KitapSerializers(serializers.ModelSerializer):

        yorumlar = YorumSerializers(many=True, read_only=True)
        class Meta:
            model = Kitap
            fields = '__all__'
            
            