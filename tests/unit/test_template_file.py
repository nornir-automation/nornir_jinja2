import os

from jinja2 import Environment, TemplateSyntaxError

from nornir_jinja2.plugins.tasks import template_file

data_dir = "{}/test_data".format(os.path.dirname(os.path.realpath(__file__)))


class Test(object):
    def test_template_file(self, nr):
        result = nr.run(
            template_file, template="simple.j2", my_var="asd", path=data_dir
        )

        assert result
        for h, r in result.items():
            assert h in r.result
            if h == "host3.group_2":
                assert "my_var: comes_from_all" in r.result
            if h == "host4.group_2":
                assert "my_var: comes_from_host4.group_2" in r.result

    def test_template_file_error_broken_file(self, nr):
        results = nr.run(template_file, template="broken.j2", path=data_dir)
        processed = False
        for result in results.values():
            processed = True
            assert isinstance(result.exception, TemplateSyntaxError)
        assert processed

    def test_template_file_no_path_or_jinja_env(self, nr):
        results = nr.run(template_file, template="simple.j2", my_var="asd")

        processed = False
        for result in results.values():
            processed = True
            assert isinstance(result.exception, ValueError)
        assert processed

    def test_template_file_jinja_env_without_loader(self, nr):
        jinja_env = Environment(
            loader=None,
            trim_blocks=True,
        )
        results = nr.run(
            template_file, template="simple.j2", my_var="asd", jinja_env=jinja_env
        )

        processed = False
        for result in results.values():
            processed = True
            assert isinstance(result.exception, TypeError)
        assert processed
