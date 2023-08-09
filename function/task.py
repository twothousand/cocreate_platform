# myapp/tasks.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.utils import timezone
from team.models import Team

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

try:
    @scheduler.scheduled_job(CronTrigger(hour=0, minute=1, second=0))  # 每天凌晨1分触发任务
    def update_team_deadlines():
        today = timezone.now().date()
        teams_to_update = Team.objects.filter(recruitment_end_date__lt=today, is_recruitment_open=True)
        for team in teams_to_update:
            team.is_recruitment_open = False
            team.save()
except Exception as e:
    print(e)
    # 遇到错误，停止定时器
    scheduler.shutdown()

register_events(scheduler)
# 启动定时任务
scheduler.start()
