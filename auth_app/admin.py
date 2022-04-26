from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms

from .models import User
from app.models import Company, Job



class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ( 'username', 'email', 'is_staff', 'is_employer', 'is_seeker', 'is_verified')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Two Password doesn't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_staff', 'is_employer', 'is_seeker', 'is_verified')

    def clean_password(self):
        return self.initial["password"]



class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['username', 'email', 'is_staff', 'is_employer', 'created_at']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_staff', 'is_employer', 'is_seeker', )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username' ,'email', 'is_staff', 'is_employer', 'is_seeker', 'password1', 'password2')}
        ),
    )

    search_fields = ('email', 'username', )

    ordering = ('-created_at',)


admin.site.register(User, UserAdmin)





class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'address']

admin.site.register(Company, CompanyAdmin)




class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'role', 'vaccancy']

admin.site.register(Job, JobAdmin)
