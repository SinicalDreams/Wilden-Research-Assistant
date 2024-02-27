def get_level(xp):
    totals = [0,300,900,2700,6500,14000,23000,34000,48000,64000,85000,100000,120000,140000,165000,195000,225000,265000,305000,355000,355000]
    for lvl in range(len(totals)):
        if (totals[lvl] > xp):
            break
    return lvl