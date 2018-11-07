import pytest

import account.forms


def test_account_forms_create_user_fields():
    test_form = account.forms.SignInForm()

    for field in ('username','email','password1','password2'):
        assert field in test_form.fields
