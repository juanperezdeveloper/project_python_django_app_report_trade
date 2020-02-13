from django.forms import ModelForm

from django_mlds.flatblocks.models import FlatBlock

class FlatBlockForm(ModelForm):
    class Meta:
        model = FlatBlock
        exclude = ('slug', )
