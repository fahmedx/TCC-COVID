#!/usr/bin/env python
# coding: utf-8

# In[32]:


import pandas as pd
import numpy as np
import sys
import math 
import seaborn as sea
import datetime as dt
from datetime import timedelta
from operator import itemgetter
from functools import partial


# In[38]:


def aver(input):
    medias = input.groupby(['cod_location'])['total_cases'].mean()
    return medias


# In[39]:


def diff(input):
    difference = input.groupby('cod_location')['total_cases'].apply(lambda x: x.tail(1).values[0] - x.head(1).values[0])
    return difference


# In[40]:


def range(init, end, step=1):
    start = float(init)
    stop = float(end)
    step = float(step)
    
    result = [start]
    curr = start
    while curr < stop:
        curr += step
        result.append(curr)
    return result


# In[41]:


#Funções de mebramento
def up(a, b, x):
    a = float(a)
    b = float(b)
    x = float(x)
    if x < a:
        return 0
    if x < b:
        return (x - a) / (b - a)
    return 1.0


# In[42]:


def down(a, b, x):
    return 1. - up(a, b, x)


# In[43]:


def tri(a, b, x):
    a = float(a)
    b = float(b)
    m = (a + b) / 2.
    first = (x - a) / (m - a)
    second = (b - x) / (b - m)
    return max(min(first, second), 0.)


# In[44]:


def trap(a, b, c, d, x):
    first = (x - a) / (b - a)
    second = (d - x) / (d - c)
    return max(min(first, 1., second), 0.)


# In[45]:


def edge(p, valor):
    if not p:
        return 0.0
    return math.pow(valor,p)
muito = partial(edge,2.)
extremamente = partial(edge,3.)
pouco = partial(edge,0.5)
levemente = partial(edge, 1. /3.)


# In[46]:


def fuzzyficacao(dominio,tipo):
    domin_sz = float(len(dominio))
    delta = lambda x: x if (x < 0.5) else (1.0 - x)
    result = (2. / domin_sz) 
    return result


# In[47]:


def aprox(fuzzy, n, dominio):
    hw = fuzzy * (max(dominio) - min(dominio))
    return  partial(tri, n - hw, n + hw)


# In[48]:


########################USAR PARA TESTES, DEPOIS SUBSTITUIR PELOS DADOS DO DATASET#############################################
companies = [
    ('a', 500, 7), ('b', 600, -9), ('c', 800, 17),
    ('d', 850, 12), ('e', 900, -11), ('f', 1000, 15),
    ('g', 1100, 14), ('h', 1200, 1), ('i', 1300, -2),
    ('j', 1400, -6), ('k', 1500, 12)
]
profit = itemgetter(2)
sales = itemgetter(1)

percentages = map(float, range(-10, 30, 1))
profitable = partial(up, 0., 15.)
high = partial(up, 600., 1150.)

fand = min

def filtro(predicado, itens):
    snd = itemgetter(1)
    return filtro(
        lambda x: snd(x) != 0.0,
        map(predicado, itens)
    )

def p1(company):
    value = profitable(profitable(profit(company)))
    return (company, fand(value,1))

def p2(company):
    a = profitable(profit(company))
    b = high(sales(company))
    return (company,fand(a,b))

def p3(company):
    a = somewhat(profitable(profit(company)))
    b = very(high(sales(company)))
    return (company,fand(a,b))

# exemplo 
sizes = range(4,13,0.5)

short = partial(down, 1.5, 1.625)
medium = partial(tri, 1.525, 1.775)
tall = partial(tri, 1.675, 1.925)
very_tall = partial(up, 1.825, 1.95)

def small(size):
    return down(4., 6., size)


#average = partial(tri, 5., 9.)
def average(size):
    return tri(5., 9., size)


#big = partial(tri, 8., 12.)
def big(size):
    return tri(8., 12., size)


#very_big = partial(up, 11., 13.)
def very_big(size):
    return up(11., 13., size)

#fl.near(20, fl.range(0, 40, 1))(17.5)
near = partial(aprox, 0.125)
around = partial(aprox, 0.25)
roughly = partial(aprox, 0.375)


rules = [
    (short, small),
    (medium, average),
    (tall, big),
    (very_tall, very_big)
]
################################################################################################################################


# In[49]:


def func_att(val,func, sz):
    prim = func(sz)
    return (val * prim)


# In[50]:


def regra_base(altura):
    atualizado = []
    for funcao_input, output in rules:
        val = funcao_input(altura)
        updated.append(partial(func_att,val,output))
    funcao_regrabase = lambda s: sum([r(s) for r in atualizado])
    return funcao_regrabasegrabase


# In[51]:


def centroide(dominio, funcao_pertinencia):
    fdom = map(funcao_pertinencia,dominio)
    prim = sum([a * b for (a,b) in zip(domain, fdom)])
    ult = sum(fdom)
    return prim / ult


# In[52]:


## 
def exemplo_sapato(h):
    result = centroide(sz,regra_base(h))
    return result
##


# In[53]:


def exemplo_centroide():
    dominio = map(float, range(0,10))
    funcao_pertinencia = partial(trap, 2, 3, 6, 9)
    return centroid(dominio, funcao_perinencia)


# In[54]:


def mand(func, val):
    return min([func(val) for func in funcs])


# In[55]:


def exemplo_preco(cost= 13.25, comp_price=29.99):
    preco = range(15.,35.,0.5)
    high = partial(up,15.,35.)
    low = lambda p: 1- very(high(v))
    preco1 = centroide(preco,partial(mand, [high, low]))
    preco2 = centroide(preco,partial(mand, [high, low, around(2.0 * man_costs, prices)]),)
    preco3 = centroide(
        preco,
        partial(
            mand, [
                high, low, around(2.0 * man_costs, prices),
                lambda p: not_very(comp_price) * around(comp_price,prices)(p)
            ]
        )
    )
    return preco1, preco2, preco3
    #print preco1,preco2,preco3


# In[57]:


if __name__ == 'main':
    height = float(sys.argv[1])
    size = exemplo_sapato(height)
    print('For Height of %.2f the shoe size is %.2f' % height,size)
    exemplo_preco()


# In[ ]:




