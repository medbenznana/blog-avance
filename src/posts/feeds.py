from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from .models import Post

class ArchiveFeed(Feed):
	title = 'BENZNANA Blog Feed'
	description = 'BENZNANA Blog Feed'
	link = '/feed/archive/'

	def items(self):
		return Post.objects.all().order_by("-id")[:25]

	def item_link(self, item):
		return item.get_absolute_url()

	def item_title(self, item):
		return item.title

	def item_description(self, item):
		return item.content


class AtomSiteNewsFeed(ArchiveFeed):
    feed_type = Atom1Feed
    subtitle = ArchiveFeed.description