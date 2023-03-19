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
        password_2 = cleaned_data.get("password_2")
        if password != password_2:
            raise forms.ValidationError("passwords doesn't match")

        return cleaned_data


class RegisterJobSeekerForm(forms.ModelForm):
    """
    Register job seeker
    """

    password_2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = JobSeeker
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "cv",
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

    def clean_first_name(self):
        """
        verify first name is valid
        """
        first_name = self.cleaned_data.get("first_name")
        if re.match(r"^[a-zA-Z]+$", first_name) is None:
            raise forms.ValidationError("First name is invalid")

        return first_name

    def clean_last_name(self):
        """
        verify last name is valid
        """
        last_name = self.cleaned_data.get("last_name")
        if re.match(r"^[a-zA-Z]+$", last_name) is None:
            raise forms.ValidationError("Last name is invalid")

        return last_name

    def clean_phone_number(self):
        """
        verify nip number is valid and available
        """
        phone_number = self.cleaned_data.get("phone_number")
        if JobSeeker.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("nip number is taken")

        if re.match(r"^\d{9}$") is None:
            raise forms.ValidationError("nip number is invalid")

        return phone_number

    def clean(self):
        """
        verify passwords are the same
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password != password_2:
            raise forms.ValidationError("passwords doesn't match")

        return cleaned_data

