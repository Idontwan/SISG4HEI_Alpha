import os


D_H, H_M = 24, 60
D_M = D_H*H_M


def creat_floder(path):
    if not os.path.exists(path): os.makedirs(path)


def in_range(sensor_xy, xy, range=60):
    [x0, y0], [x1, y1] = sensor_xy, xy
    if (x1-x0)*(x1-x0)+(y1-y0)*(y1-y0) < range*range:
        return True
    return False


def update_PIRlog(sensors, PIRlog, PIRstatu, path, arrive_time, step_time=0.8/60):
    # sensors represent the coordinates of all sensors
    M, N = len(PIRstatu), len(path)
    time = arrive_time - (N-1)*step_time
    for i in range(N-1):
        [x0, y0, _], [x1, y1, _] = path[i], path[i+1]
        dx, dy = x1-x0, y1-y0
        for k in range(8):
            time += step_time/8
            x, y = x0+k*dx/8, y0+k*dy/8
            for j in range(M):
                P_t = in_range(sensors[j], [x, y])
                if P_t != PIRstatu[j]:
                    PIRlog[2*j + P_t].append(time)
                    PIRstatu[j] = P_t


def PIRrecords(sensors, TPs, times, endids, locations):
    PIRstatu = [False for sensor in sensors]
    PIRlog = [[] for i in range(2*len(sensors))]
    for i in range(len(endids)):
        e_id = endids[i]
        if locations[e_id] !='Wander':
            update_PIRlog(sensors, PIRlog, PIRstatu, TPs[i], times[e_id])
        else: update_PIRlog(sensors, PIRlog, PIRstatu, TPs[i], times[e_id+1])
    return PIRlog


def gen_subtxt(absminu, i):
    day, left_minu = int(absminu//D_M), absminu%D_M
    PorA = 'AM' if left_minu<D_M//2 else 'PM'
    hour, minu = int(left_minu//H_M), int(left_minu%H_M)
    if PorA == 'PM': hour -= int(D_H//2)
    second = round(60*((left_minu%H_M)-minu), 2)
    ID, on_off = i//2, i%2
    txt1 = str(day)+'d '+PorA+' '+str(hour)+'h '+str(minu)+'m '+str(second)+'s'
    txt2 = 'Sensor #' + str(ID)
    txt3 = 'Turn On' if on_off else 'Turn Off'
    txt_l = ['\n', txt1, txt2, txt3]
    return '   '.join(txt_l)


def save_records(path, PIRlog, sensors):
    timeline = []
    for i in range(len(PIRlog)):
        for time in PIRlog[i]:
            timeline.append((time, i))
    timeline = sorted(timeline, key=lambda x: x[0])
    Txt = ''
    for i in range(len(sensors)):
        Txt += 'Sensor #' + str(i) + ' : [' + str(sensors[i][0]) + ', ' + str(sensors[i][1]) + ']  '
    for (time, i) in timeline:
        subtxt = gen_subtxt(time, i)
        Txt += subtxt
    creat_floder(path+'/PIR')
    filename = path + '/PIR/Record.txt'
    with open(filename, "w") as f:
        f.write(Txt)