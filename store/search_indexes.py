from haystack import indexes
from .models import Product


class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
        template_name="search/text.txt"
    )
    product_name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().objects.all()