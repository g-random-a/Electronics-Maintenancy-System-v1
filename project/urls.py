from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from project_user.views import *
# from articles.views import HomeView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('users/', include('users.urls')),
    path('', include('django.contrib.auth.urls')),
    
    path('', HomeView.as_view(), name='home'),
    
    path('signup/', PreSignUp.as_view(), name='signup-pre'),
    path('signup/<str:role>', SignUpView.as_view(), name='signup'),
    path('signup/technician/get', SignUpNextView.as_view(), name='signup-next'),
    
    path('technician/', TechniciansListView.as_view(), name='technicianList'), # new
    path('technician/get', TechniciansListView.as_view(), name='technicianList_get'),
    path('Order/<int:deviceId>/', TechniciansListView.as_view(), name='technicianListOrder'),
    path('Order/<int:deviceId>/get', TechniciansListView.as_view(), name='technicianListOrder_get'),
    
    path('technician/detail/<int:pk>/', TechniciansDetailView.as_view(), name='technicianDetail'), # new
    path('Order/<int:deviceId>/<int:pk>/', TechniciansDetailView.as_view(), name='technicianDetailOrder'), # new
    path('Order/<int:deviceId>/<int:pk>/final', OrderFinalView.as_view(), name='technicianDetailOrder'), # new
    
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name='updateProfile'), # new
    path('user/delete/<int:pk>/', UserUpdateView.as_view(), name='deleteProfile'), # new
    
    path('order/<int:pk>', OrderView.as_view(), name='ordert'), # new
    
    path('order/', OrderListView.as_view(), name='order'), # new
    path('order/get', OrderListView.as_view(), name='orderSearch'), # new
    path('order/detail/<int:pk>', OrderDetailView.as_view(), name='orderDetail'), # neworderSuccess
    
    path('device/', DeviceListView.as_view(), name='deviceList'), # new
    path('feedback/', FeedbackView.as_view(), name='feedback'), # new
    
    
    
    # path('articles/', include('articles.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)