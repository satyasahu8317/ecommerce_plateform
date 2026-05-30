# pyrefly: ignore [missing-import]
from django.db import models

class Category(models.Model):
    parent = models.ForeignKey(
        'self',
        related_name='children',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    name = models.CharField(max_length=225, db_index=True)
    slug = models.SlugField(max_length=225, unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        unique_together = ('slug', 'parent')
    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return '>'.join(full_path[::-1])



