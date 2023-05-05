from django.urls import reverse
from django.db import models
from django.template.defaultfilters import slugify
from .views import *
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

class Menu(models.Model):

    name = models.CharField(max_length=255, verbose_name = 'Имя:')

    menu_name = models.CharField(max_length=255, verbose_name = 'Меню:')

    parent = models.ForeignKey('self', 
                               on_delete=models.CASCADE, 
                               null=True, blank=True, 
                               related_name='children',
                               verbose_name = 'Подпункт для:')

    slug = models.SlugField(null=True, blank=True, unique=True, verbose_name = 'URL')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('myurl', args=[self.slug])

@receiver(pre_save, sender=Menu)
def create_slug(sender, instance, **kwargs):

    if instance.parent:
        #если меню родителя изменилось, то меняется и меню его детей
        instance.menu_name = instance.parent.menu_name
        instance.slug = instance.parent.slug + slugify(instance.name) +'/'
    else:
        #проверка на существование меню
        #если меню существует, то в нём есть начальный элемент
        #если начальный элемент просто изменился, то проблем нет, а если произошла
        #попытка задать второй начльный элемент, то возникает исключение
        menu=Menu.objects.select_related('parent').filter(menu_name=instance.menu_name)
        if menu:
            for element in menu:
                if element.parent is None:
                    if element.pk != instance.pk:
                        raise Exception('Нельзя задать два начальных элемента для одного меню')
                    else:
                        break
                     
        instance.slug = slugify(instance.name)+'/'

#при изменении имени модели меняется и слаг, а значит, его нужно поменять у всех детей тоже, чтобы url работали
#так же срабатывает при изменении меню модели.
@receiver(post_save, sender=Menu)
def rewrite_children(sender, instance, **kwargs):
    children = Menu.objects.prefetch_related('children').get(pk=instance.pk).children.all()
    for child in children:
        child.save()
