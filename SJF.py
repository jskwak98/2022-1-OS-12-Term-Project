from asyncore import poll3
from collections import deque
from sys import ps1
from scheduler import Scheduler
from utils import Schedule
from process import Process
import heapq

class SJF(Scheduler):

    def __init__(self, process_list: list[Process]):
        super().__init__(process_list)
        self.pq = []
        self.process_list = deque(sorted(process_list, key=lambda x: x.arrival_time))
        self.process_dict = {}
        for p in process_list:
            self.process_dict[p.process_ID] = p

    def do_schedule(self) -> Schedule:
        while True:
            if self.process_list:
                while self.process_list and self.process_list[0].arrival_time <= self.current_time:
                    p = self.process_list.popleft()
                    heapq.heappush(self.pq, (p.cpu_burst_time, p.arrival_time, p.process_ID))
                if not self.pq:
                    process = self.process_list.popleft()
                    self.schedule.add_schedule("None", self.current_time) #스케쥴러 추가가 먼저일지?
                    self.current_time = process.arrival_time #현재 시간을 다음 프로세스 도착 시간으로 바꿔주는게 먼저일지?
                    continue
            elif not self.pq:
                break

            pid = heapq.heappop(self.pq)[2]
            self.current_time += self.process_dict[pid].cpu_burst_time
            self.schedule.add_schedule(pid, self.current_time)

        return self.schedule