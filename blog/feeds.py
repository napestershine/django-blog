from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.utils.feedgenerator import Atom1Feed

from .models import Post


class LatestPostFeed(Feed):
    title = 'My Blog'
    link = ''
    description = 'Latest posts of my blog.'

    def items(self):
        return Post.objects.filter(status=1)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)


class AtomSiteNewsFeed(LatestPostFeed):
    feed_type = Atom1Feed
    subtitle = LatestPostFeed.description
