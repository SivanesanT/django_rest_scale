from rest_framework import serializers
from .models import person, color
from django.contrib.auth.models import User


class registerserializer(serializers.Serializer):
     username=serializers.CharField()
     email=serializers.EmailField()
     password = serializers.CharField()
     # user already is exits are not
     def validate(self,data):
          if data['username']:
               if User.objects.filter(username=data['username']).exists():
                    raise serializers.ValidationError('Username is taken already')
          if data['email']:
               if User.objects.filter(username=data['email']).exists():
                    raise serializers.ValidationError('email is taken already')
          return data
     
     def create(self,validated_data):
           
           user=User.objects.create(username=validated_data['username'],email=validated_data['email'])
          #  , password=validated_data.set_password(['password']))
           user.set_password(validated_data['password'])
           user.save()
           return validated_data
           print(validated_data)


class LoginSerializer(serializers.Serializer):
     username=serializers.CharField()
     # email = serializers.EmailField()
     password = serializers.CharField()

# it not connet to model so only not use the modelserializer

class colorSerializer(serializers.ModelSerializer):
     class Meta:
          model=color
          fields=['color_name']


class peopleSerializer(serializers.ModelSerializer):
     color = colorSerializer()
     country=serializers.SerializerMethodField()
    #  in this country name used to below declare get_country
     color_info=serializers.SerializerMethodField()

     class Meta:
          model=person
        #   all field means '__all__'
        # exclude=['name'] name a mattu vi2 tu mithi allam aduthukkum etha exclude 
        #   field=['name','age']
          fields='__all__'
          # depth=1 depth potta foreing key varum non declare above means in here after above defined
        # serializers with validation

     def get_country(self,obj):
          return "INDIA"
      
     def get_color_info(self,obj):
          color_obj= color.objects.get(id=obj.color.id)
          return {'color_name':color_obj.color_name, 'hex_code':'#000'}

     def validate(self,data):
        
        special_characters= "!@#$%^&*()_+?-=<>/"
        if any(c in special_characters for c in data['name']):
             raise serializers.ValidationError('Name does not contain special chars')
  
        if data['age'] < 18 :
             raise serializers.ValidationError('Age should be greater than 18')
        return data