from django import forms
from .models import MenuItem, MenuCategory

class CategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Add New Category',
                'class': 'w-full px-3 py-2 border rounded-l-md focus:outline-none'
            })
        }

class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = ['name']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['category', 'name', 'description', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border px-3 py-2 rounded', 'placeholder': 'E.g. Spaghetti'}),
            'description': forms.Textarea(attrs={'class': 'w-full border px-3 py-2 rounded', 'placeholder': 'Optional...', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'w-full border px-3 py-2 rounded'}),
            'category': forms.Select(attrs={'class': 'w-full border px-3 py-2 rounded'}),
        }

    def __init__(self, *args, **kwargs):
        restaurant = kwargs.pop("restaurant", None)
        super(MenuItemForm, self).__init__(*args, **kwargs)
        if restaurant:
            self.fields["category"].queryset = MenuCategory.objects.filter(restaurant=restaurant)

