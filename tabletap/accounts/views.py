from django.shortcuts import render, redirect
from django.contrib.auth import login
from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from restaurant.models import Restaurant, Table

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField()
    full_name = forms.CharField(max_length=255)
    restaurant_name = forms.CharField(max_length=255)
    restaurant_address = forms.CharField(required=False)
    num_tables = forms.IntegerField(min_value=1, label="Number of Tables")

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        user.is_staff = True

        if commit:
            user.save()
            restaurant = Restaurant.objects.create(
                name=self.cleaned_data['restaurant_name'],
                address=self.cleaned_data['restaurant_address'],
                owner=user
            )
            for i in range(1, self.cleaned_data['num_tables'] + 1):
                Table.objects.create(restaurant=restaurant, table_number=i)
        return user

def signup_view(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = CustomSignupForm()
    return render(request, "accounts/signup.html", {"form": form})
