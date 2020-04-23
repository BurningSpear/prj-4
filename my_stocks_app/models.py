from django.db import models

class Stock(models.Model):
	stockItem = models.CharField(max_length=40)

	def __str__(self):
		return self.stockItem

