from unittest import mock

from django.test import TestCase, override_settings

from model_bakery import baker

from sales.tasks import automatic_approve, process


class AutomaticApproveTest(TestCase):
    @override_settings(VIP_RESELLERS=["35551565432"])
    @mock.patch("sales.models.Sale.automatic_approve")
    def test_automatic_approve(self, m_automatic_approve):
        reseller = baker.make_recipe("users.user", cpf="355.515.654-32")
        sale = baker.make_recipe("sales.sale", reseller=reseller)
        automatic_approve(sale_id=sale.id)

        self.assertEqual(m_automatic_approve.call_count, 2)


class ProcessTest(TestCase):
    @mock.patch("sales.models.Sale.process")
    def test_process(self, m_process):
        sale = baker.make_recipe("sales.sale", value=2000)
        process(sale_id=sale.id)
        sale.refresh_from_db()
        
        self.assertEqual(m_process.call_count, 2)

