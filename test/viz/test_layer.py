import unittest
from cartoframes.viz import Layer, Source, Style, Popup, Legend


class TestLayer(unittest.TestCase):
    def test_is_layer_defined(self):
        """Layer"""
        self.assertNotEqual(Layer, None)

    def test_initialization_objects(self):
        """Layer should initialize layer attributes"""
        layer = Layer(Source('layer_source'))

        self.assertFalse(layer.is_basemap)
        self.assertEqual(layer.orig_query, 'SELECT * FROM "public"."layer_source"')
        self.assertTrue(isinstance(layer.source, Source))
        self.assertTrue(isinstance(layer.style, Style))
        self.assertTrue(isinstance(layer.popup, Popup))
        self.assertTrue(isinstance(layer.legend, Legend))
        self.assertEqual(layer.interactivity, [])

    def test_initialization_simple(self):
        """Layer should initialize layer attributes"""
        layer = Layer('layer_source', '')

        self.assertFalse(layer.is_basemap)
        self.assertEqual(layer.orig_query, 'SELECT * FROM "public"."layer_source"')
        self.assertTrue(isinstance(layer.source, Source))
        self.assertTrue(isinstance(layer.style, Style))
        self.assertTrue(isinstance(layer.popup, Popup))
        self.assertTrue(isinstance(layer.legend, Legend))
        self.assertEqual(layer.interactivity, [])


class TestLayerStyle(unittest.TestCase):
    def test_style_dict(self):
        """Layer style should set the style when it is a dict"""
        layer = Layer(
            'layer_source',
            {
                'vars': {
                    'grad': '[red, green, blue]'
                },
                'color': 'blue',
                'width': 10,
                'strokeColor': 'black',
                'strokeWidth': 1
            }
        )

        self.assertTrue(isinstance(layer.style, Style))
        self.assertTrue('@grad: [red, green, blue]' in layer.viz)
        self.assertTrue('color: blue' in layer.viz)
        self.assertTrue('width: 10' in layer.viz)
        self.assertTrue('strokeColor: black' in layer.viz)
        self.assertTrue('strokeWidth: 1' in layer.viz)

    def test_style_str(self):
        """Layer style should set the style when it is a dict"""
        layer = Layer(
            'layer_source',
            """
                @grad: [red, green, blue]
                color: blue
                width: 10
                strokeColor: black
                strokeWidth: 1
            """
        )

        self.assertTrue(isinstance(layer.style, Style))
        self.assertTrue('@grad: [red, green, blue]' in layer.viz)
        self.assertTrue('color: blue' in layer.viz)
        self.assertTrue('width: 10' in layer.viz)
        self.assertTrue('strokeColor: black' in layer.viz)
        self.assertTrue('strokeWidth: 1' in layer.viz)

    def test_style_dict_valid_properties(self):
        """Layer style should set only the valid properties"""
        with self.assertRaises(ValueError):
            Layer(
                'layer_source',
                {
                    'invalid': 1
                }
            )
