from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework import generics,permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.exceptions  import ValidationError
from django.contrib.auth import login
from kitaplar.models import Kitap,Yorum
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from kitaplar.api.serializers import YorumSerializers,KitapSerializers,UserSerializer, RegisterSerializer
from kitaplar.api.permissions import IsAdminUserOrReadOnly,IsYorumSahibiReadOnly




class KitapListCreateApıWiews(generics.ListCreateAPIView):  
    queryset = Kitap.objects.all()
    serializer_class = KitapSerializers
        

    
class KitapDetailWiew(generics.RetrieveUpdateDestroyAPIView):      
    queryset = Kitap.objects.all()
    serializer_class = KitapSerializers
    #permission_classes = [IsAdminUserOrReadOnly]

    

class YorumCreateAPIView(generics.CreateAPIView):
    queryset = Yorum.objects.all()
    serializer_class = YorumSerializers 
    #permission_classes = [IsAdminUserOrReadOnly]
    
    def perform_create(self,serializer):
        
        kitap_pk = self.kwargs.get('kitap_pk')
        kitap = get_object_or_404(Kitap, pk=kitap_pk)
        kullanıcı = self.request.user
        yorumlar = Yorum.objects.filter(kitap = kitap, yorum_sahibi =kullanıcı)
        if yorumlar.exists():
            raise ValidationError('Bir kitaba sadece bir yorum yapabilirsiniz')
        
        serializer.save(kitap=kitap, yorum_sahibi = kullanıcı)
        
         

class YorumDetailWiew(generics.RetrieveUpdateDestroyAPIView):   
    queryset = Yorum.objects.all()
    serializer_class = YorumSerializers    
    permission_classes = [IsYorumSahibiReadOnly]
    
    
    
# Register API


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })    
        
        
class LoginAPI(KnoxLoginView):
        permission_classes = (permissions.AllowAny,)

        def post(self, request, format=None):
         serializer = AuthTokenSerializer(data=request.data)
         serializer.is_valid(raise_exception=True)
         user = serializer.validated_data['user']
         login(request, user)
         return super(LoginAPI, self).post(request, format=None)
        