from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from rest_framework.generics import*
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from django.contrib.auth import authenticate
from rest_framework.permissions import BasePermission
from .permission import UserCanViewOwnBlog
# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }
# class UserCanViewOwnBlog(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         print(obj,'+++++++++++++++++++++++')
#         print(request,'+++++++++++++++++++++++')

#         # Check if the request user is the owner of the blog
#         return obj.email == request.user
ordering = sorted(['date_joined'],reverse=True)
class usercreateViews(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializers

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        if not serializer:
            return Response({"error":True,"message":serializer.errors})
        if not serializer.is_valid():
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                  "Message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        if User.objects.filter(email=serializer.validated_data['email']).exists():
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                  "Message": "User Email Already Registered",},
                            status=status.HTTP_400_BAD_REQUEST)
            
        else:
            # try:
                # User.objects.create(email=email,password=password)

                serializer.save()
                return Response(data={"Status": status.HTTP_201_CREATED,
                                      "Message": "User Registered",
                                      "Results": serializer.data},
                                status=status.HTTP_201_CREATED)
            # except:
            #     return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
            #                           "Message": serializer.errors},
            #                     status=status.HTTP_201_CREATED)

# class LoginViews(GenericAPIView):
#     serializer_class = UserLoginSerializer
#     queryset = User.objects.all()


#     def post(self,request):
#          serializer=UserLoginSerializer(data=request.data)
#          if serializer.is_valid(raise_exception=True):
#             email = serializer.validated_data.get('email')
#             print(email,'***************')
#             password = serializer.validated_data.get('password')
#             print(password,'***************')
#             user = authenticate(email=email,password=password)
#             print(user,'++++++++++++++++')
#             if user is not None:
#                 token = get_tokens_for_user(user)
#                 return Response({'token':token,'msg':'Login SucessFully'},status=status.HTTP_200_OK)
#             else:
#                 return Response({'msg':'Inavlid Data'},status=status.HTTP_404_NOT_FOUND)
#          return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)

class CreateBlogViews(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateBlogSerializer

    def post(self,request):
        serializer =self.get_serializer(data=request.data)
        if not serializer:
            return Response({"error":True,"message":serializer.errors})
        if serializer.is_valid():
            title = serializer.validated_data.get('title')
            detail = serializer.validated_data.get('detail')
            Blog.objects.create(user=request.user,title=title,detail=detail)
            return Response(data={"Status": status.HTTP_201_CREATED,
                                      "Message": "Blog Created",
                                      "Results": serializer.data},
                                status=status.HTTP_201_CREATED)

class ListBlogViews(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListBlogSerializer

    def get(self,request):
        all = Blog.objects.filter(user=request.user)
        serializer =self.get_serializer(all,many=True)
        if not serializer:
            return Response({"error":True,"message":serializer.errors})
        
        return Response(data={"Status": status.HTTP_201_CREATED,
                                      "Message": "Blog listed successfully",
                                      "Results": serializer.data},
                                status=status.HTTP_201_CREATED)

class UpdateBlogViews(GenericAPIView):
    permission_classes = [UserCanViewOwnBlog]

    def put(self,request,id):
        title = request.data['title']
        detail = request.data['detail']
        blog_obj = Blog.objects.filter(id=id).first()
        if not blog_obj:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                  "Message": "blog object not found",},
                            status=status.HTTP_400_BAD_REQUEST)
        if blog_obj.user==request.user:
            if blog_obj:
                blog_obj.title=title
                blog_obj.detail=detail
                blog_obj.save()
            else:
                pass
            return Response(data={"Status": status.HTTP_201_CREATED,
                                        "Message": "Blog updated successfully",},
                                    status=status.HTTP_201_CREATED)
        else:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                    "Message": "not owner",},
                                status=status.HTTP_400_BAD_REQUEST)

class DeleteBlogViews(GenericAPIView):
    permission_classes =  [IsAuthenticated,UserCanViewOwnBlog]
    # authentication_classes = [TokenAuthentication]
    def delete(self,request,id):
        blog_obj = Blog.objects.get(id=id)
        if blog_obj.user==request.user:
            if blog_obj:
                blog_obj.active=False
                blog_obj.save()
                return Response(data={"Status": status.HTTP_201_CREATED,
                                        "Message": "Blog delete successfully",},
                                    status=status.HTTP_201_CREATED)
            else:
                return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                    "Message": "blog object not found",},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                    "Message": "not owner",},
                                status=status.HTTP_400_BAD_REQUEST)


class Adminpanelview(GenericAPIView):
    permission_classes = [IsAdminUser]
    
    def get(self,request):
        date_start = request.data.get('start')
        date_end = request.data.get('end')
        if not date_start and date_end:
            user_obj = User.objects.all()
        else:
            user_obj = User.objects.filter(created_at__range=[date_start,date_end])
        serializer = AdminViewSerializer(user_obj,many=True)
        return Response(data={"Status": status.HTTP_201_CREATED,
                                        "Message": "user list below","user":serializer.data},
                                    status=status.HTTP_201_CREATED)
       
class AdminBlogView(GenericAPIView):
    # permission_classes = [IsAdminUser]

    def get(self,request):
        date_start = request.data.get('start')
        date_end = request.data.get('end')
        if date_start and date_end:
            user_obj = Blog.objects.filter(created_at__date__range=[date_start,date_end])
        else:
            user_obj = Blog.objects.all()
        serializer = ListBlogSerializer(user_obj,many=True)
        return Response(data={"Status": status.HTTP_201_CREATED,
                                        "Message": "blog list below","user":serializer.data},
                                    status=status.HTTP_201_CREATED)

class AdminUserUpdate(GenericAPIView):
    permission_classes = [IsAdminUser]
 
    def put(self,request,id):
        email = request.data.get('email')
        address = request.data.get('address')
        user_obj = User.objects.get(id=id)
        if not user_obj:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                    "Message": "user object not found",},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            user_obj.email = email
            user_obj.address = address
            user_obj.save()
            return Response(data={"Status": status.HTTP_201_CREATED,
                                        "Message": "Blog updated successfully",},
                                    status=status.HTTP_201_CREATED)

class AdminUserDelete(GenericAPIView):
    permission_classes = [IsAdminUser]
    
    def delete(self,request,id):
        user_obj = User.objects.get(id=id)
        if user_obj:
            user_obj.active=False
            user_obj.save()
            return Response(data={"Status": status.HTTP_201_CREATED,
                                        "Message": "user delete successfully",},
                                    status=status.HTTP_201_CREATED)
        else:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                    "Message": "user object not found",},
                                status=status.HTTP_400_BAD_REQUEST)

class AdminBlogUpdate(GenericAPIView):
    permission_classes = [IsAdminUser]

    def put(self,request,id):
        title = request.data['title']
        detail = request.data['detail']
        blog_obj = Blog.objects.filter(id=id).first()
        if not blog_obj:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                  "Message": "blog object not found",},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            blog_obj.title=title
            blog_obj.detail=detail
            blog_obj.save()
            return Response(data={"Status": status.HTTP_201_CREATED,
                                    "Message": "Blog updated successfully",},
                                status=status.HTTP_201_CREATED)

class AdminBlogDelete(GenericAPIView):
    permission_classes = [IsAdminUser]
    
    def delete(self,request,id):
        blog_obj = Blog.objects.filter(id=id).first()
        if not blog_obj:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                  "Message": "blog object not found",},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            blog_obj.active=False
            blog_obj.save()
            return Response(data={"Status": status.HTTP_201_CREATED,
                                    "Message": "Blog Delete successfully",},
                                status=status.HTTP_201_CREATED)

class AdminUserActive(GenericAPIView):
    # permission_classes = [IsAdminUser]
    
    def get(self,request,id):
        user_obj = User.objects.filter(id=id).first()
        if user_obj:
            if user_obj.active==False:
                user_obj.active=True
                user_obj.save()
                return Response(data={"Status": status.HTTP_201_CREATED,
                                        "Message": "user active successfully",},
                                    status=status.HTTP_201_CREATED)
            else:
                return Response(data={"Status": status.HTTP_201_CREATED,
                                        "Message": "user active already",},
                                    status=status.HTTP_201_CREATED)
        else:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                  "Message": "user object not found",},
                            status=status.HTTP_400_BAD_REQUEST)

from django.db.models import Count
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.template import loader
import logging
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
class UserBlogCount(GenericAPIView):
    
    def post(self,request,id):
        date_str = request.data.get('date')
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse("Invalid date format. Please use the format YYYY-MM-DD.")

        # Calculate the start and end dates for the selected week
        start_date = date - timedelta(days=date.weekday())
        end_date = start_date + timedelta(days=6)
        
        # Query the database for the user's blog posts for the selected week
        posts = Blog.objects.filter(user=id, created_at__range=[start_date, end_date])
        
        # Count the number of posts for each day of the week
        post_counts = {}
        for i in range(7):
            day = start_date + timedelta(days=i)
            post_counts[day] = 0
    
        for post in posts:
            post_day = post.created_at.date()
            if post_day in post_counts:
                post_counts[post_day] += 1
        # Generate the bar chart
        x = post_counts.keys()
        y = post_counts.values()
        plt.bar(x, y)
        plt.title(f"Blog Posts for Week of {start_date.strftime('%B %d, %Y')}")
        plt.xlabel("Day of the Week")
        plt.ylabel("Number of Posts")
        
        # Save the chart to a BytesIO buffer and render it as an HTTP response
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        response = HttpResponse(buffer.getvalue(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename=blog_posts_week_{start_date}.png'
        return response