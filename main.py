from multiprocessing import Process
import traceback
from random import shuffle
from moviepy.editor import*
import os

class WorkDivider:
    def __init__(self, Dir, time) -> None:
        pass

class MontageVideo:
    def __init__(self, Dir=None):
        self.time = 6
        self.Dir = "F:/vid/Short/War Thunder/" if Dir is None else Dir
    def _run(self):
        WorkDivider(self, self.Dir, self.time)
    def run(self):
        Process.run(target=self._run)