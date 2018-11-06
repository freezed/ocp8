#########################
## OMEGA PROJECT TESTS ##
#########################
import pytest
import omega.forms

def test_omega_forms_create_user_fields():
    test_form = omega.forms.SignInForm()

    for field in ('username','email','password1','password2'):
        assert field in test_form.fields
