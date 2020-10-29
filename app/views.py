from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Book
from app.serializers import BookModelSerializer


class BookAPIView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        if id:
            try:
                book=Book.objects.get(id=id,is_delete=False)
                data=BookModelSerializer(book).data
                return Response({
                    "status":200,
                    "messages":"查询单个",
                    'result':data
                })
            except Book.DoesNotExist:
                return Response({
                    "status":200,
                    "messages":"该书不存在"
                })
        else:
            book_all=Book.objects.all()
            book_all_ser=BookModelSerializer(book_all,many=True).data
            return Response({
                "status":200,
                "messages":"查询全部",
                'result':book_all_ser
            })


    def post(self,request,*args,**kwargs):
        data=request.data
        print("datadata",data)
        if isinstance(data,dict):
            many=False
        elif isinstance(data,list):
            many=True
        else:
            return Response({
                "status":400,
                "messages":"参数错误",
            })
        serializer=BookModelSerializer(data=data,many=many)
        serializer.is_valid(raise_exception=True)
        book_obj=serializer.save()
        return Response({
            "status":200,
            "messages":"添加成功",
            'result':BookModelSerializer(book_obj,many=many).data
        })
    def delete(self,request,*args,**kwargs):
        id=kwargs.get('id')
        if id:
            ids=[id]
        else:
            ids=request.data.get('ids')
        print(ids)
        Book_obj=Book.objects.filter(pk__in=ids)
        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        print(response)
        if response:
            return Response({
                "status":200,
                "messages":"删除成功",

            })
        return Response({
            "status":400,
            "messages":"删除失败",
        })
    def put(self,request,*args,**kwargs):
        data=request.data
        id=kwargs.get("id")
        try:
            book=Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response({
                "status":400,
                "messages":"图书不存在"
            })
        serializer=BookModelSerializer(data=data,instance=book)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "status":200,
            "messages":"修改单个成功",
            'result':BookModelSerializer(book).data
        })