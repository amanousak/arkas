# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()


crab_data_Run2018B_part2_210420_075723_0001 = kreator.makeDataComponentFromEOS('crab_data_Run2018A_part5_0000','/store/cmst3/group/bpark/gmelachr/NanoAOD_for_Kstar/NanoAOD_for_Kstar_2021Apr20/ParkingBPH2/crab_data_Run2018B_part2/210420_075723/0001/','.*root')


#crab_data_Run2018A_part5_0000 = kreator.makeDataComponentFromEOS('crab_data_Run2018A_part5_0000','/store/cmst3/group/bpark/BParkingNANO_2020Feb05/ParkingBPH5/crab_data_Run2018A_part5/200205_165610/0000/','.*root')
#crab_data_Run2018B_part5_0000 = kreator.makeDataComponentFromEOS('crab_data_Run2018B_part5_0000','/store/cmst3/group/bpark/BParkingNANO_2020Feb05/ParkingBPH5/crab_data_Run2018B_part5/200205_165723/0000/','.*root')
#crab_data_Run2018C_part5_0000 = kreator.makeDataComponentFromEOS('crab_data_Run2018C_part5_0000','/store/cmst3/group/bpark/BParkingNANO_2020Feb05/ParkingBPH5/crab_data_Run2018C_part5/200205_170223/0000/','.*root')
#crab_data_Run2018A_part5_0000 = kreator.makeDataComponentFromEOS('crab_data_Run2018A_part5_0001','/store/cmst3/group/bpark/BParkingNANO_2020Feb05/ParkingBPH5/crab_data_Run2018A_part5/200205_165610/0001/','.*root')
#crab_data_Run2018B_part5_0000 = kreator.makeDataComponentFromEOS('crab_data_Run2018B_part5_0001','/store/cmst3/group/bpark/BParkingNANO_2020Feb05/ParkingBPH5/crab_data_Run2018B_part5/200205_165723/0001/','.*root')
#crab_data_Run2018C_part5_0000 = kreator.makeDataComponentFromEOS('crab_data_Run2018C_part5_0001','/store/cmst3/group/bpark/BParkingNANO_2020Feb05/ParkingBPH5/crab_data_Run2018C_part5/200205_170223/0001/','.*root')
#crab_data_Run2018A_part1_0000 = kreator.makeDataComponentFromEOS('crab_data_Run2018A_part1_0000','/store/cmst3/group/bpark/BParkingNANO_2020Mar05/ParkingBPH1/crab_data_Run2018A_part1/200305_121157/0000/','.*root')
#crab_data_Run2018A_part1_0001 = kreator.makeDataComponentFromEOS('crab_data_Run2018A_part1_0001','/store/cmst3/group/bpark/BParkingNANO_2020Mar05/ParkingBPH1/crab_data_Run2018A_part1/200305_121157/0001/','.*root')
#crab_data_Run2018B_part1_0000 = kreator.makeDataComponentFromEOS('crab_data_Run2018B_part1_0000','/store/cmst3/group/bpark/BParkingNANO_2020Mar06/ParkingBPH1/crab_data_Run2018B_part1/200306_083819/0000/','.*root')
#crab_data_Run2018B_part1_0001 = kreator.makeDataComponentFromEOS('crab_data_Run2018B_part1_0001','/store/cmst3/group/bpark/BParkingNANO_2020Mar06/ParkingBPH1/crab_data_Run2018B_part1/200306_083819/0001/','.*root')


samples = [crab_data_Run2018B_part2_210420_075723_0001]
#samples = [crab_data_Run2018A_part5_0001,crab_data_Run2018B_part5_0001,crab_data_Run2018C_part5_0001]


if __name__ == "__main__":
	from CMGTools.RootTools.samples.tools import runMain
	runMain(samples, localobjs=locals())
