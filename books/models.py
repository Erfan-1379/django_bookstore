from django.db import models
from django.urls import reverse
import os
from django.dispatch.dispatcher import receiver
from django.contrib.auth import get_user_model


class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    book_cover = models.ImageField(upload_to='book-covers/', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', args=[self.id])

    def delete(self, *args, **kwargs):
        self.book_cover.delete()
        super().delete(*args, **kwargs)


@receiver(models.signals.pre_save, sender=Book)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if instance.pk is not None:
        old_instance = Book.objects.get(pk=instance.pk)
        if old_instance.book_cover:    # چک کردن وجود عکس قبلی
            if instance.book_cover != old_instance.book_cover:    # چک کردن تغییر در عکس
                if os.path.isfile(old_instance.book_cover.path):   # چک کردن وجود فایل عکس قبلی
                    os.remove(old_instance.book_cover.path)    # حذف فایل عکس قبلی


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.text}'

