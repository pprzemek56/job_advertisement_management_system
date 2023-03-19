import re
from django import forms

from .models import Company, JobSeeker


class RegisterCompanyForm(forms.ModelForm):
    """
    Register company
    """

    password_2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Company
        fields = [
            "email",
            "company_name",
            "nip_number",
            "password"
        ]

    def clean_email(self):
        """
        verify email is available
        """
        email = self.cleaned_data.get("email")
        if Company.objects.filter(email=email).exists() \
                or JobSeeker.objects.filter(email=email).exists():
            raise forms.ValidationError("email is taken")

        return email

    def clean_nip_number(self):
        """
        verify nip number is valid and available
        """
        nip_number = self.cleaned_data.get("nip_number")
        if Company.objects.filter(nip_number=nip_number).exists():
            raise forms.ValidationError("nip number is taken")

        if re.match(r"^\d{10}$") is None:
            raise forms.ValidationError("nip number is invalid")

        return nip_number

    def clean(self):
        """
        verify passwords are the same
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        if password != self.password_2:
            raise forms.ValidationError("passwords doesn't match")

        return cleaned_data

