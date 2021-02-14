from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    # content = models.TextField()
    content = RichTextField(blank=True, null=True, config_name='special')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='blog_images',
                              storage=gd_storage, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='blogpost_like')

    def __str__(self):
        ''' Show BlogPost title and author when querying the database using Django's ORM, eg: BlogPost.objects.all()
        Will also be the default description when viewing list in Admin page
        '''
        return self.author.username + ', ' + self.title[:40]

    def get_absolute_url(self):
        return reverse('blogpost-detail', kwargs={'pk': self.pk})

    @property
    def number_of_comments(self):
        return BlogComment.objects.filter(blogpost_connected=self).count()

    def number_of_likes(self):
        return self.likes.count()

class BlogComment(models.Model):
    blogpost_connected = models.ForeignKey(
        BlogPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.author) + ', ' + self.blogpost_connected.title[:40]

# BEGIN;
# -- Create model BlogPost
# CREATE TABLE "MainApp_blogpost"(
#   "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
#   "title" varchar(100) NOT NULL,
#   "subtitle" varchar(200) NOT NULL,
#   "content" text NOT NULL, "date_posted" datetime NOT NULL,
#   "image" varchar(100) NOT NULL,
#   "author_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
# CREATE INDEX "MainApp_blogpost_author_id_68614009" ON "MainApp_blogpost" ("author_id");
# COMMIT;
