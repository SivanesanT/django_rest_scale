from rest_framework.decorators import api_view
from rest_framework.response import Response

from home.models import person
from home.serializers import peopleSerializer,LoginSerializer,registerserializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from django.core.paginator import Paginator
from rest_framework.decorators import action


class LoginAPI(APIView):
    def post(self,request):
      data=request.data
      serializer=LoginSerializer(data=data)
      if not serializer.is_valid():
          return Response({
              'stauts':False,
              'message': serializer.errors
          }, status.HTTP_400_BAD_REQUEST)
      user=authenticate(username=serializer.data['username'],password=serializer.data['password'])
      print(serializer.data)
      print(user)
      if not user:
           return Response({
              'stauts':False,
              'message':'invalid credentials'
          }, status.HTTP_400_BAD_REQUEST)
          
    #   token, _ = Token.objects.get_or_create(user=user)
      token, created = Token.objects.get_or_create(user=user)
      print(token)
      return Response({'status':True,'message':'userlogined', 'token':str(token)},status.HTTP_200_OK)

class registerapi(APIView):

    def post(self,request):
      data=request.data
      serializer=registerserializer(data=data)
      if not serializer.is_valid():
          return Response({
              'stauts':False,
              'message': serializer.errors
          }, status.HTTP_400_BAD_REQUEST)
      serializer.save()
      return Response({'status':True,'message':'user created'},status.HTTP_200_OK)
   

class personAPI(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def get(self,request):
        print(request.user)
        objs=person.objects.filter(color__isnull = False)
        # http://127.0.0.1:8000/api/persons/?page=3 paginator like this use only come 2
        try:
            page = request.GET.get('page',1)
            page_size=2
            paginator = Paginator(objs,page_size)
            serializer= peopleSerializer(paginator.page(page),many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'status':False,
                'message':'invalid page'
            },status=status.HTTP_204_NO_CONTENT)

        # print(paginator.page(page))
        # more than one data we have to give many true
        # serializer=peopleSerializer(objs,many=True)
        # return Response(serializer.data)
        # return Response({"message":"This is from get request"})


    def post(self,request):
        data=request.data
        serializer=peopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    
    def put(self,request):
        data=request.data
        obj= person.objects.get(id=data['id'])
        serializer=peopleSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            # we want to give all data to update the data with id.
            return Response(serializer.data)
        return Response(serializer.errors)
    
    
    def patch(self,request):
        data=request.data
        obj= person.objects.get(id=data['id'])
        serializer=peopleSerializer(obj,data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # we want to give that chabge characteristic only with id.
            return Response(serializer.data)
        return Response(serializer.errors)
    
    
    def delete(self,request):
        data=request.data
        obj=person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message':'person deleted'})

# it is viewset it use to essay access of the data it has to specialityes as get and post the datas and lists are using this method as using search functionalityes
class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class= peopleSerializer
    queryset = person.objects.all()
    
    def list(self, request):
        search= request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset =queryset.filter(name__startswith = search)
            
            serializer =peopleSerializer(queryset,many=True)
            return Response({'status':200 , 'data': serializer.data}, status=status.HTTP_204_NO_CONTENT)





# ----------------------------first one hour
# person.object.all()
# [1,2,3,4]->queryset
# serializer is done the queryset to convert to give json format it help to all data or query set in to json- javascript object notation
# basically serializer means a class which help you to serialize the data in query set to json response and voiceversa  


@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)

    if serializer.is_valid():
        print('hii')
        data = serializer.validated_data
        return Response({'message' : 'success' })
    return Response(serializer.errors)

#example api
@api_view(['GET', 'POST', 'PUT'])
def index(request):
    courses={
            'couse_name': 'python',
            'learn'     : ['flask', 'django' , 'tornado' , 'Fastapi'],
            'course provider':'scaler'
        }
    if request.method=='GET':
        print(request.GET.get('search'))
        print("YOu hit a get method")
        return Response(courses) 
    elif request.method == 'POST':
        data=request.data
        print('.........')
        print(data)
        print(data['name'])
        print(data['age'])

        print("YOu hit a Post method")
        return Response(courses)
    elif request.method == 'PUT':
        print("YOu hit a PUt method")
        return Response(courses)



# api decorator this is 
@api_view(['GET', 'POST','PUT','PATCH','DELETE'])
def people(request): 
    if request.method == 'GET':
        objs=person.objects.filter(color__isnull = False)
        # more than one data we have to give many true
        serializer=peopleSerializer(objs,many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data=request.data
        serializer=peopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


# PUT we want to give all data to update the data with id.
# {
#     "id":1,
#     "name":"siva",
#     "age":40
# }
    elif request.method == 'PUT':
        data=request.data
        obj= person.objects.get(id=data['id'])
        serializer=peopleSerializer(obj,data=data)
        if serializer.is_valid():
            serializer.save()
            # we want to give all data to update the data with id.
            return Response(serializer.data)
        return Response(serializer.errors)


# PATCH we want to give that chabge characteristic only with id.
# {
#     "id":1,
#     "age":40
# }    
    elif request.method == 'PATCH':
        data=request.data
        obj= person.objects.get(id=data['id'])
        serializer=peopleSerializer(obj,data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # we want to give that chabge characteristic only with id.
            return Response(serializer.data)
        return Response(serializer.errors)
    
    else:
        data=request.data
        obj=person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message':'person deleted'})
    

#last topic in scalr in viewset action 
@action(detail=True,method=['POST'])
def send_mail_to_person(self,pk,request):
    print(pk)
    obj=person.object.get(pk=pk)
    serializer=peopleSerializer(obj)
    return Response({
        'status':True,
        'message':'email sent successfully',
        'data':serializer.data
    })