from django.test import runner


class TestRunner(runner.DiscoverRunner):

    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        if not test_labels:
            test_labels = ('src',)

        return super(TestRunner, self).build_suite(
            test_labels, extra_tests, **kwargs)
