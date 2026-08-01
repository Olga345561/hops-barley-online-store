import json
from django.test import TestCase, Client


class GraphQLTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.graphql_url = "/graphql/"

    def test_query_orders_and_products_analytics(self):
        query = """
            {
                ordersCount
                totalRevenue
                averageOrderValue
                repeatCustomersCount
                allProducts {
                    id
                    name
                    price
                    stock
                }
                allUsers {
                    id
                    email
                    ordersCount
                    isRepeatCustomer
                }
            }
        """

        response = self.client.post(
            self.graphql_url,
            data=json.dumps({"query": query}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertNotIn("errors", content)

        data = content.get("data", {})

        self.assertIn("ordersCount", data)
        self.assertIn("totalRevenue", data)
        self.assertIn("averageOrderValue", data)
        self.assertIn("repeatCustomersCount", data)
        self.assertIn("allProducts", data)
        self.assertIn("allUsers", data)