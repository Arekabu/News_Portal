from django.core.management.base import BaseCommand, CommandError
from posts.models import Post, Category


class Command(BaseCommand):
    help = 'Удаляет все статьи выбранной категории.'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write(
            f'Вы правда хотите удалить все статьи категории {options['category']} ? yes/no'
        )
        answer = input()

        if answer == 'yes':
            try:
                category = Category.objects.get(name = options['category'])
                Post.objects.filter(category=category).delete()
                self.stdout.write(self.style.SUCCESS(
                    f'Статьи категории {options['category']} удалены!'))
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Категория {options['category']} не найдена.'))
            return
        else:
            self.stdout.write(self.style.ERROR('Отменено'))