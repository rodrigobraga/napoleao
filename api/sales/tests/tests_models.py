import decimal

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
    
    def test_process_on_change(self):
        """Ensure that when a sale is created, cashback are calculated"""
        reseller = baker.make_recipe("users.user")
        baker.make_recipe("sales.sale", reseller=reseller, _quantity=3)

        total = sum(reseller.sales.values_list("cashback", flat=True))

        self.assertEqual(total, decimal.Decimal(420))
    
    def test_process_on_delete(self):
        """Ensure that when a sale is removed, cashback are calculated"""
        reseller = baker.make_recipe("users.user")
        sale = baker.make_recipe("sales.sale", reseller=reseller)
        baker.make_recipe("sales.sale", reseller=reseller, _quantity=2)

        sale.delete()

        total = sum(reseller.sales.values_list("cashback", flat=True))

        self.assertEqual(total, decimal.Decimal(210))
    
    def test_process_on_delete_last_sale(self):
        """Ensure that when the last sale is removed the flow is interrupted"""
        reseller = baker.make_recipe("users.user")
        sale = baker.make_recipe("sales.sale", reseller=reseller)
        sale.delete()

        total = sum(reseller.sales.values_list("cashback", flat=True))

        self.assertEqual(total, decimal.Decimal(0))