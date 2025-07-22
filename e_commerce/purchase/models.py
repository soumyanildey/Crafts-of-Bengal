from django.db import models
from login.models import User
# Create your models here.
class Purchase(models.Model):
    order_id=models.CharField(max_length=1200,primary_key=True)
    quantity=models.PositiveIntegerField()
    actual_price=models.DecimalField(max_digits=10,decimal_places=2)
    discount=models.DecimalField(max_digits=10,decimal_places=2)
    user_id=models.CharField(max_length=150)

    @property
    def sell_price(self):
        return (self.actual_price*self.discount/100)*self.quantity
    

    
