from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=40,primary_key=True)
    password=models.CharField(max_length=22)
    status=models.BooleanField(default=False)
    class Meta:
        db_table="User"
        verbose_name="用户"
        verbose_name_plural=verbose_name

class BookBase(models.Model):
    is_delete=models.BooleanField(default=False)
    create_time=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=True)
    class Meta:
        abstract=True
class Book(BookBase):
    book_name=models.CharField(max_length=120)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    pic=models.ImageField(upload_to="img",default='img/1.jpg')
    author=models.ManyToManyField(to='Author',db_constraint=False,related_name="books")
    publish=models.ForeignKey(to='Press',on_delete=models.CASCADE,db_constraint=False,
                              related_name="books")
    class Meta:
        db_table="book"
        verbose_name="图书"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.book_name

class Press(BookBase):
    press_name=models.CharField(max_length=120)
    pic=models.ImageField(upload_to="img",default="img/1.jpg")
    address=models.CharField(max_length=256)

    class Meta:
        db_table="press"
        verbose_name="出版社"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.press_name
class Author(BookBase):
    author_name=models.CharField(max_length=120)
    age=models.IntegerField()

    class Meta:
        db_table="Author"
        verbose_name="作者"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.author_name

class AuthorDetail(BookBase):
    phone=models.CharField(max_length=12)
    author=models.OneToOneField(to="Author",on_delete=models.CASCADE,related_name='detail')
    class Meta:
        db_table='detail'
        verbose_name="作者详情"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.author.author_name

