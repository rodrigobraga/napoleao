from unittest import mock

from django.test import TestCase

from sales.tasks import automatic_approve, process


class AutomaticApproveTest(TestCase):
    @mock.patch("sales.models.Sale.objects.get")
    @mock.patch("sales.models.Sale.automatic_approve")
    def test_automatic_approve(self, m_automatic_approve, m_get):
        sale = mock.Mock(id=1)

        automatic_approve(sale_id=sale.id)

        sale.assert_called_once


class ProcessTest(TestCase):
    @mock.patch("sales.models.Sale.objects.get")
    @mock.patch("sales.models.Sale.process")
    def test_process(self, m_process, m_get):
        sale = mock.Mock(id=1)

        m_get.return_value = sale

        process(sale_id=sale.id)

        sale.process.assert_called_once()

