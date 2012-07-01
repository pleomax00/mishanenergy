from django import forms
from django.conf import settings
from django.core import validators
import re
from django.contrib.auth.models import User
from thirdparty import titlecase as t

class RegisterForm (forms.Form):
    email = forms.CharField ( min_length = 5, max_length = 500, validators=[validators.validate_email],
                              error_messages={'invalid': u'Enter a valid e-mail address.'})
    name = forms.CharField ( min_length = 3, max_length = 128 )
    password = forms.CharField ( min_length = 4, max_length = 12, widget = forms.PasswordInput )
    repassword = forms.CharField ( min_length = 4, max_length = 12, widget = forms.PasswordInput )
    
    def clean_name (self):
        name = self.cleaned_data["name"]
        return t.titlecase(name)

    def clean_email (self):
        try:
            u = User.objects.get ( email = self.cleaned_data["email"] )
            raise forms.ValidationError ( "This email address is already registered!" )
        except User.DoesNotExist:
            pass
        return self.cleaned_data["email"]

    def clean_repassword (self):
        passwd = self.cleaned_data.get("password", "")
        repasswd = self.cleaned_data.get("repassword", "pass2")
        if repasswd != passwd:
            raise forms.ValidationError ( "Both the supplied passwords must match!" )
        return self.cleaned_data["repassword"]


class BlogPostForm (forms.Form):
    title = forms.CharField ( max_length = 500 )
    tags = forms.CharField ( max_length = 200 )
    catagory = forms.CharField (max_length = 50)
    post = forms.CharField ( widget = forms.Textarea )


class ContactUsForm (forms.Form):
    name = forms.CharField ( max_length = 256, required = True )
    email = forms.EmailField ()
    company = forms.CharField ( max_length = 100 )
    cellnum = forms.CharField ( max_length = 12, required = True )
    enquiry = forms.CharField ( widget = forms.Textarea )
