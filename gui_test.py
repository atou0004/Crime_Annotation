import unittest
import tempfile
import os
import numpy as np
from mmaction2.analyse_vid import human_action_recognition, get_top5_labels
from Scene_Detection.run_placesCNN_unified import scene_predict, load_labels, vid_slice
from yolov7.yolov7_detect_txt import detect_final


class TestModels(unittest.TestCase):
    # Video for testing the functions
    video_path = "C:/Users/Tee/Desktop/FYP/GitFYP/Crime_Annotation/test/Abuse005_x264.mp4"
    # Error message
    the_msg = "The output is not as expected"
    the_msg2 = "The object detection output is not as expected"
    # Label file for action recognition model
    action_label_map = "C:/Users/Tee/Desktop/FYP/GitFYP/Crime_Annotation/mmaction2/tools/data/kinetics/label_map_k600.txt"
    # Example dictionary as input for get_top5_labels function
    result_dict = {'predictions': [{'rec_labels': [[173]], 'rec_scores': [[0.00031767028849571943, 0.0002578711719252169, 0.0004939882201142609, 0.0012777966912835836, 0.000717011746019125, 0.00019567451090551913, 0.0005043435376137495, 0.00029396754689514637, 0.00018010701751336455, 0.00014389495481736958, 0.012081902474164963, 0.00033120118314400315, 0.0002047223097179085, 0.00015767986769787967, 0.00015884664026089013, 0.00022891402477398515, 0.0002805634867399931, 0.00016596424393355846, 0.0004025779780931771, 5.850932211615145e-05, 6.839691923232749e-05, 7.937720511108637e-05, 0.00012140300532337278, 8.569416240788996e-05, 0.00025457062292844057, 6.767493323422968e-05, 0.00041728076757863164, 3.406205360079184e-05, 0.00036579056177288294, 0.0003084657364524901, 0.0007034522714093328, 9.257609053747728e-05, 6.0822309023933485e-05, 4.939531208947301e-05, 4.934462049277499e-05, 9.437506378162652e-05, 0.0002974689123220742, 6.718738586641848e-05, 0.0001542678364785388, 0.00023044613772071898, 0.00012526311911642551, 0.0005536667304113507, 0.00017275853315368295, 0.00020431517623364925, 0.00033688449184410274, 0.00010872897109948099, 6.948412919882685e-05, 0.000433418492320925, 0.00010284287418471649, 0.0007939982460811734, 0.0002566592884249985, 7.750483200652525e-05, 0.00012926693307235837, 0.0002015279169427231, 0.00024138722801581025, 6.390536145772785e-05, 0.0003205867833457887, 0.0002745143719948828, 0.00012788278399966657, 0.0003271492896601558, 0.0006350933108478785, 0.000609512091614306, 0.0006200001225806773, 7.417832966893911e-05, 0.0001133495825342834, 0.00015341266407631338, 0.00026825006352737546, 0.000402728037443012, 0.0002665995270945132, 0.0005637526046484709, 0.00018591631669551134, 0.0004646028974093497, 0.00016292047803290188, 0.000273676443612203, 0.00015285273548215628, 0.00019108832930214703, 0.00022546402760781348, 0.0005171935190446675, 0.00014319780166260898, 0.00017487574950791895, 8.881594840204343e-05, 0.00012066656199749559, 0.00017912867770064622, 0.0002755114110186696, 0.0006068020593374968, 0.00027241086354479194, 0.00014935484796296805, 5.523352592717856e-05, 0.0012756135547533631, 8.134028757922351e-05, 0.00019783047901000828, 0.0004587853036355227, 0.00019972454174421728, 0.0002478130627423525, 6.2873812566977e-05, 4.868943869951181e-05, 0.00025961495703086257, 0.00010180327808484435, 0.00011504718713695183, 0.0003763652639463544, 0.00029767933301627636, 0.00010766240302473307, 0.00033103543682955205, 0.0001584542915225029, 7.987509889062494e-05, 6.535239663207904e-05, 0.0007128248689696193, 0.0002947961911559105, 0.00015977333532646298, 8.371859439648688e-05, 5.1389091822784394e-05, 0.00012314924970269203, 5.887900260859169e-05, 0.0001738017308525741, 0.0046914066188037395, 0.0008532168576493859, 0.0006940698949620128, 0.00045678747119382024, 0.00023322016932070255, 0.0006474677938967943, 0.0001558445510454476, 0.00035042379749938846, 0.00048573839012533426, 9.680509538156912e-05, 9.760698594618589e-05, 0.0002987428451888263, 6.754593050573021e-05, 6.60109071759507e-05, 0.00014677470608148724, 0.00029009877471253276, 6.180445780046284e-05, 0.0002365998807363212, 0.0013609162997454405, 0.0006184945232234895, 5.909590981900692e-05, 0.005645057186484337, 0.00029800800257362425, 0.00249309279024601, 0.00011357065523043275, 4.314772377256304e-05, 0.0006850536447018385, 0.00018965252093039453, 4.636395169654861e-05, 7.374960114248097e-05, 0.00047882995568215847, 0.0005084788426756859, 0.00013478433538693935, 0.0005045154830440879, 0.0001772184477886185, 0.0007172393379732966, 0.0005140203284099698, 0.00015703881217632443, 0.034593746066093445, 8.733635331736878e-05, 0.001051185536198318, 0.00030874196090735495, 0.000229936238611117, 0.00021122457110323012, 0.0002875995123758912, 0.00013142034003976732, 9.600039629731327e-05, 0.0003812295035459101, 7.641580305062234e-05, 4.6380409912671894e-05, 0.00016014324501156807, 0.00016005669021978974, 0.00021490160725079477, 0.0007015021983534098, 0.0004717772826552391, 0.00019345953478477895, 0.0003565142396837473, 0.005269719287753105, 0.0005911082262173295, 0.3114425539970398, 0.0002327482361579314, 0.0005506937741301954, 0.00023937596415635198, 0.00015611246635671705, 0.0003735865466296673, 0.00028313888469710946, 0.00022416449792217463, 0.0002736658207140863, 0.0002444846904836595, 0.00034304038854315877, 0.000168129539815709, 0.00038459221832454205, 0.00010486930841580033, 3.907809514203109e-05, 0.0009443543385714293, 0.00019000182510353625, 4.134995833737776e-05, 0.00035414620651863515, 5.9086109104100615e-05, 7.956534682307392e-05, 0.00019357530982233584, 0.0001528232533019036, 0.0002292145072715357, 0.0001654266961850226, 0.00011918970267288387, 0.0002337100013392046, 0.00023622297157999128, 0.00019338233687449247, 4.500336217461154e-05, 8.16559768281877e-05, 0.00023383030202239752, 0.0003255557967349887, 0.00016208458691835403, 0.000135114518343471, 0.0022058580070734024, 0.10478419810533524, 0.0001348772639175877, 0.0007224184228107333, 0.00020959626999683678, 0.00029048093711026013, 0.0001237515389220789, 0.0016820644959807396, 0.00013001816114410758, 9.857746044872329e-05, 0.0012975791469216347, 0.003521681996062398, 0.0031753189396113157, 0.0006134043214842677, 0.00022869514941703528, 0.00011210679076611996, 0.000272017321549356, 0.0002560781722422689, 0.00021853172802366316, 0.0003443945315666497, 0.0002339505444979295, 5.531956412596628e-05, 0.0001472870062571019, 6.979083991609514e-05, 0.0001908035046653822, 2.7086472982773557e-05, 0.000317040306981653, 4.8693938879296184e-05, 0.00020354866865091026, 0.00014239156735129654, 0.00014518089301418513, 6.371999916154891e-05, 0.00020292121917009354, 0.000292885466478765, 0.0006402189610525966, 0.00023817876353859901, 0.0001309537619818002, 0.00019013072596862912, 0.00031297403620555997, 0.00035589002072811127, 0.0002657650038599968, 7.797192665748298e-05, 0.0002510678314138204, 0.0002014666679315269, 0.001230693655088544, 0.0004571298777591437, 0.0003883064491674304, 0.00023107997549232095, 3.687164280563593e-05, 0.000245773873757571, 0.00020253213006071746, 0.0001496918557677418, 0.00022009786334820092, 0.0005738661857321858, 0.0008501942502334714, 0.0003541871556080878, 0.00022133981110528111, 0.002774826716631651, 0.00015078198339324445, 6.5268250182271e-05, 0.000728042796254158, 9.720995149109513e-05, 0.00043217220809310675, 0.00020559468248393387, 0.00031535106245428324, 0.0001699488057056442, 0.00014415846089832485, 0.00027535707340575755, 8.960184641182423e-05, 0.0001574999769218266, 0.00010754021059256047, 0.00029925175476819277, 0.00011370970605639741, 0.0005739302141591907, 0.001651904545724392, 0.000105382438050583, 6.271887104958296e-05, 9.270169539377093e-05, 7.106340490281582e-05, 7.164933776948601e-05, 0.00010143080726265907, 0.0005205916240811348, 0.0011382659431546926, 0.0005604908801615238, 0.00011700754112098366, 4.479615017771721e-05, 0.02552829310297966, 9.11424940568395e-05, 8.050209726206958e-05, 0.00012724076805170625, 0.00035041087539866567, 0.0006255261832848191, 0.1347990483045578, 0.00013310290523804724, 0.0013029893161728978, 0.0003210064023733139, 0.0004932525334879756, 0.00033139099832624197, 0.0005098182591609657, 0.00042101950384676456, 0.0003758811508305371, 0.00013712854706682265, 7.163048576330766e-05, 5.90727140661329e-05, 8.133069786708802e-05, 0.0003024142642971128, 0.000705770798958838, 0.0002717095776461065, 0.002830089535564184, 0.026935195550322533, 0.00013581753592006862, 0.0002770379651337862, 0.004009324125945568, 6.58276112517342e-05, 0.00011188046482857317, 0.0004323770699556917, 0.0004186956211924553, 0.0001309844956267625, 0.00039448548341169953, 0.0001884058874566108, 0.0005812083836644888, 0.00029617431573569775, 0.0005582979647442698, 6.702225073240697e-05, 9.497315477347001e-05, 0.00037308898754417896, 9.84835933195427e-05, 0.00032690761145204306, 0.00042694644071161747, 0.00013149328879080713, 0.00039666847442276776, 8.336403698194772e-05, 0.00010000674228649586, 0.00012558499292936176, 0.0002725408994592726, 9.654440509621054e-05, 0.0001311513624386862, 0.00014135983656160533, 0.00028687535086646676, 8.934316429076716e-05, 5.1688592066057026e-05, 0.0002833034086506814, 0.00014506769366562366, 0.00042095445678569376, 0.0008360467618331313, 9.635272726882249e-05, 0.00017929727619048208, 7.008243119344115e-05, 0.0003661818918772042, 0.00020731553377117962, 0.00012578550376929343, 7.176422514021397e-05, 0.0002782689407467842, 0.00012610746489372104, 0.00037297519156709313, 0.00017087775631807745, 0.0005285216029733419, 0.00011956949310842901, 3.2842795917531475e-05, 0.0003241242957301438, 2.9787237508571707e-05, 5.611836604657583e-05, 0.0002625199849717319, 0.00036925519816577435, 0.00017331894196104258, 0.00010896868479903787, 7.364994962699711e-05, 0.00011161186557728797, 0.0002295112208230421, 0.00013944535749033093, 0.00014361157082021236, 8.401971717830747e-05, 0.0001163576525868848, 0.00021157845912966877, 4.067227928317152e-05, 0.00048756919568404555, 0.0002071098715532571, 0.0001361453323625028, 0.00012044065806549042, 0.00023130213958211243, 0.0002719439216889441, 0.0005705883959308267, 0.001138892606832087, 0.0012954184785485268, 0.000304904708173126, 0.0023199717979878187, 0.0008500149706378579, 0.0004847098607569933, 0.020780958235263824, 0.00011118222755612805, 0.00024763401597738266, 0.00012221370707266033, 0.00016259969561360776, 0.00026806138339452446, 5.235952266957611e-05, 0.00031837253482080996, 0.0003610546118579805, 0.00016343194874934852, 0.00010858145105885342, 0.0010450833942741156, 0.00020305803627707064, 0.000816745450720191, 0.0001910676364786923, 0.00047942379023879766, 0.00012175597657915205, 0.00017614293028600514, 0.0001586948346812278, 0.002103627659380436, 0.0007975684711709619, 0.0006317106308415532, 0.0005730990087613463, 0.00030580017482861876, 0.0001857658353401348, 0.0001875883317552507, 0.000564566464163363, 0.00100166245829314, 0.0004421836929395795, 0.000129748645122163, 0.00010187529551330954, 0.00038991644396446645, 0.0001568637089803815, 0.0003133929567411542, 0.00018210260896012187, 0.0003038890426978469, 0.0003302778350189328, 0.00025109745911322534, 0.00023172219516709447, 0.00019366401829756796, 0.0001048989943228662, 0.00023225814220495522, 0.00013975868932902813, 0.00017467737779952586, 0.002045729663223028, 0.0003969835233874619, 0.00037952628917992115, 7.905189704615623e-05, 0.0005833462928421795, 0.00012545904610306025, 0.0004625745350494981, 0.000530863821040839, 0.0013513003941625357, 8.086601155810058e-05, 0.0006354969227686524, 0.0004282193840481341, 0.000617463025264442, 0.00014966033631935716, 0.00021529918012674898, 0.00011570366768864915, 0.00017142700380645692, 0.00012369381147436798, 0.001513649127446115, 0.00015102417091839015, 0.0004194127395749092, 9.418503032065928e-05, 0.0012977332808077335, 0.00028957135509699583, 0.00041495150071568787, 0.0007439086912199855, 0.0002635028795339167, 8.6649575678166e-05, 0.00016534587484784424, 0.00021544045011978596, 0.00036970898509025574, 0.00018219277262687683, 0.07786894589662552, 9.887308988254517e-05, 0.0006757046794518828, 0.006874065846204758, 0.00018095535051543266, 0.0004476221511140466, 9.928499639499933e-05, 8.252197585534304e-05, 0.00024320340889971703, 0.0002529389748815447, 0.0001156744547188282, 4.9141235649585724e-05, 0.00015269475989043713, 0.00016133591998368502, 0.0007362063624896109, 0.0004205478762742132, 8.771652210270986e-05, 0.0003034625551663339, 0.00017803996161092073, 0.0002935510128736496, 5.814183168695308e-05, 9.2686343123205e-05, 0.005245169624686241, 0.0001572297333041206, 0.00022360263392329216, 0.00035051009035669267, 0.000578681705519557, 0.0005025248974561691, 0.00015311772585846484, 0.00013393053086474538, 0.00015263403474818915, 0.0011604574974626303, 0.00023147456522565335, 0.0007471343851648271, 0.000306822475977242, 8.701151818968356e-05, 0.00011343476944603026, 0.00016507769760210067, 0.00026110291946679354, 0.0011139116249978542, 0.00016275502275675535, 0.008754181675612926, 0.0015492511447519064, 0.0004530671867541969, 0.0002800026268232614, 9.908615902531892e-05, 0.0002449850144330412, 0.0002984218008350581, 0.00017730412946548313, 0.00023469133884645998, 0.00010646313603501767, 0.0001181315747089684, 0.0011936952359974384, 0.0034627066925168037, 0.00013378728181123734, 0.00034186261473223567, 0.0009304664563387632, 0.0001307675993302837, 0.0012515629641711712, 0.00016866475925780833, 0.004636749159544706, 0.0003954088024329394, 0.0009086115751415491, 0.00017050589667633176, 0.0003294864436611533, 0.0009772370103746653, 0.00023133913055062294, 0.002468788530677557, 0.00016848028462845832, 0.00017170648789033294, 8.310903649544343e-05, 0.00012638211774174124, 0.00012617319589480758, 0.00012619995686691254, 0.00010453356662765145, 8.487740706186742e-05, 6.982278864597902e-05, 0.00012548624363262206, 0.0001270063512492925, 0.0001945151452673599, 0.001827927422709763, 0.00011437937791924924, 0.0004544119001366198, 0.00015430428902618587, 0.00036189070669934154, 0.00019700286793522537, 0.0026759528554975986, 0.000669797882437706, 8.523974975105375e-05, 0.00013686082093045115, 9.370812040288001e-05, 0.0005486903828568757, 0.0021994048729538918, 0.00018008476763498038, 0.0006080239545553923, 0.000390321685699746, 0.001008461695164442, 0.0009187581017613411, 0.0004923013621009886, 0.0015526204369962215, 0.00037439135485328734, 2.9720264137722552e-05, 0.0005006222054362297, 0.00015973355039022863, 0.00018417408864479512, 0.00037212559254840016, 0.00033007466117851436, 0.0003931530227418989, 0.0002695912844501436, 0.00012671986769419163, 0.00031609530560672283, 8.659960440127179e-05, 4.620711843017489e-05, 0.00016431769472546875, 0.00015044884639792144, 0.00037867692299187183, 7.274438394233584e-05, 0.0003254844341427088, 0.00022044414072297513, 0.00010541590745560825, 8.495053043588996e-05, 0.00023763044737279415, 0.0006100393366068602, 0.00028714220388792455, 0.00023691350361332297, 8.735113078728318e-05, 0.00023063638946041465, 7.173978519858792e-05]]}]}

    def test_temp_file(self):
        with open(self.video_path, 'rb') as f:
            video_data = f.read()

        # Creating a temp file object
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_data)

        tfile.seek(0)

        # to check if the video file exists
        self.assertEqual(tfile.read(), video_data, msg= "There is no video file")

        tfile.close()

    def test_action_detection_output_is_not_None(self):
        os.chdir('C:/Users/Tee/Desktop/FYP/GitFYP/Crime_Annotation/mmaction2')
        # Cehck to see if the output is not None
        self.assertIsNotNone(human_action_recognition(self.video_path))
        os.chdir("C:/Users/Tee/Desktop/FYP/GitFYP/Crime_Annotation")

    def test_action_detection_output_is_correct(self):
        # Check to see if the output is consistent (correct)
        os.chdir('C:/Users/Tee/Desktop/FYP/GitFYP/Crime_Annotation/mmaction2')
        self.assertEqual(human_action_recognition(self.video_path), ['falling off chair', 'opening door', 'headbutting', 'slapping', 'drop kicking'] , msg = self.the_msg)
        os.chdir("C:/Users/Tee/Desktop/FYP/GitFYP/Crime_Annotation")

    def test_action_detection_failure1(self):
        # without specifying the directory, the code will fail
        with self.assertRaises(RuntimeError):
            human_action_recognition(self.video_path)

    def test_action_detection_failure2(self):
        # giving the model a None value, the code will raise an error
        os.chdir('C:/Users/Tee/Desktop/FYP/GitFYP/Crime_Annotation/mmaction2')
        with self.assertRaises(ValueError):
            human_action_recognition(None)
        os.chdir("C:/Users/Tee/Desktop/FYP/GitFYP/Crime_Annotation")

    def test_get_top5_labels(self):
        # Check to see if the function is able to get top 5 labels from dictionary
        self.assertEqual(get_top5_labels(str(self.result_dict), self.action_label_map), ['falling off chair', 'opening door', 'headbutting', 'slapping', 'drop kicking'], msg = self.the_msg)

    def test_scene_prediction_output_is_not_None(self):
        with open(self.video_path, 'rb') as f:
            video_data = f.read()

        # Creating a temp file object
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_data)
                    
        # Testing if the output if not None
        network_name_lst = ['psnr-small', 'psnr-large', 'rrdn', 'noise-cancel', 'none']
        for i in (network_name_lst):
            network_name = i
            # Check to see if each of the network names are working
            self.assertIsNotNone(scene_predict(tfile.name, i))
    
    def test_scene_prediction_output_is_correct(self):
        with open(self.video_path, 'rb') as f:
            video_data = f.read()

        # Creating a temp file object
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_data)

        # Testing if the each of the output is consistent (correct)
        self.assertEqual(scene_predict(tfile.name, 'psnr-small'), {'environment': 'indoor', 'scene_category': ['science museum', 'beauty salon', 'arena performance', 'television studio', 'elevator shaft'], 'attribute_1': 'no horizon', 'attribute_2': 'enclosed area', 'attribute_3': 'indoor lighting'}, msg = self.the_msg)
        self.assertEqual(scene_predict(tfile.name, 'psnr-large'), {'environment': 'indoor', 'scene_category': ['science museum', 'beauty salon', 'arena performance', 'television studio', 'elevator shaft'], 'attribute_1': 'no horizon', 'attribute_2': 'enclosed area', 'attribute_3': 'indoor lighting'} , msg = self.the_msg)
        self.assertEqual(scene_predict(tfile.name, 'rrdn'), {'environment': 'indoor', 'scene_category': ['science museum', 'beauty salon', 'elevator shaft', 'jacuzzi indoor', 'museum indoor'], 'attribute_1': 'no horizon', 'attribute_2': 'enclosed area', 'attribute_3': 'indoor lighting'}, msg = self.the_msg)
        self.assertEqual(scene_predict(tfile.name, 'noise-cancel'), {'environment': 'indoor', 'scene_category': ['science museum', 'museum indoor', 'elevator shaft', 'beauty salon', 'natural history museum', 'natural history museum'], 'attribute_1': 'no horizon', 'attribute_2': 'enclosed area', 'attribute_3': 'indoor lighting'} , msg = self.the_msg)
        self.assertEqual(scene_predict(tfile.name, 'none'), {'environment': 'indoor', 'scene_category': ['science museum', 'beauty salon', 'arena performance', 'television studio', 'museum indoor'], 'attribute_1': 'no horizon', 'attribute_2': 'enclosed area', 'attribute_3': 'indoor lighting'} , msg = self.the_msg)       

    def test_object_prediction_output_is_not_none(self):
        # Check to see if the output is not None
        self.assertIsNotNone(detect_final(self.video_path))

    def test_object_prediction_output_is_correct(self):
        # Check to see if the output is not None
        the_msg = "The output is not as expected"
        correct_output = {'person': 4, 'suitcase': 2, 'chair': 2, 'motorcycle': 1, 'handbag': 1, 'bench': 1, 'potted plant': 1, 'skateboard': 1, 'snowboard': 2, 'dog': 1, 'knife': 1, 'pistol': 1}
        
        # Make sure that at least one out of 3 output is correct
        for _ in range(3):
            current_output = detect_final(self.video_path)
            if current_output == correct_output:
                break
    
        self.assertEqual(current_output, correct_output, msg = self.the_msg2)

    def test_object_prediction_failure1(self):
        # giving the model a None value, the code will raise an error
        with self.assertRaises(ValueError):
            human_action_recognition(None)

    def test_load_labels_is_instance(self):
        #Call load_labels
        classes, labels_IO, labels_attribute, W_attribute = load_labels()

        # Checking to see if the output types are correct for load labels
        self.assertIsInstance(classes, tuple)
        self.assertIsInstance(labels_IO, np.ndarray)
        self.assertIsInstance(labels_attribute, list)
        self.assertIsInstance(W_attribute, np.ndarray)
    
    def test_load_labels_is_correct(self):
        # Call the load_labels function
        classes, labels_IO, labels_attribute, W_attribute = load_labels()

        # Check to see if the output is correct or not
        self.assertEqual(len(classes), 365)
        self.assertEqual(labels_IO.shape, (365, ))
        self.assertEqual(len(labels_attribute), 102)
        self.assertEqual(W_attribute.shape, (102, 512 ))
    
    def test_vid_slice(self):
        # Call the function
        frame = vid_slice(self.video_path)

        # Check to see if the a frame was taken from the given video
        self.assertIsInstance(frame, np.ndarray)
        self.assertEqual(frame.shape, (240, 320, 3))

if __name__ == '__main__':
    unittest.main()