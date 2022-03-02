import random

subs = ["maths","social","science","language","english"]
extra = ["art","PT","music"]

def main():
    timetable = [[0 for i in range(6)] for j in range(5)]
    for i in range(5):
        dup = [0]*6
        for j in range(6):
            while True:
                sub = random.choice(subs+extra)
                if sub in subs:
                    sub_ind = subs.index(sub)
                    if not(any(ele>=2 for ele in dup) and dup[sub_ind]>=1):
                        timetable[i][j] = sub
                        dup[sub_ind]+=1
                        break
                    

                else:
                    if not (any(period in extra for period in timetable[i]) or any(sub in row for row in timetable)):
                        timetable[i][j] = sub
                        break
    return timetable

def check(t):
    for row in t:
        if len(set(row))<=len(row)-2:
            raise RuntimeError
    print("done")


for _ in range(1):
    a=main()
    print(*a,sep="\n")
    # check(a)