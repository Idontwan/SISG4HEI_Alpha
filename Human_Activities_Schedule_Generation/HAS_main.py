import RePo as RP
import Real_Act as RA
import Origin as Or
import MarkovProcess as MP


def post_process(Durs, Markchains, ReMD2D):
    ACTSEQ = []
    N = len(Markchains)
    for i in range(N-1):
        code = Markchains[i][0]
        if code == len(ReMD2D)-1:
            num, smin = 17, Markchains[i][1]
            ACTSEQ.append([num, smin])
        else:
            smin, emin = Markchains[i][1], Markchains[i+1][1]
            actdur = emin - smin
            nums = ReMD2D[code]
            ThisDurs = [Durs[j] for j in nums]
            sumTD = sum(ThisDurs)
            ws = [TD/sumTD for TD in ThisDurs]
            for j in range(len(nums)):
                ACTSEQ.append([nums[j], smin])
                smin += ws[j]*actdur
    return ACTSEQ


def main(floorplancode, speedpara, sleepdur, is_sleep_noon, GRWdurs, fres, order):
    Durs = RP.sam_bas_dura(speedpara, sleepdur, GRWdurs)
    Oft_Days, Toi_shor_Times, eatT4TL, Twan = RP.sam_fres(fres, order)
    MDurs, Tot_Sle_Dur, MD2D = RA.Mid_dur(Durs, floorplancode, Oft_Days, is_sleep_noon)
    weights = RA.Mid_weight(MDurs, Tot_Sle_Dur, Oft_Days, Toi_shor_Times, eatT4TL, Twan)
    MVs, start_minu = Or.origin_MVs_minu(weights, MDurs, Oft_Days, Tot_Sle_Dur, eatT4TL)
    ReMD2D, Redurs, Reweights = RA.real_act_dur(MDurs, weights, MD2D)
    start_node = 1 if ReMD2D[0] == [0] else 0
    Markchains = MP.Markchain(start_minu, start_node, MVs, ReMD2D, Reweights, Redurs)
    Actseq = post_process(Durs, Markchains, ReMD2D)
    return Actseq


def actseq_gen(Savedlist, speedpara, sleepdur, is_sleep_noon, GRWdurs, fres, order):
    Actseqs = []
    for path in Savedlist:
        [stj, fpc, houspara] = path.split('/')
        ActSeq = main(fpc, speedpara, sleepdur, is_sleep_noon, GRWdurs, fres, order)
        Actseqs.append(ActSeq)
    return Actseqs