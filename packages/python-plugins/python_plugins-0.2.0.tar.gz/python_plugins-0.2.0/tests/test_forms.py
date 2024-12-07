from wtforms.form import Form
from python_plugins.forms.fields import JSONField
from python_plugins.forms.fields import DateTimeField
from python_plugins.forms.mixins.user import LoginForm
from python_plugins.forms.mixins.user import RegisterForm


class DummyPostData(dict):
    def getlist(self, key):
        v = self[key]
        if not isinstance(v, (list, tuple)):
            v = [v]
        return v


class UserLoginForm(Form, LoginForm):
    pass


class UserRegisterForm(Form, RegisterForm):
    pass


def test_fields():
    class F(Form):
        json_field = JSONField()
        datetime_field = DateTimeField()

    formdata = DummyPostData(
        json_field="[1,2,3]",
        datetime_field="2000-01-01 12:12:12",
    )

    f = F(formdata)
    assert f.validate()

    json_field_text = f.json_field()
    assert '<textarea id="json_field" name="json_field">' in json_field_text
    assert "[1, 2, 3]</textarea>" in json_field_text

    datetime_field_text = f.datetime_field()
    assert "<input" in datetime_field_text
    assert (
        'data-date-format="YYYY-MM-DD HH:mm:ss" data-role="datetimepicker"'
        in datetime_field_text
    )
    assert 'value="2000-01-01 12:12:12"' in datetime_field_text


def test_user_form():
    login_form = UserLoginForm()

    for k in login_form:
        # print(k.label())
        # print(k())
        assert k() is not None

    assert "username" in login_form.username()

    register_form = UserRegisterForm()

    for k in register_form:
        # print(k.label())
        # print(k())
        assert k() is not None
