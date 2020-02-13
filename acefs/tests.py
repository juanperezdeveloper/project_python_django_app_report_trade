from django.test import TestCase
from acefs import *
from models import *
from django.test.client import Client
import random
import hashlib
import time
import base64

from django.conf import settings


class AcefsUnitTests(TestCase):

    fixtures=['july_2011.json',]

    def failUnlessArraysEqual(self, one, two):
        self.failUnlessEqual(len(one), len(two))
        for i in range(len(one)):
            self.failUnlessEqual(one[i], two[i])

    def failUnlessArraysAlmostEqual(self, one, two, places=3):
        self.failUnlessEqual(len(one), len(two))
        for i in range(len(one)):
            self.failUnlessAlmostEqual(one[i], two[i], places)

    def test_all(self):
        """

        These tests are all non-destructive, so we're running them all in one
        method to save on setup/teardown time (nearly 20 sec, due to the large
        amount of supporting data.)

        """
        
        # norminv()

        self.failUnlessAlmostEqual(norminv(0.98, 100, 15), 130.806, 3)

        # smoothedPrMajors()
        self.failUnlessAlmostEqual(smoothedPrMajors(0, 0, 1), 100.0, 1)
        self.failUnlessAlmostEqual(smoothedPrMajors(1, 1, 5), 2.885, 3)

        # smoothedMLBData()
        self.failUnlessAlmostEqual(smoothedMLBData(0, 0, 0, 1), 361404.0, 1)
        self.failUnlessAlmostEqual(smoothedMLBData(1, 1, 5, 4), 308.0, 1)

        # max_bonus()
        self.failUnlessEqual(max_bonus(1), 4000000)
        self.failUnlessEqual(max_bonus(2), 3250000)
        self.failUnlessEqual(max_bonus(8), 1512000)
        self.failUnlessEqual(max_bonus(15), 168300)

        # DraftCell

        c = DraftCell(1)
        self.failUnlessEqual(c.index, 0)
        self.failUnlessEqual(c.cell, 1)
        self.failUnlessAlmostEqual(c.MLBAverage, 4.12, 2)
        self.failUnlessAlmostEqual(c.MiLBAverage, 4.00, 2)
        self.failUnlessEqual(c.lower, 1)
        self.failUnlessEqual(c.upper, 1)
        self.failUnlessEqual(c.draft_point, '1')

        c = DraftCell(13)
        self.failUnlessEqual(c.index, 12)
        self.failUnlessEqual(c.cell, 13)
        self.failUnlessAlmostEqual(c.MLBAverage, 3.745, 3)
        self.failUnlessAlmostEqual(c.MiLBAverage, 5.00, 2)
        self.failUnlessEqual(c.lower, 91)
        self.failUnlessEqual(c.upper, 120)
        self.failUnlessEqual(c.draft_point, '91 - 120')

        c = DraftCell(26)
        self.failUnlessEqual(c.index, 25)
        self.failUnlessEqual(c.cell, 26)
        self.failUnlessAlmostEqual(c.MLBAverage, 4.52, 2)
        self.failUnlessAlmostEqual(c.MiLBAverage, 5.00, 0)
        self.failUnlessEqual(c.lower, 1201)
        self.failUnlessEqual(c.upper, None)
        self.failUnlessEqual(c.draft_point, '1201 +')


        # Status

        s = Status(0)
        self.failUnlessEqual(s.text, 'HS')
        self.failUnlessEqual(s.travel_time, 5.2)

        s = Status(1)
        self.failUnlessEqual(s.text, 'JC')
        self.failUnlessEqual(s.travel_time, 4.9)

        s = Status(2)
        self.failUnlessEqual(s.text, '4YR')
        self.failUnlessEqual(s.travel_time, 4.07)

        # Position

        p = Position(0)
        self.failUnlessEqual(p.text, 'C')

        p = Position(1)
        self.failUnlessEqual(p.text, '1B-DH')

        p = Position(2)
        self.failUnlessEqual(p.text, '2B')

        p = Position(3)
        self.failUnlessEqual(p.text, '3B')

        p = Position(4)
        self.failUnlessEqual(p.text, 'SS')

        p = Position(5)
        self.failUnlessEqual(p.text, 'OF')

        p = Position(6)
        self.failUnlessEqual(p.text, 'LHP')

        p = Position(7)
        self.failUnlessEqual(p.text, 'RHP')

        p = Position(8)
        self.failUnlessEqual(p.text, 'ALL')

        # AcefsModel

        college = College.objects.get(school="Abilene Christian University")
        alt = DOLSalary.objects.get(occupation="[DEFAULT] All Occupations")
        sec = DOLSalary.objects.get(occupation="[DEFAULT] All Occupations")

        m = AcefsModel(college=college.id, alt=alt.id, secondary=sec.id, position=4, status=0)
        self.failUnlessEqual(m.college.school, u'Abilene Christian University') # C5
        self.failUnlessEqual(m.alt.occupation, u'[DEFAULT] All Occupations') # C6
        self.failUnlessEqual(m.secondary.occupation, u'[DEFAULT] All Occupations') #C7
        self.failUnlessEqual(m.risk_tolerance, 0.0) # C8
        self.failUnlessEqual(m.position.text, 'SS') # C12
        self.failUnlessEqual(m.status.text, 'HS') # C13
        self.failUnlessAlmostEqual(m.bonus_threshold, 0.0, 0) # B23
        self.failUnlessEqual(m.max_slotted_bonus, 6500000) # C26
        self.failUnlessEqual(m.play_ball, True) # B29
        self.failUnlessEqual(m.travel_time, 5.2) # C37
        self.failUnlessEqual(m.MLBAverage, 4.12) # C38
        self.failUnlessEqual(m.MiLBAverage, 4) # C39
        self.failUnlessAlmostEqual(m.pr_mlb, 0.607, 3) # C40
        self.failUnlessAlmostEqual(m.career_adj_factor, 0.989, 3) # C43
        self.failUnlessEqual(m.use_adj_factor, False) # C44

        all_positions = [772123.0, 1490909.0, 1830303.0, 2662222.0, 3042666.0, 1380000.0, 2054519.0, 3145834.0, 3109524.0, 2523810.0, 795107.0, 117431.0, 264220.0, 266055.0, 495413.0, 908334.0, 1208334.0, 800000.0, 593867.0, 1529167.0]
        self.failUnlessArraysAlmostEqual(m.all_positions, all_positions) # F

        selected_position = [1133333.0, 887225.0, 833333.0, 1625000.0, 3277777.0, 1266667.0, 3022223.0, 6833334.0, 7333334.0, 5833334.0, 676002.0, 293578.0, 275229.0, 786370.0, 1345566.0, 1816667.0, 2416667.0, 1600000.0, 2476190.0, 4754000.0]
        self.failUnlessArraysAlmostEqual(m.selected_position, selected_position) # G

        mlb_sal_shift = [8064994.0, 0, 0, 0, 0, 0, 2236148.7000000002, 4306250.5999999996, 4488095.5999999996, 3595238.6000000001, 667954.30000000005, 176146.70000000001, 242201.60000000001, 447575.5, 785932.90000000002, 1180833.8, 1570833.8, 1040000.0, 1287409.5, 2666183.5]
        self.failUnlessArraysAlmostEqual(m.mlb_sal_shift, mlb_sal_shift) # H

        school = [True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        self.failUnlessArraysEqual(m.school, school) # I

        pr_minors = [1.0, 1.0, 1.0, 0.47236655274101469, 0.36787944117144233, 0.28650479686019009, 0.22313016014842982, 0.17377394345044514, 0.1353352832366127, 0.10539922456186433, 0.0820849986238988, 0.06392786120670757, 0.049787068367863944, 0.038774207831722009, 0.030197383422318501, 0.023517745856009107, 0.018315638888734179, 0.014264233908999256, 0.011108996538242306, 0.0086516952031206341]
        self.failUnlessArraysAlmostEqual(m.pr_minors, pr_minors) # J

        pr_out = [0, 0, 0, 0, 0, 0, 0.49990242745457292, 0.60767727549880446, 0.69222582030017821, 0.75855350767577179, 0.81058707162332067, 0.85140700496054, 0.88342993076540455, 0.90855167137757853, 0.92825948493687183, 0.94372011409007817, 0.95584885952872467, 0.96536376765165699, 0.97282814037229892, 0.97868388373763726]
        self.failUnlessArraysAlmostEqual(m.pr_out, pr_out) # K

        MiLB_sal = [13200.0, 13596.0, 14003.879999999999, 6813.4134562168065, 5465.4804871436236, 4384.2160977464046, 3516.8638579815338, 2821.1044163480874, 2262.9906784354316, 1815.291479822268, 1456.1629387680848, 1168.0826621019069, 936.99480269520916, 751.62425465505146, 602.92652484383962, 483.64643917339009, 387.96415232467081, 311.21118920311011, 249.64266338752427, 200.25455878626207]
        self.failUnlessArraysAlmostEqual(m.MiLB_sal, MiLB_sal) # L

        # AltStart - spot check
        alt_start_14 = [44384.377732459478, 42256.668862285012, 40109.744381604578, 37937.510091634591, 35733.378548957291, 33490.110080008722, 31199.616764407368, 28852.714294996844, 26438.800040291248, 23945.425278280436, 21357.71288214067, 21357.71288214067, 21357.71288214067, 21357.71288214067, 21357.71288214067, 0.0, 0.0, 0.0, 0.0, 0.0]
        alt_start_19 = [63677.628824785912, 61226.660272152716, 58784.958866163317, 56346.32836780107, 53904.626961811678, 51453.65840917849, 48987.060678327092, 46498.186788394269, 43979.9718927266, 41424.779338953944, 38824.216361207211, 36168.906843073113, 33448.20365537484, 30649.815442311439, 27759.310723198378, 24759.442830608812, 24759.442830608812, 24759.442830608812, 24759.442830608812, 24759.442830608812]
        self.failUnlessArraysAlmostEqual(m.alt_start[14], alt_start_14) # M-AG
        self.failUnlessArraysAlmostEqual(m.alt_start[19], alt_start_19) # M-AG
        
        # SecStart - spot check
        sec_start_13 = [49773.024008791304, 47708.243890123566, 45640.863644450503, 43565.636937347663, 41477.177058397858, 39369.856031593758, 37237.692075389845, 35074.219262292143, 32872.331466088093, 30624.089961016067, 28320.479859146151, 25951.094111478382, 23503.713632579205, 20963.735728010033, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        sec_start_18 = [69838.815595338849, 67367.053198754744, 64924.090566153478, 62502.993173271272, 60097.236653431974, 57700.576332903227, 55306.930272201636, 52910.26995167289, 50504.513431833606, 48083.416038951385, 45640.453406350127, 43168.691009766015, 40660.633067088958, 38108.041630432046, 35501.713540836827, 32831.198072443454, 30084.430603156288, 27247.245864020555, 24302.715329958672, 0.0]
        self.failUnlessArraysAlmostEqual(m.sec_start[13], sec_start_13) # M-AG
        self.failUnlessArraysAlmostEqual(m.sec_start[18], sec_start_18) # M-AG

        # BB30
        e_mlb_wo_min = [8078194.0, 13596.0, 14003.879999999999, 3218.4286267123753, 2010.6379073438186, 1256.0989424760089, 3090144.4293109979, 6278899.5431778664, 6906051.321287212, 5838503.0212807516, 1145857.0758578037, 319909.05532609427, 463571.49258056091, 902692.25270293327, 1671589.8890293429, 2649613.5506760338, 3719140.1549523952, 2598811.9452332985, 3394620.6824726285, 7417852.3692662669]
        self.failUnlessArraysAlmostEqual(m.e_mlb_wo_min, e_mlb_wo_min)

        # BC30
        e_mlb = [8078194.0, 13596.0, 14003.879999999999, 3218.4286267123753, 2010.6379073438186, 16548.96656940809, 3090144.4293109979, 6278899.5431778664, 6906051.321287212, 5838503.0212807516, 1145857.0758578037, 319909.05532609427, 463571.49258056091, 902692.25270293327, 1671589.8890293429, 2649613.5506760338, 3719140.1549523952, 2598811.9452332985, 3394620.6824726285, 7417852.3692662669]
        self.failUnlessArraysAlmostEqual(m.e_mlb, e_mlb)

        # BD30
        e_alt = [0.0, 0.0, 0.0, 0.0, 15892.144191712265, 18352.174596358171, 20871.032895985558, 23459.897072476964, 26129.187854754582, 28888.863145008156, 31748.644019016861, 34718.195936985707, 37807.280970501051, 41025.892099305835, 44384.377732459478, 47893.5628782965, 51564.872440967476, 55410.46174584156, 59443.359487526905, 63677.628824785912]
        self.failUnlessArraysAlmostEqual(m.e_alt, e_alt)

        self.failUnlessAlmostEqual(m.npv_mlb_wo_min, 29838424, 0) # BB
        self.failUnlessAlmostEqual(m.npv_mlb, 29849205, 0) # BC
        self.failUnlessAlmostEqual(m.npv_alt, 270297, 0) # BD




        college = College.objects.get(school="Gardner-Webb University")
        alt = DOLSalary.objects.get(occupation="Elementary school teachers, except special education")
        sec = DOLSalary.objects.get(occupation="Clergy")

        m = AcefsModel(college=college.id, alt=alt.id, secondary=sec.id, position=7, status=1, expected_pick=9)
        self.failUnlessEqual(m.college.school, u'Gardner-Webb University') # C5
        self.failUnlessEqual(m.alt.occupation, u'Elementary school teachers, except special education') # C6
        self.failUnlessEqual(m.secondary.occupation, u'Clergy') #C7
        self.failUnlessEqual(m.risk_tolerance, 0.0) # C8
        self.failUnlessEqual(m.position.text, 'RHP') # C12
        self.failUnlessEqual(m.status.text, 'JC') # C13
        self.failUnlessAlmostEqual(m.bonus_threshold, 58206, 0) # B23
        self.failUnlessEqual(m.max_slotted_bonus, 1000000) # C26
        self.failUnlessEqual(m.play_ball, True) # B29              # not sure this is right, but it's what the spreadsheet says.

        self.failUnlessEqual(m.travel_time, 4.9) # C37
        self.failUnlessEqual(m.MLBAverage, 4.12) # C38
        self.failUnlessEqual(m.MiLBAverage, 4) # C39
        self.failUnlessAlmostEqual(m.pr_mlb, 0.065, 3) # C40
        self.failUnlessAlmostEqual(m.career_adj_factor, 0.804, 3) # C43
        self.failUnlessEqual(m.use_adj_factor, False) # C44


        all_positions = [25843.0, 31662.0, 21157.0, 43011.0, 56944.0, 57174.0, 26726.0, 32983.0, 16485.0, 6095.0, 5215.0, 19573.0, 10933.0, 5560.0, 3799.0, 7878.0, 11829.0, 2688.0, 4959.0, 23333.0]
        self.failUnlessArraysAlmostEqual(m.all_positions, all_positions) # F

        selected_position = [16667.0, 19660.0, 2042.0, 11905.0, 10260.0, 5077.0, 10933.0, 1538.0, 4154.0, 6154.0, 2961.0, 2127.0, 2234.0, 2823.0, 2669.0, 1664.0, 1000.0, 2418.0, 333.0, 14756.0]
        self.failUnlessArraysAlmostEqual(m.selected_position, selected_position) # G

        mlb_sal_shift = [70940.800000000003, 0, 0, 0, 0, 30617.799999999999, 17736.200000000001, 17106.700000000001, 9904.1000000000004, 5509.1000000000004, 3791.9000000000001, 10637.299999999999, 6360.1000000000004, 3909.1999999999998, 2967.1000000000004, 4604.6000000000004, 6314.5, 2311.1999999999998, 2612.6999999999998, 17568.900000000001]
        self.failUnlessArraysAlmostEqual(m.mlb_sal_shift, mlb_sal_shift) # H

        school = [True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        self.failUnlessArraysEqual(m.school, school) # I

        pr_minors = [1.0, 1.0, 1.0, 0.47236655274101469, 0.36787944117144233, 0.28650479686019009, 0.22313016014842982, 0.17377394345044514, 0.1353352832366127, 0.10539922456186433, 0.0820849986238988, 0.06392786120670757, 0.049787068367863944, 0.038774207831722009, 0.030197383422318501, 0.023517745856009107, 0.018315638888734179, 0.014264233908999256, 0.011108996538242306, 0.0086516952031206341]
        self.failUnlessArraysAlmostEqual(m.pr_minors, pr_minors) # J

        pr_out =  [0, 0, 0, 0, 0, 0.71349520313980985, 0.77686983985157021, 0.82622605654955483, 0.8646647167633873, 0.89460077543813565, 0.91791500137610116, 0.93607213879329243, 0.95021293163213605, 0.96122579216827797, 0.96980261657768152, 0.97648225414399092, 0.98168436111126578, 0.98573576609100078, 0.98889100346175773, 0.99134830479687941]
        self.failUnlessArraysAlmostEqual(m.pr_out, pr_out) # K

        MiLB_sal = [13200.0, 13596.0, 14003.879999999999, 6813.4134562168065, 5465.4804871436236, 4384.2160977464046, 3516.8638579815338, 2821.1044163480874, 2262.9906784354316, 1815.291479822268, 1456.1629387680848, 1168.0826621019069, 936.99480269520916, 751.62425465505146, 602.92652484383962, 483.64643917339009, 387.96415232467081, 311.21118920311011, 249.64266338752427, 200.25455878626207]
        self.failUnlessArraysAlmostEqual(m.MiLB_sal, MiLB_sal) # L

        # AltStart - spot check
        alt_start_14 = [58672.090567791347, 57559.395626513739, 56436.651795135011, 55300.672084940365, 54148.011562710963, 52974.884208533986, 51777.060408001147, 50549.737186299812, 49287.369849518174, 47983.448282386096, 46630.192424393652, 46630.192424393652, 46630.192424393652, 46630.192424393652, 46630.192424393652, 0.0, 0.0, 0.0, 0.0, 0.0]
        alt_start_19 = [74409.61389121518, 73127.868842362775, 71850.970089606228, 70575.677281831042, 69298.77852907448, 68017.03348022209, 66727.115082194199, 65425.54726639657, 64108.635439437101, 62772.385979547442, 61412.409851997931, 60023.803774460714, 58600.999782756, 57137.570056981909, 55625.967589285057, 54057.173157219819, 54057.173157219819, 54057.173157219819, 54057.173157219819, 54057.173157219819]
        self.failUnlessArraysAlmostEqual(m.alt_start[14], alt_start_14) # M-AG
        self.failUnlessArraysAlmostEqual(m.alt_start[19], alt_start_19) # M-AG

        # SecStart - spot check
        sec_start_13 = [63808.009819181607, 62339.036166307807, 60868.212670910623, 59391.806864348953, 57905.986408444543, 56406.747318269852, 54889.833896374046, 53350.64600299202, 51784.12803337154, 50184.632035522089, 48545.744429260041, 46860.061190957451, 45118.889136094651, 43311.839277874788, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        sec_start_18 = [82606.638581808002, 80848.120178846511, 79110.091170429863, 77387.618036835265, 75676.059062142347, 73970.971516057078, 72268.028444450712, 70562.940898365458, 68851.381923672539, 67128.908790077941, 65390.879781661308, 63632.361378699803, 61848.020758425577, 60031.997089319484, 58177.742847066009, 56277.822934434822, 54323.654058788561, 52305.158436690464, 50210.292385088687, 0.0]
        self.failUnlessArraysAlmostEqual(m.sec_start[13], sec_start_13) # M-AG
        self.failUnlessArraysAlmostEqual(m.sec_start[18], sec_start_18) # M-AG

        # BB30
        e_mlb_wo_min = [84140.800000000003, 13596.0, 14003.879999999999, 3218.4286267123753, 2010.6379073438186, 41842.830981133666, 26155.019302435554, 26533.487785815123, 16782.385821562832, 10431.212159626839, 7911.0523812210213, 20562.110541175687, 13367.902265932304, 9001.2983851804493, 7330.2090828751398, 11248.465661296232, 15767.527539906583, 6500.9204324228622, 7527.8978606485425, 49435.265131622138]
        self.failUnlessArraysAlmostEqual(m.e_mlb_wo_min, e_mlb_wo_min)

        # BC30
        e_mlb = [84140.800000000003, 13596.0, 14003.879999999999, 3218.4286267123753, 2010.6379073438186, 41842.830981133666, 35216.488857507633, 36272.983523232862, 37361.17302892985, 38482.008219797754, 39636.468466391685, 40825.562520383435, 42050.329395994937, 43311.839277874788, 44611.194456211037, 45949.53028989736, 47328.01619859429, 48747.856684552113, 50210.292385088687, 51716.601156641344]
        self.failUnlessArraysAlmostEqual(m.e_mlb, e_mlb)

        # BD30
        e_alt = [0.0, 0.0, 0.0, 0.0, 34697.242433454667, 36775.317639165754, 38907.904894255887, 41101.562206817835, 43362.472949059498, 45696.600470015335, 48109.806943857635, 50607.948815157266, 53196.957107300412, 55882.908375256062, 58672.090567791347, 61571.067159460516, 64586.742417667941, 67726.430473754561, 70997.930914915327, 74409.61389121518]
        self.failUnlessArraysAlmostEqual(m.e_alt, e_alt)

        self.failUnlessAlmostEqual(m.npv_mlb_wo_min, 244743, 0) # BB
        self.failUnlessAlmostEqual(m.npv_mlb, 410685, 0) # BC
        self.failUnlessAlmostEqual(m.npv_alt, 397950, 0) # BD


class AcefsUITests(TestCase):

    # Ugh, so slow.
    fixtures=['july_2011.json',]

    def _make_cookies(self):
        salt = str(random.randrange(10000,10000000))
        h = hashlib.sha256()
        h.update(salt)
        h.update(settings.SECRET)
        hash =  h.hexdigest()
        return (salt, hash)

    def test_page_responds(self):
        client = Client()
        response = client.get("/")
        self.failUnlessEqual(response.status_code, 200)

    def test_cookie(self):
        client = Client()

        (salt, hash) = self._make_cookies()
        client.cookies['salt'] = salt
        client.cookies['hash'] = hash

        response = client.get("/")

        self.assertContains(response, 'Career path after pro baseball:')

    def test_no_cookie(self):
        client = Client()
        response = client.get("/")
        self.assertContains(response, 'This page is only available to clients.')

    def test_bad_cookie(self):
        client = Client()
        client.cookies['salt'] = 'bad'
        client.cookies['hash'] = 'cookie'
        response = client.get("/")
        self.assertContains(response, 'This page is only available to clients.')

    def test_index(self):
        client = Client()

        (salt, hash) = self._make_cookies()
        client.cookies['salt'] = salt
        client.cookies['hash'] = hash

        response = client.get("/")

        self.assertContains(response, 'Career path after pro baseball:')
        self.assertContains(response, '<select', 6)

    def test_output(self):
        client = Client()

        college = College.objects.get(school="Gardner-Webb University")
        alt = DOLSalary.objects.get(occupation="Elementary school teachers, except special education")
        sec = DOLSalary.objects.get(occupation="Clergy")

        data = {
            'college': college.id,
            'alt': alt.id,
            'sec': sec.id,
            'pick': 9,
            'pos': 7,
            'status': 1
        }

        response = client.post("/output", data)

        self.assertContains(response, 'Future Expected Salaries*')
        self.assertContains(response, '$58,205')

    def test_token(self):

        client = Client()

        t = str(int(time.time()))
        encoded = base64.b64encode(t)

        h = hashlib.sha256()
        h.update(t)
        h.update(settings.SECRET)
        hashed = h.hexdigest()

        response = client.post("/", {'encoded':encoded, 'hashed':hashed})

        self.assertRedirects(response, "/")


    def test_token_bad_secret(self):
        client = Client()

        t = str(int(time.time()))
        encoded = base64.b64encode(t)

        h = hashlib.sha256()
        h.update(t)
        h.update('bad secret')
        hashed = h.hexdigest()

        response = client.post("/", {'encoded':encoded, 'hashed':hashed})

        self.assertContains(response, "This page is only available to clients.")

    def test_expired_token(self):
        client = Client()

        t = str(int(time.time()-(3*60*60)))
        encoded = base64.b64encode(t)

        h = hashlib.sha256()
        h.update(t)
        h.update(settings.SECRET)
        hashed = h.hexdigest()

        response = client.post("/", {'encoded':encoded, 'hashed':hashed})

        self.assertContains(response, "This page is only available to clients.")
