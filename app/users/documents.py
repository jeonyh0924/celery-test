from django.contrib.auth import get_user_model
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Car

User = get_user_model()

@registry.register_document
class CarDocument(Document):
    class Index:
        name = 'cars'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Car

        fields = [
            'name',
            'color',
            'description',
            'type',
        ]


@registry.register_document
class UserDocument(Document):
    class Index:
        name = 'users'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = User

        fields = [
            'name',
            'color',
            'description',
            'type',
        ]
