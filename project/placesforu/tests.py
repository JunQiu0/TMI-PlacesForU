from django.test import TestCase

# Create your tests here.

# Test google vision api
class TestVisionAPI(TestCase):
    def test_get_landmark_path(self):
        from .APIs import get_landmark
        # Test with a known image
        image_path = "./placesforu/test_resources/test.png"
        result = get_landmark(image_path)
        self.assertAlmostEqual(result["latitude"], 51.506835599999995, delta=0.0001)
        self.assertAlmostEqual(result["longitude"], -0.0105343, delta=0.0001)
        self.assertEqual(result["landmark"], "Traffic Light Tree")
        self.assertGreaterEqual(float(result["score"]), 0.48)

    def test_get_landmark_link(self):
        from .APIs import get_landmark
        # Test with a known image
        image_path = "https://media-cdn.tripadvisor.com/media/photo-s/1b/4b/59/86/caption.jpg"
        result = get_landmark(image_path, link=True)
        self.assertAlmostEqual(result["latitude"], 48.858052, delta=0.0001)
        self.assertAlmostEqual(result["longitude"], 2.2948624, delta=0.0001)
        self.assertEqual(result["landmark"], "Bureau De Gustave Eiffel")
