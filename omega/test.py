#########################
## OMEGA PROJECT TESTS ##
#########################
import pytest
import omega.forms

def test_omega_forms_create_user_fields():
    test_form = omega.forms.SignInForm()

    for field in ('username','email','password1','password2'):
        assert field in test_form.fields

## TESTING USERS & VIEWS
# from django.contrib.auth.models import User

# @pytest.mark.django_db
# def test_root_user():
    # root = User.objects.get(username='root')
    # assert root.is_superuser

def test_user_login_valid():
    pass

def test_user_login_invalid():
    pass
