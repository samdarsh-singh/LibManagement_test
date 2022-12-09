from rest_framework import serializers
from .models import *

# create user as student

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
# custome user field
class StudentRegisterSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()
    class Meta:
        model = User
        read_only_fields = ('username', 'password', 'email', )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserRegisterSerializer.create(UserRegisterSerializer(), validated_data=user_data)
        myuser = MyUsers.objects.create(user=user, is_student=True)
        Student.objects.create(user=myuser, **validated_data)
        
class LibrarianRegisterSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()
    class Meta:
        model = User
        read_only_fields = ('username', 'password', 'email', )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserRegisterSerializer.create(UserRegisterSerializer(), validated_data=user_data)
        myuser = MyUsers.objects.create(user=user, is_librarian=True)
        Librarian.objects.create(user=myuser, **validated_data)

class BorrowBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBooks
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarian
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BorrowedBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBooks
        fields = '__all__'

class MyUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUsers
        fields = '__all__'

    


    

