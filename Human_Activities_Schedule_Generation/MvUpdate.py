import numpy as np


import Tools as Tl


Norm_IntVal = 10000.
eat_toil_lag = 2.5*60


def eat_hungry(absminu, hun_v):
    w = 0.95 + np.random.rand() / 10
    if Tl.is_lundin(absminu): hun_v = max(hun_v-w*Norm_IntVal, 0)
    else: hun_v = max(hun_v-2*w*Norm_IntVal/3, 0)
    return hun_v


def goout_eat_toilL_value(abs_minu, goout_dur, hun_v, eat_dur, eat_w, tolL_v, tolL_w, tolL_dur,
                          toL_lag=False, remain_minu=-1., pass_times=[5, 10]): #[20, 30]
    # calculate how hungary and toilet_long value change during go out
    pass_time = pass_times[0] + (pass_times[1]-pass_times[0])*np.random.rand()
    w = 0.95 + np.random.rand()/10

    if toL_lag:
        if remain_minu > goout_dur:
            hun_v += goout_dur * eat_w * w
            remain_minu -= goout_dur
            return hun_v, tolL_v, toL_lag, remain_minu
        else:
            tolL_v += tolL_w
            toL_lag = False

    if tolL_v >= Norm_IntVal:
        tolL_v -= Norm_IntVal
        if tolL_v < tolL_w and goout_dur-pass_time < tolL_dur+remain_minu:
            tolL_v += Norm_IntVal

    goout_dur -= pass_time
    abs_minu += pass_time/2
    hun_v += pass_time/2*eat_w*w
    eat_times = 0
    wait_time = max((Norm_IntVal-hun_v)/eat_w/w, 0)
    while goout_dur >= eat_dur+wait_time:
        eat_times += 1
        hun_v = daytimeinc(hun_v, wait_time, eat_w)
        goout_dur -= wait_time+eat_dur
        hun_v = eat_hungry(abs_minu+wait_time, hun_v)
        abs_minu += wait_time+eat_dur
        w = 0.95 + np.random.rand()/10
        wait_time = max((Norm_IntVal-hun_v)/eat_w/w, 0)
    hun_v = daytimeinc(hun_v, goout_dur+pass_time/2, eat_w)

    if eat_times > 0:
        tolL_v += tolL_w * (eat_times-1)
        if goout_dur + pass_time/2 < eat_toil_lag:
            toL_lag = True
            remain_minu = eat_toil_lag - goout_dur - pass_time/2
        else:
            tolL_v += tolL_w
            toL_lag = False

    if tolL_v >= Norm_IntVal:
        tolL_v -= Norm_IntVal
        if tolL_v < tolL_w and goout_dur < eat_toil_lag+tolL_dur:
            if toL_lag == False: tolL_v += Norm_IntVal

    if toL_lag == False: remain_minu = -1
    return hun_v, tolL_v, toL_lag, remain_minu


def goout_toilS_val(toils_v, goout_dur, toils_dur, toils_w):
    w = 0.95 + np.random.rand()/10
    wait_time = max((Norm_IntVal-toils_v)/toils_w/w, 0)
    while goout_dur >= wait_time+toils_dur:
        goout_dur -= wait_time+toils_dur
        toils_v = daytimeinc(toils_v, wait_time, toils_w)
        toils_v = norm_decrese(toils_v, toils_dur, toils_dur)
        w = 0.95 + np.random.rand()/10
        wait_time = max((Norm_IntVal-toils_v)/toils_w/w, 0)
    toils_v = daytimeinc(toils_v, goout_dur, toils_w)
    return toils_v


def lag(moti_val, add_val, durtime, remaintime):
    # for washing and toilet(long) value
    # after bath/eat serval hours, corresponding value increase
    remaintime -= durtime
    if remaintime<=0: moti_val += add_val
    return moti_val, remaintime


def norm_decrese(MV, dur, real_dur):
    MV -= real_dur/dur*Norm_IntVal*(0.95+np.random.rand()/10)
    return MV


def daytimeinc(Mv, redur, act_w):
    Mv += redur*act_w*(0.95+np.random.rand()/10)
    return Mv


def sleeptimeinc(Mv, redur, act_w):
    Mv += redur*act_w*(0.95+np.random.rand()/10)/10
    return Mv