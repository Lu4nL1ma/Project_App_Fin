from models import customers
from django.forms import ModelForm


#CREATE YOUR FORMS HERE!

# class loginform(forms.ModelForm):
#    class Meta:
#       model = users

# class financasform(forms.ModelForm):
#    class Meta:
#       model = financas
#       fields = 'cliente', 'parcela', 'valor', 'curso'

class financasform(ModelForm):
   class Meta:
      model = customers
      fields = '__all__'