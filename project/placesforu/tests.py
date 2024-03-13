from django.test import TestCase

# Create your tests here.

# Test google vision api
class TestVisionAPI(TestCase):
    def test_get_landmark(self):
        from .APIs import get_landmark
        # Test with a known image
        image_path = "./placesforu/test_resources/test.png"
        result = get_landmark(image_path)
        self.assertAlmostEqual(result["latitude"], 51.506835599999995, delta=0.0001)
        self.assertAlmostEqual(result["longitude"], -0.0105343, delta=0.0001)
        self.assertEqual(result["landmark"], "Traffic Light Tree")
