from unittest import TestCase
from configcascade import Settings, YamlFileLoader
import os


class SettingsTestCase(TestCase):
    def test_with_merge(self):
        config_file = os.path.realpath("%s/fixture/config/settings_test.yml" % os.path.dirname(os.path.realpath(__file__)))
        file_loader = YamlFileLoader()
        settings_loader = Settings(file_loader, ['routes', 'parameters', 'services'])
        settings = settings_loader.compile(config_file)

        expected_parameters = {'driver': {'surname': 'Carmona', 'complete_name': '{{ driver.name }} {{ driver.surname }}', 'name': 'Felix'}}
        expected_routes = {'my_controller_with_service': {'path': '/my_controller/with/service', 'controller': 'felix.SomeController'}, 'hello': {'path': '/hello/{name}', 'controller': 'felix.HelloController'}}
        expected_server = {'foo': 'bar'}
        expected_server_adapter = None
        expected_services = {'car': {'class': 'felix.services.Car', 'arguments': ['@driver']}, 'driver': {'class': 'felix.services.Driver', 'arguments': ['{{ driver.complete_name }}']}}
        expected_error_handler = 'felix.handler.DefaultErrorHandler'
        expected_debug = False

        self.assertEqual(settings['parameters'], expected_parameters)
        self.assertEqual(settings['routes'], expected_routes)
        self.assertEqual(settings['server'], expected_server)
        self.assertEqual(settings['server_adapter'], expected_server_adapter)
        self.assertEqual(settings['services'], expected_services)
        self.assertEqual(settings['error_handler'], expected_error_handler)
        self.assertEqual(settings['debug'], expected_debug)

    def test_without_merge(self):
        config_file = os.path.realpath("%s/fixture/config/settings_test.yml" % os.path.dirname(os.path.realpath(__file__)))
        file_loader = YamlFileLoader()
        settings_loader = Settings(file_loader)
        settings = settings_loader.compile(config_file)

        expected_parameters = {'driver': {'surname': 'Carmona', 'complete_name': '{{ driver.name }} {{ driver.surname }}', 'name': 'Felix'}}
        expected_routes = {'my_controller_with_service': {'path': '/my_controller/with/service', 'controller': 'felix.SomeController'}, 'hello': {'path': '/hello/{name}', 'controller': 'felix.HelloController'}}
        expected_server = {'foo': 'bar'}
        expected_server_adapter = None
        expected_services = {'car': {'class': 'felix.services.Car', 'arguments': ['@driver']}}
        expected_error_handler = 'felix.handler.DefaultErrorHandler'
        expected_debug = False

        self.assertEqual(settings['parameters'], expected_parameters)
        self.assertEqual(settings['routes'], expected_routes)
        self.assertEqual(settings['server'], expected_server)
        self.assertEqual(settings['server_adapter'], expected_server_adapter)
        self.assertEqual(settings['services'], expected_services)
        self.assertEqual(settings['error_handler'], expected_error_handler)
        self.assertEqual(settings['debug'], expected_debug)
