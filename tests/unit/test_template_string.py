import os

from jinja2 import TemplateSyntaxError
from nornir_jinja2.plugins.tasks import template_string


data_dir = "{}/test_data".format(os.path.dirname(os.path.realpath(__file__)))

simple_j2 = """

host-name: {{ host }}

my_var: {{ my_var}}

"""

simple2_j2 = """

host-name: {{ host }}

my_var: {{ my_var | to_upper }}

"""

broken_j2 = """
#Broken template

host-name {{ host

my_var: {{ my_var}}
"""


def jinja_filter_to_upper(value):
    return str(value).upper()


class Test(object):
    def test_template_string(self, nr):

        result = nr.run(template_string, template=simple_j2, my_var="asd")

        assert result
        for h, r in result.items():
            assert "host-name: {}".format(h) in r.result
            if h == "host1.group_1":
                assert "my_var: comes_from_host1.group_1" in r.result
            if h == "host2.group_1":
                assert "my_var: comes_from_group_1" in r.result

    def test_jinja_filter(self, nr):
        filters = {
            "to_upper": jinja_filter_to_upper,
        }
        result = nr.run(template_string, template=simple2_j2, my_var="asd", jinja_filters=filters)

        assert result
        for h, r in result.items():
            assert "host-name: {}".format(h) in r.result
            if h == "host1.group_1":
                assert "my_var: COMES_FROM_HOST1.GROUP_1" in r.result
            if h == "host2.group_1":
                assert "my_var: COMES_FROM_GROUP_1" in r.result
            if h == "dev3.group_2":
                assert "my_var: ASD" in r.result

    def test_template_string_error_broken_string(self, nr):
        results = nr.run(template_string, template=broken_j2)
        processed = False
        for result in results.values():
            processed = True
            assert isinstance(result.exception, TemplateSyntaxError)
        assert processed
