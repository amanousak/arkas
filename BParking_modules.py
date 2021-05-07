
def SkimCuts(Bdecay,Bcuts):
    BParking_skim_cut = ("Sum$( "+
#                         "BToKMuMu_l_xy_unc>0 && BToKMuMu_l_xy/BToKMuMu_l_xy_unc>-1 && "+
                         Bdecay+"_fit_pt>{ptmin} && "+
                         Bdecay+"_fit_mass>{mmin} && "+
                         Bdecay+"_fit_mass<{mmax} && "+
                         Bdecay+"_l_xy_unc>0 && "+
                         Bdecay+"_l_xy/"+Bdecay+"_l_xy_unc>{slxy} && "+
                         Bdecay+"_fit_cos2D>{cos} && "+
                         Bdecay+"_svprob>{prob} &&"+
                         Bdecay+"_fit_l1_pt>{l1pt} &&"+
                         Bdecay+"_fit_l2_pt>{l2pt} &&"+
                         Bdecay+"_fit_kstar_pt>{kpt} &&"+
                         Bdecay+"_mll_fullfit>{mllmin} &&"+
                         Bdecay+"_mll_fullfit<{mllmax}"+
                         " )>0"
            ).format(
                     ptmin=Bcuts["Pt"],     mmin=Bcuts["MinMass"], 
                     mmax=Bcuts["MaxMass"], slxy=Bcuts["LxySign"], 
                     cos=Bcuts["Cos2D"],    prob=Bcuts["Prob"],
                     l1pt=Bcuts["L1Pt"],    l2pt=Bcuts["L2Pt"],
                     kpt=Bcuts["KPt"],      mllmin=Bcuts["Mllmin"],
                     mllmax=Bcuts["Mllmax"]
                    )
    return BParking_skim_cut


def KstarMuMuData ( process, Bcuts):
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionSkimmer import collectionSkimmer
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionEmbeder import collectionEmbeder
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.branchCreator import branchCreator

    BKsLLSelection = lambda l : l.fit_pt > Bcuts["Pt" ] and l.fit_cos2D > Bcuts["Cos2D"] and l.svprob > Bcuts["Prob"] and l.l_xy_unc >0 and (l.l_xy)/l.l_xy_unc > Bcuts["LxySign"] and l.mll_fullfit>Bcuts["Mllmin"] and l.fit_mass>Bcuts["MinMass"] and l.fit_mass<Bcuts["MaxMass"] and l.mll_fullfit<Bcuts["Mllmax"]

    BSkim = collectionSkimmer(input = "BToKsMuMu",
                            output = "SkimBToKsMuMu",
                            selector = BKsLLSelection,
                            branches = ["fit_pt","fit_mass","mass","l_xy",
                                        "l_xy_unc","fit_cos2D","svprob",
                                        "l1_idx","l2_idx","kstar_idx","fit_eta",
                                        "mll_fullfit",
                                        "fit_l1_pt","fit_l1_eta","fit_l1_phi",
                                        "fit_l2_pt","fit_l2_eta","fit_l2_phi",
                                        "fit_kstar_pt","fit_kstar_eta","fit_kstar_phi"
                                         ],
                            TriggerMuonId = "Muon_isTriggering",
                            #selectTagMuons = True,
                            selectTagMuons = False,
                            flat = False
    )   
    process.append(BSkim)
    Mu1 = collectionEmbeder( inputColl = "Muon",
                             embededColl = "SkimBToKsMuMu",
                             inputBranches = ["softId","vz","pfRelIso03_all","isTriggering"],
                             embededBranches = ["l1_softId","l1_vz","l1_iso","l1_isTrg"], 
                             embededCollIdx = "l1_idx"
    )
    process.append(Mu1)
    Mu2 = collectionEmbeder( inputColl = "Muon",
                             embededColl = "SkimBTosKMuMu",
                             inputBranches = ["softId","vz","pfRelIso03_all","isTriggering"],
                             embededBranches = ["l2_softId","l2_vz","l2_iso","l2_isTrg"], 
                             embededCollIdx = "l2_idx"
    )
    process.append(Mu2)
    K = collectionEmbeder( inputColl = "ProbeTracks",
                           embededColl = "SkimBToKsMuMu",
                           inputBranches = ["vz"],
                           embededBranches = ["k_vz"],  
                           embededCollIdx = "kstar_idx"
    )
    process.append(K)
    # in case of inf in L_xy/unc produces -99
    CreateVars = branchCreator(
      collection="SkimBToKsMuMu",
        inputBranches=[["l_xy","l_xy_unc"],["l1_vz","l2_vz"],
                       ["k_vz","l1_vz","l2_vz"],
                       ["fit_l1_eta","fit_l1_phi","fit_l2_eta","fit_l2_phi"],
                       ["fit_kstar_eta","fit_kstar_phi","fit_l1_eta","fit_l1_phi","fit_l2_eta","fit_l2_phi"]],
        operation=["{0}/{1}","abs({0}-{1})",
                   "min(abs({0}-{1}),abs({0}-{2}))",
                   "deltaR({0},{1},{2},{3})",
                   "min( deltaR({0},{1},{2},{3}),deltaR({0},{1},{3},{4}))"],
        createdBranches=["l_xy_sig","l1l2_dz","lk_dz","l1l2_dr","lk_dr"],
    )
    process.append(CreateVars)
    return process

def KMuMuData ( process, Bcuts):
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionSkimmer import collectionSkimmer
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionEmbeder import collectionEmbeder
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.branchCreator import branchCreator

    BKLLSelection = lambda l : l.fit_pt > Bcuts["Pt" ] and l.fit_cos2D > Bcuts["Cos2D"] and l.svprob > Bcuts["Prob"] and l.l_xy_unc >0 and (l.l_xy)/l.l_xy_unc > Bcuts["LxySign"] and l.mll_fullfit>Bcuts["Mllmin"] and l.fit_mass>Bcuts["MinMass"] and l.fit_mass<Bcuts["MaxMass"] and l.mll_fullfit<Bcuts["Mllmax"]

    BSkim = collectionSkimmer(input = "BToKMuMu",
                            output = "SkimBToKMuMu",
                            selector = BKLLSelection,
                            branches = ["fit_pt","fit_mass","mass","l_xy",
                                        "l_xy_unc","fit_cos2D","svprob",
                                        "l1Idx","l2Idx","kIdx","fit_eta",
                                        "mll_fullfit",
                                        "fit_l1_pt","fit_l1_eta","fit_l1_phi",
                                        "fit_l2_pt","fit_l2_eta","fit_l2_phi",
                                        "fit_k_pt","fit_k_eta","fit_k_phi"
                                         ],
                            TriggerMuonId = "Muon_isTriggering",
                            selectTagMuons = False,
                            flat = False
    )   
    process.append(BSkim)
    Mu1 = collectionEmbeder( inputColl = "Muon",
                             embededColl = "SkimBToKMuMu",
                             inputBranches = ["softId","vz","pfRelIso03_all","isTriggering"],
                             embededBranches = ["l1_softId","l1_vz","l1_iso","l1_isTrg"], 
                             embededCollIdx = "l1Idx"
    )
    process.append(Mu1)
    Mu2 = collectionEmbeder( inputColl = "Muon",
                             embededColl = "SkimBToKMuMu",
                             inputBranches = ["softId","vz","pfRelIso03_all","isTriggering"],
                             embededBranches = ["l2_softId","l2_vz","l2_iso","l2_isTrg"], 
                             embededCollIdx = "l2Idx"
    )
    process.append(Mu2)
    K = collectionEmbeder( inputColl = "ProbeTracks",
                           embededColl = "SkimBToKMuMu",
                           inputBranches = ["vz"],
                           embededBranches = ["k_vz"],  
                           embededCollIdx = "kIdx"
    )
    process.append(K)
    # in case of inf in L_xy/unc produces -99
    CreateVars = branchCreator(
      collection="SkimBToKMuMu",
        inputBranches=[["l_xy","l_xy_unc"],["l1_vz","l2_vz"],
                       ["k_vz","l1_vz","l2_vz"],
                       ["fit_l1_eta","fit_l1_phi","fit_l2_eta","fit_l2_phi"],
                       ["fit_k_eta","fit_k_phi","fit_l1_eta","fit_l1_phi","fit_l2_eta","fit_l2_phi"]],
        operation=["{0}/{1}","abs({0}-{1})",
                   "min(abs({0}-{1}),abs({0}-{2}))",
                   "deltaR({0},{1},{2},{3})",
                   "min( deltaR({0},{1},{2},{3}),deltaR({0},{1},{3},{4}))"],
        createdBranches=["l_xy_sig","l1l2_dz","lk_dz","l1l2_dr","lk_dr"],
    )
    process.append(CreateVars)
    return process

def KEEData ( process, Bcuts,use_PF=False,use_1LowPt_1PF=False):
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionSkimmer import collectionSkimmer
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionEmbeder import collectionEmbeder
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.branchCreator import branchCreator

    BKLLSelection = lambda l : l.fit_pt > Bcuts["Pt" ] and l.fit_cos2D > Bcuts["Cos2D"] and l.svprob > Bcuts["Prob"] and l.l_xy_unc >0 and (l.l_xy)/l.l_xy_unc > Bcuts["LxySign"] and l.mll_fullfit>Bcuts["Mllmin"] and l.fit_mass>Bcuts["MinMass"] and l.fit_mass<Bcuts["MaxMass"] and l.mll_fullfit<Bcuts["Mllmax"]
    
    if use_PF and not use_1LowPt_1PF:
      BKLLSelection = lambda l : l.fit_pt > Bcuts["Pt" ] and l.fit_cos2D > Bcuts["Cos2D"] and l.svprob > Bcuts["Prob"] and l.l_xy_unc >0 and (l.l_xy)/l.l_xy_unc > Bcuts["LxySign"] and l.mll_fullfit>Bcuts["Mllmin"] and l.fit_mass>Bcuts["MinMass"] and l.fit_mass<Bcuts["MaxMass"] and l.mll_fullfit<Bcuts["Mllmax"] and l.l1isPF == 1 and l.l2isPF == 1 and l.l1PFId>-30.5 and l.l2PFId>-50.0
    elif use_1LowPt_1PF and not use_PF:
      BKLLSelection = lambda l : l.fit_pt > Bcuts["Pt" ] and l.fit_cos2D > Bcuts["Cos2D"] and l.svprob > Bcuts["Prob"] and l.l_xy_unc >0 and (l.l_xy)/l.l_xy_unc > Bcuts["LxySign"] and l.mll_fullfit>Bcuts["Mllmin"] and l.fit_mass>Bcuts["MinMass"] and l.fit_mass<Bcuts["MaxMass"] and l.mll_fullfit<Bcuts["Mllmax"] and ( (l.l1isPF == 1 and l.l2isPF == 0 and l.l2isPFoverlap==0 and l.l1PFId>-1.25 and l.l2LowPtId>-1.5) or (l.l1isPF == 0 and l.l2isPF == 1 and l.l1isPFoverlap==0 and l.l2PFId>-1.25 and l.l1LowPtId>-1.5) )
    else:
      BKLLSelection = lambda l : l.fit_pt > Bcuts["Pt" ] and l.fit_cos2D > Bcuts["Cos2D"] and l.svprob > Bcuts["Prob"] and l.l_xy_unc >0 and (l.l_xy)/l.l_xy_unc > Bcuts["LxySign"] and l.mll_fullfit>Bcuts["Mllmin"] and l.fit_mass>Bcuts["MinMass"] and l.fit_mass<Bcuts["MaxMass"] and l.mll_fullfit<Bcuts["Mllmax"]
    
    BSkim = collectionSkimmer(input = "BToKEE",
                            output = "SkimBToKEE",
                            importedVariables = ["Electron_isPF","Electron_isPF"
                             ,"Electron_isPFoverlap","Electron_isPFoverlap",
                              "Electron_pfmvaId","Electron_pfmvaId",
                              "Electron_mvaId","Electron_mvaId"],
                            importIds = ["l1Idx","l2Idx",
                                         "l1Idx","l2Idx",
                                         "l1Idx","l2Idx",
                                         "l1Idx","l2Idx"],
                            varnames = ["l1isPF","l2isPF",
                                        "l1isPFoverlap","l2isPFoverlap",
                                        "l1PFId","l2PFId",
                                        "l1LowPtId","l2LowPtId"],
                            selector = BKLLSelection,
                            branches = ["fit_pt","fit_eta","fit_phi",
                                        "fit_mass","l_xy","l_xy_unc",
                                        "fit_cos2D","svprob","fit_massErr",
                                        "b_iso04","mll_fullfit",
                                        "vtx_x","vtx_y","vtx_z",
                                        "l1Idx","l2Idx","kIdx",
                                        "fit_k_pt","fit_k_eta","fit_k_phi",
                                        "k_iso04",
                                        "fit_l1_pt","fit_l1_eta","fit_l1_phi",
                                        "l1_iso04",
                                        "fit_l2_pt","fit_l2_eta","fit_l2_phi",
                                        "l2_iso04",
                                        "l1isPF","l2isPF","l1PFId","l2PFId",
                                        "l1LowPtId","l2LowPtId"
                                        ],
                            flat = False
    )
    process.append(BSkim)
    El1 = collectionEmbeder( inputColl = "Electron",
                             embededColl = "SkimBToKEE",
                             inputBranches = ["pt","eta","phi","vx","vy","vz"],
                             embededBranches = ["l1Pt","l1Eta","l1Phi","l1Vx","l1Vy","l1Vz"], 
                             embededCollIdx = "l1Idx"
    )
    process.append(El1)
    El2 = collectionEmbeder( inputColl = "Electron",
                             embededColl = "SkimBToKEE",
                             inputBranches = ["pt","eta","phi","vx","vy","vz"],
                             embededBranches = ["l2Pt","l2Eta","l2Phi","l2Vx","l2Vy","l2Vz"],
                             embededCollIdx = "l2Idx"
    )
    process.append(El2)
    K = collectionEmbeder( inputColl = "ProbeTracks",
                           embededColl = "SkimBToKEE",
                           inputBranches = ["vx","vy","vz"],
                           embededBranches = ["kVx","kVz","kVz"],
                           embededCollIdx = "kIdx"
    )
    process.append(K)
    # in case of inf in L_xy/unc produces -99
    CreateVars = branchCreator(
        collection="SkimBToKEE",
        inputBranches=[["l_xy","l_xy_unc"],["l1Vz","l2Vz"],["kVz","l1Vz","l2Vz"]
                      ,["fit_l1_eta","fit_l1_phi","fit_l2_eta","fit_l2_phi"],
                       ["fit_k_eta","fit_k_phi","fit_l1_eta","fit_l1_phi","fit_l2_eta","fit_l2_phi"]],
        operation=["{0}/{1}","abs({0}-{1})","min(abs({0}-{1}),abs({0}-{2}))",
                   "deltaR({0},{1},{2},{3})",
                   "min( deltaR({0},{1},{2},{3}),deltaR({0},{1},{3},{4}))"],
        createdBranches=["l_xy_sig","l1l2Dz","lKDz","l1l2Dr","lKDr"],
    )
    process.append(CreateVars)
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.functionWrapper import functionWrapper
    TagVars = functionWrapper(
      functionName="TagVars",
      collections=["ProbeTracks","TriggerMuon","SkimBToKEE"],
      createdBranches=["SkimBToKEE_TagMuEtRatio","SkimBToKEE_TagMuDphi","SkimBToKEE_TagMu4Prod"],
      nCol="nSkimBToKEE"
    )
    process.append(TagVars)
    ClosestTrkVars = functionWrapper(
      functionName="ClosestTrkVars",
      collections=["ProbeTracks","SkimBToKEE","Electron"],
      createdBranches=["SkimBToKEE_l1_trk_mass","SkimBToKEE_l2_trk_mass",
                       "SkimBToKEE_trk_minxy1","SkimBToKEE_trk_minxy2",
                       "SkimBToKEE_trk_minxy3","SkimBToKEE_trk_mean"],
      nCol="nSkimBToKEE"
    )
    process.append(ClosestTrkVars)
    return process


def KMuMuMC (process,Jpsi=[]):
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.genDecayConstructorPython import genDecayConstructorPython
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.genRecoMatcher import genRecoMatcher
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.compositeRecoMatcher import compositeRecoMatcher
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.branchCreatorMC import branchCreatorMC
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.genTriggerMuon import genTriggerMuon
   #cuts_on_lep = lambda l: True
   cuts_on_B = "True"
   cuts_on_B_vars = []
   GenDecay = genDecayConstructorPython( momPdgId = 521,
                                   daughtersPdgId = [13, -13, 321],
                                   outputMomColl = "genB",
                                   intermediateDecay = Jpsi,
                                   trgMuonPtEtaThresholds = [], #best for training - probe/tag side kinematics no trigger eff reduction
                                   selectTrgMuon = False,
                                   excludeTrgMuon = False,
                                   outputDaughterColls = ["genMu1","genMu2","genK"] 
    )                             
   process.append(GenDecay)   
   RecoMu1 = genRecoMatcher( recoInput="Muon",
                             genInput = "genMu1",
                             output = "recoMu1",
                             branches = ["pt","eta","phi","softId","vz","pfRelIso03_all","dxy","dxyErr"],
                             addChargeMatching=False,
                             skipNotMatched=False,
                             DRcut=0.1
   )                             
   process.append(RecoMu1)
   RecoMu2 = genRecoMatcher( recoInput="Muon",
                             genInput = "genMu2",
                             output = "recoMu2",
                             branches = ["pt","eta","phi","softId","vz","pfRelIso03_all","dxy","dxyErr"],
                             addChargeMatching=False,
                             skipNotMatched=False,
                             DRcut=0.1
   )                             
   process.append(RecoMu2)
   #deal with trg muon
   TriggerObj= genTriggerMuon( trgBranch="Muon_isTriggering", 
                               skipNoTrgEvt=True, 
                               skipProbe=False, 
                               skipTag=True, 
                               selectionPathList=["HLT_Mu9_IP6"],
                               outputColl="trgMu", 
                               recoIdx=["recoMu1_Idx","recoMu2_Idx"], 
                               trgMuMinPt=8.5,
                               branches=["pt","eta","phi","dxy","dxyErr"]
   )
   process.append(TriggerObj)
   RecoK = genRecoMatcher( recoInput="ProbeTracks",
                             genInput = "genK",
                             output = "recoK",
                             branches = ["vz"],
                             skipNotMatched=False,
                             DRcut=0.1
   )                             
   process.append(RecoK)
   RecoB = compositeRecoMatcher(   compositeColl = "BToKMuMu",
                             lepCompositeIdxs = ["l1Idx","l2Idx"],
                             hadronCompositeIdxs = ["kIdx"],
                             lepMatchedRecoIdxs = ["recoMu1_Idx","recoMu2_Idx"],
                             hadronMatchedRecoIdxs = ["recoK_Idx"],
                             outputColl = "recoB",
                             cuts_vars=cuts_on_B_vars,
                             cuts=cuts_on_B,
                             branches = ["fit_pt","fit_eta","fit_phi",
                                         "fit_mass","mll_fullfit","l_xy",
                                         "l_xy_unc","fit_cos2D","svprob",
                                         "fit_massErr","b_iso04",
                                          "vtx_x","vtx_y","vtx_z",
                                         "l1Idx","l2Idx","kIdx",
                                         "fit_l1_pt","fit_l1_eta","fit_l1_phi",
                                         "l1_iso04","n_l1_used",
                                         "fit_l2_pt","fit_l2_eta","fit_l2_phi",
                                         "l2_iso04","n_l2_used",
                                         "fit_k_pt","fit_k_eta","fit_k_phi",
                                         "k_iso04","n_k_used"
                                        ],
                             sortTwoLepByIdx=True,
                             lepLabelsToSort = ["l1","l2"]# branches need to have lep labels between "_" eg fit_l1_pt or l1_iso - lep indexes also sorted
   )                                  
   process.append(RecoB)
   # in case of inf in L_xy/unc produces -99
   CreateVars = branchCreatorMC(
      inputBranches=[["recoB_l_xy","recoB_l_xy_unc"],
                     ["recoMu1_vz","recoMu2_vz"],
                     ["recoK_vz","recoMu1_vz","recoMu2_vz"],
                     ["recoB_fit_l1_eta","recoB_fit_l1_phi","recoB_fit_l2_eta","recoB_fit_l2_phi"], 
                     ["recoB_fit_k_eta","recoB_fit_k_phi","recoB_fit_l1_eta","recoB_fit_l1_phi","recoB_fit_l2_eta","recoB_fit_l2_phi"]
                   ],
      operation=["{0}/{1}","abs({0}-{1})",
                 "min(abs({0}-{1}),abs({0}-{2}))","deltaR({0},{1},{2},{3})",
                 "min(deltaR({0},{1},{2},{3}),deltaR({0},{1},{4},{5}))"
                ],
      createdBranches=["recoB_l_xy_sig","recoB_l1l2Dz","recoB_lKDz","recoB_l1l2Dr","recoB_lKDr"],
      checkForBCandBranch="recoB_l_xy" #if provided branch puts -99 when branch value is -99. eg Useful for evt where recoK is found but B not
    )
   process.append(CreateVars)
   return process  


def KEEMC (process,Jpsi=[],use_PF=False,use_1lowPt_1PF=False):
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.genDecayConstructorPython import genDecayConstructorPython
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.genRecoMatcher import genRecoMatcher
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.compositeRecoMatcher import compositeRecoMatcher
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.branchCreatorMC import branchCreatorMC

   cuts_on_lep = lambda l: True
   cuts_on_B = "True"
   cuts_on_B_vars = []
   if use_PF and not use_1lowPt_1PF:
     cuts_on_lep= lambda l: l.isPF == 1 and l.pfmvaId>-5000
     cuts_on_B_vars = ["recoE1_pfmvaId","recoE2_pfmvaId"]
     cuts_on_B = cuts_on_B+" and ( {0}>-300.5 or {1}>-300.5 )"
   elif use_1lowPt_1PF and not use_PF:
     cuts_on_lep= lambda l: ( (l.isPF == 1 and l.pfmvaId>-1.25) or ( l.isPF == 0 and l.isPFoverlap==0 and l.mvaId>-1.5) )
     cuts_on_B_vars = ["recoE1_isPF","recoE2_isPF"]
     cuts_on_B = cuts_on_B+" and ( ({0}==1 and {1}==0) or  ( {0}==0 and {1}==1) )"
   
   GenDecay = genDecayConstructorPython( momPdgId = 521,
                                   daughtersPdgId = [11, -11, 321],
                                   outputMomColl = "genB",
                                   intermediateDecay = Jpsi,
                                   trgMuonPtEtaThresholds = [], #was 7,1.6
                                   outputDaughterColls = ["genE1","genE2","genK"] 
    )                             
   process.append(GenDecay)   
   RecoE1 = genRecoMatcher( recoInput="Electron",
                             genInput = "genE1",
                             output = "recoE1",
                             branches = ["pt","eta","phi","vx","vy","vz","isPF","pfmvaId","isPFoverlap","mvaId"],
                             cuts=cuts_on_lep,
                             skipNotMatched=False
   )                             
   process.append(RecoE1)
   RecoE2 = genRecoMatcher( recoInput="Electron",
                             genInput = "genE2",
                             output = "recoE2",
                             branches = ["pt","eta","phi","vx","vy","vz","isPF","pfmvaId","isPFoverlap","mvaId"],
                             cuts=cuts_on_lep,
                             skipNotMatched=False
   )                             
   process.append(RecoE2)
   RecoK = genRecoMatcher( recoInput="ProbeTracks",
                             genInput = "genK",
                             output = "recoK",
                             branches = ["pt","eta","phi","vx","vy","vz"],
                             skipNotMatched=False
   )                             
   process.append(RecoK)
   RecoB = compositeRecoMatcher(   compositeColl = "BToKEE",
                             lepCompositeIdxs = ["l1Idx","l2Idx"],
                             hadronCompositeIdxs = ["kIdx"],
                             lepMatchedRecoIdxs = ["recoE1_Idx","recoE2_Idx"],
                             hadronMatchedRecoIdxs = ["recoK_Idx"],
                             outputColl = "recoB",
                             cuts_vars=cuts_on_B_vars,
                             cuts=cuts_on_B,
                             branches =["fit_pt","fit_eta","fit_phi","fit_mass",
                                         "l_xy","l_xy_unc","fit_cos2D","svprob",
                                         "fit_massErr","b_iso04", "mll_fullfit",
                                         "l1Idx","l2Idx","kIdx",
                                         "vtx_x","vtx_y","vtx_z",
                                         "fit_l1_pt","fit_l1_eta","fit_l1_phi",
                                         "l1_iso04",
                                         "fit_l2_pt","fit_l2_eta","fit_l2_phi",
                                         "l2_iso04",
                                         "fit_k_pt","fit_k_eta","fit_k_phi",
                                         "k_iso04",
                                        ],
                             sortTwoLepByIdx=True,
                             lepLabelsToSort = ["l1","l2"]# branches need to have lep labels between "_" eg fit_l1_pt or l1_iso - lep indexes also sorted
   )                                  
   process.append(RecoB)
   # in case of inf in L_xy/unc produces -99
   CreateVars = branchCreatorMC(
      inputBranches=[["recoB_l_xy","recoB_l_xy_unc"], ["recoE1_vz","recoE2_vz"],
                     ["recoK_vz","recoE1_vz","recoE2_vz"], 
                     ["recoE1_eta","recoE1_phi","recoE2_eta","recoE2_phi"], 
                     ["recoK_eta","recoK_phi","recoE1_eta","recoE1_phi","recoE2_eta","recoE2_phi"] ],
      operation=["{0}/{1}","abs({0}-{1})",
                 "min(abs({0}-{1}),abs({0}-{2}))",
                 "deltaR({0},{1},{2},{3})",
                 "min(deltaR({0},{1},{2},{3}),deltaR({0},{1},{4},{5}))"],
      createdBranches=["recoB_l_xy_sig","recoB_l1l2Dz","recoB_lKDz","recoB_l1l2Dr","recoB_lKDr"],
      checkForBCandBranch="recoB_l_xy" #if provided branch puts -99 when branch value is -99. eg Useful for evt where recoK is found but
    )
   process.append(CreateVars)
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.functionWrapper import functionWrapper
   TagVars = functionWrapper(
      functionName="TagVarsMC",
      collections=["ProbeTracks","TriggerMuon","recoB_fit_pt","recoB_fit_eta","recoB_fit_phi","recoB_fit_mass"],
      createdBranches=["recoB_TagMuEtRatio","recoB_TagMuDphi","recoB_TagMu4Prod"],
    )
   process.append(TagVars)
   ClosestTrkVars = functionWrapper(
      functionName="ClosestTrkVarsMC",
      collections=["ProbeTracks","BToKEE","recoB_Idx","Electron","recoB_l1Idx","recoB_l2Idx"],
      createdBranches=["recoB_l1_trk_mass","recoB_l2_trk_mass","recoB_trk_minxy1","recoB_trk_minxy2","recoB_trk_minxy3","recoB_trk_mean"],
   )
   process.append(ClosestTrkVars)
   return process  




########################################### B->K*ll #########################

def KstarMuMuMC (process):
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.genDecayConstructor import genDecayConstructor
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.genRecoMatcher import genRecoMatcher
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.compositeRecoMatcher import compositeRecoMatcher
   GenDecay = genDecayConstructor( momPdgId = 511,
                                   daughtersPdgId = [13, -13, 321,-211],
                                   outputMomColl = "genB",
                                   interDecay = ["313->321,-211"],
                                   outputDaughterColls = ["genMu1","genMu2","genK","genPi"] 
    )                             
   process.append(GenDecay)   
   RecoMu1 = genRecoMatcher( recoInput="Muon",
                             genInput = "genMu1",
                             output = "recoMu1",
                             branches = ["pt","eta","phi"]
   )                             
   process.append(RecoMu1)
   RecoMu2 = genRecoMatcher( recoInput="Muon",
                             genInput = "genMu2",
                             output = "recoMu2",
                             branches = ["pt","eta","phi"]
   )                             
   process.append(RecoMu2)
   RecoK = genRecoMatcher( recoInput="ProbeTracks",
                             genInput = "genK",
                             output = "recoK",
                             branches = ["pt","eta","phi"]
   )                             
   process.append(RecoK)
   RecoPi = genRecoMatcher( recoInput="ProbeTracks",
                             genInput = "genPi",
                             output = "recoPi",
                             branches = ["pt","eta","phi"]
   )
   process.append(RecoPi)
   RecoB = compositeRecoMatcher(   compositeColl = "BToKsMuMu",
                             lepCompositeIdxs = ["l1_idx","l2_idx"],
                             hadronCompositeIdxs = ["trk1_idx","trk2_idx"],
                             lepMatchedRecoIdxs = ["recoMu1_Idx","recoMu2_Idx"],
                             hadronMatchedRecoIdxs = ["recoK_Idx","recoPi_Idx"],
                             outputColl = "recoB",
                             branches = ["pt","eta","phi"]
   )                                  
   process.append(RecoB)
   return process  



################################### Kshort LL #################################
def KshortMuMuData ( process, cuts):
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionSkimmer import collectionSkimmer
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionEmbeder import collectionEmbeder
    BSkim = collectionSkimmer(input = "BToKshortMuMu",
                            output = "SkimBToKshortMuMu",
                            importedVariables = ["Kshort_svprob"],
                            importIds = ["kshort_idx"],
                            varnames = ["kshort_prob"],
                            selector = cuts,
                            branches = [ #B vars
                                        "fit_pt","fit_mass","fit_eta","fit_phi",
                                        "l_xy","l_xy_unc","fit_cos2D","svprob",
                                         # lep 
                                        "mll_fullfit","lep1pt_fullfit", 
                                        "lep1eta_fullfit","lep2pt_fullfit", 
                                        "lep2eta_fullfit","l1_idx", "l2_idx",
                                        # kshort
                                        "ptkshort_fullfit", "etakshort_fullfit",
                                        "mkshort_fullfit", "kshort_idx",
                                        "kshort_prob"
                                       ],
                   #         triggerMuonId = "TriggerMuon_trgMuonIndex",
                            flat = False
    )   
    process.append(BSkim)
    Mu1 = collectionEmbeder( inputColl = "Muon",
                             embededColl = "SkimBToKshortMuMu",
                             inputBranches = ["softMvaId","softId","triggerIdLoose"],
                             embededBranches = ["lep1softMvaId","lep1softId","lep1trigger"], 
                             embededCollIdx = "l1_idx"
    )
    Mu2 = collectionEmbeder( inputColl = "Muon",
                             embededColl = "SkimBToKshortMuMu",
                             inputBranches = ["softMvaId","softId","triggerIdLoose"],
                             embededBranches = ["lep2softMvaId","lep2softId","lep2trigger"], 
                             embededCollIdx = "l2_idx"
    )
    Kshort = collectionEmbeder( inputColl = "Kshort",
                             embededColl = "SkimBToKshortMuMu",
                             inputBranches = ["trk1_pt","trk2_pt"],
                             embededBranches = ["trk1pt","trk2pt"], 
                             embededCollIdx = "kshort_idx"
    )
    process.append(Mu1)
    process.append(Mu2)    
    process.append(Kshort)
    return process
