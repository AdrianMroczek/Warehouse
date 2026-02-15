from playwright.sync_api import expect
from tests.pages.api_enpoints import ApiEndpoints

def test_api_seed(page):
    api = ApiEndpoints(page.request)
    # Seed the database
    responses = page.request.post(api.api_seed())
    expect(responses).to_be_ok()

def test_check_seeded_categories(page):
    api = ApiEndpoints(page.request)

    expected_categories = [
  {
    "id": 1,
    "name": "Monitory"
  },
  {
    "id": 2,
    "name": "Laptopy"
  },
  {
    "id": 3,
    "name": "Myszy"
  }
]
    # Check if the seeded data is present
    response = page.request.get(api.api_get_categories())
    expect(response).to_be_ok()

    actual_categories = response.json()

    assert actual_categories == expected_categories

def test_check_seeded_products(page):
    api = ApiEndpoints(page.request)

    expected_products = [
  {
    "id": 1,
    "name": "Lenovo Legion 27Q-10",
    "price": 799.99,
    "quantity": 20,
    "category_id": 1,
    "category": {
      "id": 1,
      "name": "Monitory"
    }
  },
  {
    "id": 2,
    "name": "Samsung Odyssey G5",
    "price": 1799.99,
    "quantity": 15,
    "category_id": 1,
    "category": {
      "id": 1,
      "name": "Monitory"
    }
  },
  {
    "id": 3,
    "name": "Logitech Lift",
    "price": 249.99,
    "quantity": 150,
    "category_id": 3,
    "category": {
      "id": 3,
      "name": "Myszy"
    }
  },
  {
    "id": 4,
    "name": "ASUS ROG Strix G16",
    "price": 4999.99,
    "quantity": 7,
    "category_id": 2,
    "category": {
      "id": 2,
      "name": "Laptopy"
    }
  }
]

    # Check if the seeded data is present
    response = page.request.get(api.api_get_products())
    expect(response).to_be_ok()

    actual_products = response.json()

    assert actual_products == expected_products
