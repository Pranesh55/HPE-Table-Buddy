import random

subs = ["maths","social","science","language","english"]
extra = ["art","PT","music"]

timetable = [[[0 for i in range(6)] for j in range(5)] for k in range(3)]

def main():
    for m in range(3):
        for i in range(5):
            dup = [0]*6
            for j in range(6):
                while True:
                    sub = random.choice(subs+extra)
                    if(m==0 or sub!=timetable[m-1][i][j]):
                        if sub in subs:
                            sub_ind = subs.index(sub)
                            if not(any(ele>=2 for ele in dup) and dup[sub_ind]>=1):
                                timetable[m][i][j] = sub
                                dup[sub_ind]+=1
                                break
                        else:
                            if not (any(period in extra for period in timetable[m][i]) or any(sub in row for row in timetable[m])):
                                timetable[m][i][j] = sub
                                break
    return timetable


def check(t):
    for row in t:
        if len(set(row))<=len(row)-2:
            raise RuntimeError
    print("done")


for _ in range(1):
    a=main()
    # b=main2()
    print("II - A")
    print(*a[0],sep="\n")
    print("=================================================\n=================================================")
    print("II - B")
    print(*a[1],sep="\n")
    print("=================================================\n=================================================")

    print("II - C")
    print(*a[2],sep="\n")
    # print("=================================================\n=================================================")

    # print("II -D")
    # print(*a[3],sep="\n")
    # print(*b,sep="\n")
    # check(a)