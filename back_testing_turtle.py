import sqlite3

from matplotlib import pyplot as plt

conn = sqlite3.connect('24_10_18.db')
cur = conn.cursor()
data = []
symbols = []
symbols2 = ['CRUDEOIL18NOVFUT']

ts = 0
pt = 20
sl = 50
bw = 10
dir = 10
s = 0
trd = 0
tp=0
# symbols2=['TATAMOTORS','IOC','SBIN','YESBANK','BANKNIFTY18NOVFUT','CRUDEOIL18NOVFUT','GOLDM18NOVFUT','USDINR18NOVFUT','NIFTY18NOVFUT']

symbols = symbols2

val = {}

for j in range(len(symbols)):
    cur.execute("select last_price from " + symbols[j])  # +" where rowid<500")
    data = cur.fetchall()
    val.update({symbols[j]: {'ltp': [], 'ltp_diff': [], 'ltp_dir': []}})
    p_diff = data[0][0]

    for i in range(len(data)):

        val[symbols[j]]['ltp'].append(data[i][0])
        val[symbols[j]]['ltp_diff'].append(data[i][0] - p_diff)
        p_diff = data[i][0]

        if val[symbols[j]]['ltp_diff'][i] != 0:
            s = s + (abs(val[symbols[j]]['ltp_diff'][i]) / val[symbols[j]]['ltp_diff'][i])
            val[symbols[j]]['ltp_dir'].append(s)
        elif val[symbols[j]]['ltp_diff'][i] == 0:
            val[symbols[j]]['ltp_dir'].append(s)

# print(val,s)
tp=val[symbols[0]]['ltp'][100]
print(tp)

for i in val:

    profit = 0
    k = 0
    t = 0
    tr = {'buy': [], 'buy_cl': [], 'buy_sl': [], 'sell': [], 'sell_cl': [], 'sell_sl': []}

    ts = 0
    tpb = dir
    tps = -dir
    # print(val[i]['ltp'][0],tpb,tps)

    for j in (range(len(val[i]['ltp']))):
        if trd==0:

            ##########################BUY##############################
            if val[i]['ltp'][j] >= tp+10 and ts == 0:
                t = val[i]['ltp'][j]
                ts = 1
                k = k + 1
                tr['buy'].append(t)

            elif val[i]['ltp'][j] <= tp-10 and ts == 1:
                profit = profit + (val[i]['ltp'][j]-t)
                ts = 0
                k = k + 1
                tr['buy_sl'].append(val[i]['ltp'][j])

            ##########################SELL##############################
            if val[i]['ltp'][j] <= tp-10 and ts == 0:
                t = val[i]['ltp'][j]
                ts = -1
                k = k + 1
                tr['sell'].append(t)
            elif val[i]['ltp'][j] >= tp+10 and ts == -1:
                profit = profit + (t - val[i]['ltp'][j])
                ts = 0
                k = k + 1
                tr['sell_sl'].append(val[i]['ltp'][j])

    print(profit)
    if ts ==1 : profit = profit + (val[i]['ltp'][j]-t)
    elif ts==-1:profit = profit + (t-val[i]['ltp'][j])
    print(tr, k, ts, profit,t,val[i]['ltp'][j])
# print(val)
#"""""
for j in range(len(symbols)):

    plt.subplot(211)
    plt.plot(val[symbols[j]]['ltp_dir'])
    plt.title(symbols[j])

    plt.subplot(212)
    plt.plot(val[symbols[j]]['ltp'])
    plt.title(symbols[j])

    plt.show()

#"""""
