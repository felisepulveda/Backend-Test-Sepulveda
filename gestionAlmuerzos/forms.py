from django import forms

class FormularioIngreso(forms.Form):
    nombre=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
