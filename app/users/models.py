from datetime import datetime
from time import sleep

from django.core.cache import cache
from django.db import models


class Account(models.Model):
    balance = models.PositiveIntegerField(default=0)

    def log(self, *args):
        print(datetime.now(), *args)

    def update_balance(self, val):
        # 해당 함수 시작
        self.log('Update Balance:', val)
        # 캐시 키 값 초기화
        key = f'lock:account:{self.id}'
        # ttl 해당 캐시를 얼마나 지속할 지에 대하여
        ttl = 60

        for i in range(5):
            self.log('실행 ')
            lock = cache.get(key)
            if not lock:
                # 캐시가 없다면 반복문을 끝낸다.
                self.log('락이 없다.')
                break
            # 캐시가 있다면 대기
            self.log('Lock Exists and wait')
            # lock 이 존재하므로 대기
            sleep(2)

        else:
            # 브레이크가 걸리지 않았을 경우 표시.
            self.log('lock acquire failed')
            return False

        # value 값이 중요하지는 않고, 키가 존재하는 것이 중요!

        # 반복문이 끝났다면 ( 반복문이 끝난 경우는 캐시가 없는 경우 )
        cache.set(key, True, ttl)
        self.log('Lock Acquired')

        self.log('start logic')
        # 지금부터 해당 시간동안 락이 걸려 접근하는 동작에 대해서 접근을 막는다.

        # 어떤 로직이 돌아가는 시간.
        sleep(9)

        self.log('Finish logic:', val)
        cache.delete(key)
        self.log('Lock Released')


class Car(models.Model):
    name = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    description = models.TextField(default=' ')
    type = models.IntegerField(choices=[
        (1, "Sedan"),
        (2, "Truck"),
        (4, "SUV"),
    ])
