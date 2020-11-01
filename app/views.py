from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, status, viewsets

from app.models import Book, User
from app.serializers import BookModelSerializer, BookLoginSerializer


class BookAPIView( APIView ):
    def get(self, request, *args, **kwargs):
        id = kwargs.get( "id" )
        if id:
            try:
                book = Book.objects.get( id=id, is_delete=False )
                data = BookModelSerializer( book ).data
                return Response( {
                    "status": 200,
                    "messages": "查询单个",
                    'result': data
                } )
            except Book.DoesNotExist:
                return Response( {
                    "status": 200,
                    "messages": "该书不存在"
                } )
        else:
            book_all = Book.objects.all()
            book_all_ser = BookModelSerializer( book_all, many=True ).data
            return Response( {
                "status": 200,
                "messages": "查询全部",
                'result': book_all_ser
            } )

    def post(self, request, *args, **kwargs):
        data = request.data
        print( "datadata", data )
        if isinstance( data, dict ):
            many = False
        elif isinstance( data, list ):
            many = True
        else:
            return Response( {
                "status": 400,
                "messages": "参数错误",
            } )
        serializer = BookModelSerializer( data=data, many=many )
        serializer.is_valid( raise_exception=True )
        book_obj = serializer.save()
        return Response( {
            "status": 200,
            "messages": "添加成功",
            'result': BookModelSerializer( book_obj, many=many ).data
        } )

    def delete(self, request, *args, **kwargs):
        id = kwargs.get( 'id' )
        if id:
            ids = [id]
        else:
            ids = request.data.get( 'ids' )
        print( ids )
        Book_obj = Book.objects.filter( pk__in=ids )
        response = Book.objects.filter( pk__in=ids, is_delete=False ).update( is_delete=True )
        print( response )
        if response:
            return Response( {
                "status": 200,
                "messages": "删除成功",

            } )
        return Response( {
            "status": 400,
            "messages": "删除失败",
        } )

    def put(self, request, *args, **kwargs):
        data = request.data
        id = kwargs.get( "id" )
        try:
            book = Book.objects.get( id=id )
        except Book.DoesNotExist:
            return Response( {
                "status": 400,
                "messages": "图书不存在"
            } )
        serializer = BookModelSerializer( data=data, instance=book )
        serializer.is_valid( raise_exception=True )
        serializer.save()
        return Response( {
            "status": 200,
            "messages": "修改单个成功",
            'result': BookModelSerializer( book ).data
        } )

    def patch(self, request, *args, **kwargs):
        data = request.data
        id = kwargs.get( 'id' )
        print( "data", data )
        print( "id", id )
        if id and isinstance( data, dict ):
            ids = [id]
            request_data = [data]
        elif not id and isinstance( data, list ):  # 修改多个
            ids = []
            for dic in data:
                pk = dic.pop( "id", None )
                print( "pk", pk )
                if pk:
                    ids.append( pk )
                else:
                    return Response( {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "PK不存在",
                    } )
        else:
            return Response( {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "参数格式有误",
            } )
        book_list = []
        new_data = []
        for index, pk in enumerate( ids ):
            try:
                book_obj = Book.objects.get( pk=pk )
                book_list.append( book_obj )
                new_data.append( request.data[index] )
            except Book.DoesNotExist:
                continue
        print( 'newdata', new_data )
        print( 'booklist', book_list )
        book_ser = BookModelSerializer( data=new_data, instance=book_list, partial=True, many=True )
        book_ser.is_valid( raise_exception=True )
        book_ser.save()

        return Response( {
            "status": status.HTTP_200_OK,
            "message": "修改成功",
        } )


class BookAPIView2( GenericAPIView,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin, ):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return self.retrieve( request, *args, **kwargs )
        return self.list( request, *args, **kwargs )

    def post(self, request, *args, **kwargs):
        return self.create( request, *args, **kwargs )

    def delete(self, request, *args, **kwargs):
        return self.destroy( request, *args, **kwargs )

    def put(self, request, *args, **kwargs):
        return self.partial_update( request, *args, **kwargs )


class BookLoginRegister( viewsets.GenericViewSet, mixins.UpdateModelMixin,
                         mixins.CreateModelMixin ):
    queryset = User.objects.all()
    serializer_class = BookLoginSerializer
    lookup_field = "username"
    def user_login(self, request, *args, **kwargs):
        data = request.data
        print( data['username'] )
        if data and isinstance( data, dict ):
            try:
                user = User.objects.get( username=data['username'], password=data['password'] )
            except User.DoesNotExist:
                return Response( {
                    "status": 400,
                    "message": "用户名或密码错误",
                } )
            return self.partial_update( request, *args, **kwargs )

        else:
                return Response( {
                    "status": 400,
                    "message": "参数错误"
                } )

    def user_register(self, request, *args, **kwargs):
        data = request.data
        print( data["username"] )
        try:
            user = User.objects.get( username=data["username"] )
            return Response( {
                "status": 400,
                "message": "用户名已存在"
            } )
        except User.DoesNotExist:

            return self.create( request, *args, **kwargs )
