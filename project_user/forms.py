from typing import DefaultDict
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, UserModel, UsernameField
from django.forms import widgets
from django.forms.fields import EmailField
from django.utils.regex_helper import Choice
from .models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('is_customer', 'is_Technician', 'phoneNumber', 'first_name', 'last_name', 'email')
        # exclude = ('',)
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm,self).__init__(*args,**kwargs)
        #self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Username'})
     
class techniciansForm(forms.ModelForm):   
    class Meta():
        model = Technician
        fields = "__all__"
        
        
# class techniciansForm(UserCreationForm):   
#     class Meta(UserCreationForm.Meta):
#         model = Customer
#         fields = "__all__"
       
#class testform(forms.ModelForm):
#     class Meta:
#         model = image
#         fields = '__all__'


class customerCreationForm(forms.ModelForm):
    class Meta():
        model = Customer
        fields = "__all__"
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
  
class OrderForm(forms.ModelForm):
    class Meta():
        model = Order
        fields = "__all__" 

class Feedback(forms.ModelForm):
    name = forms.CharField(max_length=50, required = True)
    class Meta():
        model = Feedback
        fields = "__all__"
        
class FilterForm(forms.Form):
    mostRated = forms.BooleanField( 
                label= 'newest', label_suffix = ' : ', required= False, 
                disabled= False,  
                widget = forms.widgets.CheckboxInput(
                    attrs = {
                        'class' : 'check_box__mostRated checkbox-inline',
                        'id' : 'newest',
                    }
                ))
    
            
class TechnicianSearchForm(forms.Form):
    filters = [
        ('name', 'name'),
        ('device', 'device'),
        ('technicianName', 'technicianName'),
        ('location', 'location')
    ]
    
    searchFilter = forms.ChoiceField(required=False,
                        widget = forms.widgets.DateTimeInput(
                            attrs = {
                                'class' : 'searchfilter',
                                'id' : 'searchFilter',
                        }
                        ), 
                        choices = filters                
                    )
    searchInput = forms.CharField(
        required=False,
        widget = forms.widgets.DateTimeInput(
                            attrs = {
                                'class' : 'searchInput',
                                'id' : 'searchInput',
                        }
                        ) 
    )
class OrderSearchForm(forms.Form):
    filters = [
        ('name', 'name'),
        ('device', 'device'),
        ('technicianName', 'technicianName'),
        ('location', 'location')
    ]
    
    searchFilter = forms.ChoiceField(required=False,
                        widget = forms.widgets.DateTimeInput(
                            attrs = {
                                'class' : 'searchfilter',
                                'id' : 'searchFilter',
                        }
                        ), 
                        choices = filters                
                    )
    searchInput = forms.CharField(
        required=False,
        widget = forms.widgets.DateTimeInput(
                            attrs = {
                                'class' : 'searchInput',
                                'id' : 'searchInput',
                        }
                        ) 
    )
    