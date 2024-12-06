# coding: utf-8
import os
from datetime import datetime
import time
from .nlp_logging import *
from logging.handlers import BaseRotatingHandler

log_level = {
    "debug": DEBUG,
    "info": INFO,
    "warning": WARNING,
    "error": ERROR,
    "critical": CRITICAL
}

log_color = {
    "debug": 32,
    "info": 37,
    "warning": 33,
    "error": 31,
    "critical": 35
}


def get_current_time():
    return datetime.now().strftime('%Y-%m-%d')


class MyFormatter(Formatter):
    """
    重写format类
    1、重置默认的时间格式
    2、把包路径改到3层路径
    Attribute:
        default_time_format: 除了毫秒的时间格式
        default_msec_format: 毫秒的时间格式，这里时区写死+0800
        with_color: 是否带上颜色，输出系统的format可以带颜色，输出到文件的不能带颜色
    """

    def __init__(self, with_color=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_time_format = "%Y-%m-%d %H:%M:%S"
        # self.default_msec_format = "%s.%03d"
        self.default_msec_format = "%s"
        self.with_color = with_color
        if with_color:
            self.color_template = "\033[1;%dm%s\033[0m"

    @staticmethod
    def get_3_path(record):
        """
        仅保留三层路径
        """
        pathname = record.pathname
        dir_list = []
        if pathname:
            file_name = os.path.basename(pathname)
            dir_list.append(file_name)
            base_path = pathname
            while len(dir_list) < 3:
                base_path = os.path.dirname(base_path)
                base_name = os.path.basename(base_path)
                if base_name:
                    dir_list.append(base_name)
                else:
                    break
        dir_list = dir_list[::-1]
        new_path = "/".join(dir_list)
        record.pathname = new_path

    @staticmethod
    def only_filename(record):
        pathname = record.pathname
        if pathname:
            file_name = os.path.basename(pathname)
            record.pathname = file_name

    def format(self, record):
        self.only_filename(record)
        level = record.levelname.lower()
        source_msg = record.msg  # 有两个handle，分别是控制台和文件，共用record，如果修改了record的msg不改回去，msg会重复拼接
        if level == "error" and record.error_code:
            record.msg = f"{record.error_code} | {record.msg}"
        else:
            record.msg = f" {record.msg}"
        result_without_color = super().format(record)
        record.msg = source_msg
        if not self.with_color:  # 不带颜色
            return result_without_color
        else:
            record_log_level = record.levelname.lower()
            result = self.color_template % (log_color[record_log_level], result_without_color)
            return result

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        t = time.strftime(self.default_time_format, ct)
        # t = self.default_msec_format % (t, record.msecs)
        return t


class MyHandler(BaseRotatingHandler):
    """
    重写的日志流转类
    需要重写：
        shouldRollover: 什么时候流转日志。在日期跨一天和原文件大小到达上限的时候。
        doRollover: 如何流转日志。
    Attribute:
        log_module: 同Logger类中的MODULE
        log_type: 同Logger类中的TYPE
        max_bytes: 最大日志大小，Byte
        backup_count: 每天最大日志数量
        dateNow: 当前的时间，{YYYY-mm-dd}
        stream: 文件流
        baseFilename: 当前日志流向的位置
    """

    def __init__(self, name=None, max_bytes=None, backup_count=100, date_now=None, *args,
                 **kwargs):
        super(MyHandler, self).__init__(*args, **kwargs)
        self.name = name
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.dateNow = date_now
        self.dir_name = os.path.dirname(self.baseFilename)

    def shouldRollover(self, record):
        """
        判断是否需要流转文件
        """
        if self.stream is None:
            self.stream = self._open()
        if self.max_bytes > 0:
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) >= self.max_bytes:
                return 1
        if get_current_time() != self.dateNow:
            return 1
        return 0

    def doRollover(self):
        """
        只要进来了，就必须流转日志
        再进行一次判断，如果是日期变了，那就不需要再考虑日志顺序了。
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        now_time = get_current_time()
        if self.dateNow != now_time:
            # 新的一天的日志
            self.dateNow = now_time
            # XX-xx.2022-01-25
            new_day_template = os.path.join(self.dir_name, f'{self.name}.{self.dateNow}')
            self.baseFilename = new_day_template + ".0.log"
        else:
            # 文件容量达到预设值，需要新增一个当天的日志文件
            base_file_name = os.path.basename(self.baseFilename)  # XX-xx.2022-01-25.1.log
            template_list = base_file_name.split(".")
            template_ = ".".join(template_list[:-2]) + "."
            template_file_name = template_ + "%d.log"
            now_index = int(template_list[-2])  # 当前日志的下标
            exists_log_file_list = []
            for fn in os.listdir(self.dir_name):  # 遍历日志文件下已有的文件
                if fn.startswith(template_) and fn.endswith(".log"):
                    log_index = int(fn.replace(template_, "").replace(".log", ""))  # 日志的下标
                    exists_log_file_list.append(log_index)
            # 如果当前的日志是99.log满了，需要流转到100.log，那么就要删除0.log保证该天的日志文件只有100个
            assert len(exists_log_file_list) > 0, "当前日志数量一定是大于0的"
            exists_log_file_list.sort()  # 对已有的日志下标进行排序
            max_index = exists_log_file_list[-1]  # 当前已有日志的下标
            assert max_index == now_index, "当前日志下标一定是最大的"
            self.baseFilename = os.path.join(self.dir_name, template_file_name % (now_index + 1))
            exists_log_file_list.append(now_index + 1)
            if len(exists_log_file_list) > self.backup_count:  # 删除，保证日志文件数量<=100
                for i in exists_log_file_list[:len(exists_log_file_list) - self.backup_count]:
                    delete_path = os.path.join(self.dir_name, template_file_name % i)
                    if os.path.exists(delete_path):
                        os.remove(delete_path)
        if not self.delay:
            self.stream = self._open()


class MyLogger:
    """
    日志工具
    日志的具体路径如：dir_name/{name}.{YYYY-MM-DD}.{N}.log
    {N}：日志文件序列号，数字从0开始。比如2020年11月6日vcm组件自身日志输出两个日志文件，则日志文件如下vcm-main.20201126.0.log（大小>=100MB）和vcm-main.2020-11-26.1.log（大小<100MB）
    Args:
        name: 日志文件名
        dir_name: 日志所在的文件夹
    """

    def __init__(self, name=None, dir_name=None, level="info", *, need_level=True, need_pos=True):
        self.name = name
        self.dir_name = dir_name
        self.date_now = get_current_time()  # 当前时间的年月日
        self.max_bytes = 100 * 1024 * 1024  # 最大100M日志
        self.backup_count = 10000000  # 每天最多100个日志文件
        self.logger = getLogger(os.path.realpath(__file__))
        self.logger.setLevel(log_level[level.lower()])
        self.logger.propagate = False
        # self.fmt_str = "%(asctime)s | %(levelname)s | %(pathname)s:%(lineno)d | %(process)d/%(thread)d | %(message)s"
        self.fmt_str = "%(asctime)s"
        if need_level:
            self.fmt_str += " | %(levelname)s"
        if need_pos:
            self.fmt_str += " | %(pathname)s:%(lineno)d"
        self.fmt_str += " |%(message)s"
        # 用于输出系统
        self.sh = StreamHandler()
        self.sh.setLevel(log_level[level.lower()])
        self.sh.setFormatter(MyFormatter(fmt=self.fmt_str, with_color=True))
        self.logger.addHandler(self.sh)
        if dir_name:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            log_file_now_path = self.build_log()
            # 用于输出文件
            self.handler = MyHandler(
                name=name,
                max_bytes=self.max_bytes,
                backup_count=self.backup_count,
                date_now=self.date_now,
                filename=log_file_now_path,
                mode="a",
                delay=False,
                encoding="utf-8"
            )
            self.handler.setLevel(log_level[level.lower()])
            self.handler.setFormatter(MyFormatter(fmt=self.fmt_str))
            self.logger.addHandler(self.handler)

    def build_log(self):
        """
        找到最新的日志文件
        """
        exists_log_file_list = []
        template_ = f"{self.name}.{get_current_time()}."
        template_file_name = template_ + "%d.log"
        for fn in os.listdir(self.dir_name):  # 遍历日志文件下已有的文件
            if fn.startswith(template_) and fn.endswith(".log"):
                log_index = int(fn.replace(template_, "").replace(".log", ""))  # 日志的下标
                exists_log_file_list.append(log_index)
        # 根据已有的日志去判读当前的日志序号是多少
        if len(exists_log_file_list) > 0:
            if len(exists_log_file_list) > self.backup_count:  # 如果出了意外导致最大数量超过了100个，那就删了以前的
                exists_log_file_list.sort()
                for i in exists_log_file_list[:len(exists_log_file_list) - self.backup_count]:
                    delete_path = os.path.join(self.dir_name, template_file_name % i)
                    if os.path.exists(delete_path):
                        os.remove(delete_path)
            now_index = max(exists_log_file_list)
            file_path = os.path.join(self.dir_name, template_file_name % now_index)
            if os.path.getsize(file_path) < self.max_bytes:  # 如果最近的文件还没有满，继续往里面写
                return file_path
            else:  # 如果满了，就新建下一个序号
                if len(exists_log_file_list) >= self.backup_count:
                    # 如果超出了每天最大的文件数量(100)，删除当天最早的日志，保证当天的日志总数不大于100
                    min_index = min(exists_log_file_list)
                    os.remove(template_file_name % min_index)
                file_path = os.path.join(self.dir_name, template_file_name % (now_index + 1))
                return file_path
        else:
            file_path = os.path.join(self.dir_name, template_file_name % 0)
            return file_path

    def get_logger(self):
        return self.logger

# logger = MyLogger(name="test", dir_name="./").get_logger()
# for i in range(100):
#     logger.error(i, error_code="500")
