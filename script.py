import random
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import Schoolkid, Chastisement, Lesson, Subject, Commendation


def get_schoolkid(fullname):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=fullname)
        return schoolkid
    except ObjectDoesNotExist:
        print('Введенное имя не найдено')
    except MultipleObjectsReturned:
        print('С таким именем найдено много детей, добавьте фамилию или отчество')


def fix_marks(kid_name):
    schoolkid = get_schoolkid(kid_name)
    for bad_point in schoolkid.mark_set.filter(points__in=['2', '3']):
        bad_point.points = '5'
        bad_point.save()


def remove_chastisements(kid_name):
    schoolkid = get_schoolkid(kid_name)
    schoolkid_chastisement = Chastisement.objects.filter(schoolkid=schoolkid.pk)
    schoolkid_chastisement.delete()


def create_commendation(kid_name, subject_title):
    schoolkid = Schoolkid.objects.get(full_name__contains=kid_name)
    subject = Subject.objects.get(title=subject_title, year_of_study=schoolkid.year_of_study)
    schoolkid_lessons = Lesson.objects.filter(subject=subject.pk)
    compliment = ['Молодец!',
                  'Отлично!',
                  'Хорошо!',
                  'Гораздо лучше, чем я ожидал !',
                  'Ты меня приятно удивил!',
                  'Великолепно!',
                  'Прекрасно!',
                  'Ты меня очень обрадовал!',
                  'Именно этого я давно ждал от тебя!',
                  'Сказано здорово – просто и ясно!',
                  'Ты, как всегда, точен!',
                  'Очень хороший ответ!',
                  'Талантливо!',
                  'Ты сегодня прыгнул выше головы!',
                  'Я поражен!',
                  'Уже существенно лучше!',
                  'Потрясающе!',
                  'Замечательно!',
                  'Прекрасное начало!',
                  'Так держать!',
                  'Ты на верном пути!'
                  ]
    lesson_commendation = random.choice(schoolkid_lessons)
    Commendation.objects.create(text=random.choice(compliment), created=lesson_commendation.date,
                                schoolkid_id=schoolkid.pk, subject_id=subject.pk,
                                teacher_id=lesson_commendation.teacher.pk)
