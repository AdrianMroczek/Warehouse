class ApiEndpoints:
    def __init__(self, request):
        self.request = request

### Admin API endpoints ###
    def api_seed(self):
        return "http://127.0.0.1:8000/api/seed"

    def api_reset(self):
        return "http://127.0.0.1:8000/api/reset"

### Employee API endpoints ###
    def api_get_products(self):
        return "http://127.0.0.1:8000/api/products"

    def api_get_categories(self):
        return "http://127.0.0.1:8000/api/categories"