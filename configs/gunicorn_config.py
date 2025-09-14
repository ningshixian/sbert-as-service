# gunicorn -c config/gunicorn_config.py main:app
import multiprocessing

# ip + port
bind = "0.0.0.0:8096"

# worker超时时间，超时重启
timeout = 30

# 并行工作进程数
workers = 1
# workers = multiprocessing.cpu_count() * 2 + 1  # 内存占用大

# 每个进程开启的线程数(此配置只适用于gthread 进程工作方式)
threads = 200

# 监听队列的最大连接数 (建议 64-2048)
backlog = 512

# 工作模式：sync(同步), eventlet(并发), gevent(协程)
worker_class = "uvicorn.workers.UvicornWorker"

# # 设置最大并发量(客户端最大同时连接数)
# worker_connections = 2000

# # 在keep-alive连接上等待请求的秒数
# keep_alive = 5

# 设置守护进程,False将进程交给supervisor管理,True是后台运行
daemon = False

# 设置日志记录水平
loglevel = 'info'

# # 设置进程文件目录
# pidfile = 'logs/gunicorn.pid'
# # 设置访问日志和错误信息日志路径
# accesslog = 'logs/gun-access.log'
# errorlog = 'logs/gun-error.log'

# reload=true 自动重启