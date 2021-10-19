# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# 게임룰
#  승 : 동전 앞면/ 패 : 동전 뒷면
#  Terminate : s < 1 or s > 99
#  action = [1, 2, 3, ..., min(s, 100 - s)]
#  gamma = 1
#  R = 0 until Terminate/ 1 승리
#  v(s) : 이길 확률
#  p = 0.4 : 동전 앞면 나올 확률
#  value iteration을 사용할 것
'''
/*******************************************************************************
* Copyright juhyeong lee
*******************************************************************************/
'''

states = [0] * 99
for i in range(1,100):
  states[i-1] = i
# print(states)

# +
# state에 따른 actions 생성. (단, 함수 사용전에 a = []으로 초기화 매번 해줘야함.)
def CreateAction(s,a):
  for i in range(1,min(s, 100-s) + 1):
    a.append(i)

# CreateAction함수 테스트
'''
a = []
s = 51
CreateAction(s,a)
print(a)
'''

# s, a에 따른 s'생성
def CreateSprime(s,a,s_prime):
  s_prime.append(s + a)
  s_prime.append(s - a)

'''
s_primes = []
CreateSprime(21, 21, s_primes)
print(s_primes)
'''


# R 정의
def Reward(s_prime):
  if(s_prime == 100):
    return 1
  else:
    return 0



# P 정의
def P(s,a,s_prime):
  if(s_prime == s + a):
    return 0.4
  else:
    return 0.6


# 최고값 원소의 순서 출력 함수 정의
def MaxList(q):
  maxList = 0
  maxVal = 0
  size = len(q)
  for i in range(0,size):
    if(q[i] > maxVal):
      maxList = i
      maxVal = q[i]
  return maxList
'''
q = [9, 2, 3, 5, 2, 11]
MaxList(q)
'''

# +
# value iteration(1)

# 0~100 states에 대한 state-value, OptimalPolicy 초기화
v = [0] * 101
optPolicy = [0] * 101
for _ in range(100):
  for s in states:
    #print('s = ', s)
    # 가능한 action 생성
    actions = []
    CreateAction(s, actions)
    #print('actions = ', actions)
    
    # q(s,a)를 a마다 만들고 이를 배열로 저장하기 위한 q 초기화
    q = []
    
    # 가능한 s' 생성 후 s에 대한 value Iteration진행
    for a in actions:
      s_primes = []
      CreateSprime(s, a, s_primes)
      q.append(sum(P(s, a, s_prime)*(Reward(s_prime) + v[s_prime]) for s_prime in s_primes))
      #print('q = ', q)
    v[s] = max(q)
    optPolicy[s] = MaxList(q) + 1
  
    # 문제점 : 마지막 a에 대한 s'만이 저장된다.
    # 해결책 : q-value를 따로 만들어서 배열에 a에 따른 q값을 저장하고 각 s에서 max(q배열)을 구한다.

print(v)
print(optPolicy)  

# +
# 그래프그리기
import matplotlib.pyplot as plt
'''plt.plot(v)
plt.plot(optPolicy)
'''
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

x = range(0, 101)
y1 = v
y2 = optPolicy
ax1.plot(x, y1)
ax2.bar(x, y2)

plt.show()
