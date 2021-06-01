from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user_id=models.OneToOneField(User, on_delete=models.CASCADE)
    job = models.CharField(max_length=200, default="Сотрудник")
    patronymic = models.CharField(max_length=200, default="Ивановна")
    signature_image = models.ImageField(upload_to='sign_image/%Y/%m/%d', blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user_id=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return '{0} {1} {2} ({3})'.format(self.user_id.last_name,self.user_id.first_name,self.patronymic, self.job)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


# class Countries(models.Model):
#     country = models.CharField(max_length=200, default="Россия")
#
#
# class UnitsOfMeasurement(models.Model):
#     unit_of_measurement = models.CharField(max_length=10, default="кг")
#
#
# class Products(models.Model):
#     name = models.CharField(max_length=200, default="ПPOBOЛOKA.AЛ CПЛ AK5.CBAPOЧHAЯ.D1")
#     country = models.ForeignKey(Countries, on_delete=models.CASCADE)
#     unit_price = models.FloatField(default=0)
#     unit_of_measurement = models.ForeignKey(UnitsOfMeasurement, on_delete=models.CASCADE)

class Company(models.Model):
    title = models.CharField(max_length=200, default='ООО "Наименование"')
    phone = models.CharField(max_length=50, default='+7(999) 999-99-99')
    name = models.CharField(max_length=200, default='Иванов И.И.')
    inn = models.CharField(max_length=12, default='999999999999')
    ogrn = models.CharField(max_length=15, default='999999999999999')
    address = models.CharField(max_length=200, default='999999, Челябинская обл, г.Челябинск, ул.Ленина, дом № 9, квартира 9')
    mail_address = models.CharField(max_length=200, default='999999, Челябинская обл, г.Челябинск, ул.Ленина, дом № 9, квартира 9')
    email = models.CharField(max_length=100, default='email@mail.com')
    created_data = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')

    def __str__(self):
        return '{0} ({1})'.format(self.title, self.created_data)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['-created_data']


class ContractTemplate(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='buyer')
    supplier = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='supplier')
    json_file = models.FileField(upload_to='json/', blank=True)
    created_data = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        return '{0} - {1} ({2})'.format(self.buyer.title, self.supplier.title, self.created_data)

    class Meta:
        verbose_name = 'Шаблон договора'
        verbose_name_plural = 'Шаблоны договоров'
        ordering = ['-created_data']

