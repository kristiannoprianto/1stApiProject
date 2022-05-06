#q1

total=0
for i in range(1,5):
    if(i%2)==0:
        total+=10
    else:
        total-=5
print("q1 = " + str(total))

#q2
a=2
b=5
c=7
while True:
    if a>2*b:
        break
    a+=c-b
    b-=1
    c+=1
print(c-a)

k=5
while k>0:
    print(k)
    k-=1

ch = ['Z', 'X', 'C']

for i in range(5):
    tmp=ch[0]
    ch[0]=ch[2]
    ch[1]=tmp
    ch[2]=ch[1]
print("q2 = " + str(ch))

#q7

amount = [0,0,0,0,0,0,0,0,0,0]
number = [1,2,3,4,2,9,3]

for i in range(len(number)):
    amount[number[i]]+=1

print(amount[1])