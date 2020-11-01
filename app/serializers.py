from rest_framework import serializers

from app.models import Press, Book, User


class PressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Press
        fields = ("press_name", "pic", "address")
class Bookmodelserializer(serializers.ModelSerializer):
    press=PressModelSerializer()
    class Meta:
        model=Book
        fields=("book_name","price","pic","publish")

class BookListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        print("instance",instance)
        print("validated_data",validated_data)
        print(self.child)
        for index,obj in enumerate(instance):
            self.child.update(obj,validated_data[index])
        return instance

class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=("book_name","price","author",'publish',"pic")
        list_serializer_class=BookListSerializer
        extra_kwargs={
            "book_name":{
                "required":True,
                "min_length":2,
                "error_messages":{
                    "required":"必须有图书名称",
                    "min_length":"名称长度必须大于两位",
                }
            },
            "pic": {
                "read_only": True
            },
            # 指定某个字段只参与反序列化
            "publish": {
                "write_only": True
            },
            "authors": {
                "write_only": True
            },
        }
    def validate(self, attrs):
        print("全局",attrs)
        return  attrs
    def validate_price(self,price):
        print("局部",price)
        return price


class BookLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("username","password","status")