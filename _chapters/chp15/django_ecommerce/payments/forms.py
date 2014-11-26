from django import forms
from django.core.exceptions import NON_FIELD_ERRORS


class PaymentForm(forms.Form):
    def addError(self, message):
        self._errors[NON_FIELD_ERRORS] = self.error_class([message])


class SigninForm(PaymentForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        required=True, widget=forms.PasswordInput(render_value=False)
    )


class CardForm(PaymentForm):
    last_4_digits = forms.CharField(
        required=True,
        min_length=4,
        max_length=4,
        widget=forms.HiddenInput()
    )
    stripe_token = forms.CharField(required=True, widget=forms.HiddenInput())


class UserForm(CardForm):

    name = forms.CharField(required=True, min_length=3)
    email = forms.EmailField(required=True)
    password = forms.CharField(
        required=True,
        label=('Password'),
        widget=forms.PasswordInput(render_value=False)
    )
    ver_password = forms.CharField(
        required=True,
        label=('Verify Password'),
        widget=forms.PasswordInput(render_value=False)
    )

    ng_scope_prefix = "userform"

    def __init__(self, *args, ** kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            attrs = {"ng-model": "%s.%s" % (self.ng_scope_prefix, name)}

            if field.required:
                attrs.update({"required": True})
            if field.min_length:
                attrs.update({"ng-minlength": field.min_length})
            field.widget.attrs.update(attrs)

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        ver_password = cleaned_data.get('ver_password')
        if password != ver_password:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data
