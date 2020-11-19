from unittest import TestCase

from shopwareapi.exceptions import ConfigurationError, FronzenConfigurationError
from shopwareapi.utils.conf import DefaultConfiguration, Configuration


class UtilsConfigurationTestCase(TestCase):

    def test_default_config_inherith(self):
        """
            check if default values are inherited by the configuration object
        """
        DefaultConfiguration.FOOBAR = "test"
        settings = Configuration()
        self.assertEqual(settings.FOOBAR, "test")

        settings = Configuration(FOOBAR="hallo")
        self.assertEqual(settings.FOOBAR, "hallo")

    def test_invalid_config_name(self):
        """
            checks if invalid configuration names generate the corresponding errors
        """
        with self.assertRaises(ConfigurationError) as e:
            settings = Configuration(TESTASDF="hi")

    def test_config_update_method(self):
        """
            tests the configuration object update method
        """

        DefaultConfiguration.FOOBAR = "test"
        settings = Configuration()
        settings.update(FOOBAR="TestWert123")
        self.assertEqual(settings.FOOBAR, "TestWert123")

        with self.assertRaises(ConfigurationError) as e:
            settings = Configuration(ANOTHERTEST="hi")

    def test_config_freeze(self):
        """
            check the configuration freeze method.
            freeze should refuse to edit the configuration object
        """

        DefaultConfiguration.TESTWERT_A = "testa"
        DefaultConfiguration.TESTWERT_B = "testb"
        DefaultConfiguration.TESTWERT_C = "testc"

        settings = Configuration()

        self.assertEqual(settings.TESTWERT_A, "testa")
        self.assertEqual(settings.TESTWERT_B, "testb")
        self.assertEqual(settings.TESTWERT_C, "testc")

        settings.TESTWERT_A = "foobar"

        settings.freeze()

        with self.assertRaises(FronzenConfigurationError) as e:
            settings.TESTWERT_B = "hallo"

        with self.assertRaises(FronzenConfigurationError) as e:
            settings.update(TESTWERT_B="hallo")

        self.assertEqual(settings.TESTWERT_A, "foobar")
        self.assertEqual(settings.TESTWERT_B, "testb")
        self.assertEqual(settings.TESTWERT_C, "testc")
