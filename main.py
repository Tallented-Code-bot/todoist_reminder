from win10toast import ToastNotifier
from apscheduler.schedulers.background import BackgroundScheduler
import todoist











if __name__=="__main__":
	n=ToastNotifier()
	scheduler=BackgroundScheduler()

	tasks=[]
	todoist.sync(scheduler,tasks)

	scheduler.add_job(todoist.sync,'interval',seconds=30,args=[scheduler,tasks])
	scheduler.start()
	while True:
		pass
