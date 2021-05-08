from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Creating model manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status=1)


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_categories')
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_tags')
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS = (
        (0, "Draft"),
        (1, "Publish")
    )

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    published_on = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    image = models.ImageField(upload_to='images/featured/%Y/%m/%d/')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='blog_posts_categories',
        null=True,
        blank=True
    )
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ['-published_on']

    objects = models.Manager()  # The default manager
    published = PublishedManager()  # Our custom manager

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse('blog:post_detail', kwargs={'slug': str(self.slug)})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)
