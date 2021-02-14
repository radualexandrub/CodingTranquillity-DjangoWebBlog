from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import BlogPost

class BlogPostSitemap(Sitemap):
	changefreq = "weekly"

	def items(self):
		return BlogPost.objects.all()

class StaticViewSitemap(Sitemap):
	changefreq = 'monthly'

	def items(self):
		return ['index', 'about', 'contact']

	def location(self, item):
	    return reverse(item)
