from celery import task


@task
def retrieve():
    from core.models import Entry
    Entry.objects.retrieve()
