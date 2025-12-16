from django.apps import AppConfig


class ProductsStoreConfig(AppConfig):
    name = 'products_store'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import products_store.signals
