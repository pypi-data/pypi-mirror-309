import django
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

class InventoryOptimizer:
    """A library for optimizing inventory based on weekly sales average."""
    
    def __init__(self, min_stock_threshold=10):
        self.min_stock_threshold = min_stock_threshold
        self.period = 7

    def calculate_weekly_average(self, product_id, inventory_model, start_date=None, end_date=None):
        """
        Calculate 7-day average usage for a product
        
        Args:
            product_id: ID of the product to analyze
            inventory_model: Django model class for inventory
            start_date: Optional start date for analysis
            end_date: Optional end date for analysis
            
        Returns:
            float: Daily average sales
        """
        end_date = end_date or timezone.now()
        start_date = start_date or (end_date - timedelta(days=self.period))

        sales = inventory_model.objects.filter(
            product_id=product_id,
            status="REMOVE",
            created_at__range=(start_date, end_date)
        ).aggregate(total_usage=Sum('quantity'))['total_usage'] or 0

        return abs(sales) / self.period

    def generate_recommendations(self, product_id, product_model, inventory_model, notification_model):
        """
        Generate reorder recommendations based on 7-day average
        
        Args:
            product_id: ID of the product to analyze
            product_model: Django model class for products
            inventory_model: Django model class for inventory
            notification_model: Django model class for notifications
            
        Returns:
            dict: Recommendations including reorder estimate and current status
        """
        product = product_model.objects.get(id=product_id)
        daily_average = self.calculate_weekly_average(product_id, inventory_model)
        
        reorder_point = daily_average * 3
        
        if product.stock_quantity <= reorder_point:
            notification_model.objects.create(
                product_name=product,
                type="STOCK_ISSUE",
                notes=f"Stock Alert: Current stock ({product.stock_quantity}) is below stock level threshold ({reorder_point}). "
                      f"Recommended order: {daily_average * 7} units (7-day supply)"
            )

        return {
            'product_id': product_id,
            'current_stock': product.stock_quantity,
            'daily_average_usage': daily_average,
            'reorder_point': reorder_point,
            'recommended_order': daily_average * 7,
            'needs_reorder': product.stock_quantity <= reorder_point
        }