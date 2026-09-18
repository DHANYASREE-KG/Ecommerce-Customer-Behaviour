import pandas as pd
from django.test import TestCase
from matplotlib import pyplot as plt

from .analysis.matplotlib_charts import build_category_distribution
from .models import Customer, Order, RfmSegment
from .views import _prepare_data


class DashboardPerformanceTests(TestCase):
	def setUp(self):
		champion = Customer.objects.create(
			customer_id="C-CHAMPION",
			customer_name="Champion Customer",
			segment="Consumer",
		)
		other = Customer.objects.create(
			customer_id="C-OTHER",
			customer_name="Other Customer",
			segment="Corporate",
		)
		Order.objects.create(
			order_id="O-CHAMPION",
			customer=champion,
			order_date="2025-01-01",
			ship_date="2025-01-03",
			ship_mode="Standard",
			state="Karnataka",
			region="South",
			category="Technology",
			sub_category="Phones",
			sales=100,
			quantity=1,
			discount=0.1,
			profit=20,
		)
		Order.objects.create(
			order_id="O-OTHER",
			customer=other,
			order_date="2025-01-01",
			ship_date="2025-01-03",
			ship_mode="Standard",
			state="Kerala",
			region="South",
			category="Furniture",
			sub_category="Tables",
			sales=200,
			quantity=1,
			discount=0.1,
			profit=30,
		)
		RfmSegment.objects.create(
			customer=champion,
			recency=1,
			frequency=4,
			monetary=100,
			r_score=4,
			f_score=4,
			m_score=4,
			rfm_score=12,
			segment="Champion",
		)
		RfmSegment.objects.create(
			customer=other,
			recency=20,
			frequency=1,
			monetary=200,
			r_score=1,
			f_score=1,
			m_score=1,
			rfm_score=3,
			segment="Lost",
		)

	def test_segment_filter_is_applied_before_dataframe_creation(self):
		orders, rfm = _prepare_data(segment="Champion")

		self.assertEqual(orders["Order ID"].tolist(), ["O-CHAMPION"])
		self.assertEqual(rfm["Customer ID"].tolist(), ["C-CHAMPION"])

	def test_chart_builder_closes_its_figure(self):
		build_category_distribution(
			pd.DataFrame(
				{
					"Category": ["Technology"],
					"Sales": [100],
					"Month": ["2025-01"],
				}
			)
		)

		self.assertEqual(plt.get_fignums(), [])
