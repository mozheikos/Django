from django.db import migrations


def forward(apps, schema_editor):
    category_model = apps.get_model("mainapp", "Category")
    product_model = apps.get_model("mainapp", "Product")
    contact_model = apps.get_model("mainapp", "Contact")

    category_object = category_model.objects.create(pk=1, title="все продукты", description="все наши продукты")

    del category_object

    category_object = category_model.objects.create(
        pk=2, title="дом", description="отличная мебель для домашнего интерьера."
    )

    product_model.objects.create(
        pk=1,
        category=category_object,
        name="комфорт 1",
        image="products_images/product-1.jpg",
        short_desc="комфортный стул",
        description="подойдет для просмотра фильмов",
        price="2989.50",
        count=17,
    )

    product_model.objects.create(
        pk=2,
        category=category_object,
        name="комфорт 2",
        image="products_images/product-2.jpg",
        short_desc="очень комфортный стул",
        description="подойдет для общения с друзьями",
        price="3687.2",
        count=21,
    )

    product_model.objects.create(
        pk=3,
        category=category_object,
        name="люкс",
        image="products_images/product-3.jpg",
        short_desc="использованы премиальные материалы",
        description="для тех, кто стремится к лучшему",
        price="8157.99",
        count=7,
    )

    del category_object

    category_object = category_model.objects.create(
        pk=3, title="офис", description="стильная и надежная офисная мебель нового поколения."
    )

    product_model.objects.create(
        pk=4,
        category=category_object,
        name="стандарт",
        image="products_images/product-4.jpg",
        short_desc="универсальное решение",
        description="подойдет для любого офиса",
        price="1895.25",
        count=27,
    )

    product_model.objects.create(
        pk=5,
        category=category_object,
        name="премиум",
        image="products_images/product-5.jpg",
        short_desc="улучшенный дизайн",
        description="идеально впишется в строгий интерьер офиса",
        price="3587.41",
        count=9,
    )

    del category_object

    category_object = category_model.objects.create(
        pk=4, title="модерн", description="мебель в стиле МОДЕРН подойдет для любого интерьера."
    )

    product_model.objects.create(
        pk=6,
        category=category_object,
        name="новинка",
        image="products_images/product-6.jpg",
        short_desc="инновационный дизайн",
        description="нестандартное решение для современного интерьера",
        price="5361.47",
        count=18,
    )

    product_model.objects.create(
        pk=7,
        category=category_object,
        name="прогресс",
        image="products_images/product-7.jpg",
        short_desc="прогрессивный дизайн",
        description="функциональное и комфортное решение",
        price="6789.33",
        count=12,
    )

    del category_object

    category_object = category_model.objects.create(
        pk=5, title="классика", description="классический стиль актуален в любые времена."
    )

    product_model.objects.create(
        pk=8,
        category=category_object,
        name="венеция",
        image="products_images/product-8.jpg",
        short_desc="классические формы",
        description="окунитесь в европейский комфорт",
        price="4147.51",
        count=25,
    )

    product_model.objects.create(
        pk=9,
        category=category_object,
        name="тоскана",
        image="products_images/product-9.jpg",
        short_desc="эргономичная спинка",
        description="почувствуйте комфорт и насладитесь цветовой гаммой",
        price="7147.35",
        count=18,
    )

    product_model.objects.create(
        pk=10,
        category=category_object,
        name="рим",
        image="products_images/product-10.jpg",
        short_desc="удачные пропорции",
        description="компактность и функциональность",
        price="8357.77",
        count=8,
    )

    contact_model.objects.create(
        pk=1,
        city="Москва",
        phone="955-95-95",
        mail="moscow_mail@yandex.ru",
        address="ул. 3-я Строителей, 25, оф. 12",
    )

    contact_model.objects.create(
        pk=2,
        city="Ленинград",
        phone="955-95-95",
        mail="leningrad_mail@yandex.ru",
        address="ул. 3-я Строителей, 25, оф. 12",
    )

    contact_model.objects.create(
        pk=3,
        city="Белгород",
        phone="55-95-95",
        mail="belgorod_mail@yandex.ru",
        address="ул. 3-я Строителей, 25, оф. 12",
    )


def reverse(apps, schema_editor):
    category_model = apps.get_model("mainapp", "Category")
    contact_model = apps.get_model("mainapp", "Contact")

    category_model.objects.all().delete()
    contact_model.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [("mainapp", "0003_contact")]

    operations = [migrations.RunPython(forward, reverse)]
