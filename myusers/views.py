from django.shortcuts import render
from rest_framework import viewsets
# import gentiv view
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from .forms import *
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm 
# Create your views here.






# register html page view
class StudentRegister(generics.GenericAPIView):
    template_name = "register.html"
    serializer_class = StudentRegisterSerializer
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "user_form": UserRegisterForm(),
            "student": True,
        })

    def post(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()
        data = request.data
        user = User.objects.create_user(username=data["username"], password=data["password"])
        user.save()
        myuser = MyUsers.objects.create(user=user, is_student=True)
        myuser.save()
        student = Student.objects.create(user=myuser) 
        student.save()
        return redirect("/login")

class LibrarianRegister(generics.GenericAPIView):
    template_name = "register.html"
    serializer_class = LibrarianRegisterSerializer
    def get(self, request, *args, **kwargs):
        return render(request , self.template_name, {
            "user_form": UserRegisterForm(),})

    def post(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.create_user(username=data["username"], password=data["password"])
        user.save()
        myuser = MyUsers.objects.create(user=user, is_librarian=True)
        myuser.save()
        librarian = Librarian.objects.create(user=myuser) 
        librarian.save()
        return redirect("/login")

class LoginView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        return render(request, "login.html", {
            "form": AuthenticationForm()
        })
    def post(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.get(username=data["username"])
        if user.check_password(data["password"]):
            request.session["user_id"] = user.id
            return redirect("home")
        else:
            return redirect("/login")


def borrowdata(borrowed):
    x = {}
    for i in borrowed:
        borrow_serilazer = BorrowBookSerializer(i)
        x["borrow"] = borrow_serilazer.data

        date_book = i.date_borrowed
        today = datetime.date.today()
        days = (today - date_book).days
        if i.date_returned == None:
            if days > 30:
                x["status"] = "overdue"
                x["day_left"] = days
            else:
                x["status"] = "borrowed"
                x["day_left"] = 30 - days
        else:
            x["status"] = "renewed"
    return x

class HomeView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        book = Book.objects.all()
        serilazer = BookSerializer(book, many=True)
        if request.session.get("user_id"):
            user = User.objects.get(id=request.session.get("user_id"))
            myuser = MyUsers.objects.get(user=user)
            if user.myusers.is_student:
                x = {}
                try:
                    borrowed = BorrowedBooks.objects.filter(user=myuser)
                    x = borrowdata(borrowed)
                                   
                except:
                    pass
                
                return Response({"type": "student", "books": serilazer.data, "borrowed": x})
            elif user.myusers.is_librarian:
                students = Student.objects.all()
                s = []
                for student in students:
                    import pdb; pdb.set_trace()
                    try:
                        borrowed = BorrowedBooks.objects.filter(user=student.user)
                        s.append({'student':StudentSerializer(student).data,
                        'borrowed': borrowdata(borrowed)
                        })
                    except:
                        s.append(StudentSerializer(student).data)
                        

                return  Response({"type": "librarian", "books": serilazer.data, "students": s})
        else:
            return Response({"type": "anonymous", "books": serilazer.data})



class BookPostView(generics.GenericAPIView):
    serializer_class = BookSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        book = Book.objects.create(title=data["title"], author=data["author"])
        book.save()
        return redirect("home")

import datetime


class BorrowbookView(generics.GenericAPIView):
    serializer_class = BorrowBookSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        book = Book.objects.get(id=data["book"])
        user = User.objects.get(id=data["user"])
        myuser = MyUsers.objects.get(user=user)
        student = Student.objects.get(user=myuser)
        if student.borrow <= 10:
            borrow = BorrowedBooks.objects.create(book=book, user=myuser)
            borrow.save()
            book.available -= 1
            book.save()
            student.borrow += 1
            student.save()
            return Response({"message": "Book borrowed successfully"})
        else:
            return Response({"message": "You have already borrowed 10 books"})

        

class ReturnBookView(generics.GenericAPIView):
    serializer_class = BorrowBookSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        book = Book.objects.get(id=data["book_id"])
        user = User.objects.get(id=data["user"])

        myuser = MyUsers.objects.get(user=user)
        borrow = BorrowedBooks.objects.get(book=book, user=myuser)
        borrow.date_returned = datetime.datetime.now()
        borrow.save()
        return Response({"message": "Book returned successfully"})

# create user as librarian

