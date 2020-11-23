from django.test import TestCase, override_settings

from model_bakery import baker

from sales.models import Sale


class SaleTest(TestCase):

    def setUp(self):
        self.sale = baker.make_recipe("sales.sale", code="123456")

    def test_str(self):
        self.assertEqual(self.sale.code, str(self.sale))
    
    @override_settings(VIP_RESELLERS=["35551565432"])
    def test_automatic_approve(self):
        """
        Ensure that all sales made by VIP resellers are automatically approved
        """
        reseller = baker.make_recipe("users.user", cpf="355.515.654-32")
        sale = baker.make_recipe("sales.sale", reseller=reseller)
        
        sale.refresh_from_db()
        
        self.assertEqual(sale.status, Sale.APPROVED)