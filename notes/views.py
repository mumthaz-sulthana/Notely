from django.shortcuts import render

from rest_framework import generics

from notes.serializers import UserSerializer,TaskSerializer

from notes.models import User,Task

from rest_framework import authentication,permissions

from rest_framework.response import Response

from rest_framework.views import APIView

from notes.permissions import OwnerOnly

from django.db.models import Count
# Create your views here.


class UserCreationView(generics.CreateAPIView):
    
    serializer_class=UserSerializer
    
    
            
class TaskListCreateView(generics.ListCreateAPIView):
    
    serializer_class=TaskSerializer
    
    queryset=Task.objects.all()
    
    #authentication_classes=[authentication.BasicAuthentication]
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]
    
    
    
    def perform_create(self, serializer):
        
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        
        qs=Task.objects.filter(owner=self.request.user)
        
        if "category" in self.request.query_params:
            
            category_values=self.request.query_params.get("category")
            
            qs=qs.filter(category=category_values)
            
        if "priority" in self.request.query_params:
            
            category_values=self.request.query_params.get("priority")
            
            qs=qs.filter(category=category_values)
            
        return qs
    
class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class=TaskSerializer
    
    queryset=Task.objects.all()
    
    #authentication_classes=[authentication.BasicAuthentication]
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[OwnerOnly]
    
    
class TaskSummaryView(APIView):
    
    #authentication_classes=[authentication.BasicAuthentication]
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request,*args,**kwargs):
        
        qs=Task.objects.filter(owner=request.user)
        
        category_summary=qs.values("category").annotate(count=Count("category"))
        
        status_summary=qs.values("status").annotate(count=Count("status"))
        
        priority_summary=qs.values("priority").annotate(count=Count("priority"))
        
        total_count=qs.count()
        
        context={
            "category_summary":category_summary,
            
            "status_summary":status_summary,
            
            "priority_summary" : priority_summary,
            
            "total_count": total_count
        }
        
        return Response(data=context)
        
        
class CategoryListView(APIView):
    
    def get(self,reuest,*args,**kwargs):
        
        qs=Task.category_choices
        
        st={cat for tp in qs for cat in tp}
        
        return Response(data=st)
        
        
    
    
        
        
