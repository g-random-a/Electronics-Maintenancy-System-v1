from django.db.models.query_utils import Q
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from project_user.models import *
from .forms import *
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value
from django.db.models.functions import Concat


class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['latest_articles'] = Article.objects.all()[:5]
        return context   

class PreSignUp(TemplateView):
    template_name = 'signin-pre.html'
        
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = '/get?next='
    template_name = 'signup.html' 
    page = 1
    cust = False
    tech = False
    
    def post(self, request, *args, **kwargs):
        request.session['userName'] = request.POST['username']
        print(request.POST['username'])
        return super().post(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if 'role' in self.kwargs and "role" not in request.session:
            self.page = 2
            if self.kwargs['role'] == 'customer':
                request.session['role'] = "customer"
                success_url = 'customer/get?next='
                self.cust == True
            if self.kwargs['role'] == 'technician':
                success_url = 'technician/get?next='
                request.session['role'] = "technician"
                self.tech == False
            else:
                print("redirect")
        elif "role" in request.session :
            pass
        else:
            print("redirect")
        return super().get(request, *args, **kwargs)
     
class SignUpNextView(CreateView):
    success_url = 'home.html'
    template_name = 'signup-Next.html' 
    userName = ''
    role = ''
    
    def get(self, request, *args, **kwargs):
        if 'userName' in request.session:
            self.userName = 1; #CustomUser.objects.all().filter(username = request.session['userName']).get().id
            self.role = request.session['role']
            del request.session['userName']
        else:
            print("redirect")
            
        if self.role == "customer":
            self.form_class = customerCreationForm
        else:
            self.form_class = techniciansForm
            
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # request.POST['User'] = self.userName
        return super().post(request, *args, **kwargs)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['userName'] = self.userName 
        context['role'] = self.role
        return context 
    
class TechniciansListView(ListView):
    model = Technician
    template_name = 'technicianList.html'
    searchKeyWord ={}
    address = ["alkjhlf", "haba", "abs", "hsg", "uytu"]
    fristAddress = True
    # queryset = Technician.objects.all().order_by('-date')
    
    def Search(self, request):
        searchFilter = request.GET['searchFilter']
        value = request.GET['searchInput']
        if ('mostRated' in request.GET):
            filter = "Most Rated"
        else:  filter = False
        
        if request.GET['searchInput'] or ('mostRated' in request.GET):
            self.searchKeyWord = {
                'value': value,
                'filter': filter
            }
        if searchFilter == 'name':
            self.searchKeyWord['name'] = True
            # queryset = Technician.objects.filter( Q(user__first_name__contains = value) | Q(user__last_name__contains = value) | Q(value in user.get_full_name()))
            # queryset = Technician.objects.annotate(search_name=('user__first_name'+ (' ') + 'user__last_name'))
            queryset = Technician.objects.annotate(search_name=Concat('user__first_name', Value(' '), 'user__last_name'))
            queryset = queryset.filter(search_name__contains = value )
            
            print(queryset.all())
        elif(searchFilter == 'device'):
            self.searchKeyWord['device'] = True
            queryset = Technician.objects.filter( Q(device__devicename__contains = value) | Q(device__deviceDescription__contains = value))
        elif(searchFilter == 'orgName'):
            self.searchKeyWord['orgName'] = True
            queryset = Technician.objects.filter(organizationName__contains = value )
        else:
            queryset = Technician.objects.all()
            
        if ('mostRated' in request.GET): 
            self.searchKeyWord['mostRated'] = True
            queryset = queryset.order_by('-rating')
        temp_queryset  = queryset 
        for address in self.address:
            if (address in request.GET): 
                self.searchKeyWord[address] = True
                if self.fristAddress:
                    temp_queryset = queryset.filter(Location = address )
                    print("frist query, :", temp_queryset, address)
                    self.fristAddress = False
                else:
                    temp_queryset = temp_queryset | queryset.filter(Location = address )
                    print("query :", temp_queryset)
            
        queryset = temp_queryset                
        self.queryset = queryset
    
    def get(self, request, *args, **kwargs):
        print()
        if(request.GET):
            self.Search(request)
        return super().get(self, request, *args, **kwargs)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['FilterForm'] = FilterForm
        context['SearchForm'] = TechnicianSearchForm
        if "deviceId" in self.kwargs:
            context['deviceId'] = self.kwargs['deviceId']
        else: context['deviceId'] = False
        context['searched'] = self.searchKeyWord 
        context['address'] = self.address 
        
        return context 
  
class TechniciansDetailView(DetailView): 
    model = Technician
    template_name = 'technicianDetail.html'
    # user:CustomUser 
    
    # def dispatch(self, request, *args, **kwargs):
    #     self.request = request
    #     obj = self.get_object().id
    #     obj = Technician.objects.get(id = obj)
    #     user = self.request.user
    #     self.user = user
    #     obj.incrementSeen(user)
    #     self.userPostCount()
    #     return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "deviceId" in self.kwargs:
            context['deviceId'] = self.kwargs['deviceId']
        return context 
   
# class UserPostView(DetailView):
#     model = CustomUser
#     template_name = 'user_post.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['latest_articles'] = Article.objects.all()[:5]
#         return context 
    
 
class UserUpdateView(LoginRequiredMixin, UpdateView): 
    model = Customer
    fields = ('__all__')
    template_name = 'updateProfile.html'
    login_url = 'login'
    role:any
    
    def dispatch(self, request, *args, **kwargs): # new
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'userDelete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'
    
    def dispatch(self, request, *args, **kwargs): # new
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    

# class CreateArticleView(LoginRequiredMixin, CreateView):
#     model = Article
#     template_name = 'article_create.html'
#     fields = ('title', 'body')    
#     success_url = reverse_lazy('article_list')
#     login_url = 'login'
    
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)
    
#     # def dispatch(self, request, *args, **kwargs): # new
#     #     obj = self.get_object()
#     #     if obj.author != self.request.user:
#     #         raise PermissionDenied
#     #     return super().dispatch(request, *args, **kwargs)

class OrderListView(ListView): 
    model = Order
    template_name = 'orderList.html'
    searchKeyWord ={}
    queryset = Order.objects.all().order_by('status')
    successMessage = ""
    
    def Search(self, request):
        searchFilter = request.GET['searchFilter']
        value = request.GET['searchInput']
        
        if ('newest' in request.GET):
            nfilter = "selected"
        else:  nfilter = False
        
        if request.GET['searchInput'] or nfilter:
            self.searchKeyWord = {
                'value': value,
                'filter': nfilter
            }
        if(searchFilter == 'device'):
            queryset = Order.objects.filter( Q(device__devicename__contains = value) | Q(device__deviceDescription__contains = value))
            self.searchKeyWord['device'] = True
        elif(searchFilter == 'technicianName'):
            queryset = Order.objects.filter(technician__organizationName__contains = value )
            self.searchKeyWord['tech'] = True
        else:
            queryset = Order.objects.all()
            
        if nfilter: 
            queryset = queryset.order_by('-date')
                    
        self.queryset = queryset
    
    def get(self, request, *args, **kwargs):
        if(request.GET and 'order' not in request.GET):
            self.Search(request)
        else:
            self.successMessage = "Your Order Is SuccessFully Submitted"
        return super().get(self, request, *args, **kwargs)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['searched'] = self.searchKeyWord
        if self.successMessage:
            context['success'] = self.successMessage
        context['SearchForm'] = OrderSearchForm
        context['FilterForm'] = FilterForm
        
        return context 

    
class OrderDetailView(DetailView): 
    model = Order
    template_name = 'orderDetail.html'
    
class DeviceListView(ListView):
    model = Device
    template_name = 'DeviceList.html'

class SelectTechnician(ListView):
    model = Technician
    template_name = 'DeviceList.html'
    success_url = reverse_lazy("orderSuccess")
    
    def get(self, request, *args, **kwargs):
        self.queryset=Technician.objects.filter(device__id = self.session['deviceId'])
        request.session['techId'] = self.kwargs['pk']
        return super().get(self, request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(str(self.success_url) ) 
    
class OrderFinalView(CreateView):
    form_class = OrderForm
    success_url = "/order/get?order=success"
    template_name = 'order.html'
    technician, device = '', ''
        
    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        post['User'] = request.user.id
        post['technician'] = self.kwargs['pk']
        post['device'] = self.kwargs['deviceId']
        request.POST = post
        return super().post(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        self.technician = Technician.objects.filter(id = self.kwargs['pk']).get()
        self.device = Device.objects.filter(id = self.kwargs['deviceId']).get()
        # print(self.technician.first())
        return super().get(request, *args, **kwargs)
        
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['device'] = self.device
        context['technician'] = self.technician
        return context 
    

class OrderView(CreateView):
    form_class = Order
    success_url = reverse_lazy("orderSuccess")
    template_name = 'order.html'
        
    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        post['User'] = request.user.id
        post['technician'] = self.kwargs['pk']
        request.POST = post
        return super().post(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        print(request.user)
        return super().get(request, *args, **kwargs)
    
    
class FeedbackView(CreateView):
    form_class = Feedback
    success_url = reverse_lazy("feedbackSuccess")
    template_name = 'feedback.html'
        
    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        if request.user != "AnonymousUser" or request.user.is_authenticated:
            post['user'] = request.user.id
        else: 
            post['user'] = "AnonymousUser"
        request.POST = post
        return super().post(request, *args, **kwargs)
