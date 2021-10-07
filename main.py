from win10toast import ToastNotifier
from apscheduler.schedulers.background import BackgroundScheduler
import todoist











if __name__=="__main__":
	n=ToastNotifier()
	scheduler=BackgroundScheduler(job_defaults={'misfire_grace_time':2*60})

	tasks=[]
	todoist.sync(scheduler,tasks)

	scheduler.add_job(todoist.sync,'interval',seconds=30,args=[scheduler,tasks])
	scheduler.start()
	while True:
		pass
