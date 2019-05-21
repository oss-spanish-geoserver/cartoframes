import unittest
from cartoframes import vis
from .utils import build_geojson


class TestMap(unittest.TestCase):
    def test_is_defined(self):
        """vis.Map"""
        self.assertNotEqual(vis.Map, None)


class TestMapInitialization(unittest.TestCase):
    def test_size(self):
        """vis.Map should set the size by default"""
        map = vis.Map()
        self.assertIsNone(map.size)

    def test__init(self):
        """vis.Map should return a valid template"""
        map = vis.Map()
        self.assertIsNotNone(map._htmlMap)


class TestMapLayer(unittest.TestCase):
    def test_one_layer(self):
        """vis.Map layer should be able to initialize one layer"""
        source = vis.Source(build_geojson([-10, 0], [-10, 0]))
        layer = vis.Layer(source)
        map = vis.Map(layer)

        self.assertEqual(map.layers, [layer])
        self.assertEqual(len(map.sources), 1)
        self.assertEqual(map.sources[0].get('interactivity'), [])
        self.assertIsNotNone(map.sources[0].get('credentials'))
        self.assertIsNone(map.sources[0].get('legend'))
        self.assertIsNotNone(map.sources[0].get('query'))
        self.assertEqual(map.sources[0].get('type'), 'GeoJSON')
        self.assertIsNotNone(map.sources[0].get('viz'))

    def test_two_layers(self):
        """vis.Map layer should be able to initialize two layers in the correct order"""
        source_1 = vis.Source(build_geojson([-10, 0], [-10, 0]))
        source_2 = vis.Source(build_geojson([0, 10], [10, 0]))
        layer_1 = vis.Layer(source_1)
        layer_2 = vis.Layer(source_2)
        map = vis.Map([
            layer_1,
            layer_2
        ])

        self.assertEqual(map.layers, [
            layer_2,
            layer_1
        ])
        self.assertEqual(len(map.sources), 2)

    def test_interactive_layer(self):
        """vis.Map layer should indicate if the layer has interactivity configured"""
        source_1 = vis.Source(build_geojson([-10, 0], [-10, 0]))
        layer = vis.Layer(
            source_1,
            popup={
                'click': ['$pop'],
                'hover': [{
                    'label': 'Pop',
                    'value': '$pop'
                }]
            }
        )

        map = vis.Map(layer)
        self.assertEqual(map.sources[0].get('interactivity'), [{
            'event': 'click',
            'attrs': [{
                'name': 'v559339',
                'label': '$pop'
            }]
        }, {
            'event': 'hover',
            'attrs': [{
                'name': 'v559339',
                'label': 'Pop'
            }]
        }])

    def test_default_interactive_layer(self):
        """vis.Map layer should get the default event if the interactivity is set to []"""
        source_1 = vis.Source(build_geojson([-10, 0], [-10, 0]))
        layer = vis.Layer(
            source_1,
            popup={}
        )

        map = vis.Map(layer)
        self.assertEqual(map.sources[0].get('interactivity'), [])


class TestMapDevelopmentPath(unittest.TestCase):
    def test_default_carto_vl_path(self):
        """vis.Map dev path should use default paths if none are given"""
        map = vis.Map()
        template = map._htmlMap.html
        self.assertTrue(vis.defaults.CARTO_VL_PATH in template)

    def test_custom_carto_vl_path(self):
        """vis.Map dev path should use custom paths"""
        _carto_vl_path = 'custom_carto_vl_path'
        map = vis.Map(_carto_vl_path=_carto_vl_path)
        template = map._htmlMap.html
        self.assertTrue(_carto_vl_path in template)

    def test_default_airship_path(self):
        """vis.Map dev path should use default paths if none are given"""
        map = vis.Map()
        template = map._htmlMap.html
        self.assertTrue(vis.defaults.AIRSHIP_COMPONENTS_PATH in template)
        self.assertTrue(vis.defaults.AIRSHIP_BRIDGE_PATH in template)
        self.assertTrue(vis.defaults.AIRSHIP_STYLES_PATH in template)
        self.assertTrue(vis.defaults.AIRSHIP_ICONS_PATH in template)

    def test_custom_airship_path(self):
        """vis.Map dev path should use custom paths"""
        _airship_path = 'custom_airship_path'
        map = vis.Map(_airship_path=_airship_path)
        template = map._htmlMap.html
        self.assertTrue(_airship_path + vis.defaults.AIRSHIP_SCRIPT in template)
        self.assertTrue(_airship_path + vis.defaults.AIRSHIP_BRIDGE_SCRIPT in template)
        self.assertTrue(_airship_path + vis.defaults.AIRSHIP_STYLE in template)
        self.assertTrue(_airship_path + vis.defaults.AIRSHIP_ICONS_STYLE in template)
