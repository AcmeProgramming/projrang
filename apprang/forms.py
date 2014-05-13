from django import forms
from apprang.models import Page, Category, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    """This Meta ties CategoryForm models.Category."""
    class Meta:
        model = Category

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the url of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        """This def clean cleans data incoming to PageForm."""
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        """This if prepends http:// if there is no http://."""
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url 

        return cleaned_data

    """This Meta ties PageForm to models.Page."""
    class Meta:
        model = Page
        """Including fields/attributes from model.Page"""
        fields = ('title', 'url', 'views')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
