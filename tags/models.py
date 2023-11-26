from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return TaggedItem.objects \
            .select_related('tag') \
            .filter(
                content_type=content_type,
                object_id=obj_id
            )

class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.label

class TaggedItem(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    #we want to make the tags app independent of the store app so we dont want to import the Product model from
    #the store app. So we define a generic relationship. And that requires three components:
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #this field is assumed to be the id of the object we are linking in this model. Only issue is that
    #if the id of the model isnt an integer, then we may have an issue
    object_id = models.PositiveSmallIntegerField()
    #using this field, we can read the actual object that this particular tag is applied to. So it 
    #could be a product, or blog post. Whatever it is.
    content_object = GenericForeignKey()
