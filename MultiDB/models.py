from django.db import models
from django.core.validators import ValidationError
# Create your models here.

class MultiDBProxyModel(models.Model):
    """Simulates a OneToOne-type relationship, potentially accross databases.
    
    Attributes::
        _linked_model = The other side of the OneToOne relationship
    
        linked_model = Gets the instance of _linked_model associated with this object.
    """
    class Meta:
        abstract = True
    
    _linked_model = None
    
    _linked_id = models.IntegerField(unique=True,
         help_text="The ID# of the {} that this class is linked to.".format(_linked_model))
    
    # The following property attempts to make the fuckery of foreign keys
    # invisible to the view-writer.
    @property
    def linked_model(self):
        return self.__class__._linked_model.objects.get(pk=self._linked_id)
    @linked_model.setter
    def linked_model(self, value):
        if isinstance(value, self.__class__._linked_model):
            self._linked_id = value.id
        else:
            raise ValidationError("{} is not an instance of {}.".format(value, 
                                                                        self.__class__._linked_model))
    