from wtforms.form import Form
from python_plugins.forms.fields import JSONField
from python_plugins.forms.fields import DateTimeField

class F(Form):
    a = JSONField()
    b = DateTimeField()


def test_fields():
    f=F()

    # print(f.a())
    assert "textarea" in f.a()

    # print(f.b())
    assert "input" in f.b()


