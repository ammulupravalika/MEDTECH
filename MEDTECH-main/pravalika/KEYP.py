import pyautogui as pt
import time

limit = int(input())

message=input()
i=0
while i<=limit:
    pt.typewrite(message)
    pt.press("enter")
    i+=1
