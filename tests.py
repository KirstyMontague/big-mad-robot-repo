

class RedundancyTests():

	def getTests(self):
		return self.tests

	def __init__(self):

		self.tests = []
		self.subbehaviour_tests = []

		self.subbehaviour_tests.append({
			"bt" : "probm2(seqm3(increaseDensity2, increaseDensity3, ifFoodToRight), goAwayFromNest7)",
			"trimmed" : "probm2(seqm2(increaseDensity2, increaseDensity3), goAwayFromNest7)",
			"fitness" : []
		})

		self.subbehaviour_tests.append({
			"bt" : "probm3(seqm2(selm3(probm3(ifInNest, ifGotFood, ifOnFood), seqm3(reduceDensity7, goAwayFromFood5, goAwayFromFood2), seqm4(gotoFood3, goAwayFromFood2, gotoFood3, ifNestToRight)), seqm2(probm3(goAwayFromFood5, gotoNest4, ifRobotToLeft), seqm3(gotoFood1, goAwayFromFood7, increaseDensity6))), probm4(seqm4(probm3(reduceDensity2, gotoNest1, reduceDensity5), selm3(gotoFood2, goAwayFromNest1, increaseDensity2), probm3(ifFoodToLeft, reduceDensity8, gotoNest2), seqm2(goAwayFromNest7, reduceDensity4)), seqm2(probm3(goAwayFromFood1, goAwayFromNest3, gotoFood2), selm2(goAwayFromFood2, gotoNest1)), probm3(seqm3(increaseDensity2, increaseDensity3, ifFoodToRight), probm4(increaseDensity6, gotoFood5, increaseDensity8, goAwayFromFood5), seqm2(increaseDensity2, goAwayFromFood1)), selm2(selm3(gotoFood3, ifNestToRight, gotoNest2), probm4(gotoFood8, ifNestToRight, reduceDensity7, ifNestToRight))), selm2(selm2(seqm3(goAwayFromNest7, goAwayFromFood7, reduceDensity3), seqm4(goAwayFromNest4, gotoFood8, goAwayFromNest8, increaseDensity1)), seqm2(probm4(gotoFood7, goAwayFromFood7, goAwayFromFood2, ifNestToRight), probm4(goAwayFromNest6, gotoNest1, gotoNest1, gotoFood7))))",
			"trimmed" : "",
			"fitness" : []
		})

		self.subbehaviour_tests.append({
			# caused combinatorial explosion before bug fix in replaceObsoleteConditionsWithStop 12/10/25
			"bt" : "selm2(seqm4(gotoFood1, gotoFood1, ifGotFood, seqm4(gotoFood1, gotoFood1, ifGotFood, gotoNest1)), probm4(probm4(probm4(ifInNest, increaseDensity1, increaseDensity1, seqm4(ifInNest, gotoFood1, increaseDensity1, probm4(probm4(probm4(ifInNest, ifInNest, ifGotFood, probm4(ifInNest, increaseDensity1, increaseDensity1, seqm4(ifInNest, gotoFood1, gotoFood1, probm4(probm4(probm4(probm4(ifInNest, increaseDensity1, increaseDensity1, seqm4(ifInNest, gotoFood1, gotoFood1, probm4(probm4(probm4(gotoFood1, ifInNest, probm4(seqm4(ifInNest, gotoFood1, gotoFood1, probm4(probm4(probm4(ifInNest, ifInNest, ifGotFood, ifGotFood), ifGotFood, ifGotFood, ifGotFood), ifOnFood, ifInNest, ifGotFood)), seqm4(gotoFood1, ifOnFood, gotoNest1, ifGotFood), ifGotFood, ifGotFood), ifGotFood), ifGotFood, ifGotFood, ifGotFood), ifOnFood, ifInNest, ifGotFood))), seqm4(gotoFood1, ifOnFood, gotoNest1, ifGotFood), ifOnFood, ifGotFood), increaseDensity1, gotoFood1, gotoFood1), ifOnFood, ifInNest, ifGotFood)))), ifGotFood, ifGotFood, ifGotFood), ifOnFood, ifInNest, ifGotFood))), seqm4(gotoFood1, ifOnFood, gotoNest1, ifGotFood), ifGotFood, ifGotFood), increaseDensity1, gotoFood1, gotoFood1))",
			"trimmed" : "selm2(seqm4(gotoFood1, gotoFood1, ifGotFood, seqm4(gotoFood1, gotoFood1, ifGotFood, gotoNest1)), probm4(probm4(probm4(ifInNest, increaseDensity1, increaseDensity1, seqm4(ifInNest, gotoFood1, increaseDensity1, probm4(probm4(probm4(ifInNest, ifInNest, ifInNest, probm4(ifInNest, increaseDensity1, increaseDensity1, seqm4(ifInNest, gotoFood1, gotoFood1, probm4(probm4(probm4(probm4(ifInNest, increaseDensity1, increaseDensity1, seqm4(ifInNest, gotoFood1, gotoFood1, probm4(probm4(probm4(gotoFood1, ifInNest, probm4(seqm4(ifInNest, gotoFood1, gotoFood1, probm4(probm4(probm4(ifInNest, ifInNest, ifInNest, ifInNest), ifInNest, ifInNest, ifInNest), ifInNest, ifInNest, ifInNest)), seqm3(gotoFood1, ifOnFood, gotoNest1), ifInNest, ifInNest), ifInNest), ifInNest, ifInNest, ifInNest), ifInNest, ifInNest, ifInNest))), seqm3(gotoFood1, ifOnFood, gotoNest1), ifInNest, ifInNest), increaseDensity1, gotoFood1, gotoFood1), ifInNest, ifInNest, ifInNest)))), ifInNest, ifInNest, ifInNest), ifInNest, ifInNest, ifInNest))), seqm3(gotoFood1, ifOnFood, gotoNest1), ifInNest, ifInNest), increaseDensity1, gotoFood1, gotoFood1))",
			"fitness" : [0.711111111111111, -118.48888888888887, 0.6222222222222221, 0.7011988888888888]
		})

		self.tests.append({
			"bt" : "seqm3(rr, seqm2(ifNestToLeft, seqm2(selm2(seqm2(seqm2(ifNestToLeft, selm2(selm2(seqm2(seqm2(seqm2(selm2(seqm2(seqm2(seqm2(seqm2(ifNestToLeft, rl), seqm2(seqm2(r, selm2(selm2(seqm2(seqm2(ifOnFood, rl), seqm2(r, r)), ifOnFood), r)), selm2(seqm2(seqm2(seqm2(seqm2(ifNestToLeft, rl), r), rl), seqm2(probm2(ifFoodToRight, seqm2(seqm2(seqm2(seqm2(ifNestToLeft, rl), ifNestToLeft), rl), seqm2(ifNestToLeft, rl))), ifNestToLeft)), ifOnFood))), r), seqm2(probm2(ifInNest, seqm2(seqm2(seqm2(seqm2(ifNestToLeft, ifNestToLeft), ifNestToLeft), rl), seqm2(ifNestToLeft, ifRobotToRight))), ifRobotToRight)), ifOnFood), seqm2(seqm2(ifNestToLeft, rl), r)), ifOnFood), seqm2(r, r)), ifOnFood), r)), seqm2(seqm2(r, seqm2(seqm2(ifNestToLeft, seqm2(seqm2(selm2(seqm2(seqm2(seqm2(seqm2(ifNestToLeft, rl), r), rl), seqm2(probm2(ifFoodToRight, seqm2(seqm2(seqm2(seqm2(ifNestToLeft, rl), ifNestToLeft), rl), seqm2(ifNestToLeft, rl))), ifNestToLeft)), ifOnFood), seqm2(r, ifNestToLeft)), ifOnFood)), ifOnFood)), ifNestToLeft)), ifOnFood), seqm2(seqm2(ifNestToLeft, r), seqm2(seqm2(seqm2(ifNestToLeft, seqm2(r, ifNestToLeft)), r), selm2(ifNestToLeft, ifOnFood))))), rl)",
			"trimmed" : "seqm3(rr, seqm2(ifNestToLeft, seqm2(selm2(seqm2(seqm2(ifNestToLeft, selm2(selm2(seqm2(seqm2(seqm2(selm2(seqm2(seqm2(seqm2(seqm2(ifNestToLeft, rl), seqm2(seqm2(r, selm2(selm2(seqm2(seqm2(ifOnFood, rl), seqm2(r, r)), ifOnFood), r)), selm2(seqm2(seqm2(seqm2(seqm2(ifNestToLeft, rl), r), rl), seqm2(probm2(ifFoodToRight, seqm2(seqm2(seqm2(seqm2(ifNestToLeft, rl), ifNestToLeft), rl), seqm2(ifNestToLeft, rl))), ifNestToLeft)), ifOnFood))), r), seqm2(probm2(ifInNest, seqm2(seqm2(seqm2(seqm2(ifNestToLeft, ifNestToLeft), ifNestToLeft), rl), seqm2(ifNestToLeft, ifRobotToRight))), ifRobotToRight)), ifOnFood), seqm2(seqm2(ifNestToLeft, rl), r)), ifOnFood), seqm2(r, r)), ifOnFood), r)), seqm2(seqm2(r, seqm2(seqm2(ifNestToLeft, seqm2(seqm2(selm2(seqm2(seqm2(seqm2(seqm2(ifNestToLeft, rl), r), rl), seqm2(probm2(ifFoodToRight, seqm2(seqm2(seqm2(seqm2(ifNestToLeft, rl), ifNestToLeft), rl), seqm2(ifNestToLeft, rl))), ifNestToLeft)), ifOnFood), seqm2(r, ifNestToLeft)), ifOnFood)), ifOnFood)), ifNestToLeft)), ifOnFood), seqm2(seqm2(ifNestToLeft, r), seqm2(seqm2(seqm2(ifNestToLeft, seqm2(r, ifNestToLeft)), r), selm2(ifNestToLeft, ifOnFood))))), rl)",
			"fitness" : [0.5627290888888888, -11.9, 13.788888888888888, 0.5498492444444444]
		})

		self.tests.append({
			"bt" : "selm2(fr, probm3(ifNestToRight, f, ifNestToRight))",
			"trimmed" : "fr",
			"fitness" : [0.4975353333333333, 0.597520111111111, 0.5642124111111111, 0.5024646555555556]
		})

		self.tests.append({
			"bt" : "seqm4(seqm4(rr, r, ifInNest, probm3(probm3(ifFoodToRight, ifFoodToRight, ifInNest), selm3(probm3(ifInNest, ifNestToLeft, ifNestToRight), ifRobotToLeft, ifFoodToRight), ifInNest)), ifNestToRight, selm3(probm4(fr, ifNestToLeft, probm3(ifRobotToLeft, rl, f), ifNestToRight), ifRobotToLeft, probm3(rr, ifFoodToRight, ifRobotToLeft)), selm3(selm3(fr, ifRobotToLeft, fl), r, ifRobotToLeft))",
			"trimmed" : "seqm4(seqm4(rr, r, ifInNest, probm3(probm3(ifFoodToRight, ifFoodToRight, ifInNest), selm3(probm3(ifInNest, ifNestToLeft, ifNestToRight), ifRobotToLeft, ifFoodToRight), ifInNest)), ifNestToRight, selm3(probm4(fr, ifNestToLeft, probm3(ifRobotToLeft, rl, f), ifNestToRight), ifRobotToLeft, probm3(rr, ifFoodToRight, ifRobotToLeft)), fr)",
			"fitness" : [0.0,0.0,0.0,0.0]
		})

		self.tests.append({
			"bt" : "probm3(seqm3(seqm3(r, ifRobotToLeft, ifInNest), selm4(probm4(rr, r, probm2(seqm3(ifInNest, seqm3(seqm3(r, ifRobotToLeft, seqm2(fr, fl)), selm2(rl, ifInNest), ifNestToRight), ifFoodToLeft), stop), ifRobotToLeft), ifInNest, seqm2(fr, fl), ifNestToLeft), probm2(seqm3(selm4(fl, ifInNest, ifInNest, ifRobotToLeft), ifNestToLeft, ifInNest), stop)), selm3(seqm3(r, rl, ifNestToLeft), seqm4(fl, fl, ifInNest, selm3(ifInNest, ifNestToLeft, rl)), probm3(ifFoodToRight, fl, seqm3(seqm3(ifOnFood, ifRobotToLeft, ifInNest), selm2(ifInNest, ifInNest), ifNestToRight))), seqm3(ifInNest, probm3(fr, fl, ifNestToRight), seqm4(ifFoodToLeft, ifNestToRight, r, ifNestToLeft)))",
			"trimmed" : "probm3(seqm3(seqm3(r, ifRobotToLeft, ifInNest), selm3(probm4(rr, r, probm2(seqm3(ifInNest, seqm3(seqm3(r, ifRobotToLeft, seqm2(fr, fl)), rl, ifNestToRight), ifFoodToLeft), stop), ifRobotToLeft), ifInNest, seqm2(fr, fl)), probm2(fl, stop)), selm3(seqm3(r, rl, ifNestToLeft), seqm4(fl, fl, ifInNest, selm3(ifInNest, ifNestToLeft, rl)), probm3(ifInNest, fl, ifInNest)), seqm3(ifInNest, probm3(fr, fl, ifNestToRight), seqm3(ifFoodToLeft, ifNestToRight, r)))",
			"fitness" : [0.5128149000000001, -15.822222222222223, 3.088888888888889, 0.5214352555555557]
		})

		self.tests.append({
			"bt" : "probm2(seqm3(ifNestToRight, seqm3(r, ifInNest, rr), seqm3(ifNestToRight, rl, ifOnFood)), selm2(seqm3(ifNestToRight, selm2(seqm3(ifNestToRight, rr, seqm3(r, rr, seqm3(ifNestToRight, seqm3(ifNestToRight, rr, ifRobotToRight), seqm3(ifNestToRight, rr, probm4(ifNestToRight, r, f, ifNestToRight))))), selm3(ifNestToRight, selm3(ifInNest, seqm3(ifNestToRight, probm3(ifNestToLeft, rr, ifNestToRight), seqm3(ifNestToRight, ifNestToLeft, probm4(ifNestToRight, rr, ifFoodToLeft, ifNestToRight))), rl), rr)), seqm3(r, rr, seqm3(ifNestToRight, seqm3(ifNestToRight, rr, ifRobotToRight), seqm3(selm3(ifInNest, ifNestToRight, rl), selm2(ifNestToRight, seqm3(r, seqm3(rl, rr, rr), ifNestToRight)), probm4(ifFoodToRight, r, rl, ifNestToRight))))), selm3(ifNestToRight, selm3(ifInNest, ifNestToRight, rl), ifRobotToLeft)))",
			"trimmed" : "probm2(seqm3(ifNestToRight, seqm3(r, ifInNest, rr), seqm2(ifNestToRight, rl)), selm2(seqm3(ifNestToRight, selm2(seqm3(ifNestToRight, rr, seqm3(r, rr, seqm3(ifNestToRight, seqm3(ifNestToRight, rr, ifRobotToRight), seqm3(ifNestToRight, rr, probm4(ifNestToRight, r, f, ifNestToRight))))), selm2(ifNestToRight, selm3(ifInNest, seqm3(ifNestToRight, probm3(ifNestToLeft, rr, ifNestToRight), seqm3(ifNestToRight, ifNestToLeft, probm4(ifNestToRight, rr, ifFoodToLeft, ifNestToRight))), rl))), seqm3(r, rr, seqm3(ifNestToRight, seqm3(ifNestToRight, rr, ifRobotToRight), seqm3(selm3(ifInNest, ifNestToRight, rl), selm2(ifNestToRight, seqm3(r, seqm3(rl, rr, rr), ifNestToRight)), probm4(ifFoodToRight, r, rl, ifNestToRight))))), selm2(ifNestToRight, selm3(ifInNest, ifNestToRight, rl))))",
			"fitness" : [0.5538614000000001, -8.044444444444444, -0.8555555555555557, 0.7648123333333332]
		})

		self.tests.append({
			"bt" : "seqm3(selm2(ifNestToRight, seqm4(ifNestToLeft, fl, ifNestToRight, probm2(f, selm4(ifOnFood, ifFoodToRight, fr, f)))), probm2(f, selm4(selm3(ifFoodToRight, fr, selm2(ifNestToRight, seqm4(ifNestToLeft, ifOnFood, seqm2(ifFoodToRight, ifNestToRight), seqm4(seqm4(ifRobotToLeft, fr, ifRobotToRight, r), probm4(ifRobotToLeft, ifOnFood, fl, ifInNest), selm2(ifOnFood, fr), probm4(ifOnFood, ifInNest, ifNestToLeft, ifInNest))))), f, ifNestToRight, ifFoodToRight)), seqm2(f, selm4(ifOnFood, ifFoodToRight, fr, probm2(ifOnFood, f))))",
			"trimmed" : "seqm3(selm2(ifNestToRight, seqm4(ifNestToLeft, fl, ifNestToRight, probm2(f, selm3(ifOnFood, ifFoodToRight, fr)))), probm2(f, selm2(ifFoodToRight, fr)), seqm2(f, selm3(ifOnFood, ifFoodToRight, fr)))",
			"fitness" : [0.5437501888888888, 13.633333333333331, 0.9666666666666665, 0.7555296222222221]
		})

		self.tests.append({
			"bt" : "selm4(seqm2(seqm2(ifNestToLeft, selm3(probm3(seqm4(ifInNest, r, ifInNest, r), selm2(selm3(seqm2(selm2(rl, ifRobotToLeft), r), ifOnFood, ifRobotToLeft), fl), selm2(seqm3(seqm4(seqm4(ifInNest, seqm2(probm4(ifNestToRight, ifRobotToLeft, rl, ifRobotToLeft), fl), r, r), rr, selm2(rl, ifNestToLeft), ifRobotToLeft), selm2(selm3(selm2(selm3(probm3(seqm4(seqm2(seqm2(ifFoodToLeft, selm3(probm3(seqm4(ifInNest, rl, ifNestToLeft, r), selm2(probm3(selm2(rl, r), ifOnFood, rl), fl), selm2(seqm3(seqm4(r, ifRobotToLeft, ifInNest, ifRobotToLeft), selm2(selm3(selm3(rr, rl, rl), rl, rl), fr), probm2(probm3(ifNestToLeft, ifRobotToLeft, ifNestToLeft), selm2(ifRobotToLeft, stop))), r)), ifFoodToRight, r)), selm3(selm2(selm3(seqm2(selm2(r, r), r), ifOnFood, rl), fl), ifInNest, rl)), rl, ifNestToLeft, r), selm2(selm3(selm2(ifNestToRight, selm3(selm2(rl, r), ifNestToRight, rl)), ifNestToRight, rl), fl), selm2(seqm3(seqm4(r, ifRobotToLeft, ifNestToRight, ifRobotToLeft), selm2(selm3(seqm2(selm2(ifNestToLeft, probm2(seqm2(ifOnFood, rl), seqm4(r, rr, stop, ifInNest))), seqm3(r, r, seqm4(seqm4(ifInNest, seqm4(seqm2(ifNestToRight, r), fl, f, probm3(ifNestToRight, rr, rl)), selm3(seqm2(r, r), rl, rl), r), r, ifNestToRight, ifRobotToLeft))), rl, rl), fr), selm2(ifNestToLeft, stop)), r)), ifOnFood, selm3(ifOnFood, ifRobotToLeft, rr)), seqm4(f, rr, stop, rl)), rl, f), fr), selm2(ifNestToLeft, ifInNest)), r)), rl, r)), selm3(selm2(selm3(seqm2(selm2(seqm2(seqm2(ifNestToLeft, selm3(probm3(seqm4(seqm2(seqm2(ifNestToLeft, selm3(probm3(seqm4(ifInNest, rl, ifNestToLeft, r), selm2(selm3(selm2(rl, r), ifOnFood, rl), fl), selm2(seqm3(seqm4(r, ifRobotToLeft, ifInNest, ifFoodToRight), selm2(selm3(selm3(seqm2(r, r), rl, rl), rl, rl), seqm4(ifInNest, rl, stop, r)), probm2(probm3(ifNestToLeft, ifRobotToLeft, ifNestToLeft), selm2(ifRobotToLeft, fl))), r)), ifFoodToRight, r)), selm3(selm2(selm3(seqm2(selm2(rl, r), r), ifOnFood, rl), fl), selm3(ifOnFood, ifRobotToLeft, rr), rl)), rl, ifNestToLeft, r), selm2(selm3(selm2(rl, r), selm3(ifNestToRight, stop, fl), rl), fl), selm2(seqm3(seqm4(r, ifRobotToLeft, ifNestToRight, ifRobotToLeft), selm2(selm3(seqm2(selm2(ifNestToLeft, probm2(seqm2(f, rl), seqm4(r, rr, stop, ifInNest))), seqm3(rr, r, seqm4(seqm4(ifInNest, seqm4(selm2(ifNestToRight, r), fl, selm3(selm3(rr, rl, rl), rl, ifFoodToRight), probm3(ifNestToRight, rr, rl)), r, r), r, ifNestToRight, ifRobotToLeft))), rl, ifOnFood), ifRobotToLeft), rl), r)), ifFoodToRight, r)), selm3(selm2(selm3(seqm2(selm2(rl, r), r), ifOnFood, rl), fl), ifInNest, rl)), rl), r), rl, selm3(r, ifRobotToLeft, rr)), fl), ifInNest, selm2(rl, r))), ifInNest, ifNestToLeft, rr)",
			"trimmed" : "selm4(seqm2(seqm2(ifNestToLeft, selm2(probm3(seqm4(ifInNest, r, ifInNest, r), seqm2(rl, r), selm2(seqm3(seqm4(seqm4(ifInNest, seqm2(probm4(ifNestToRight, ifRobotToLeft, rl, ifRobotToLeft), fl), r, r), rr, rl, ifRobotToLeft), selm3(probm3(seqm4(seqm2(seqm2(ifFoodToLeft, selm3(probm3(seqm4(ifInNest, rl, ifNestToLeft, r), selm2(probm3(rl, ifOnFood, rl), fl), selm2(seqm3(seqm4(r, ifRobotToLeft, ifInNest, ifRobotToLeft), rr, probm2(probm3(ifNestToLeft, ifRobotToLeft, ifNestToLeft), selm2(ifRobotToLeft, stop))), r)), ifFoodToRight, r)), seqm2(r, r)), rl, ifNestToLeft, r), selm2(ifNestToRight, rl), selm2(seqm3(seqm4(r, ifRobotToLeft, ifNestToRight, ifRobotToLeft), selm2(seqm2(selm2(ifNestToLeft, probm2(seqm2(ifOnFood, rl), seqm4(r, rr, stop, ifInNest))), seqm3(r, r, seqm4(seqm4(ifInNest, seqm4(seqm2(ifNestToRight, r), fl, f, probm3(ifNestToRight, rr, rl)), seqm2(r, r), r), r, ifNestToRight, ifRobotToLeft))), rl), selm2(ifNestToLeft, stop)), r)), ifOnFood, selm3(ifOnFood, ifRobotToLeft, rr)), selm2(ifNestToLeft, ifInNest)), r)), rl)), seqm2(selm2(seqm2(seqm2(ifNestToLeft, selm3(probm3(seqm4(seqm2(seqm2(ifNestToLeft, selm3(probm3(seqm4(ifInNest, rl, ifNestToLeft, r), rl, selm2(seqm3(seqm4(r, ifRobotToLeft, ifInNest, ifFoodToRight), seqm2(r, r), probm2(probm3(ifNestToLeft, ifRobotToLeft, ifNestToLeft), selm2(ifRobotToLeft, fl))), r)), ifFoodToRight, r)), seqm2(rl, r)), rl, ifNestToLeft, r), rl, selm2(seqm3(seqm4(r, ifRobotToLeft, ifNestToRight, ifRobotToLeft), selm2(seqm2(selm2(ifNestToLeft, probm2(seqm2(f, rl), seqm4(r, rr, stop, ifInNest))), seqm3(rr, r, seqm4(seqm4(ifInNest, seqm4(selm2(ifNestToRight, r), fl, rr, probm3(ifNestToRight, rr, rl)), r, r), r, ifNestToRight, ifRobotToLeft))), rl), rl), r)), ifFoodToRight, r)), seqm2(rl, r)), rl), r)), ifInNest, ifNestToLeft, rr)",
			"fitness" : [0.5559078888888889, -11.366666666666667, 2.1444444444444444, 0.6946360111111113]
		})

		self.tests.append({
			"bt" : "probm2(selm4(ifNestToRight, probm3(selm4(ifNestToRight, probm3(seqm3(ifFoodToLeft, probm4(ifRobotToRight, probm3(selm2(selm2(ifInNest, ifFoodToLeft), selm2(selm2(rl, r), rl)), selm2(ifNestToRight, selm2(selm2(ifNestToLeft, rr), ifNestToRight)), r), ifFoodToLeft, ifRobotToRight), selm2(rr, probm3(seqm3(ifNestToRight, selm4(ifNestToRight, probm3(seqm3(rl, probm3(seqm3(seqm2(ifInNest, r), ifNestToRight, ifInNest), ifInNest, ifInNest), rl), seqm4(ifOnFood, f, rl, rl), r), probm4(probm3(f, selm4(ifNestToRight, ifInNest, probm2(ifNestToLeft, ifInNest), rl), r), seqm4(r, probm4(ifRobotToRight, probm3(selm2(ifInNest, ifOnFood), selm2(fl, rl), rr), ifFoodToLeft, r), ifInNest, ifNestToRight), probm2(ifOnFood, fl), seqm4(stop, f, ifInNest, r)), rr), selm2(ifOnFood, selm2(seqm3(selm4(ifNestToRight, probm3(seqm3(ifInNest, r, ifInNest), ifInNest, ifInNest), selm2(rl, ifInNest), seqm2(fl, rl)), ifInNest, stop), rl))), ifInNest, seqm2(ifInNest, r)))), rl, ifInNest), selm2(rl, r), rl), ifNestToRight, seqm4(ifFoodToRight, ifFoodToLeft, r, ifInNest)), ifInNest, rl), selm2(ifInNest, r))",
			"trimmed" : "probm2(selm4(ifNestToRight, probm3(selm3(ifNestToRight, probm3(seqm3(ifFoodToLeft, probm4(ifRobotToRight, probm3(selm2(selm2(ifInNest, ifFoodToLeft), rl), selm2(ifNestToRight, selm2(ifNestToLeft, rr)), r), ifFoodToLeft, ifRobotToRight), rr), rl, ifInNest), rl), ifNestToRight, seqm4(ifFoodToRight, ifFoodToLeft, r, ifInNest)), ifInNest, rl), selm2(ifInNest, r))",
			"fitness" : [0.5067850555555556, -17.988888888888887, -6.977777777777777, 0.7413316000000002]
		})

		self.tests.append({
			"bt" : "probm3(probm4(selm3(probm4(stop, fr, ifNestToRight, ifNestToLeft), r, ifNestToLeft), seqm3(seqm4(fl, ifOnFood, stop, r), probm4(ifFoodToLeft, r, probm2(probm3(ifRobotToLeft, r, stop), probm3(ifFoodToRight, ifInNest, ifFoodToLeft)), f), probm4(fl, r, ifNestToLeft, f)), seqm4(seqm4(ifNestToLeft, ifFoodToLeft, seqm4(fl, stop, stop, probm4(selm3(probm4(stop, fr, ifNestToRight, ifRobotToLeft), r, ifNestToLeft), seqm3(seqm4(fl, stop, stop, r), probm4(ifFoodToLeft, r, ifNestToRight, fl), probm4(fl, r, ifNestToLeft, ifInNest)), seqm4(ifNestToLeft, selm2(ifInNest, ifFoodToRight), ifNestToRight, ifInNest), selm2(selm2(rl, ifNestToLeft), seqm4(rr, ifNestToLeft, r, ifFoodToLeft)))), f), selm2(rl, ifFoodToRight), ifFoodToRight, ifNestToLeft), ifFoodToLeft), selm4(seqm4(ifFoodToRight, ifRobotToLeft, ifInNest, seqm3(seqm4(seqm3(ifFoodToLeft, r, seqm3(selm4(rl, f, ifOnFood, rr), selm4(fl, rr, fl, ifOnFood), selm4(ifRobotToLeft, ifNestToLeft, stop, rl))), ifOnFood, seqm4(rr, ifInNest, ifOnFood, ifFoodToRight), ifFoodToRight), seqm2(probm3(ifFoodToRight, f, fl), seqm4(fl, seqm4(ifInNest, ifFoodToLeft, ifRobotToLeft, f), f, ifRobotToLeft)), selm3(ifInNest, probm2(ifNestToLeft, ifFoodToRight), ifRobotToRight))), seqm2(ifNestToLeft, seqm4(fl, f, ifFoodToRight, ifInNest)), probm3(ifRobotToLeft, selm2(fr, ifNestToLeft), probm3(ifNestToLeft, ifOnFood, ifNestToRight)), probm4(probm3(ifRobotToRight, ifFoodToRight, seqm4(ifOnFood, f, ifNestToRight, ifRobotToLeft)), probm4(ifNestToLeft, probm2(probm2(ifFoodToRight, ifRobotToRight), seqm4(ifInNest, rl, ifNestToRight, f)), seqm4(ifFoodToRight, ifRobotToLeft, f, seqm4(ifFoodToRight, ifRobotToLeft, f, f)), fl), ifNestToLeft, seqm4(seqm4(seqm4(ifInNest, ifFoodToLeft, seqm4(ifInNest, ifFoodToLeft, ifRobotToLeft, r), fr), selm2(ifNestToRight, fl), ifNestToLeft, ifNestToLeft), ifFoodToLeft, f, fl))), seqm3(seqm4(seqm3(ifFoodToLeft, ifRobotToLeft, rl), seqm4(ifRobotToRight, fl, fl, ifInNest), seqm4(ifInNest, rl, ifNestToRight, ifNestToRight), probm2(stop, fr)), seqm2(seqm4(ifFoodToRight, ifRobotToLeft, f, f), seqm4(ifFoodToRight, ifRobotToLeft, ifInNest, seqm3(seqm4(seqm3(ifRobotToLeft, r, rl), ifOnFood, seqm4(rr, rr, ifOnFood, ifFoodToRight), ifOnFood), seqm2(probm3(f, f, fl), seqm4(ifFoodToRight, ifRobotToLeft, f, ifRobotToLeft)), selm3(probm4(fr, rl, f, f), probm2(ifNestToLeft, ifNestToLeft), fr)))), probm4(stop, ifFoodToRight, f, ifInNest)))",
			"trimmed" : "probm3(probm4(selm2(probm4(stop, fr, ifNestToRight, ifNestToLeft), r), seqm3(seqm4(fl, ifOnFood, stop, r), probm4(ifFoodToLeft, r, probm2(probm3(ifRobotToLeft, r, stop), probm3(ifFoodToRight, ifInNest, ifFoodToLeft)), f), probm4(fl, r, ifInNest, f)), seqm2(seqm4(ifNestToLeft, ifFoodToLeft, seqm4(fl, stop, stop, probm4(selm2(probm4(stop, fr, ifNestToRight, ifRobotToLeft), r), seqm3(seqm4(fl, stop, stop, r), probm4(ifFoodToLeft, r, ifNestToRight, fl), probm4(fl, r, ifNestToLeft, ifInNest)), seqm4(ifNestToLeft, selm2(ifInNest, ifFoodToRight), ifNestToRight, ifInNest), rl)), f), rl), ifInNest), selm4(seqm4(ifFoodToRight, ifRobotToLeft, ifInNest, seqm3(seqm4(seqm3(ifFoodToLeft, r, seqm3(rl, fl, selm3(ifRobotToLeft, ifNestToLeft, stop))), ifOnFood, seqm4(rr, ifInNest, ifOnFood, ifFoodToRight), ifFoodToRight), seqm2(probm3(ifFoodToRight, f, fl), seqm4(fl, seqm4(ifInNest, ifFoodToLeft, ifRobotToLeft, f), f, ifRobotToLeft)), selm3(ifInNest, probm2(ifNestToLeft, ifFoodToRight), ifRobotToRight))), seqm2(ifNestToLeft, seqm4(fl, f, ifFoodToRight, ifInNest)), probm3(ifRobotToLeft, fr, probm3(ifNestToLeft, ifOnFood, ifNestToRight)), probm4(probm3(ifInNest, ifInNest, seqm2(ifOnFood, f)), probm4(ifInNest, probm2(probm2(ifInNest, ifInNest), seqm4(ifInNest, rl, ifNestToRight, f)), seqm4(ifFoodToRight, ifRobotToLeft, f, seqm4(ifFoodToRight, ifRobotToLeft, f, f)), fl), ifInNest, seqm4(seqm4(seqm4(ifInNest, ifFoodToLeft, seqm4(ifInNest, ifFoodToLeft, ifRobotToLeft, r), fr), selm2(ifNestToRight, fl), ifNestToLeft, ifNestToLeft), ifFoodToLeft, f, fl))), seqm3(seqm4(seqm3(ifFoodToLeft, ifRobotToLeft, rl), seqm4(ifRobotToRight, fl, fl, ifInNest), seqm4(ifInNest, rl, ifNestToRight, ifNestToRight), probm2(stop, fr)), seqm2(seqm4(ifFoodToRight, ifRobotToLeft, f, f), seqm4(ifFoodToRight, ifRobotToLeft, ifInNest, seqm3(seqm4(seqm3(ifRobotToLeft, r, rl), ifOnFood, seqm4(rr, rr, ifOnFood, ifFoodToRight), ifOnFood), seqm2(probm3(f, f, fl), seqm4(ifFoodToRight, ifRobotToLeft, f, ifRobotToLeft)), probm4(fr, rl, f, f)))), probm4(stop, ifInNest, f, ifInNest)))",
			"fitness" : [0.5070581, 1.922222222222222, -2.9555555555555557, 0.7745563999999999]
		})

		self.tests.append({
			"bt" : "seqm4(probm3(selm3(rr, ifNestToRight, rr), rr, r), selm4(ifNestToRight, rl, ifNestToLeft, rr), ifNestToLeft, rl)",
			"trimmed" : "seqm4(probm3(rr, rr, r), selm2(ifNestToRight, rl), ifNestToLeft, rl)",
			"fitness" : [0.546722188888889, -6.588888888888889, -5.9222222222222225, 0.5257987555555557]
		})

		self.tests.append({
			"bt" : "seqm4(seqm3(probm2(stop, probm3(ifInNest, ifNestToRight, fr)), selm4(ifInNest, ifNestToLeft, fr, probm3(ifNestToLeft, rr, rr)), seqm3(seqm4(ifNestToLeft, fl, ifFoodToLeft, fl), probm3(ifNestToLeft, ifRobotToRight, r), selm3(seqm4(ifFoodToLeft, ifNestToLeft, rl, ifOnFood), f, ifRobotToRight))), selm2(seqm3(ifInNest, ifNestToRight, ifRobotToLeft), fl), selm3(selm4(fl, r, seqm2(ifNestToLeft, rr), seqm2(ifOnFood, fl)), probm3(probm3(fl, ifRobotToLeft, rr), seqm2(ifRobotToRight, ifOnFood), ifFoodToRight), seqm4(selm3(fl, ifFoodToLeft, ifNestToLeft), probm4(fr, ifRobotToRight, f, ifFoodToLeft), f, probm2(ifInNest, rr))), seqm4(probm3(probm3(ifFoodToLeft, ifNestToRight, ifOnFood), probm4(fl, ifRobotToLeft, seqm3(ifFoodToLeft, ifNestToRight, ifRobotToRight), ifNestToLeft), probm3(rl, f, selm3(fl, fr, ifNestToLeft))), seqm4(ifNestToLeft, f, probm4(fl, ifFoodToLeft, r, ifNestToLeft), seqm4(ifRobotToRight, ifOnFood, ifFoodToLeft, seqm3(ifFoodToRight, ifNestToRight, ifRobotToRight))), seqm4(seqm4(ifOnFood, rl, fr, probm3(ifFoodToRight, rr, rr)), seqm4(ifFoodToLeft, rr, ifRobotToRight, stop), probm2(rr, ifRobotToLeft), stop), stop))",
			"trimmed" : "seqm4(seqm3(probm2(stop, probm3(ifInNest, ifNestToRight, fr)), selm3(ifInNest, ifNestToLeft, fr), seqm3(seqm4(ifNestToLeft, fl, ifFoodToLeft, fl), probm3(ifNestToLeft, ifRobotToRight, r), selm2(seqm4(ifFoodToLeft, ifNestToLeft, rl, ifOnFood), f))), selm2(seqm3(ifInNest, ifNestToRight, ifRobotToLeft), fl), fl, seqm4(probm3(probm3(ifFoodToLeft, ifNestToRight, ifOnFood), probm4(fl, ifRobotToLeft, seqm3(ifFoodToLeft, ifNestToRight, ifRobotToRight), ifNestToLeft), probm3(rl, f, fl)), seqm4(ifNestToLeft, f, probm4(fl, ifFoodToLeft, r, ifNestToLeft), seqm4(ifRobotToRight, ifOnFood, ifFoodToLeft, seqm3(ifFoodToRight, ifNestToRight, ifRobotToRight))), seqm4(seqm4(ifOnFood, rl, fr, probm3(ifFoodToRight, rr, rr)), seqm4(ifFoodToLeft, rr, ifRobotToRight, stop), probm2(rr, ifRobotToLeft), stop), stop))",
			"fitness" : [0.5259182111111109, 0.5555555555555556, -2.6444444444444444, 0.6592900888888888]
		})

		self.tests.append({
			"bt" : "selm4(seqm2(selm3(ifInNest, ifOnFood, f), seqm2(selm3(ifInNest, ifOnFood, fr), ifInNest)), ifNestToRight, fl, probm2(f, seqm2(selm3(ifInNest, ifOnFood, ifFoodToRight), ifOnFood)))",
			"trimmed" : "selm3(seqm2(selm3(ifInNest, ifOnFood, f), seqm2(selm3(ifInNest, ifOnFood, fr), ifInNest)), ifNestToRight, fl)",
			"fitness" : [0.5305057555555555, 6.2555555555555555, 0.5777777777777777, 0.8356987111111109]
		})

		self.tests.append({
			"bt" : "probm4(seqm3(selm2(fl, ifOnFood), selm2(ifRobotToRight, stop), seqm3(ifRobotToLeft, ifNestToLeft, ifNestToRight)), selm4(seqm3(selm2(fl, ifOnFood), selm2(stop, stop), ifNestToRight), ifOnFood, stop, fr), selm3(probm4(ifFoodToRight, ifRobotToRight, fl, stop), probm4(ifRobotToRight, selm2(ifNestToLeft, stop), ifOnFood, fr), probm2(rr, ifRobotToLeft)), selm2(seqm2(rr, ifRobotToLeft), probm4(ifRobotToLeft, r, ifRobotToRight, ifRobotToLeft)))",
			"trimmed" : "probm4(seqm2(fl, selm2(ifRobotToRight, stop)), selm3(seqm3(fl, stop, ifNestToRight), ifOnFood, stop), selm3(probm4(ifFoodToRight, ifRobotToRight, fl, stop), probm4(ifRobotToRight, selm2(ifNestToLeft, stop), ifOnFood, fr), probm2(rr, ifInNest)), selm2(seqm2(rr, ifRobotToLeft), probm4(ifInNest, r, ifInNest, ifInNest)))",
			"fitness" : [0.5003987444444443, -0.7777777777777779, 20.18888888888889, 0.5343835777777777]
		})

		self.tests.append({
			"bt" : "probm2(seqm3(probm3(selm3(ifNestToRight, rr, seqm4(stop, fr, ifNestToLeft, ifNestToLeft)), seqm4(f, ifInNest, fl, ifFoodToRight), selm4(fl, seqm4(f, ifFoodToRight, fl, ifFoodToRight), probm3(seqm3(probm3(selm3(ifNestToRight, rr, ifRobotToRight), seqm4(stop, ifNestToLeft, fr, ifFoodToRight), fl), probm3(seqm3(ifRobotToRight, ifNestToLeft, stop), selm2(ifRobotToRight, fl), seqm4(stop, ifNestToLeft, fl, ifNestToRight)), seqm3(ifFoodToLeft, ifOnFood, probm2(ifOnFood, ifOnFood))), probm2(stop, ifFoodToRight), seqm4(selm3(ifNestToLeft, fr, r), ifNestToLeft, fl, f)), seqm4(stop, ifNestToLeft, f, ifNestToRight))), probm3(seqm3(ifNestToLeft, ifNestToLeft, stop), selm2(ifRobotToRight, fl), seqm4(ifRobotToLeft, ifNestToLeft, seqm4(ifRobotToLeft, ifNestToLeft, fl, ifNestToRight), ifNestToRight)), probm2(seqm3(ifNestToRight, ifRobotToLeft, rr), seqm3(ifRobotToLeft, seqm4(selm4(selm2(rr, fr), selm4(fr, ifNestToLeft, ifRobotToLeft, f), selm2(f, ifInNest), seqm2(stop, ifRobotToRight)), ifRobotToLeft, ifOnFood, ifFoodToRight), ifRobotToLeft))), probm2(fr, selm2(selm3(ifNestToLeft, fr, f), ifFoodToLeft)))",
			"trimmed" : "probm2(seqm3(probm3(selm2(ifNestToRight, rr), seqm4(f, ifInNest, fl, ifFoodToRight), fl), probm3(seqm3(ifNestToLeft, ifNestToLeft, stop), selm2(ifRobotToRight, fl), seqm4(ifRobotToLeft, ifNestToLeft, seqm4(ifRobotToLeft, ifNestToLeft, fl, ifNestToRight), ifNestToRight)), probm2(seqm3(ifNestToRight, ifRobotToLeft, rr), seqm2(ifRobotToLeft, rr))), probm2(fr, selm2(ifNestToLeft, fr)))",
			"fitness" : [0.5180064111111111, 5.911111111111111, -1.1111111111111112, 0.5778998888888889]
		})

		self.tests.append({
			"bt" : "seqm3(selm2(seqm3(selm4(ifFoodToLeft, rl, ifRobotToRight, ifRobotToRight), seqm2(f, ifInNest), seqm3(f, f, rr)), seqm4(probm2(rr, fl), seqm4(f, f, ifNestToRight, fr), seqm4(ifRobotToLeft, ifInNest, ifOnFood, seqm3(probm2(r, ifRobotToLeft), ifOnFood, probm2(fr, rl))), probm3(rl, f, ifRobotToLeft))), probm4(probm4(seqm4(r, fl, stop, seqm2(ifRobotToRight, seqm4(f, f, ifInNest, rl))), selm2(ifRobotToRight, stop), seqm4(stop, rr, f, fr), seqm3(probm2(f, rl), selm3(rl, ifNestToRight, r), probm2(f, rl))), ifOnFood, selm3(seqm4(ifRobotToLeft, fr, ifFoodToLeft, fl), probm4(f, ifRobotToRight, ifFoodToLeft, ifNestToLeft), selm2(rr, f)), seqm3(ifInNest, selm3(ifOnFood, probm2(rr, fl), ifRobotToRight), probm2(rr, probm4(seqm4(ifFoodToRight, probm4(selm2(ifRobotToRight, f), seqm3(ifNestToRight, seqm2(ifRobotToRight, ifRobotToRight), seqm3(f, f, stop)), probm3(seqm4(f, ifRobotToLeft, ifNestToRight, fr), selm2(r, ifRobotToLeft), ifNestToRight), f), f, r), ifRobotToLeft, f, probm3(rl, ifInNest, selm3(ifInNest, seqm4(f, ifNestToRight, ifNestToLeft, ifRobotToRight), seqm4(f, stop, ifInNest, rr))))))), seqm2(seqm2(stop, ifNestToRight), selm3(selm2(ifRobotToRight, rr), probm2(r, seqm4(f, f, ifInNest, rl)), ifRobotToRight)))",
			"trimmed" : "seqm3(selm2(seqm3(selm2(ifFoodToLeft, rl), seqm2(f, ifInNest), seqm3(f, f, rr)), seqm4(probm2(rr, fl), seqm4(f, f, ifNestToRight, fr), seqm4(ifRobotToLeft, ifInNest, ifOnFood, seqm3(probm2(r, ifRobotToLeft), ifOnFood, probm2(fr, rl))), probm3(rl, f, ifRobotToLeft))), probm4(probm4(seqm4(r, fl, stop, seqm2(ifRobotToRight, seqm4(f, f, ifInNest, rl))), selm2(ifRobotToRight, stop), seqm4(stop, rr, f, fr), seqm3(probm2(f, rl), rl, probm2(f, rl))), ifOnFood, selm3(seqm4(ifRobotToLeft, fr, ifFoodToLeft, fl), probm4(f, ifRobotToRight, ifFoodToLeft, ifNestToLeft), rr), seqm3(ifInNest, selm2(ifOnFood, probm2(rr, fl)), probm2(rr, probm4(seqm4(ifFoodToRight, probm4(selm2(ifRobotToRight, f), seqm3(ifNestToRight, seqm2(ifRobotToRight, ifRobotToRight), seqm3(f, f, stop)), probm3(seqm4(f, ifRobotToLeft, ifNestToRight, fr), r, ifNestToRight), f), f, r), ifRobotToLeft, f, probm3(rl, ifInNest, selm3(ifInNest, seqm4(f, ifNestToRight, ifNestToLeft, ifRobotToRight), seqm4(f, stop, ifInNest, rr))))))), seqm2(seqm2(stop, ifNestToRight), selm2(ifRobotToRight, rr)))",
			"fitness" : [0.5177636666666666, 22.344444444444445, -0.48888888888888893, 0.39566415555555556]
		})

		self.tests.append({
			"bt" : "selm4(ifInNest, seqm3(seqm3(seqm3(seqm3(selm3(ifNestToRight, probm3(probm3(seqm3(probm3(selm3(ifOnFood, probm3(ifNestToRight, ifNestToRight, fr), fr), fr, ifNestToRight), fl, ifNestToRight), seqm3(ifNestToRight, selm3(ifRobotToLeft, selm3(ifNestToRight, probm3(ifNestToRight, ifFoodToRight, ifNestToRight), ifNestToRight), ifNestToRight), ifNestToRight), fr), ifOnFood, ifNestToRight), ifNestToRight), fr, ifNestToRight), f, selm3(ifNestToRight, probm3(probm3(seqm3(probm3(selm3(ifOnFood, probm3(ifFoodToLeft, ifFoodToLeft, ifNestToRight), ifOnFood), fr, fl), f, ifNestToRight), selm3(ifNestToRight, probm3(ifNestToRight, seqm3(fl, f, stop), probm3(ifFoodToLeft, ifFoodToLeft, ifNestToRight)), probm3(selm3(f, ifRobotToLeft, ifRobotToLeft), seqm3(ifInNest, ifNestToRight, stop), rr)), ifRobotToLeft), fr, ifNestToRight), ifNestToRight)), f, ifNestToRight), f, ifNestToRight), fl, ifNestToRight)",
			"trimmed" : "selm3(ifInNest, seqm3(seqm3(seqm3(seqm3(selm3(ifNestToRight, probm3(probm3(seqm3(probm3(selm3(ifOnFood, probm3(ifNestToRight, ifNestToRight, fr), fr), fr, ifNestToRight), fl, ifNestToRight), seqm3(ifNestToRight, selm3(ifRobotToLeft, selm3(ifNestToRight, probm3(ifNestToRight, ifFoodToRight, ifNestToRight), ifNestToRight), ifNestToRight), ifNestToRight), fr), ifOnFood, ifNestToRight), ifNestToRight), fr, ifNestToRight), f, selm3(ifNestToRight, probm3(probm3(seqm3(probm3(selm3(ifOnFood, probm3(ifFoodToLeft, ifFoodToLeft, ifNestToRight), ifOnFood), fr, fl), f, ifNestToRight), selm3(ifNestToRight, probm3(ifNestToRight, seqm3(fl, f, stop), probm3(ifFoodToLeft, ifFoodToLeft, ifNestToRight)), probm3(f, seqm3(ifInNest, ifNestToRight, stop), rr)), ifRobotToLeft), fr, ifNestToRight), ifNestToRight)), f, ifNestToRight), f, ifNestToRight), fl)",
			"fitness" : [0.5334002444444443, 12.011111111111111, 5.055555555555555, 0.7284346333333334]
		})

		self.tests.append({
			"bt" : "seqm3(selm3(seqm4(ifRobotToRight, ifNestToLeft, ifRobotToRight, f), seqm4(fr, seqm2(seqm4(ifRobotToRight, ifFoodToLeft, ifRobotToRight, stop), seqm4(selm2(stop, rr), ifRobotToLeft, selm3(stop, ifNestToLeft, rl), ifInNest)), stop, seqm2(ifRobotToRight, seqm4(fr, seqm2(seqm4(ifRobotToRight, ifFoodToLeft, seqm4(selm3(seqm4(ifRobotToRight, ifNestToLeft, ifRobotToRight, f), seqm4(fr, seqm2(seqm4(ifRobotToRight, ifFoodToLeft, seqm4(ifNestToLeft, selm3(stop, seqm2(seqm4(ifRobotToRight, ifFoodToLeft, ifFoodToRight, stop), ifFoodToLeft), seqm4(ifNestToLeft, ifRobotToRight, seqm4(ifRobotToLeft, ifFoodToLeft, ifRobotToRight, stop), ifRobotToRight)), ifNestToLeft, ifFoodToRight), seqm2(ifRobotToRight, ifFoodToRight)), ifFoodToLeft), stop, seqm2(ifRobotToRight, seqm4(ifNestToLeft, fl, fl, ifFoodToRight))), ifNestToLeft), selm3(stop, seqm2(seqm4(ifRobotToRight, ifFoodToLeft, seqm4(ifNestToLeft, f, ifNestToLeft, ifFoodToRight), stop), ifFoodToLeft), ifRobotToRight), ifNestToLeft, ifFoodToRight), r), ifFoodToLeft), stop, seqm2(ifRobotToRight, seqm4(ifNestToLeft, selm3(stop, selm4(ifRobotToRight, ifRobotToLeft, ifRobotToRight, stop), seqm4(fl, ifRobotToRight, rl, rr)), ifNestToLeft, ifRobotToRight))))), ifNestToLeft), fl, selm2(fl, ifFoodToRight))",
			"trimmed" : "seqm3(selm3(seqm4(ifRobotToRight, ifNestToLeft, ifRobotToRight, f), seqm4(fr, seqm2(seqm4(ifRobotToRight, ifFoodToLeft, ifRobotToRight, stop), seqm4(stop, ifRobotToLeft, stop, ifInNest)), stop, seqm2(ifRobotToRight, seqm4(fr, seqm2(seqm4(ifRobotToRight, ifFoodToLeft, seqm4(selm3(seqm4(ifRobotToRight, ifNestToLeft, ifRobotToRight, f), seqm4(fr, seqm2(seqm4(ifRobotToRight, ifFoodToLeft, seqm4(ifNestToLeft, stop, ifNestToLeft, ifFoodToRight), seqm2(ifRobotToRight, ifFoodToRight)), ifFoodToLeft), stop, seqm2(ifRobotToRight, seqm4(ifNestToLeft, fl, fl, ifFoodToRight))), ifNestToLeft), stop, ifNestToLeft, ifFoodToRight), r), ifFoodToLeft), stop, seqm2(ifRobotToRight, seqm4(ifNestToLeft, stop, ifNestToLeft, ifRobotToRight))))), ifNestToLeft), fl, fl)",
			"fitness" : [0.5450333, 0.8555555555555555, -10.711111111111112, 0.6893617222222224]
		})

		self.tests.append({
			"bt" : "probm2(seqm3(probm4(probm4(ifOnFood, fl, seqm3(ifOnFood, rl, ifRobotToLeft), rl), seqm3(ifOnFood, ifInNest, ifInNest), probm3(r, ifInNest, f), selm3(ifInNest, r, stop)), rl, probm3(probm4(r, ifNestToRight, fr, ifNestToRight), rl, seqm2(stop, probm3(ifOnFood, r, rl)))), seqm4(seqm3(seqm2(fr, rl), probm2(ifOnFood, ifInNest), probm2(r, ifFoodToLeft)), probm2(selm3(rl, ifFoodToLeft, fr), selm4(r, stop, fr, f)), selm4(selm2(ifRobotToRight, stop), selm3(probm2(fr, ifFoodToLeft), seqm2(ifRobotToRight, f), probm4(ifFoodToLeft, selm2(stop, ifRobotToRight), ifInNest, rr)), seqm4(seqm3(rl, ifNestToLeft, fl), selm3(ifOnFood, ifFoodToLeft, f), selm4(seqm4(r, fr, rl, ifNestToLeft), seqm4(r, probm3(selm3(rl, stop, fr), probm4(rl, ifRobotToLeft, f, ifNestToLeft), selm3(ifOnFood, ifInNest, f)), rl, seqm2(stop, probm3(ifNestToLeft, r, ifOnFood))), seqm3(f, ifNestToRight, ifFoodToLeft), probm4(fr, ifFoodToLeft, probm4(ifInNest, f, probm3(ifInNest, rl, rl), fl), rl)), selm3(probm3(rl, ifNestToRight, fl), probm3(ifRobotToRight, ifFoodToRight, r), ifInNest)), probm4(seqm4(ifInNest, ifFoodToLeft, ifOnFood, ifNestToLeft), r, ifFoodToRight, ifNestToLeft)), selm3(probm3(rl, ifNestToRight, fl), probm3(ifRobotToRight, fr, rl), selm3(f, ifInNest, rl))))",
			"trimmed" : "probm2(seqm3(probm4(probm4(ifOnFood, fl, seqm3(ifOnFood, rl, ifRobotToLeft), rl), seqm3(ifOnFood, ifInNest, ifInNest), probm3(r, ifInNest, f), selm2(ifInNest, r)), rl, probm3(probm4(r, ifInNest, fr, ifInNest), rl, seqm2(stop, probm3(ifInNest, r, rl)))), seqm4(seqm3(seqm2(fr, rl), probm2(ifOnFood, ifInNest), probm2(r, ifFoodToLeft)), probm2(rl, r), selm2(ifRobotToRight, stop), selm3(probm3(rl, ifNestToRight, fl), probm3(ifRobotToRight, fr, rl), f)))",
			"fitness" : [0.49631834444444445, -3.9333333333333336, -27.755555555555553, 0.34979584444444445]
		})

		self.tests.append({
			"bt" : "selm3(ifInNest, ifOnFood, probm3(r, probm3(rr, selm3(selm3(rr, probm3(rr, probm3(r, r, ifNestToLeft), rr), fl), probm3(ifRobotToRight, stop, fl), seqm3(probm3(rl, ifFoodToRight, rr), probm3(r, r, probm3(ifNestToRight, rr, f)), seqm4(f, r, stop, fl))), probm3(seqm4(ifFoodToRight, ifRobotToRight, rr, r), stop, rl)), rl))",
			"trimmed" : "selm3(ifInNest, ifOnFood, probm3(r, probm3(rr, rr, probm3(seqm4(ifFoodToRight, ifRobotToRight, rr, r), stop, rl)), rl))",
			"fitness" : [0.5023312333333332, -6.955555555555556, -2.944444444444444, 0.8489664222222221]
		})

		self.tests.append({
			"bt" : "seqm2(seqm4(selm4(ifInNest, ifOnFood, r, probm4(selm4(ifInNest, rl, ifNestToLeft, ifFoodToLeft), rr, rl, ifInNest)), selm4(ifNestToLeft, ifInNest, ifInNest, seqm4(selm4(ifInNest, ifFoodToLeft, seqm4(selm4(ifInNest, ifRobotToLeft, ifFoodToLeft, r), selm4(ifNestToLeft, rr, rr, ifInNest), ifInNest, ifFoodToRight), r), selm4(ifNestToLeft, ifInNest, rr, ifNestToLeft), ifInNest, ifFoodToRight)), ifNestToLeft, ifNestToLeft), rl)",
			"trimmed" : "seqm2(seqm4(selm3(ifInNest, ifOnFood, r), selm4(ifNestToLeft, ifInNest, ifInNest, seqm4(selm4(ifInNest, ifFoodToLeft, seqm4(selm4(ifInNest, ifRobotToLeft, ifFoodToLeft, r), selm2(ifNestToLeft, rr), ifInNest, ifFoodToRight), r), selm3(ifNestToLeft, ifInNest, rr), ifInNest, ifFoodToRight)), ifNestToLeft, ifNestToLeft), rl)",
			"fitness" : [0.5603070888888888, -11.566666666666666, 2.1666666666666665, 0.8529456555555557]
		})

		self.tests.append({
			"bt" : "selm4(seqm3(seqm3(selm3(ifNestToLeft, seqm3(selm3(ifNestToRight, rr, selm3(ifNestToRight, f, ifNestToRight)), ifNestToRight, f), probm3(selm3(ifOnFood, rr, seqm3(ifNestToRight, stop, ifNestToRight)), fr, selm3(selm2(ifNestToRight, ifNestToRight), seqm3(ifNestToRight, ifNestToRight, fl), ifNestToRight))), selm3(ifNestToLeft, seqm3(selm3(ifFoodToLeft, ifFoodToRight, selm2(ifNestToRight, ifNestToRight)), ifNestToRight, f), seqm3(selm3(fr, fr, selm3(ifNestToRight, ifFoodToRight, ifRobotToRight)), ifNestToRight, fr)), ifNestToRight), fr, selm3(ifNestToLeft, ifNestToRight, seqm3(selm3(stop, selm3(f, rr, ifNestToRight), fr), selm3(ifOnFood, ifNestToLeft, seqm3(fr, fr, ifNestToRight)), ifRobotToLeft))), fl, seqm3(fr, ifRobotToLeft, ifNestToRight), ifNestToRight)",
			"trimmed" : "selm2(seqm3(seqm3(selm3(ifNestToLeft, seqm3(selm2(ifNestToRight, rr), ifNestToRight, f), probm3(selm2(ifOnFood, rr), fr, selm3(selm2(ifNestToRight, ifNestToRight), seqm3(ifNestToRight, ifNestToRight, fl), ifNestToRight))), selm3(ifNestToLeft, seqm3(selm3(ifFoodToLeft, ifFoodToRight, selm2(ifNestToRight, ifNestToRight)), ifNestToRight, f), seqm3(fr, ifNestToRight, fr)), ifNestToRight), fr, selm3(ifNestToLeft, ifNestToRight, seqm3(stop, selm3(ifOnFood, ifNestToLeft, seqm3(fr, fr, ifNestToRight)), ifRobotToLeft))), fl)",
			"fitness" : [0.5478681555555556, 8.588888888888889, 9.38888888888889, 0.7402713555555556]
		})

		self.tests.append({
			"bt" : "seqm2(selm4(selm3(ifRobotToRight, ifOnFood, r), ifRobotToLeft, ifFoodToLeft, selm3(ifRobotToRight, ifRobotToLeft, ifNestToRight)), selm3(ifOnFood, r, stop))",
			"trimmed" : "seqm2(selm3(ifRobotToRight, ifOnFood, r), selm2(ifOnFood, r))",
			"fitness" : [0.5071017444444446, -24.444444444444446, 0.0, 0.7897358222222224]
		})

		self.tests.append({
			"bt" : "seqm3(seqm3(f, ifFoodToLeft, ifNestToRight), probm2(probm2(selm4(selm2(probm4(ifFoodToRight, ifRobotToLeft, fl, ifFoodToLeft), ifFoodToRight), probm2(fl, stop), probm4(probm2(probm4(f, probm2(ifNestToRight, f), selm2(probm4(ifNestToRight, rr, f, stop), f), probm4(rr, ifNestToLeft, probm2(ifNestToRight, f), ifOnFood)), f), ifFoodToRight, probm2(stop, ifFoodToRight), selm4(ifFoodToRight, f, probm4(rr, ifRobotToLeft, probm2(ifNestToRight, ifFoodToRight), seqm3(stop, ifFoodToLeft, ifOnFood)), fl)), fl), f), rr), fl)",
			"trimmed" : "seqm3(seqm3(f, ifFoodToLeft, ifNestToRight), probm2(probm2(selm2(selm2(probm4(ifFoodToRight, ifRobotToLeft, fl, ifFoodToLeft), ifFoodToRight), probm2(fl, stop)), f), rr), fl)",
			"fitness" : [0.4884472777777777, 38.27777777777778, 1.711111111111111, 0.5425583666666667]
		})

		self.tests.append({
			"bt" : "selm2(selm3(seqm3(ifRobotToLeft, ifNestToRight, ifOnFood), ifOnFood, seqm3(ifRobotToLeft, r, seqm3(ifRobotToLeft, ifNestToRight, ifOnFood))), seqm3(seqm3(seqm3(r, selm3(seqm3(seqm3(ifRobotToLeft, r, seqm3(ifOnFood, ifNestToRight, seqm3(ifOnFood, f, ifOnFood))), r, seqm3(selm3(selm3(ifOnFood, ifNestToRight, ifOnFood), selm3(ifOnFood, ifNestToRight, fl), seqm3(rl, seqm3(seqm3(seqm3(r, ifOnFood, r), rl, rl), ifOnFood, selm3(seqm3(ifNestToRight, f, ifNestToRight), fl, ifNestToLeft)), r)), seqm3(seqm3(seqm3(r, seqm3(r, ifRobotToLeft, f), rl), r, r), rl, fl), seqm3(seqm3(seqm3(ifRobotToLeft, ifOnFood, seqm3(ifOnFood, ifOnFood, seqm3(ifOnFood, f, fl))), seqm3(rl, rl, ifOnFood), r), f, seqm3(ifRobotToLeft, r, seqm3(ifOnFood, ifNestToRight, seqm3(ifOnFood, f, ifOnFood)))))), ifOnFood, seqm3(ifRobotToLeft, r, seqm3(ifRobotToLeft, ifNestToRight, seqm3(ifOnFood, f, ifOnFood)))), r), rl, rl), ifOnFood, selm3(seqm3(ifNestToRight, f, ifNestToRight), fl, seqm3(selm3(seqm3(selm3(selm3(ifOnFood, ifNestToRight, ifOnFood), selm3(ifOnFood, ifNestToRight, ifOnFood), rl), seqm3(seqm3(seqm3(r, selm3(r, ifRobotToLeft, f), r), r, r), rl, fl), seqm3(seqm3(ifOnFood, seqm3(rl, ifNestToRight, ifOnFood), r), ifNestToRight, ifNestToRight)), ifRobotToLeft, seqm3(rl, rl, seqm3(ifOnFood, ifFoodToLeft, seqm3(ifOnFood, ifNestToRight, f)))), seqm3(seqm3(seqm3(r, r, rl), ifOnFood, ifRobotToLeft), rl, ifOnFood), ifOnFood))))",
			"trimmed" : "selm2(selm3(seqm3(ifRobotToLeft, ifNestToRight, ifOnFood), ifOnFood, seqm3(ifRobotToLeft, r, seqm3(ifRobotToLeft, ifNestToRight, ifOnFood))), seqm3(seqm3(seqm3(r, selm3(seqm3(seqm3(ifRobotToLeft, r, seqm3(ifOnFood, ifNestToRight, seqm3(ifOnFood, f, ifOnFood))), r, seqm3(selm2(selm3(ifOnFood, ifNestToRight, ifOnFood), selm3(ifOnFood, ifNestToRight, fl)), seqm3(seqm3(seqm3(r, seqm3(r, ifRobotToLeft, f), rl), r, r), rl, fl), seqm3(seqm3(seqm3(ifRobotToLeft, ifOnFood, seqm3(ifOnFood, ifOnFood, seqm3(ifOnFood, f, fl))), seqm3(rl, rl, ifOnFood), r), f, seqm3(ifRobotToLeft, r, seqm3(ifOnFood, ifNestToRight, seqm3(ifOnFood, f, ifOnFood)))))), ifOnFood, seqm3(ifRobotToLeft, r, seqm3(ifRobotToLeft, ifNestToRight, seqm3(ifOnFood, f, ifOnFood)))), r), rl, rl), ifOnFood, selm2(seqm3(ifNestToRight, f, ifNestToRight), fl)))",
			"fitness" : [0.5057605777777777, -24.34444444444444, -0.36666666666666664, 0.8585988333333334]
		})

		self.tests.append({
			"bt" : "selm2(ifOnFood, seqm2(seqm4(r, seqm4(r, ifOnFood, seqm2(rr, selm2(ifNestToLeft, rr)), seqm4(rr, fl, ifOnFood, ifOnFood)), seqm2(seqm4(r, ifOnFood, seqm2(rr, seqm2(ifOnFood, seqm2(fl, ifOnFood))), seqm4(fl, seqm2(fl, ifNestToRight), ifOnFood, rr)), fl), seqm4(seqm2(rr, seqm2(fl, seqm2(ifNestToLeft, ifRobotToLeft))), rr, r, seqm4(seqm2(rr, seqm2(fl, ifRobotToLeft)), rr, seqm2(ifNestToLeft, seqm2(rr, fl)), rr))), seqm4(r, ifOnFood, r, seqm4(r, seqm4(r, f, selm2(ifOnFood, rr), rr), seqm2(seqm2(fl, seqm2(ifNestToLeft, ifRobotToLeft)), fl), seqm4(fl, ifNestToLeft, rr, selm2(selm2(ifFoodToLeft, ifNestToLeft), ifRobotToLeft))))))",
			"trimmed" : "selm2(ifOnFood, seqm2(seqm4(r, seqm4(r, ifOnFood, seqm2(rr, selm2(ifNestToLeft, rr)), seqm4(rr, fl, ifOnFood, ifOnFood)), seqm2(seqm4(r, ifOnFood, seqm2(rr, seqm2(ifOnFood, seqm2(fl, ifOnFood))), seqm4(fl, seqm2(fl, ifNestToRight), ifOnFood, rr)), fl), seqm4(seqm2(rr, seqm2(fl, seqm2(ifNestToLeft, ifRobotToLeft))), rr, r, seqm4(seqm2(rr, seqm2(fl, ifRobotToLeft)), rr, seqm2(ifNestToLeft, seqm2(rr, fl)), rr))), seqm4(r, ifOnFood, r, seqm4(r, seqm4(r, f, selm2(ifOnFood, rr), rr), seqm2(seqm2(fl, seqm2(ifNestToLeft, ifRobotToLeft)), fl), seqm3(fl, ifNestToLeft, rr)))))",
			"fitness" : [0.5010820444444445, -24.34444444444444, 3.2777777777777777, 0.6341871666666666]
		})

		self.tests.append({
			"bt" : "probm2(f, seqm3(seqm3(fl, seqm3(f, f, ifNestToLeft), seqm3(seqm3(selm3(seqm3(seqm3(f, stop, fr), f, ifNestToLeft), fr, f), ifNestToLeft, seqm3(seqm3(f, seqm3(f, f, ifNestToLeft), seqm3(f, fr, seqm3(selm3(seqm3(seqm3(f, ifRobotToLeft, ifNestToLeft), f, ifNestToLeft), fr, f), fr, f))), seqm3(seqm3(ifFoodToLeft, seqm3(f, f, ifNestToLeft), ifNestToLeft), fr, f), ifOnFood)), stop, seqm3(selm3(seqm3(seqm3(stop, ifRobotToLeft, ifNestToLeft), f, ifNestToLeft), fr, seqm3(seqm3(f, seqm3(f, f, ifNestToLeft), seqm3(f, fr, seqm3(seqm3(ifFoodToLeft, seqm3(f, f, ifNestToLeft), ifNestToLeft), fr, f))), seqm3(seqm3(ifFoodToLeft, seqm3(fr, seqm3(seqm3(f, ifRobotToLeft, ifInNest), f, ifNestToLeft), ifNestToLeft), stop), fr, f), ifOnFood)), fr, f))), seqm3(seqm3(seqm3(f, fr, seqm3(selm3(seqm3(seqm3(f, ifRobotToLeft, ifNestToLeft), f, fr), fr, ifNestToLeft), stop, f)), ifRobotToLeft, ifNestToLeft), fr, f), ifOnFood))",
			"trimmed" : "probm2(f, seqm2(seqm3(fl, seqm3(f, f, ifNestToLeft), seqm3(seqm3(selm2(seqm3(seqm3(f, stop, fr), f, ifNestToLeft), fr), ifNestToLeft, seqm3(seqm3(f, seqm3(f, f, ifNestToLeft), seqm3(f, fr, seqm3(selm2(seqm3(seqm3(f, ifRobotToLeft, ifNestToLeft), f, ifNestToLeft), fr), fr, f))), seqm3(seqm3(ifFoodToLeft, seqm3(f, f, ifNestToLeft), ifNestToLeft), fr, f), ifOnFood)), stop, seqm3(selm2(seqm3(seqm3(stop, ifRobotToLeft, ifNestToLeft), f, ifNestToLeft), fr), fr, f))), seqm3(seqm3(seqm3(f, fr, seqm3(selm2(seqm3(seqm3(f, ifRobotToLeft, ifNestToLeft), f, fr), fr), stop, f)), ifRobotToLeft, ifNestToLeft), fr, f)))",
			"fitness" : [0.4907122222222222, 31.46666666666666, 3.0, 0.23263946666666674]
		})

		self.tests.append({
			"bt" : "selm4(ifOnFood, seqm2(ifNestToRight, seqm2(seqm2(seqm2(seqm2(r, seqm2(seqm2(ifOnFood, selm2(rl, ifOnFood)), seqm2(rl, ifOnFood))), ifNestToLeft), ifRobotToLeft), selm4(stop, seqm2(seqm2(seqm2(seqm2(ifOnFood, ifNestToRight), ifNestToRight), ifNestToLeft), seqm2(seqm2(ifOnFood, ifNestToRight), ifRobotToRight)), ifNestToRight, f))), seqm2(seqm2(seqm2(r, seqm2(ifNestToLeft, ifOnFood)), rl), seqm2(seqm2(ifNestToRight, ifNestToRight), ifRobotToRight)), seqm2(seqm2(ifNestToRight, seqm2(r, seqm2(seqm2(ifNestToRight, seqm2(r, seqm2(seqm2(seqm2(ifOnFood, ifOnFood), selm2(rl, ifOnFood)), seqm2(rl, ifOnFood)))), ifNestToRight))), fl))",
			"trimmed" : "selm4(ifOnFood, seqm2(ifNestToRight, seqm2(seqm2(seqm2(seqm2(r, seqm2(seqm2(ifOnFood, rl), seqm2(rl, ifOnFood))), ifNestToLeft), ifRobotToLeft), stop)), seqm2(seqm2(seqm2(r, seqm2(ifNestToLeft, ifOnFood)), rl), seqm2(seqm2(ifNestToRight, ifNestToRight), ifRobotToRight)), seqm2(seqm2(ifNestToRight, seqm2(r, seqm2(seqm2(ifNestToRight, seqm2(r, seqm2(seqm2(seqm2(ifOnFood, ifOnFood), rl), seqm2(rl, ifOnFood)))), ifNestToRight))), fl))",
			"fitness" : [0.5054508888888888, -24.122222222222224, -0.41111111111111115, 0.8181247777777777]
		})

		self.tests.append({
			"bt" : "selm2(ifOnFood, seqm3(r, seqm3(r, seqm3(r, seqm3(r, ifInNest, r), selm3(seqm3(seqm3(r, ifRobotToLeft, seqm3(r, selm3(r, ifFoodToLeft, rr), ifFoodToLeft)), seqm3(r, seqm3(seqm3(r, ifRobotToLeft, ifNestToRight), seqm3(r, seqm3(stop, ifNestToRight, ifNestToLeft), rr), ifFoodToRight), ifNestToLeft), r), r, r)), rr), seqm3(seqm3(ifInNest, ifRobotToLeft, ifFoodToLeft), seqm3(r, seqm3(r, seqm3(seqm3(r, ifRobotToLeft, f), seqm3(stop, seqm3(r, seqm4(stop, ifFoodToRight, rr, ifNestToLeft), f), ifFoodToLeft), rr), ifFoodToRight), rl), r)))",
			"trimmed" : "selm2(ifOnFood, seqm3(r, seqm3(r, seqm3(r, seqm3(r, ifInNest, r), selm2(seqm3(seqm3(r, ifRobotToLeft, seqm3(r, r, ifFoodToLeft)), seqm3(r, seqm3(seqm3(r, ifRobotToLeft, ifNestToRight), seqm3(r, seqm3(stop, ifNestToRight, ifNestToLeft), rr), ifFoodToRight), ifNestToLeft), r), r)), rr), seqm3(seqm3(ifInNest, ifRobotToLeft, ifFoodToLeft), seqm3(r, seqm3(r, seqm3(seqm3(r, ifRobotToLeft, f), seqm3(stop, seqm3(r, seqm4(stop, ifFoodToRight, rr, ifNestToLeft), f), ifFoodToLeft), rr), ifFoodToRight), rl), r)))",
			"fitness" : [0.5044099666666668, -23.366666666666667, 0.9333333333333332, 0.5869551666666666]
		})

		self.tests.append({
			"bt" : "seqm4(seqm4(f, ifNestToLeft, ifRobotToLeft, ifFoodToLeft), seqm4(fr, ifNestToLeft, fr, seqm4(seqm4(fr, seqm3(ifOnFood, fr, ifRobotToLeft), selm4(fr, ifRobotToLeft, fr, ifRobotToLeft), rl), rl, selm4(ifRobotToLeft, selm4(fr, ifRobotToLeft, fr, ifRobotToLeft), ifNestToRight, r), selm4(f, ifNestToLeft, ifFoodToLeft, seqm4(fr, ifOnFood, rl, fr)))), fr, fr)",
			"trimmed" : "seqm4(seqm4(f, ifNestToLeft, ifRobotToLeft, ifFoodToLeft), seqm4(fr, ifNestToLeft, fr, seqm4(seqm4(fr, seqm3(ifOnFood, fr, ifRobotToLeft), fr, rl), rl, selm2(ifRobotToLeft, fr), f)), fr, fr)",
			"fitness" : [0.48622220000000016, 36.91111111111111, -3.0888888888888886, 0.5476302222222221]
		})

		self.tests.append({
			"bt" : "selm4(ifOnFood, ifOnFood, seqm3(ifInNest, rr, seqm3(rr, ifRobotToLeft, rl)), seqm3(r, ifOnFood, selm3(seqm3(r, seqm3(selm2(ifRobotToRight, selm2(ifRobotToRight, seqm3(r, ifOnFood, seqm3(seqm3(ifFoodToRight, r, rl), selm3(seqm3(r, selm2(rl, seqm3(rl, ifOnFood, seqm3(ifInNest, fl, ifRobotToLeft))), rr), fl, ifRobotToRight), ifFoodToRight)))), selm3(seqm3(r, selm3(ifInNest, ifFoodToRight, seqm3(selm2(seqm3(selm3(ifInNest, fr, ifRobotToLeft), ifInNest, f), r), fl, ifFoodToRight)), selm3(fr, ifRobotToLeft, ifRobotToLeft)), fl, ifRobotToRight), ifFoodToRight), selm3(seqm3(ifRobotToRight, rr, ifRobotToLeft), ifRobotToLeft, seqm3(ifInNest, fl, seqm3(ifRobotToLeft, rr, seqm3(rr, ifRobotToLeft, rl))))), fl, ifRobotToLeft)))",
			"trimmed" : "selm4(ifOnFood, ifOnFood, seqm3(ifInNest, rr, seqm3(rr, ifRobotToLeft, rl)), seqm3(r, ifOnFood, selm2(seqm3(r, seqm3(selm2(ifRobotToRight, selm2(ifRobotToRight, seqm3(r, ifOnFood, seqm3(seqm3(ifFoodToRight, r, rl), seqm3(r, rl, rr), ifFoodToRight)))), selm2(seqm3(r, selm3(ifInNest, ifFoodToRight, seqm3(selm2(seqm3(selm2(ifInNest, fr), ifInNest, f), r), fl, ifFoodToRight)), fr), fl), ifFoodToRight), selm3(seqm3(ifRobotToRight, rr, ifRobotToLeft), ifRobotToLeft, seqm3(ifInNest, fl, seqm3(ifRobotToLeft, rr, seqm3(rr, ifRobotToLeft, rl))))), fl)))",
			"fitness" : [0.4932347999999999, -18.833333333333332, 1.488888888888889, 0.8231369111111112]
		})

		self.tests.append({
			"bt" : "selm4(ifOnFood, seqm2(seqm2(seqm2(seqm3(selm2(r, ifOnFood), ifOnFood, rl), seqm2(ifOnFood, ifRobotToRight)), seqm2(seqm2(seqm2(selm2(ifOnFood, ifOnFood), seqm2(seqm2(seqm2(seqm2(seqm2(seqm2(selm3(fl, seqm2(rr, seqm2(seqm2(rr, ifInNest), ifRobotToLeft)), selm3(seqm2(r, ifOnFood), seqm2(fl, fl), rl)), seqm2(seqm2(ifOnFood, rr), seqm2(selm2(ifOnFood, seqm2(seqm2(seqm2(seqm2(selm3(fr, fr, ifRobotToLeft), seqm2(fl, fl)), rr), seqm2(fl, fl)), rr)), ifOnFood))), rr), fl), fl), seqm2(ifOnFood, fl)), rr)), seqm2(seqm2(selm2(selm3(seqm2(r, seqm2(seqm2(fl, fl), rr)), rr, rl), seqm2(selm3(seqm2(ifNestToRight, fl), seqm2(selm3(fl, seqm2(ifInNest, seqm2(seqm2(r, ifOnFood), ifOnFood)), selm3(seqm2(r, ifOnFood), seqm2(seqm2(ifOnFood, ifOnFood), fl), rl)), seqm2(selm2(r, ifNestToLeft), seqm2(selm2(ifOnFood, seqm2(seqm2(seqm2(fl, rr), seqm2(selm3(seqm2(ifNestToRight, fl), ifRobotToRight, ifNestToLeft), fl)), rr)), ifOnFood))), seqm2(ifOnFood, ifNestToLeft)), seqm2(seqm2(selm3(seqm2(ifNestToRight, ifOnFood), rr, seqm2(seqm2(seqm2(seqm2(selm3(ifRobotToRight, fr, r), seqm2(fl, fl)), rr), seqm2(selm3(seqm2(rr, fl), ifNestToRight, rl), f)), rl)), seqm2(fl, fl)), ifRobotToRight))), rr), seqm2(seqm2(seqm2(seqm2(seqm2(seqm2(selm2(ifOnFood, seqm2(seqm2(seqm2(seqm2(selm3(ifRobotToRight, fr, ifOnFood), seqm2(fl, fl)), rr), seqm2(selm3(seqm2(fl, fl), ifNestToRight, seqm2(ifNestToRight, fl)), rr)), fl)), seqm2(seqm2(ifOnFood, rr), seqm2(selm2(ifOnFood, seqm2(seqm2(seqm2(seqm2(selm3(f, fr, ifOnFood), seqm2(fl, rr)), rr), seqm2(seqm3(seqm2(rr, fl), ifRobotToRight, rl), rr)), fl)), ifOnFood))), seqm2(seqm2(seqm2(selm3(ifOnFood, ifInNest, ifOnFood), seqm2(fl, fl)), fr), ifNestToRight)), seqm2(seqm2(seqm2(seqm2(seqm3(selm2(r, ifNestToLeft), ifOnFood, rl), seqm2(ifOnFood, ifOnFood)), seqm2(fl, seqm2(ifOnFood, fl))), seqm2(selm3(seqm2(seqm2(selm3(seqm2(rr, fl), ifNestToRight, ifRobotToLeft), rr), fl), seqm2(rr, seqm2(ifOnFood, ifRobotToRight)), seqm2(ifNestToRight, fl)), rr)), fl)), fl), seqm2(ifOnFood, ifRobotToLeft)), rr))), ifNestToLeft)), fr), seqm2(seqm2(ifOnFood, rr), fl), ifOnFood)",
			"trimmed" : "selm3(ifOnFood, seqm2(seqm2(seqm2(seqm3(r, ifOnFood, rl), seqm2(ifOnFood, ifRobotToRight)), seqm2(seqm2(seqm2(selm2(ifOnFood, ifOnFood), seqm2(seqm2(seqm2(seqm2(seqm2(seqm2(fl, seqm2(seqm2(ifOnFood, rr), seqm2(selm2(ifOnFood, seqm2(seqm2(seqm2(seqm2(fr, seqm2(fl, fl)), rr), seqm2(fl, fl)), rr)), ifOnFood))), rr), fl), fl), seqm2(ifOnFood, fl)), rr)), seqm2(seqm2(seqm2(r, seqm2(seqm2(fl, fl), rr)), rr), seqm2(seqm2(seqm2(seqm2(seqm2(seqm2(selm2(ifOnFood, seqm2(seqm2(seqm2(seqm2(selm2(ifRobotToRight, fr), seqm2(fl, fl)), rr), seqm2(seqm2(fl, fl), rr)), fl)), seqm2(seqm2(ifOnFood, rr), seqm2(selm2(ifOnFood, seqm2(seqm2(seqm2(seqm2(f, seqm2(fl, rr)), rr), seqm2(seqm3(seqm2(rr, fl), ifRobotToRight, rl), rr)), fl)), ifOnFood))), seqm2(seqm2(seqm2(selm3(ifOnFood, ifInNest, ifOnFood), seqm2(fl, fl)), fr), ifNestToRight)), seqm2(seqm2(seqm2(seqm2(seqm3(r, ifOnFood, rl), seqm2(ifOnFood, ifOnFood)), seqm2(fl, seqm2(ifOnFood, fl))), seqm2(seqm2(seqm2(seqm2(rr, fl), rr), fl), rr)), fl)), fl), seqm2(ifOnFood, ifRobotToLeft)), rr))), ifNestToLeft)), fr), seqm2(seqm2(ifOnFood, rr), fl))",
			"fitness" : [0.49562873333333324, -23.288888888888888, 2.988888888888889, 0.8143590333333333]
		})

		self.tests.append({
			"bt" : "selm2(ifOnFood, seqm4(seqm4(selm3(selm3(ifOnFood, selm4(ifFoodToLeft, ifNestToRight, ifFoodToRight, stop), stop), seqm4(ifNestToLeft, ifOnFood, seqm4(ifRobotToLeft, ifNestToRight, ifFoodToLeft, ifNestToLeft), ifRobotToRight), rr), selm4(seqm4(ifNestToLeft, selm4(ifNestToRight, ifInNest, ifRobotToLeft, r), ifOnFood, rl), r, stop, stop), ifOnFood, selm3(ifInNest, selm4(selm4(fl, ifNestToRight, ifRobotToRight, ifFoodToLeft), ifFoodToLeft, selm3(ifNestToLeft, fr, ifNestToRight), stop), ifRobotToRight)), selm4(seqm4(r, selm4(stop, ifFoodToRight, ifFoodToLeft, ifFoodToLeft), ifOnFood, fr), r, stop, ifNestToRight), selm3(selm3(ifOnFood, selm4(ifFoodToLeft, fr, selm4(ifFoodToLeft, ifNestToRight, ifFoodToRight, ifFoodToLeft), ifFoodToLeft), stop), selm4(stop, ifNestToRight, ifFoodToLeft, ifFoodToLeft), selm3(stop, r, ifNestToLeft)), selm3(ifNestToLeft, selm4(seqm4(ifFoodToLeft, selm4(ifNestToLeft, rl, ifNestToRight, ifFoodToLeft), ifRobotToLeft, rl), ifRobotToRight, selm2(ifFoodToLeft, ifNestToRight), selm4(ifNestToLeft, ifNestToRight, ifFoodToLeft, fr)), seqm4(stop, ifOnFood, selm4(ifRobotToLeft, r, ifOnFood, r), selm4(fr, r, fr, ifOnFood)))))",
			"trimmed" : "selm2(ifOnFood, seqm4(seqm4(selm2(ifOnFood, selm4(ifFoodToLeft, ifNestToRight, ifFoodToRight, stop)), selm2(seqm4(ifNestToLeft, selm4(ifNestToRight, ifInNest, ifRobotToLeft, r), ifOnFood, rl), r), ifOnFood, selm2(ifInNest, fl)), selm2(seqm4(r, stop, ifOnFood, fr), r), selm2(ifOnFood, selm2(ifFoodToLeft, fr)), selm2(ifNestToLeft, selm4(seqm4(ifFoodToLeft, selm2(ifNestToLeft, rl), ifRobotToLeft, rl), ifRobotToRight, selm2(ifFoodToLeft, ifNestToRight), selm4(ifNestToLeft, ifNestToRight, ifFoodToLeft, fr)))))",
			"fitness" : [0.49359218888888884, -23.0, -0.4666666666666666, 0.8896677555555556]
		})

		self.tests.append({
			"bt" : "seqm2(selm3(probm4(selm4(f, fl, ifOnFood, f), selm2(seqm2(seqm3(ifNestToLeft, stop, fr), f), seqm3(f, ifRobotToRight, ifRobotToLeft)), probm3(f, ifRobotToRight, ifInNest), ifNestToLeft), selm4(probm3(ifNestToLeft, ifOnFood, ifOnFood), probm3(seqm3(ifRobotToRight, fl, ifInNest), ifInNest, fl), probm2(fl, ifRobotToLeft), probm3(fr, fr, rr)), probm3(probm4(f, probm3(seqm3(ifRobotToRight, fl, rl), ifOnFood, fl), ifInNest, ifRobotToRight), selm3(ifRobotToRight, selm4(f, fr, f, rr), ifNestToRight), selm3(ifFoodToLeft, probm4(fr, rl, fr, r), ifFoodToLeft))), seqm3(f, ifRobotToRight, ifRobotToLeft))",
			"trimmed" : "seqm2(selm2(probm4(f, selm2(seqm2(seqm3(ifNestToLeft, stop, fr), f), seqm3(f, ifRobotToRight, ifRobotToLeft)), probm3(f, ifRobotToRight, ifInNest), ifNestToLeft), selm4(probm3(ifNestToLeft, ifOnFood, ifOnFood), probm3(seqm3(ifRobotToRight, fl, ifInNest), ifInNest, fl), probm2(fl, ifRobotToLeft), probm3(fr, fr, rr))), f)",
			"fitness" : [0.4875981333333333, 34.55555555555556, 1.911111111111111, 0.5973502222222222]
		})

		self.tests.append({
			"bt" : "seqm4(selm2(selm4(rr, stop, fr, ifOnFood), probm4(ifNestToLeft, ifRobotToLeft, r, ifNestToLeft)), selm4(selm4(ifOnFood, r, probm4(ifNestToRight, stop, ifNestToLeft, f), ifNestToRight), probm3(fr, fr, ifInNest), probm2(selm2(ifInNest, f), ifNestToLeft), probm2(selm2(ifFoodToRight, ifNestToLeft), rl)), selm2(selm4(r, rl, stop, selm4(ifRobotToLeft, rr, ifRobotToLeft, ifRobotToLeft)), probm4(ifNestToRight, rl, ifNestToLeft, f)), selm4(selm2(probm4(ifNestToLeft, ifRobotToLeft, r, ifNestToLeft), rl), probm4(r, rr, ifRobotToLeft, ifFoodToRight), stop, selm4(rl, rl, f, r)))",
			"trimmed" : "seqm4(rr, selm2(ifOnFood, r), r, selm2(probm4(ifNestToLeft, ifRobotToLeft, r, ifNestToLeft), rl))",
			"fitness" : [0.4883552666666667, -22.577777777777776, 1.0666666666666667, 0.33982287777777775]
		})

		self.tests.append({
			"bt" : "seqm3(selm4(ifOnFood, selm4(ifRobotToRight, r, rl, ifFoodToRight), ifNestToLeft, ifNestToLeft), selm4(ifOnFood, selm4(r, ifNestToLeft, ifNestToRight, r), rl, ifNestToLeft), ifFoodToRight)",
			"trimmed" : "seqm2(selm2(ifOnFood, selm2(ifRobotToRight, r)), selm2(ifOnFood, r))",
			"fitness" : [0.5071017444444446, -24.444444444444446, 0.0, 0.8448649777777778]
		})

		self.tests.append({
			"bt" : "selm3(ifOnFood, ifOnFood, selm3(seqm3(r, ifOnFood, rl), ifRobotToRight, selm3(ifOnFood, r, ifOnFood)))",
			"trimmed" : "selm3(ifOnFood, ifOnFood, selm3(seqm3(r, ifOnFood, rl), ifRobotToRight, selm2(ifOnFood, r)))",
			"fitness" : [0.5063132555555556, -24.055555555555554, -0.5111111111111111, 0.8307243333333332]
		})

		self.tests.append({
			"bt" : "selm3(ifOnFood, seqm2(r, seqm2(ifOnFood, seqm2(seqm2(r, fr), seqm2(seqm2(seqm2(seqm2(seqm2(rl, seqm2(ifRobotToLeft, seqm2(ifOnFood, seqm2(rl, selm3(seqm2(r, seqm2(ifOnFood, seqm2(seqm2(r, fr), seqm2(selm2(seqm2(seqm2(seqm2(rl, seqm2(ifRobotToLeft, selm3(stop, rl, ifOnFood))), selm2(rl, seqm2(ifFoodToLeft, selm2(stop, fr)))), seqm2(ifOnFood, seqm2(ifOnFood, seqm2(ifOnFood, ifOnFood)))), ifRobotToRight), selm3(seqm2(r, seqm2(rl, seqm2(seqm2(fr, fr), seqm2(seqm2(fr, rl), rl)))), seqm2(r, fr), seqm2(ifOnFood, seqm2(fr, fr))))))), seqm2(rl, selm3(seqm2(r, seqm2(ifOnFood, seqm2(seqm2(r, fr), stop))), rl, r)), ifRobotToRight))))), selm2(rl, selm3(stop, rl, selm3(seqm2(ifOnFood, ifRobotToLeft), rl, fl)))), seqm2(ifOnFood, seqm2(fr, fr))), rl), selm2(seqm2(rl, seqm2(ifOnFood, ifOnFood)), seqm2(selm2(seqm2(fr, seqm2(fl, seqm2(fr, seqm2(ifRobotToLeft, r)))), ifRobotToRight), ifRobotToLeft)))))), ifRobotToRight)",
			"trimmed" : "selm2(ifOnFood, seqm2(r, seqm2(ifOnFood, seqm2(seqm2(r, fr), seqm2(seqm2(seqm2(seqm2(seqm2(rl, seqm2(ifRobotToLeft, seqm2(ifOnFood, seqm2(rl, selm2(seqm2(r, seqm2(ifOnFood, seqm2(seqm2(r, fr), seqm2(selm2(seqm2(seqm2(seqm2(rl, seqm2(ifRobotToLeft, stop)), rl), seqm2(ifOnFood, seqm2(ifOnFood, seqm2(ifOnFood, ifOnFood)))), ifRobotToRight), seqm2(r, seqm2(rl, seqm2(seqm2(fr, fr), seqm2(seqm2(fr, rl), rl)))))))), seqm2(rl, selm2(seqm2(r, seqm2(ifOnFood, seqm2(seqm2(r, fr), stop))), rl))))))), rl), seqm2(ifOnFood, seqm2(fr, fr))), rl), selm2(seqm2(rl, seqm2(ifOnFood, ifOnFood)), seqm2(fr, seqm2(fl, seqm2(fr, seqm2(ifRobotToLeft, r))))))))))",
			"fitness" : [0.5017264999999999, -24.355555555555554, -2.944444444444444, 0.7827747666666666]
		})

		self.tests.append({
			"bt" : "selm2(ifOnFood, seqm4(seqm4(seqm4(r, r, seqm4(ifOnFood, seqm4(r, r, seqm4(seqm4(ifOnFood, r, fl, fl), fl, stop, fl), rr), stop, fl), ifOnFood), ifOnFood, seqm4(ifOnFood, r, fl, fl), ifNestToRight), seqm4(seqm4(rl, r, ifOnFood, seqm4(fl, fl, selm4(ifOnFood, stop, ifNestToRight, seqm4(fl, fl, seqm4(rl, ifNestToRight, rl, rr), seqm4(r, ifNestToRight, stop, ifInNest))), ifOnFood)), seqm4(selm4(seqm4(fl, r, seqm4(rl, ifNestToRight, rl, r), r), ifNestToRight, seqm4(selm4(r, r, ifRobotToRight, rr), fr, seqm4(ifOnFood, r, fl, fl), rr), f), ifNestToRight, seqm4(selm4(r, f, ifOnFood, rr), stop, fl, ifNestToLeft), seqm4(fl, r, seqm4(r, r, seqm4(ifOnFood, fr, stop, fl), ifOnFood), r)), ifInNest, ifNestToRight), ifOnFood, rr))",
			"trimmed" : "selm2(ifOnFood, seqm4(seqm4(seqm4(r, r, seqm4(ifOnFood, seqm4(r, r, seqm4(seqm4(ifOnFood, r, fl, fl), fl, stop, fl), rr), stop, fl), ifOnFood), ifOnFood, seqm4(ifOnFood, r, fl, fl), ifNestToRight), seqm4(seqm4(rl, r, ifOnFood, seqm4(fl, fl, selm2(ifOnFood, stop), ifOnFood)), seqm4(selm4(seqm4(fl, r, seqm4(rl, ifNestToRight, rl, r), r), ifNestToRight, seqm4(r, fr, seqm4(ifOnFood, r, fl, fl), rr), f), ifNestToRight, seqm4(r, stop, fl, ifNestToLeft), seqm4(fl, r, seqm4(r, r, seqm4(ifOnFood, fr, stop, fl), ifOnFood), r)), ifInNest, ifNestToRight), ifOnFood, rr))",
			"fitness" : [0.4986902333333334, -25.844444444444445, 2.7444444444444445, 0.5832478333333333]
		})

		self.tests.append({
			"bt" : "selm3(ifOnFood, seqm2(seqm2(seqm2(ifInNest, seqm2(rr, seqm2(seqm2(ifFoodToRight, rr), seqm2(ifInNest, ifInNest)))), seqm2(seqm2(rr, seqm2(seqm2(r, r), ifRobotToLeft)), seqm2(ifInNest, seqm2(seqm2(rr, ifRobotToRight), seqm2(r, ifRobotToLeft))))), selm3(seqm2(rr, r), rr, seqm2(rr, selm3(ifNestToRight, ifInNest, ifFoodToLeft)))), seqm2(r, r))",
			"trimmed" : "selm3(ifOnFood, seqm2(seqm2(seqm2(ifInNest, seqm2(rr, seqm2(seqm2(ifFoodToRight, rr), seqm2(ifInNest, ifInNest)))), seqm2(seqm2(rr, seqm2(seqm2(r, r), ifRobotToLeft)), seqm2(ifInNest, seqm2(seqm2(rr, ifRobotToRight), seqm2(r, ifRobotToLeft))))), seqm2(rr, r)), seqm2(r, r))",
			"fitness" : [0.49523058888888905, -21.9, 1.5666666666666669, 0.6933087333333333]
		})

		self.tests.append({
			"bt" : "probm2(f, seqm4(seqm4(f, seqm4(ifRobotToLeft, f, ifRobotToLeft, ifOnFood), rl, fr), ifOnFood, selm3(ifInNest, seqm2(r, ifOnFood), seqm3(fr, seqm2(r, f), seqm4(stop, f, ifRobotToLeft, fr))), seqm3(seqm4(ifRobotToLeft, stop, ifRobotToLeft, ifInNest), ifNestToRight, ifRobotToLeft)))",
			"trimmed" : "probm2(f, seqm4(seqm4(f, seqm4(ifRobotToLeft, f, ifRobotToLeft, ifOnFood), rl, fr), ifOnFood, selm3(ifInNest, seqm2(r, ifOnFood), seqm3(fr, seqm2(r, f), seqm4(stop, f, ifRobotToLeft, fr))), seqm2(ifRobotToLeft, stop)))",
			"fitness" : [0.4859936666666666, 34.144444444444446, -2.155555555555556, 0.43522689999999997]
		})

		self.tests.append({
			"bt" : "selm2(ifOnFood, seqm2(r, seqm2(seqm2(ifOnFood, seqm2(selm2(r, rr), seqm2(fr, ifOnFood))), seqm4(ifRobotToRight, seqm4(rr, fl, rr, seqm4(seqm3(fl, ifOnFood, rr), seqm4(ifRobotToRight, ifOnFood, ifRobotToRight, ifNestToRight), seqm2(stop, ifOnFood), ifOnFood)), seqm4(rr, seqm4(ifRobotToRight, rr, ifOnFood, ifOnFood), rr, seqm4(ifRobotToRight, seqm4(stop, ifOnFood, ifOnFood, seqm4(f, rl, seqm2(stop, stop), seqm2(seqm2(ifOnFood, seqm2(stop, ifOnFood)), seqm4(seqm3(fl, ifOnFood, rr), seqm4(rr, ifOnFood, rr, rr), seqm4(rr, seqm2(fr, ifOnFood), ifRobotToLeft, ifFoodToRight), ifOnFood)))), ifOnFood, seqm2(stop, ifRobotToRight))), ifFoodToLeft))))",
			"trimmed" : "selm2(ifOnFood, seqm2(r, seqm2(seqm2(ifOnFood, seqm2(r, seqm2(fr, ifOnFood))), seqm3(ifRobotToRight, seqm4(rr, fl, rr, seqm4(seqm3(fl, ifOnFood, rr), seqm4(ifRobotToRight, ifOnFood, ifRobotToRight, ifNestToRight), seqm2(stop, ifOnFood), ifOnFood)), seqm4(rr, seqm4(ifRobotToRight, rr, ifOnFood, ifOnFood), rr, seqm4(ifRobotToRight, seqm4(stop, ifOnFood, ifOnFood, seqm4(f, rl, seqm2(stop, stop), seqm2(seqm2(ifOnFood, seqm2(stop, ifOnFood)), seqm4(seqm3(fl, ifOnFood, rr), seqm4(rr, ifOnFood, rr, rr), seqm4(rr, seqm2(fr, ifOnFood), ifRobotToLeft, ifFoodToRight), ifOnFood)))), ifOnFood, stop))))))",
			"fitness" : [0.5008678999999999, -24.18888888888889, 0.8, 0.7534576]
		})

		self.tests.append({
			"bt" : "probm3(selm4(seqm2(ifRobotToRight, rr), rl, selm2(rr, ifRobotToRight), probm2(seqm2(seqm2(seqm2(ifNestToRight, seqm2(ifRobotToRight, selm2(rl, rr))), ifInNest), rl), ifOnFood)), selm4(seqm2(selm2(ifRobotToRight, seqm2(ifOnFood, seqm2(seqm2(seqm2(seqm2(rl, seqm2(ifRobotToRight, rr)), fr), seqm2(ifOnFood, rr)), rr))), rr), rl, rr, seqm2(selm4(seqm2(rr, ifRobotToRight), ifInNest, selm2(fr, ifRobotToLeft), probm2(seqm2(rl, seqm2(selm2(ifRobotToRight, seqm2(rl, rr)), rr)), rr)), probm2(rl, seqm2(ifRobotToRight, rr)))), r)",
			"trimmed" : "probm3(selm2(seqm2(ifRobotToRight, rr), rl), selm2(seqm2(selm2(ifRobotToRight, seqm2(ifOnFood, seqm2(seqm2(seqm2(seqm2(rl, seqm2(ifRobotToRight, rr)), fr), seqm2(ifOnFood, rr)), rr))), rr), rl), r)",
			"fitness" : [0.5689943222222222, -13.222222222222223, -0.6444444444444445, 0.4492666666666666]
		})

		self.tests.append({
			"bt" : "selm2(seqm3(seqm4(probm4(r, ifRobotToLeft, selm3(probm3(ifFoodToLeft, probm2(ifOnFood, ifRobotToLeft), stop), seqm3(seqm4(probm3(ifRobotToLeft, f, selm4(ifInNest, ifRobotToRight, ifRobotToLeft, ifOnFood)), seqm3(r, ifRobotToLeft, stop), seqm2(ifFoodToLeft, ifInNest), stop), r, ifRobotToLeft), probm2(ifNestToLeft, ifRobotToLeft)), ifOnFood), seqm3(r, ifRobotToLeft, rl), seqm4(probm4(r, ifRobotToLeft, selm3(probm3(ifFoodToLeft, probm2(ifOnFood, ifRobotToLeft), rl), seqm3(seqm4(probm4(r, ifNestToLeft, selm3(probm3(selm4(ifRobotToRight, stop, ifFoodToRight, ifOnFood), probm2(ifOnFood, seqm2(stop, ifInNest)), ifRobotToRight), selm3(stop, r, ifRobotToRight), probm3(ifOnFood, seqm2(r, fl), ifOnFood)), ifOnFood), seqm3(r, ifRobotToLeft, stop), seqm2(ifFoodToLeft, ifInNest), stop), probm3(seqm2(fl, ifRobotToRight), selm3(rr, ifNestToRight, seqm2(stop, ifRobotToRight)), ifNestToRight), seqm3(r, ifRobotToLeft, stop)), probm2(ifNestToLeft, ifRobotToLeft)), ifOnFood), seqm3(r, ifRobotToLeft, rl), seqm2(ifNestToLeft, ifRobotToRight), probm2(fl, fl)), selm2(fl, fl)), probm3(seqm4(probm4(r, ifOnFood, selm3(probm3(probm4(ifRobotToRight, stop, ifFoodToRight, ifOnFood), probm2(ifRobotToRight, seqm2(stop, ifInNest)), ifOnFood), selm3(stop, ifRobotToRight, ifOnFood), ifOnFood), ifOnFood), rr, seqm2(rl, rr), stop), stop, selm4(ifInNest, stop, ifRobotToLeft, ifFoodToRight)), ifOnFood), seqm3(selm2(probm2(ifRobotToRight, ifNestToRight), ifRobotToRight), rr, ifFoodToRight))",
			"trimmed" : "selm2(seqm3(seqm4(probm4(r, ifRobotToLeft, selm3(probm3(ifFoodToLeft, probm2(ifOnFood, ifRobotToLeft), stop), seqm3(seqm4(probm3(ifRobotToLeft, f, selm4(ifInNest, ifRobotToRight, ifRobotToLeft, ifOnFood)), seqm3(r, ifRobotToLeft, stop), seqm2(ifFoodToLeft, ifInNest), stop), r, ifRobotToLeft), probm2(ifNestToLeft, ifRobotToLeft)), ifOnFood), seqm3(r, ifRobotToLeft, rl), seqm4(probm4(r, ifRobotToLeft, selm3(probm3(ifFoodToLeft, probm2(ifOnFood, ifRobotToLeft), rl), seqm3(seqm4(probm4(r, ifNestToLeft, selm2(probm3(selm2(ifRobotToRight, stop), probm2(ifOnFood, seqm2(stop, ifInNest)), ifRobotToRight), stop), ifOnFood), seqm3(r, ifRobotToLeft, stop), seqm2(ifFoodToLeft, ifInNest), stop), probm3(seqm2(fl, ifRobotToRight), rr, ifNestToRight), seqm3(r, ifRobotToLeft, stop)), probm2(ifNestToLeft, ifRobotToLeft)), ifOnFood), seqm3(r, ifRobotToLeft, rl), seqm2(ifNestToLeft, ifRobotToRight), probm2(fl, fl)), fl), probm3(seqm4(probm4(r, ifOnFood, selm2(probm3(probm4(ifRobotToRight, stop, ifFoodToRight, ifOnFood), probm2(ifRobotToRight, seqm2(stop, ifInNest)), ifOnFood), stop), ifOnFood), rr, seqm2(rl, rr), stop), stop, selm2(ifInNest, stop)), ifOnFood), seqm2(selm2(probm2(ifRobotToRight, ifNestToRight), ifRobotToRight), rr))",
			"fitness" : [0.5656966999999999, -14.61111111111111, 0.7, 0.6119041222222223]
		})

		self.tests.append({
			"bt" : "selm2(seqm3(ifRobotToRight, selm2(ifOnFood, r), rr), selm3(selm4(selm4(rl, ifOnFood, ifRobotToRight, selm2(selm2(ifRobotToRight, ifFoodToLeft), selm2(r, seqm3(ifRobotToRight, ifFoodToLeft, rr)))), selm2(ifOnFood, r), ifFoodToLeft, selm3(selm4(selm4(probm3(fr, ifFoodToLeft, ifOnFood), ifOnFood, stop, ifOnFood), selm2(ifOnFood, r), probm4(ifNestToLeft, ifInNest, ifNestToRight, seqm2(ifOnFood, ifOnFood)), selm4(selm4(rl, ifOnFood, rl, ifOnFood), ifFoodToRight, probm4(rr, stop, ifFoodToRight, probm4(ifRobotToLeft, probm3(stop, ifFoodToLeft, probm4(ifRobotToRight, probm3(stop, ifFoodToLeft, ifOnFood), ifOnFood, probm2(ifRobotToRight, ifOnFood))), r, probm2(selm3(ifRobotToRight, ifInNest, probm4(rl, probm3(ifRobotToRight, ifFoodToLeft, ifOnFood), seqm4(ifRobotToRight, rl, ifFoodToLeft, ifOnFood), probm2(ifOnFood, ifOnFood))), ifFoodToRight))), selm3(rl, ifInNest, probm4(ifNestToLeft, probm2(ifRobotToRight, ifFoodToRight), seqm4(ifNestToRight, rl, rr, ifOnFood), probm2(ifRobotToRight, ifOnFood))))), selm2(ifRobotToRight, selm3(selm4(selm4(ifFoodToLeft, ifOnFood, rl, ifOnFood), selm2(ifFoodToRight, stop), probm4(ifFoodToLeft, stop, ifNestToRight, f), selm4(selm4(rl, ifInNest, rl, ifOnFood), selm2(selm2(ifFoodToRight, ifRobotToLeft), r), probm4(fl, stop, ifFoodToRight, probm4(ifRobotToRight, probm3(stop, ifOnFood, ifOnFood), seqm4(ifRobotToRight, rl, rr, ifOnFood), probm2(ifRobotToRight, ifNestToLeft))), selm3(rl, ifInNest, probm4(rl, probm3(seqm2(stop, f), ifFoodToLeft, ifOnFood), seqm4(ifRobotToRight, rl, ifFoodToLeft, ifOnFood), probm2(ifOnFood, ifOnFood))))), selm2(selm3(rl, ifOnFood, probm4(ifFoodToLeft, probm3(stop, ifFoodToLeft, ifRobotToLeft), selm4(stop, ifFoodToLeft, ifFoodToRight, ifRobotToRight), probm2(ifRobotToRight, ifFoodToRight))), f), ifRobotToRight)), ifRobotToRight)), selm2(selm3(rl, rr, probm4(ifOnFood, probm3(stop, ifOnFood, selm2(r, seqm3(ifRobotToRight, ifFoodToLeft, rr))), r, probm2(ifRobotToRight, ifFoodToRight))), ifOnFood), ifRobotToRight))",
			"trimmed" : "selm2(seqm3(ifRobotToRight, selm2(ifOnFood, r), rr), rl)",
			"fitness" : [0.575399, -6.988888888888889, -0.9222222222222222, 0.5113380555555557]
		})

		self.tests.append({
			"bt" : "probm3(seqm4(seqm4(rr, ifRobotToLeft, selm2(rl, ifInNest), ifFoodToRight), probm4(stop, seqm4(ifRobotToLeft, rr, ifNestToLeft, selm2(r, seqm4(ifFoodToRight, probm4(ifRobotToLeft, ifNestToRight, stop, ifRobotToLeft), selm2(ifFoodToRight, seqm3(ifInNest, ifRobotToLeft, ifNestToRight)), selm2(ifNestToLeft, rl)))), ifRobotToRight, ifRobotToLeft), rl, selm2(ifRobotToLeft, probm2(r, r))), seqm4(seqm4(rr, ifRobotToLeft, rl, ifFoodToRight), probm4(stop, seqm4(ifRobotToLeft, ifOnFood, ifNestToLeft, selm2(ifRobotToLeft, probm4(ifRobotToLeft, ifRobotToLeft, ifRobotToLeft, selm2(ifFoodToLeft, rl)))), ifFoodToLeft, ifRobotToLeft), rl, selm2(ifRobotToLeft, probm2(ifRobotToLeft, r))), seqm3(seqm4(seqm4(seqm4(rr, ifRobotToLeft, rl, ifFoodToRight), probm4(stop, seqm4(ifRobotToLeft, ifFoodToRight, ifNestToLeft, selm2(seqm4(rr, ifRobotToLeft, ifRobotToRight, ifFoodToRight), seqm4(seqm4(rl, ifRobotToLeft, ifRobotToLeft, rr), probm4(stop, ifFoodToRight, stop, ifFoodToRight), ifNestToLeft, seqm2(ifFoodToLeft, ifRobotToLeft)))), ifRobotToRight, ifRobotToLeft), rl, selm2(ifRobotToLeft, probm2(r, r))), ifInNest, ifRobotToLeft, rl), probm2(seqm2(selm2(rl, stop), rl), selm2(seqm2(ifNestToLeft, stop), seqm3(ifInNest, fr, rl))), seqm4(ifRobotToLeft, seqm4(probm2(ifRobotToLeft, ifRobotToLeft), rl, rl, probm4(fl, rr, ifFoodToRight, rr)), seqm2(ifFoodToLeft, ifRobotToLeft), selm2(ifRobotToLeft, seqm4(seqm4(rr, ifRobotToLeft, rl, ifFoodToRight), probm4(stop, selm2(ifNestToLeft, probm2(rl, stop)), ifRobotToRight, ifRobotToLeft), rl, selm2(ifRobotToLeft, rl))))))",
			"trimmed" : "probm3(seqm4(seqm4(rr, ifRobotToLeft, rl, ifFoodToRight), probm4(stop, seqm4(ifRobotToLeft, rr, ifNestToLeft, r), ifRobotToRight, ifRobotToLeft), rl, selm2(ifRobotToLeft, probm2(r, r))), seqm4(seqm4(rr, ifRobotToLeft, rl, ifFoodToRight), probm4(stop, seqm4(ifRobotToLeft, ifOnFood, ifNestToLeft, selm2(ifRobotToLeft, probm4(ifRobotToLeft, ifRobotToLeft, ifRobotToLeft, selm2(ifFoodToLeft, rl)))), ifFoodToLeft, ifRobotToLeft), rl, selm2(ifRobotToLeft, probm2(ifInNest, r))), seqm3(seqm4(seqm4(seqm4(rr, ifRobotToLeft, rl, ifFoodToRight), probm4(stop, seqm4(ifRobotToLeft, ifFoodToRight, ifNestToLeft, selm2(seqm4(rr, ifRobotToLeft, ifRobotToRight, ifFoodToRight), seqm4(seqm4(rl, ifRobotToLeft, ifRobotToLeft, rr), probm4(stop, ifFoodToRight, stop, ifFoodToRight), ifNestToLeft, seqm2(ifFoodToLeft, ifRobotToLeft)))), ifRobotToRight, ifRobotToLeft), rl, selm2(ifRobotToLeft, probm2(r, r))), ifInNest, ifRobotToLeft, rl), probm2(seqm2(rl, rl), selm2(seqm2(ifNestToLeft, stop), seqm3(ifInNest, fr, rl))), seqm4(ifRobotToLeft, seqm4(probm2(ifRobotToLeft, ifRobotToLeft), rl, rl, probm4(fl, rr, ifFoodToRight, rr)), seqm2(ifFoodToLeft, ifRobotToLeft), selm2(ifRobotToLeft, seqm4(seqm4(rr, ifRobotToLeft, rl, ifFoodToRight), probm4(stop, selm2(ifNestToLeft, probm2(rl, stop)), ifRobotToRight, ifRobotToLeft), rl, selm2(ifRobotToLeft, rl))))))",
			"fitness" : [0.5531001999999999, -0.9, 1.9777777777777774, 0.5009403222222223]
		})

		self.tests.append({
			"bt" : "seqm4(selm4(selm4(ifRobotToLeft, selm4(ifRobotToLeft, ifRobotToLeft, fr, ifRobotToLeft), fr, ifOnFood), stop, ifRobotToLeft, ifOnFood), selm2(ifRobotToLeft, seqm4(fr, fr, ifInNest, ifRobotToLeft)), seqm4(seqm4(fl, seqm4(ifRobotToRight, f, f, ifFoodToLeft), ifRobotToLeft, ifRobotToLeft), f, ifRobotToLeft, seqm4(stop, selm4(ifInNest, fr, ifOnFood, ifFoodToLeft), ifFoodToLeft, fl)), probm4(probm2(probm2(f, rl), ifFoodToRight), probm4(ifRobotToLeft, rr, fr, rl), ifRobotToLeft, ifNestToLeft))",
			"trimmed" : "seqm4(selm2(ifRobotToLeft, selm3(ifRobotToLeft, ifRobotToLeft, fr)), selm2(ifRobotToLeft, seqm4(fr, fr, ifInNest, ifRobotToLeft)), seqm4(seqm4(fl, seqm4(ifRobotToRight, f, f, ifFoodToLeft), ifRobotToLeft, ifRobotToLeft), f, ifRobotToLeft, seqm4(stop, selm2(ifInNest, fr), ifFoodToLeft, fl)), probm4(probm2(probm2(f, rl), ifInNest), probm4(ifInNest, rr, fr, rl), ifInNest, ifInNest))",
			"fitness" : [0.5834386777777778, 10.655555555555555, -2.1, 0.6434590222222221]
		})

		self.tests.append({
			"bt" : "seqm4(selm3(ifRobotToRight, rl, selm4(seqm4(rl, ifNestToLeft, fr, ifNestToRight), selm2(r, ifNestToRight), seqm3(ifFoodToLeft, ifRobotToRight, ifOnFood), probm3(ifOnFood, ifRobotToRight, ifOnFood))), seqm3(seqm3(seqm3(ifRobotToRight, rr, ifRobotToLeft), r, r), r, r), ifRobotToRight, selm3(ifNestToRight, rl, probm3(ifNestToLeft, rl, stop)))",
			"trimmed" : "seqm4(selm2(ifRobotToRight, rl), seqm3(seqm3(seqm3(ifRobotToRight, rr, ifRobotToLeft), r, r), r, r), ifRobotToRight, selm2(ifNestToRight, rl))",
			"fitness" : [0.587041122222222, -14.4, -3.022222222222222, 0.5726256222222222]
		})

		self.tests.append({
			"bt" : "selm2(selm4(selm2(seqm3(seqm2(ifRobotToLeft, fl), fl, seqm2(ifRobotToLeft, fl)), seqm2(seqm2(f, probm2(fr, fr)), seqm3(seqm2(ifRobotToLeft, ifNestToLeft), fl, probm2(ifNestToRight, f)))), selm4(ifNestToLeft, ifNestToLeft, fr, ifRobotToLeft), seqm2(r, stop), probm4(seqm2(rl, fl), seqm2(f, fr), seqm2(ifInNest, ifFoodToRight), probm3(seqm4(ifRobotToRight, ifRobotToRight, selm2(ifRobotToRight, fr), stop), selm2(fl, rr), seqm2(ifInNest, ifFoodToRight)))), r)",
			"trimmed" : "selm2(selm2(seqm3(seqm2(ifRobotToLeft, fl), fl, seqm2(ifRobotToLeft, fl)), seqm2(seqm2(f, probm2(fr, fr)), seqm3(seqm2(ifRobotToLeft, ifNestToLeft), fl, probm2(ifNestToRight, f)))), selm3(ifNestToLeft, ifNestToLeft, fr))",
			"fitness" : [0.5739684222222222, 6.8, 3.6222222222222222, 0.5076759666666666]
		})

		self.tests.append({
			"bt" : "seqm4(selm4(ifInNest, selm4(ifInNest, ifRobotToLeft, ifRobotToLeft, ifFoodToRight), probm3(selm4(probm4(ifRobotToRight, ifNestToRight, fr, seqm4(ifRobotToRight, f, ifRobotToRight, ifNestToRight)), ifFoodToRight, selm3(ifNestToRight, fl, ifRobotToLeft), ifFoodToRight), ifRobotToRight, selm3(ifRobotToRight, seqm4(ifRobotToLeft, ifNestToRight, ifRobotToRight, f), ifRobotToLeft)), seqm4(ifRobotToLeft, stop, ifRobotToLeft, ifNestToRight)), seqm2(selm3(ifRobotToRight, fl, rr), ifRobotToRight), fr, selm3(seqm4(ifInNest, probm3(probm4(fr, selm4(ifRobotToLeft, f, probm3(selm4(probm4(ifFoodToLeft, ifFoodToLeft, ifRobotToRight, ifNestToRight), ifFoodToRight, selm3(ifNestToRight, fl, ifRobotToLeft), ifFoodToRight), stop, selm3(ifRobotToRight, seqm4(f, ifRobotToRight, ifRobotToRight, ifNestToRight), ifRobotToLeft)), seqm4(ifRobotToLeft, stop, ifRobotToRight, ifRobotToRight)), rl, ifOnFood), ifRobotToRight, fr), ifRobotToRight, stop), ifRobotToRight, f))",
			"trimmed" : "seqm4(selm4(ifInNest, selm4(ifInNest, ifRobotToLeft, ifRobotToLeft, ifFoodToRight), probm3(selm3(probm4(ifRobotToRight, ifNestToRight, fr, seqm4(ifRobotToRight, f, ifRobotToRight, ifNestToRight)), ifFoodToRight, selm2(ifNestToRight, fl)), ifRobotToRight, selm3(ifRobotToRight, seqm4(ifRobotToLeft, ifNestToRight, ifRobotToRight, f), ifRobotToLeft)), seqm4(ifRobotToLeft, stop, ifRobotToLeft, ifNestToRight)), seqm2(selm2(ifRobotToRight, fl), ifRobotToRight), fr, selm3(seqm4(ifInNest, probm3(probm4(fr, selm2(ifRobotToLeft, f), rl, ifOnFood), ifRobotToRight, fr), ifRobotToRight, stop), ifRobotToRight, f))",
			"fitness" : [0.5744331555555556, 10.655555555555555, -0.6777777777777778, 0.7768779444444445]
		})

		self.tests.append({
			"bt" : "probm2(seqm4(selm4(fr, ifOnFood, ifInNest, seqm4(fl, selm4(ifRobotToLeft, ifOnFood, fr, fr), fr, selm4(f, fr, ifNestToLeft, rl))), seqm4(fl, ifRobotToRight, rl, seqm4(selm4(ifOnFood, ifRobotToLeft, fr, r), seqm4(fl, ifRobotToRight, fr, fr), ifFoodToRight, fr)), selm4(ifRobotToLeft, rl, seqm4(fr, ifRobotToRight, rl, ifNestToLeft), seqm4(selm4(rr, fl, ifNestToRight, rl), seqm4(fl, ifRobotToRight, ifFoodToLeft, fr), ifRobotToRight, fr)), ifOnFood), seqm4(seqm4(fl, seqm4(selm4(ifRobotToLeft, ifOnFood, fr, fr), seqm4(fl, ifRobotToRight, fr, fr), ifRobotToRight, fr), fr, selm4(f, ifFoodToRight, ifNestToLeft, ifRobotToLeft)), rl, seqm4(selm4(ifRobotToLeft, ifOnFood, fr, f), seqm4(fl, ifRobotToRight, fr, fr), ifRobotToRight, fr), ifNestToLeft))",
			"trimmed" : "probm2(seqm3(fr, seqm4(fl, ifRobotToRight, rl, seqm4(selm3(ifOnFood, ifRobotToLeft, fr), seqm4(fl, ifRobotToRight, fr, fr), ifFoodToRight, fr)), selm2(ifRobotToLeft, rl)), seqm3(seqm4(fl, seqm4(selm3(ifRobotToLeft, ifOnFood, fr), seqm4(fl, ifRobotToRight, fr, fr), ifRobotToRight, fr), fr, f), rl, seqm4(selm3(ifRobotToLeft, ifOnFood, fr), seqm4(fl, ifRobotToRight, fr, fr), ifRobotToRight, fr)))",
			"fitness" : [0.5556667777777778, 0.8777777777777779, -1.0555555555555556, 0.4131979111111111]
		})

		self.tests.append({
			"bt" : "seqm4(seqm3(fr, probm3(selm2(ifRobotToLeft, seqm3(seqm4(ifNestToLeft, fl, ifFoodToLeft, fl), probm3(ifNestToLeft, ifFoodToLeft, f), seqm3(ifFoodToLeft, f, ifRobotToLeft))), probm2(f, f), ifRobotToLeft), seqm3(seqm4(ifRobotToLeft, fl, ifFoodToLeft, fl), probm3(ifFoodToLeft, ifRobotToRight, ifRobotToRight), ifRobotToLeft)), selm2(selm2(selm3(ifNestToLeft, ifNestToRight, rr), seqm3(f, ifFoodToRight, r)), selm3(probm3(fl, stop, ifRobotToRight), selm4(ifRobotToRight, rl, ifInNest, stop), probm3(rl, stop, r))), selm3(seqm2(stop, ifNestToLeft), probm3(fr, seqm2(ifRobotToRight, ifNestToLeft), selm3(ifInNest, seqm4(ifRobotToLeft, f, ifRobotToLeft, ifInNest), fl)), seqm4(selm3(seqm2(ifNestToLeft, fr), ifFoodToLeft, ifNestToLeft), probm4(ifNestToLeft, rl, ifRobotToLeft, rl), seqm4(ifFoodToLeft, ifFoodToLeft, fl, r), probm2(r, ifNestToLeft))), seqm4(probm3(rr, ifInNest, ifFoodToLeft), seqm4(selm2(selm3(ifNestToLeft, ifNestToRight, rr), seqm3(ifOnFood, ifFoodToRight, r)), seqm4(fl, fl, ifNestToRight, fr), probm4(rr, ifFoodToLeft, stop, ifRobotToRight), seqm4(ifInNest, ifNestToLeft, ifRobotToRight, ifRobotToRight)), seqm4(selm4(ifNestToLeft, ifRobotToLeft, stop, f), probm3(stop, rr, ifNestToLeft), probm2(selm3(selm3(ifFoodToRight, ifNestToRight, fl), ifRobotToLeft, ifNestToLeft), fl), seqm2(ifNestToLeft, rl)), selm2(selm2(ifRobotToRight, stop), seqm2(ifNestToRight, rr))))",
			"trimmed" : "seqm4(seqm3(fr, probm3(selm2(ifRobotToLeft, seqm3(seqm4(ifNestToLeft, fl, ifFoodToLeft, fl), probm3(ifNestToLeft, ifFoodToLeft, f), seqm3(ifFoodToLeft, f, ifRobotToLeft))), probm2(f, f), ifRobotToLeft), seqm3(seqm4(ifRobotToLeft, fl, ifFoodToLeft, fl), probm3(ifFoodToLeft, ifRobotToRight, ifRobotToRight), ifRobotToLeft)), selm3(ifNestToLeft, ifNestToRight, rr), selm3(seqm2(stop, ifNestToLeft), probm3(fr, seqm2(ifRobotToRight, ifNestToLeft), selm3(ifInNest, seqm4(ifRobotToLeft, f, ifRobotToLeft, ifInNest), fl)), seqm4(selm3(seqm2(ifNestToLeft, fr), ifFoodToLeft, ifNestToLeft), probm4(ifNestToLeft, rl, ifRobotToLeft, rl), seqm4(ifFoodToLeft, ifFoodToLeft, fl, r), probm2(r, ifNestToLeft))), seqm4(probm3(rr, ifInNest, ifFoodToLeft), seqm4(selm3(ifNestToLeft, ifNestToRight, rr), seqm4(fl, fl, ifNestToRight, fr), probm4(rr, ifFoodToLeft, stop, ifRobotToRight), seqm4(ifInNest, ifNestToLeft, ifRobotToRight, ifRobotToRight)), seqm4(selm3(ifNestToLeft, ifRobotToLeft, stop), probm3(stop, rr, ifNestToLeft), probm2(selm3(ifFoodToRight, ifNestToRight, fl), fl), seqm2(ifNestToLeft, rl)), selm2(ifRobotToRight, stop)))",
			"fitness" : [0.5422671444444445, 6.088888888888889, 0.17777777777777767, 0.5298775555555556]
		})

		self.tests.append({
			"bt" : "selm2(seqm3(ifRobotToRight, seqm3(selm4(seqm3(ifRobotToLeft, ifRobotToLeft, fr), ifRobotToLeft, fr, ifRobotToRight), fr, selm4(ifInNest, ifInNest, probm3(f, seqm4(ifOnFood, ifNestToRight, f, probm4(ifInNest, fr, f, fl)), ifInNest), ifRobotToLeft)), probm3(f, selm4(ifOnFood, ifNestToRight, f, ifNestToRight), f)), seqm3(ifRobotToLeft, selm4(ifInNest, ifRobotToLeft, fr, ifNestToRight), selm4(fl, selm4(ifInNest, stop, ifFoodToLeft, f), fr, probm2(ifNestToRight, ifInNest))))",
			"trimmed" : "selm2(seqm3(ifRobotToRight, seqm3(selm3(seqm3(ifRobotToLeft, ifRobotToLeft, fr), ifRobotToLeft, fr), fr, selm4(ifInNest, ifInNest, probm3(f, seqm4(ifOnFood, ifNestToRight, f, probm4(ifInNest, fr, f, fl)), ifInNest), ifRobotToLeft)), probm3(f, selm3(ifOnFood, ifNestToRight, f), f)), seqm3(ifRobotToLeft, selm3(ifInNest, ifRobotToLeft, fr), fl))",
			"fitness" : [0.5724882666666667, 10.644444444444444, -0.0666666666666667, 0.7205909444444444]
		})

		self.tests.append({
			"bt" : "probm3(r, seqm4(ifRobotToLeft, selm3(seqm3(ifFoodToRight, seqm3(ifFoodToRight, r, ifFoodToRight), ifFoodToRight), seqm2(rl, ifInNest), seqm4(ifOnFood, ifNestToRight, probm3(seqm4(probm2(rl, ifFoodToRight), selm3(seqm2(rl, f), ifRobotToLeft, seqm4(seqm2(seqm3(ifFoodToRight, ifOnFood, ifOnFood), seqm2(ifOnFood, ifNestToLeft)), r, seqm2(fr, ifOnFood), seqm4(ifFoodToRight, probm4(ifRobotToRight, ifNestToLeft, seqm4(probm3(probm4(ifFoodToRight, r, ifRobotToRight, ifInNest), ifFoodToRight, probm4(ifFoodToRight, ifFoodToLeft, selm3(rl, rl, selm2(seqm3(ifFoodToRight, seqm3(stop, r, ifFoodToRight), ifFoodToRight), rl)), ifFoodToRight)), selm3(seqm3(ifInNest, ifNestToRight, ifRobotToRight), ifFoodToRight, probm4(rr, fl, ifFoodToLeft, fr)), ifFoodToRight, probm3(rl, seqm3(seqm4(seqm2(ifOnFood, ifNestToRight), probm4(ifRobotToRight, ifInNest, seqm4(selm3(ifNestToRight, ifFoodToRight, probm4(ifFoodToRight, ifOnFood, ifFoodToLeft, ifOnFood)), selm3(seqm3(r, ifRobotToLeft, ifOnFood), ifFoodToRight, probm4(seqm4(ifRobotToLeft, rl, ifRobotToRight, ifNestToRight), ifOnFood, ifNestToRight, ifOnFood)), ifFoodToRight, probm3(ifFoodToRight, seqm3(ifFoodToRight, probm3(ifOnFood, ifOnFood, r), seqm2(ifFoodToLeft, ifFoodToRight)), probm3(probm3(fl, ifFoodToRight, rl), ifFoodToRight, seqm4(ifNestToLeft, ifFoodToRight, rl, r)))), ifOnFood), probm4(rl, seqm3(ifFoodToLeft, ifNestToRight, rl), ifInNest, ifInNest), ifNestToRight), probm3(ifNestToLeft, fr, r), ifOnFood), selm3(probm3(ifFoodToRight, probm3(rr, rl, r), ifRobotToLeft), stop, ifOnFood))), ifFoodToRight), probm4(ifFoodToRight, ifNestToLeft, ifInNest, ifRobotToRight), ifNestToLeft))), rl, ifOnFood), seqm2(rl, ifOnFood), ifRobotToLeft), selm3(seqm4(selm2(ifFoodToRight, ifNestToRight), selm3(probm3(ifFoodToRight, seqm3(ifRobotToLeft, probm3(stop, ifRobotToLeft, ifNestToLeft), ifOnFood), ifFoodToRight), seqm2(rl, ifFoodToRight), seqm4(seqm4(ifOnFood, stop, ifNestToRight, stop), stop, r, ifNestToRight)), r, r), seqm2(rl, ifRobotToRight), probm4(fl, ifFoodToRight, ifNestToLeft, ifInNest)))), ifNestToRight, seqm4(ifNestToLeft, stop, ifNestToLeft, ifInNest)), selm4(ifRobotToLeft, ifNestToLeft, rr, ifNestToLeft))",
			"trimmed" : "probm3(r, seqm4(ifRobotToLeft, selm3(seqm3(ifFoodToRight, seqm3(ifFoodToRight, r, ifFoodToRight), ifFoodToRight), seqm2(rl, ifInNest), seqm4(ifOnFood, ifNestToRight, probm3(seqm4(probm2(rl, ifFoodToRight), seqm2(rl, f), rl, ifOnFood), seqm2(rl, ifOnFood), ifRobotToLeft), selm3(seqm4(selm2(ifFoodToRight, ifNestToRight), selm3(probm3(ifFoodToRight, seqm3(ifRobotToLeft, probm3(stop, ifRobotToLeft, ifNestToLeft), ifOnFood), ifFoodToRight), seqm2(rl, ifFoodToRight), seqm4(seqm4(ifOnFood, stop, ifNestToRight, stop), stop, r, ifNestToRight)), r, r), seqm2(rl, ifRobotToRight), probm4(fl, ifFoodToRight, ifNestToLeft, ifInNest)))), ifNestToRight, seqm2(ifNestToLeft, stop)), selm3(ifRobotToLeft, ifNestToLeft, rr))",
			"fitness" : [0.5406416555555555, -18.255555555555553, -1.211111111111111, 0.675723]
		})

		self.tests.append({
			"bt" : "seqm4(selm2(ifRobotToLeft, rr), seqm3(ifRobotToLeft, rl, seqm3(selm3(ifRobotToRight, seqm3(ifNestToRight, rr, rl), rl), selm2(ifRobotToLeft, seqm3(selm3(ifRobotToRight, ifRobotToLeft, r), selm2(r, ifRobotToLeft), r)), ifInNest)), seqm3(selm3(seqm3(r, ifNestToRight, seqm4(probm2(rl, rl), rl, selm2(r, ifNestToRight), fl)), ifRobotToRight, ifRobotToLeft), ifNestToRight, selm3(ifNestToRight, ifFoodToLeft, seqm4(probm2(selm3(ifRobotToRight, ifRobotToRight, rl), r), probm3(probm2(ifNestToLeft, ifNestToRight), ifInNest, ifNestToRight), selm2(rl, r), selm3(selm3(ifNestToRight, ifNestToRight, ifInNest), rr, ifNestToRight)))), rl)",
			"trimmed" : "seqm4(selm2(ifRobotToLeft, rr), seqm3(ifRobotToLeft, rl, seqm3(selm3(ifRobotToRight, seqm3(ifNestToRight, rr, rl), rl), selm2(ifRobotToLeft, seqm3(selm3(ifRobotToRight, ifRobotToLeft, r), r, r)), ifInNest)), seqm3(selm3(seqm3(r, ifNestToRight, seqm4(probm2(rl, rl), rl, r, fl)), ifRobotToRight, ifRobotToLeft), ifNestToRight, selm3(ifNestToRight, ifFoodToLeft, seqm4(probm2(selm3(ifRobotToRight, ifRobotToRight, rl), r), probm3(probm2(ifNestToLeft, ifNestToRight), ifInNest, ifNestToRight), rl, selm2(selm3(ifNestToRight, ifNestToRight, ifInNest), rr)))), rl)",
			"fitness" : [0.5870354333333333, -13.977777777777778, -0.7777777777777777, 0.6612502444444445]
		})

		self.tests.append({
			"bt" : "probm2(seqm4(selm4(ifInNest, ifRobotToLeft, ifRobotToLeft, rr), selm3(selm4(ifFoodToLeft, ifRobotToLeft, ifInNest, ifNestToRight), fr, fr), seqm4(rl, selm2(ifRobotToRight, ifNestToRight), seqm3(rr, rr, ifNestToRight), probm4(ifOnFood, ifRobotToLeft, fl, ifOnFood)), seqm4(rr, selm2(rr, probm3(ifRobotToLeft, probm4(ifNestToRight, ifOnFood, ifNestToRight, ifRobotToLeft), seqm4(ifOnFood, fr, ifNestToLeft, stop))), ifOnFood, seqm4(fl, ifRobotToLeft, r, r))), r)",
			"trimmed" : "probm2(seqm4(selm4(ifInNest, ifRobotToLeft, ifRobotToLeft, rr), selm2(selm4(ifFoodToLeft, ifRobotToLeft, ifInNest, ifNestToRight), fr), seqm4(rl, selm2(ifRobotToRight, ifNestToRight), seqm3(rr, rr, ifNestToRight), probm4(ifOnFood, ifRobotToLeft, fl, ifOnFood)), seqm4(rr, rr, ifOnFood, seqm4(fl, ifRobotToLeft, r, r))), r)",
			"fitness" : [0.5505757000000001, -14.822222222222223, 0.9555555555555555, 0.6427540888888889]
		})

		self.tests.append({
			"bt" : "seqm3(selm3(selm3(selm4(ifRobotToLeft, rr, ifRobotToLeft, stop), fl, selm3(ifFoodToRight, probm2(fl, ifFoodToLeft), probm2(probm3(probm4(selm3(probm4(r, rr, ifOnFood, selm3(ifFoodToRight, probm2(fl, f), f)), ifFoodToRight, selm3(ifFoodToRight, probm2(fl, r), probm2(ifFoodToRight, stop))), rr, ifRobotToLeft, fl), probm2(seqm2(rr, selm3(selm3(probm4(ifRobotToLeft, rr, ifRobotToLeft, stop), ifRobotToLeft, ifFoodToRight), selm2(probm2(fl, f), r), r)), stop), ifNestToRight), selm3(selm3(selm4(fl, rr, stop, stop), ifFoodToRight, selm3(ifFoodToRight, probm2(rl, r), probm2(fl, ifFoodToLeft))), probm2(probm2(fl, r), ifFoodToRight), ifNestToRight)))), probm2(seqm2(selm4(ifFoodToRight, ifRobotToLeft, ifNestToRight, ifFoodToRight), probm3(selm3(selm4(seqm2(rr, selm3(selm2(probm2(fl, r), r), probm2(probm2(rr, stop), rr), ifNestToRight)), rr, ifRobotToLeft, stop), ifNestToRight, selm3(ifFoodToRight, probm2(fl, r), f)), f, rr)), ifFoodToLeft), ifNestToRight), ifRobotToLeft, selm2(rl, rr))",
			"trimmed" : "seqm3(selm2(ifRobotToLeft, rr), ifRobotToLeft, rl)",
			"fitness" : [0.5673182999999999, 0.0, -2.022222222222222, 0.6358586777777779]
		})

		self.tests.append({
			"bt" : "selm3(seqm2(seqm2(probm3(ifFoodToLeft, probm4(ifInNest, rl, ifInNest, ifRobotToRight), ifRobotToLeft), seqm2(ifRobotToLeft, rl)), ifRobotToLeft), seqm2(seqm3(seqm2(ifRobotToLeft, rl), r, rl), r), selm4(selm4(rr, ifRobotToLeft, ifInNest, r), seqm2(seqm3(seqm2(ifRobotToLeft, r), r, rl), r), ifRobotToLeft, probm2(probm4(rl, seqm3(ifNestToRight, ifRobotToRight, rl), ifRobotToLeft, f), probm4(ifRobotToLeft, seqm2(ifRobotToLeft, rl), ifRobotToLeft, ifRobotToRight))))",
			"trimmed" : "selm3(seqm2(seqm2(probm3(ifFoodToLeft, probm4(ifInNest, rl, ifInNest, ifRobotToRight), ifRobotToLeft), seqm2(ifRobotToLeft, rl)), ifRobotToLeft), seqm2(seqm3(seqm2(ifRobotToLeft, rl), r, rl), r), rr)",
			"fitness" : [0.581783688888889, -9.322222222222223, 0.5222222222222223, 0.5679173555555557]
		})

		self.tests.append({
			"bt" : "selm4(seqm2(selm3(ifNestToLeft, rr, selm3(selm4(probm4(ifFoodToRight, probm3(probm2(r, ifNestToRight), probm4(ifRobotToLeft, ifInNest, ifNestToLeft, ifInNest), ifRobotToLeft), ifFoodToLeft, ifRobotToRight), probm3(probm3(ifRobotToRight, seqm4(ifRobotToLeft, ifInNest, ifNestToLeft, ifFoodToLeft), seqm3(ifInNest, fr, fr)), ifNestToLeft, ifOnFood), probm4(ifRobotToRight, stop, ifNestToRight, ifFoodToRight), ifRobotToLeft), ifInNest, seqm4(ifInNest, probm2(ifInNest, rl), ifFoodToRight, ifNestToLeft))), probm2(r, ifNestToRight)), rl, probm3(ifRobotToRight, seqm4(ifRobotToLeft, ifInNest, ifNestToLeft, ifInNest), seqm3(ifInNest, fr, fr)), seqm4(rr, selm3(seqm4(selm3(selm4(probm4(ifFoodToRight, ifRobotToLeft, ifFoodToLeft, ifRobotToRight), fr, seqm4(ifRobotToRight, stop, ifRobotToLeft, rr), rl), ifNestToLeft, fr), ifNestToLeft, ifNestToRight, selm2(ifFoodToRight, ifNestToLeft)), rl, ifInNest), ifRobotToLeft, probm2(ifFoodToLeft, ifNestToLeft)))",
			"trimmed" : "selm2(seqm2(selm2(ifNestToLeft, rr), probm2(r, ifNestToRight)), rl)",
			"fitness" : [0.5532371333333334, -16.53333333333333, 0.9555555555555555, 0.4975775222222222]
		})

		self.tests.append({
			"bt" : "seqm3(selm3(selm3(ifRobotToRight, rl, r), selm3(ifNestToRight, selm3(ifRobotToRight, rl, r), ifNestToRight), fl), ifRobotToRight, seqm2(seqm3(selm3(ifRobotToRight, ifNestToRight, r), rr, selm4(ifNestToRight, r, ifOnFood, r)), seqm3(ifNestToRight, seqm3(selm3(ifRobotToRight, ifNestToRight, r), rr, selm4(ifNestToRight, r, ifOnFood, r)), ifRobotToRight)))",
			"trimmed" : "seqm3(selm2(ifRobotToRight, rl), ifRobotToRight, seqm2(seqm3(selm3(ifRobotToRight, ifNestToRight, r), rr, selm2(ifNestToRight, r)), seqm2(ifNestToRight, seqm3(selm3(ifRobotToRight, ifNestToRight, r), rr, selm2(ifNestToRight, r)))))",
			"fitness" : [0.5967119666666667, -12.322222222222223, -0.6333333333333333, 0.7017033777777778]
		})

		self.tests.append({
			"bt" : "probm2(seqm4(ifRobotToRight, selm4(rr, ifInNest, ifNestToRight, ifRobotToRight), rr, selm3(ifNestToRight, seqm4(ifRobotToRight, selm4(rr, ifRobotToLeft, ifNestToRight, selm3(ifInNest, ifOnFood, rl)), rr, rr), rl)), probm4(rl, seqm4(rl, seqm4(ifRobotToRight, selm4(rr, stop, probm4(rl, f, seqm4(rl, seqm4(selm3(r, selm3(ifOnFood, probm4(ifNestToRight, stop, seqm4(probm3(ifInNest, ifRobotToLeft, ifOnFood), rr, rl, rl), rl), rl), rl), selm4(ifFoodToRight, stop, fl, fr), rr, selm3(rr, probm4(rl, ifNestToLeft, seqm4(probm3(ifInNest, stop, stop), ifRobotToRight, rl, rl), rl), rl)), ifOnFood, selm3(ifRobotToRight, ifOnFood, ifNestToRight)), rl), selm3(stop, ifOnFood, seqm4(selm3(ifRobotToRight, probm4(rl, ifNestToLeft, seqm4(probm3(ifInNest, ifRobotToRight, stop), ifInNest, rl, rl), rl), rl), probm3(ifNestToLeft, ifRobotToRight, fr), rl, ifRobotToRight))), rr, selm3(rr, probm4(ifNestToRight, fl, seqm4(probm3(r, ifOnFood, rr), stop, rl, stop), ifInNest), selm4(rr, ifRobotToLeft, ifRobotToLeft, ifRobotToRight))), rr, selm3(ifOnFood, ifOnFood, probm3(ifInNest, rl, rr))), seqm4(rl, seqm4(ifRobotToRight, selm4(rr, ifRobotToLeft, probm4(fr, ifNestToLeft, seqm4(selm3(rl, fl, rl), selm4(rr, stop, fl, seqm4(rl, selm3(rr, probm4(ifRobotToLeft, rl, probm3(ifInNest, ifRobotToRight, f), ifNestToRight), rl), rl, ifRobotToRight)), probm4(selm3(rr, probm3(ifInNest, rl, rr), ifOnFood), ifNestToLeft, seqm4(selm4(rr, ifRobotToLeft, ifNestToRight, selm3(ifRobotToRight, ifOnFood, rl)), seqm4(ifNestToLeft, selm4(rr, stop, fl, probm4(ifNestToLeft, stop, probm3(ifInNest, ifRobotToRight, rl), ifNestToRight)), rr, selm3(rr, probm4(rl, ifNestToLeft, rl, rl), rl)), rr, ifNestToLeft), rl), probm4(rl, ifNestToLeft, seqm4(probm3(ifRobotToLeft, ifRobotToRight, stop), ifInNest, rl, rl), rl)), rl), probm3(ifInNest, ifRobotToRight, stop)), rr, selm3(rr, ifNestToRight, ifOnFood)), rr, selm3(ifRobotToRight, ifOnFood, seqm4(rl, rl, rr, selm3(ifNestToLeft, r, ifNestToLeft)))), rl))",
			"trimmed" : "probm2(seqm4(ifRobotToRight, rr, rr, selm3(ifNestToRight, seqm4(ifRobotToRight, rr, rr, rr), rl)), probm4(rl, seqm4(rl, seqm4(ifRobotToRight, rr, rr, rr), rr, selm3(ifOnFood, ifOnFood, probm3(ifInNest, rl, rr))), seqm4(rl, seqm4(ifRobotToRight, rr, rr, rr), rr, selm3(ifRobotToRight, ifOnFood, seqm4(rl, rl, rr, selm2(ifNestToLeft, r)))), rl))",
			"fitness" : [0.5525260111111111, -0.4444444444444445, -2.411111111111111, 0.4645167333333333]
		})

		self.tests.append({
			"bt" : "probm2(seqm3(ifRobotToLeft, rl, seqm3(rl, seqm3(ifRobotToLeft, rl, seqm3(rl, seqm3(ifRobotToLeft, seqm3(ifRobotToLeft, rl, seqm3(rl, rl, seqm3(ifRobotToRight, ifRobotToRight, r))), seqm3(ifNestToLeft, seqm3(r, rr, ifNestToRight), selm3(rr, seqm3(rl, rl, rl), ifRobotToRight))), seqm3(rl, seqm3(fr, seqm3(ifRobotToRight, ifNestToRight, r), ifInNest), seqm3(rl, ifRobotToRight, selm3(rl, ifInNest, ifRobotToLeft))))), fr)), rr)",
			"trimmed" : "probm2(seqm3(ifRobotToLeft, rl, seqm3(rl, seqm3(ifRobotToLeft, rl, seqm3(rl, seqm3(ifRobotToLeft, seqm3(ifRobotToLeft, rl, seqm3(rl, rl, seqm3(ifRobotToRight, ifRobotToRight, r))), seqm3(ifNestToLeft, seqm3(r, rr, ifNestToRight), rr)), seqm3(rl, seqm3(fr, seqm3(ifRobotToRight, ifNestToRight, r), ifInNest), seqm3(rl, ifRobotToRight, rl)))), fr)), rr)",
			"fitness" : [0.5496916000000001, -0.8, -0.033333333333333305, 0.4305357222222222]
		})

		self.tests.append({
			"bt" : "selm2(seqm3(ifRobotToRight, seqm3(selm4(seqm3(ifRobotToLeft, ifRobotToLeft, fr), ifRobotToLeft, fr, ifRobotToRight), fr, selm4(ifInNest, ifInNest, probm3(f, seqm4(ifOnFood, ifNestToRight, f, probm4(ifInNest, fr, f, fl)), ifInNest), ifRobotToLeft)), probm3(f, selm4(ifOnFood, ifNestToRight, f, ifNestToRight), f)), seqm3(ifRobotToLeft, selm4(ifInNest, ifRobotToLeft, fr, ifNestToRight), selm4(fl, selm4(ifInNest, stop, ifFoodToLeft, f), fr, probm2(ifNestToRight, ifInNest))))",
			"trimmed" : "selm2(seqm3(ifRobotToRight, seqm3(selm3(seqm3(ifRobotToLeft, ifRobotToLeft, fr), ifRobotToLeft, fr), fr, selm4(ifInNest, ifInNest, probm3(f, seqm4(ifOnFood, ifNestToRight, f, probm4(ifInNest, fr, f, fl)), ifInNest), ifRobotToLeft)), probm3(f, selm3(ifOnFood, ifNestToRight, f), f)), seqm3(ifRobotToLeft, selm3(ifInNest, ifRobotToLeft, fr), fl))",
			"fitness" : [0.5724882666666667, 10.644444444444444, -0.0666666666666667, 0.7205909444444444]
		})

		self.tests.append({
			"bt" : "probm3(r, seqm4(ifRobotToLeft, selm3(seqm3(ifFoodToRight, seqm3(ifFoodToRight, r, ifFoodToRight), ifFoodToRight), seqm2(rl, ifInNest), seqm4(ifOnFood, ifNestToRight, probm3(seqm4(probm2(rl, ifFoodToRight), selm3(seqm2(rl, f), ifRobotToLeft, seqm4(seqm2(seqm3(ifFoodToRight, ifOnFood, ifOnFood), seqm2(ifOnFood, ifNestToLeft)), r, seqm2(fr, ifOnFood), seqm4(ifFoodToRight, probm4(ifRobotToRight, ifNestToLeft, seqm4(probm3(probm4(ifFoodToRight, r, ifRobotToRight, ifInNest), ifFoodToRight, probm4(ifFoodToRight, ifFoodToLeft, selm3(rl, rl, selm2(seqm3(ifFoodToRight, seqm3(stop, r, ifFoodToRight), ifFoodToRight), rl)), ifFoodToRight)), selm3(seqm3(ifInNest, ifNestToRight, ifRobotToRight), ifFoodToRight, probm4(rr, fl, ifFoodToLeft, fr)), ifFoodToRight, probm3(rl, seqm3(seqm4(seqm2(ifOnFood, ifNestToRight), probm4(ifRobotToRight, ifInNest, seqm4(selm3(ifNestToRight, ifFoodToRight, probm4(ifFoodToRight, ifOnFood, ifFoodToLeft, ifOnFood)), selm3(seqm3(r, ifRobotToLeft, ifOnFood), ifFoodToRight, probm4(seqm4(ifRobotToLeft, rl, ifRobotToRight, ifNestToRight), ifOnFood, ifNestToRight, ifOnFood)), ifFoodToRight, probm3(ifFoodToRight, seqm3(ifFoodToRight, probm3(ifOnFood, ifOnFood, r), seqm2(ifFoodToLeft, ifFoodToRight)), probm3(probm3(fl, ifFoodToRight, rl), ifFoodToRight, seqm4(ifNestToLeft, ifFoodToRight, rl, r)))), ifOnFood), probm4(rl, seqm3(ifFoodToLeft, ifNestToRight, rl), ifInNest, ifInNest), ifNestToRight), probm3(ifNestToLeft, fr, r), ifOnFood), selm3(probm3(ifFoodToRight, probm3(rr, rl, r), ifRobotToLeft), stop, ifOnFood))), ifFoodToRight), probm4(ifFoodToRight, ifNestToLeft, ifInNest, ifRobotToRight), ifNestToLeft))), rl, ifOnFood), seqm2(rl, ifOnFood), ifRobotToLeft), selm3(seqm4(selm2(ifFoodToRight, ifNestToRight), selm3(probm3(ifFoodToRight, seqm3(ifRobotToLeft, probm3(stop, ifRobotToLeft, ifNestToLeft), ifOnFood), ifFoodToRight), seqm2(rl, ifFoodToRight), seqm4(seqm4(ifOnFood, stop, ifNestToRight, stop), stop, r, ifNestToRight)), r, r), seqm2(rl, ifRobotToRight), probm4(fl, ifFoodToRight, ifNestToLeft, ifInNest)))), ifNestToRight, seqm4(ifNestToLeft, stop, ifNestToLeft, ifInNest)), selm4(ifRobotToLeft, ifNestToLeft, rr, ifNestToLeft))",
			"trimmed" : "probm3(r, seqm4(ifRobotToLeft, selm3(seqm3(ifFoodToRight, seqm3(ifFoodToRight, r, ifFoodToRight), ifFoodToRight), seqm2(rl, ifInNest), seqm4(ifOnFood, ifNestToRight, probm3(seqm4(probm2(rl, ifFoodToRight), seqm2(rl, f), rl, ifOnFood), seqm2(rl, ifOnFood), ifRobotToLeft), selm3(seqm4(selm2(ifFoodToRight, ifNestToRight), selm3(probm3(ifFoodToRight, seqm3(ifRobotToLeft, probm3(stop, ifRobotToLeft, ifNestToLeft), ifOnFood), ifFoodToRight), seqm2(rl, ifFoodToRight), seqm4(seqm4(ifOnFood, stop, ifNestToRight, stop), stop, r, ifNestToRight)), r, r), seqm2(rl, ifRobotToRight), probm4(fl, ifFoodToRight, ifNestToLeft, ifInNest)))), ifNestToRight, seqm2(ifNestToLeft, stop)), selm3(ifRobotToLeft, ifNestToLeft, rr))",
			"fitness" : [0.5406416555555555, -18.255555555555553, -1.211111111111111, 0.675723]
		})

		self.tests.append({
			"bt" : "seqm4(selm2(ifRobotToLeft, rr), seqm3(ifRobotToLeft, rl, seqm3(selm3(ifRobotToRight, seqm3(ifNestToRight, rr, rl), rl), selm2(ifRobotToLeft, seqm3(selm3(ifRobotToRight, ifRobotToLeft, r), selm2(r, ifRobotToLeft), r)), ifInNest)), seqm3(selm3(seqm3(r, ifNestToRight, seqm4(probm2(rl, rl), rl, selm2(r, ifNestToRight), fl)), ifRobotToRight, ifRobotToLeft), ifNestToRight, selm3(ifNestToRight, ifFoodToLeft, seqm4(probm2(selm3(ifRobotToRight, ifRobotToRight, rl), r), probm3(probm2(ifNestToLeft, ifNestToRight), ifInNest, ifNestToRight), selm2(rl, r), selm3(selm3(ifNestToRight, ifNestToRight, ifInNest), rr, ifNestToRight)))), rl)",
			"trimmed" : "seqm4(selm2(ifRobotToLeft, rr), seqm3(ifRobotToLeft, rl, seqm3(selm3(ifRobotToRight, seqm3(ifNestToRight, rr, rl), rl), selm2(ifRobotToLeft, seqm3(selm3(ifRobotToRight, ifRobotToLeft, r), r, r)), ifInNest)), seqm3(selm3(seqm3(r, ifNestToRight, seqm4(probm2(rl, rl), rl, r, fl)), ifRobotToRight, ifRobotToLeft), ifNestToRight, selm3(ifNestToRight, ifFoodToLeft, seqm4(probm2(selm3(ifRobotToRight, ifRobotToRight, rl), r), probm3(probm2(ifNestToLeft, ifNestToRight), ifInNest, ifNestToRight), rl, selm2(selm3(ifNestToRight, ifNestToRight, ifInNest), rr)))), rl)",
			"fitness" : [0.5870354333333333, -13.977777777777778, -0.7777777777777777, 0.6612502444444445]
		})

		self.tests.append({
			"bt" : "probm2(seqm4(selm4(ifInNest, ifRobotToLeft, ifRobotToLeft, rr), selm3(selm4(ifFoodToLeft, ifRobotToLeft, ifInNest, ifNestToRight), fr, fr), seqm4(rl, selm2(ifRobotToRight, ifNestToRight), seqm3(rr, rr, ifNestToRight), probm4(ifOnFood, ifRobotToLeft, fl, ifOnFood)), seqm4(rr, selm2(rr, probm3(ifRobotToLeft, probm4(ifNestToRight, ifOnFood, ifNestToRight, ifRobotToLeft), seqm4(ifOnFood, fr, ifNestToLeft, stop))), ifOnFood, seqm4(fl, ifRobotToLeft, r, r))), r)",
			"trimmed" : "probm2(seqm4(selm4(ifInNest, ifRobotToLeft, ifRobotToLeft, rr), selm2(selm4(ifFoodToLeft, ifRobotToLeft, ifInNest, ifNestToRight), fr), seqm4(rl, selm2(ifRobotToRight, ifNestToRight), seqm3(rr, rr, ifNestToRight), probm4(ifOnFood, ifRobotToLeft, fl, ifOnFood)), seqm4(rr, rr, ifOnFood, seqm4(fl, ifRobotToLeft, r, r))), r)",
			"fitness" : [0.5505757000000001, -14.822222222222223, 0.9555555555555555, 0.6427540888888889]
		})

		self.tests.append({
			"bt" : "seqm3(selm3(selm3(selm4(ifRobotToLeft, rr, ifRobotToLeft, stop), fl, selm3(ifFoodToRight, probm2(fl, ifFoodToLeft), probm2(probm3(probm4(selm3(probm4(r, rr, ifOnFood, selm3(ifFoodToRight, probm2(fl, f), f)), ifFoodToRight, selm3(ifFoodToRight, probm2(fl, r), probm2(ifFoodToRight, stop))), rr, ifRobotToLeft, fl), probm2(seqm2(rr, selm3(selm3(probm4(ifRobotToLeft, rr, ifRobotToLeft, stop), ifRobotToLeft, ifFoodToRight), selm2(probm2(fl, f), r), r)), stop), ifNestToRight), selm3(selm3(selm4(fl, rr, stop, stop), ifFoodToRight, selm3(ifFoodToRight, probm2(rl, r), probm2(fl, ifFoodToLeft))), probm2(probm2(fl, r), ifFoodToRight), ifNestToRight)))), probm2(seqm2(selm4(ifFoodToRight, ifRobotToLeft, ifNestToRight, ifFoodToRight), probm3(selm3(selm4(seqm2(rr, selm3(selm2(probm2(fl, r), r), probm2(probm2(rr, stop), rr), ifNestToRight)), rr, ifRobotToLeft, stop), ifNestToRight, selm3(ifFoodToRight, probm2(fl, r), f)), f, rr)), ifFoodToLeft), ifNestToRight), ifRobotToLeft, selm2(rl, rr))",
			"trimmed" : "seqm3(selm2(ifRobotToLeft, rr), ifRobotToLeft, rl)",
			"fitness" : [0.5673182999999999, 0.0, -2.022222222222222, 0.6358586777777779]
		})

		self.tests.append({
			"bt" : "seqm2(seqm3(ifInNest, ifRobotToRight, r), seqm4(ifRobotToRight, fl, ifRobotToLeft, r))",
			"trimmed" : "seqm2(seqm3(ifInNest, ifRobotToRight, r), seqm4(ifRobotToRight, fl, ifRobotToLeft, r))",
			"fitness" : [0.5007736000000002, -0.7666666666666666, 0.7444444444444445, 0.9878674333333335]
		})

		self.tests.append({
			"bt" : "seqm2(seqm4(ifOnFood, rr, rl, ifRobotToLeft), selm4(f, r, r, ifOnFood))",
			"trimmed" : "seqm2(seqm4(ifOnFood, rr, rl, ifRobotToLeft), f)",
			"fitness" : [0.49817641111111116, 2.2444444444444445, -0.4111111111111111, 0.9157953666666666]
		})

		self.tests.append({
			"bt" : "seqm3(selm3(seqm2(probm3(ifOnFood, ifOnFood, ifOnFood), probm4(ifOnFood, rr, ifRobotToLeft, fl)), selm3(selm4(fr, ifOnFood, stop, ifNestToRight), seqm4(ifRobotToRight, stop, ifNestToRight, ifFoodToRight), selm3(fl, ifNestToRight, r)), seqm4(seqm3(rr, ifOnFood, ifRobotToLeft), probm4(rr, fl, ifInNest, ifNestToLeft), seqm3(ifInNest, fr, ifFoodToRight), probm4(rr, ifRobotToLeft, stop, rl))), selm3(seqm3(seqm3(f, rr, ifRobotToRight), probm4(ifRobotToLeft, f, rl, ifOnFood), seqm4(ifNestToRight, fr, r, ifRobotToLeft)), selm4(probm2(ifFoodToRight, stop), probm3(ifInNest, ifRobotToRight, fl), probm4(ifInNest, r, ifNestToLeft, stop), selm4(ifFoodToRight, ifRobotToRight, fr, ifOnFood)), seqm4(selm2(ifFoodToLeft, fr), selm4(fl, ifNestToLeft, ifNestToLeft, stop), selm3(ifOnFood, r, ifNestToRight), probm4(rr, rl, stop, ifNestToRight))), selm4(probm4(probm3(rl, f, ifFoodToRight), seqm4(rr, ifFoodToLeft, fl, stop), selm2(ifRobotToLeft, r), probm4(r, ifNestToLeft, stop, r)), probm4(selm3(ifRobotToLeft, ifOnFood, ifRobotToRight), probm3(f, stop, ifNestToRight), probm4(ifRobotToLeft, ifRobotToRight, rl, ifFoodToRight), selm4(ifFoodToRight, ifOnFood, stop, stop)), probm3(seqm4(f, ifOnFood, r, ifNestToRight), probm2(stop, f), probm2(rl, ifInNest)), probm4(seqm3(ifOnFood, rl, fl), seqm2(ifInNest, rl), selm2(ifRobotToRight, ifOnFood), seqm3(ifNestToRight, ifFoodToLeft, ifInNest))))",
			"trimmed" : "seqm3(selm2(seqm2(probm3(ifOnFood, ifOnFood, ifOnFood), probm4(ifOnFood, rr, ifRobotToLeft, fl)), fr), selm2(seqm3(seqm3(f, rr, ifRobotToRight), probm4(ifRobotToLeft, f, rl, ifOnFood), seqm4(ifNestToRight, fr, r, ifRobotToLeft)), selm4(probm2(ifFoodToRight, stop), probm3(ifInNest, ifRobotToRight, fl), probm4(ifInNest, r, ifNestToLeft, stop), selm3(ifFoodToRight, ifRobotToRight, fr))), selm4(probm4(probm3(rl, f, ifFoodToRight), seqm4(rr, ifFoodToLeft, fl, stop), selm2(ifRobotToLeft, r), probm4(r, ifNestToLeft, stop, r)), probm4(selm3(ifRobotToLeft, ifOnFood, ifRobotToRight), probm3(f, stop, ifNestToRight), probm4(ifRobotToLeft, ifRobotToRight, rl, ifFoodToRight), selm3(ifFoodToRight, ifOnFood, stop)), probm3(seqm4(f, ifOnFood, r, ifNestToRight), probm2(stop, f), probm2(rl, ifInNest)), probm4(seqm3(ifOnFood, rl, fl), seqm2(ifInNest, rl), ifInNest, ifInNest)))",
			"fitness" : [0.49989463333333334, 4.722222222222222, 2.2333333333333334, 0.4795404333333334]
		})

		self.tests.append({
			"bt" : "probm3(seqm3(ifInNest, ifNestToLeft, ifNestToLeft), seqm3(stop, ifNestToLeft, fl), seqm3(fl, fr, ifFoodToLeft))",
			"trimmed" : "probm3(ifInNest, seqm3(stop, ifNestToLeft, fl), seqm2(fl, fr))",
			"fitness" : [0.5023144333333333, 0.0, -2.422222222222222, 0.492915]
		})

		self.tests.append({
			"bt" : "probm3(seqm4(seqm4(seqm2(ifOnFood, ifFoodToLeft), selm4(ifFoodToRight, ifRobotToLeft, r, ifNestToRight), seqm3(ifInNest, ifFoodToLeft, rr), probm4(ifNestToRight, f, ifRobotToLeft, rl)), selm2(selm3(ifOnFood, ifRobotToLeft, ifNestToLeft), selm2(fr, ifNestToLeft)), seqm4(probm4(fl, ifRobotToLeft, stop, rl), selm3(fl, r, fr), probm4(ifRobotToRight, ifNestToRight, stop, fl), selm2(ifRobotToLeft, fl)), probm3(selm4(ifOnFood, fr, ifFoodToLeft, ifNestToLeft), selm3(rr, ifOnFood, ifFoodToLeft), seqm2(rl, ifInNest))), seqm3(seqm3(probm2(ifRobotToLeft, f), seqm3(ifNestToLeft, ifOnFood, stop), selm2(f, rl)), selm3(seqm4(ifNestToLeft, rl, rl, rl), probm4(ifOnFood, ifRobotToLeft, ifNestToRight, ifFoodToRight), seqm2(ifNestToRight, f)), selm4(selm3(ifRobotToRight, ifInNest, fl), selm4(ifFoodToLeft, stop, ifRobotToRight, ifOnFood), probm3(f, rl, ifRobotToLeft), seqm3(ifOnFood, ifNestToLeft, ifNestToRight))), probm3(probm2(probm3(ifRobotToLeft, ifNestToRight, ifFoodToLeft), seqm2(rl, ifRobotToLeft)), probm4(probm3(rr, rr, rl), probm4(ifRobotToRight, r, stop, ifNestToRight), seqm2(fr, ifOnFood), seqm2(ifNestToLeft, ifNestToLeft)), probm2(probm4(ifNestToRight, ifFoodToLeft, r, ifFoodToRight), probm4(rl, ifFoodToLeft, ifFoodToRight, ifFoodToRight))))",
			"trimmed" : "probm3(seqm4(seqm4(seqm2(ifOnFood, ifFoodToLeft), selm3(ifFoodToRight, ifRobotToLeft, r), seqm3(ifInNest, ifFoodToLeft, rr), probm4(ifNestToRight, f, ifRobotToLeft, rl)), selm2(selm3(ifOnFood, ifRobotToLeft, ifNestToLeft), fr), seqm4(probm4(fl, ifRobotToLeft, stop, rl), fl, probm4(ifRobotToRight, ifNestToRight, stop, fl), selm2(ifRobotToLeft, fl)), probm3(selm2(ifOnFood, fr), rr, rl)), seqm3(seqm3(probm2(ifRobotToLeft, f), seqm3(ifNestToLeft, ifOnFood, stop), f), selm3(seqm4(ifNestToLeft, rl, rl, rl), probm4(ifOnFood, ifRobotToLeft, ifNestToRight, ifFoodToRight), seqm2(ifNestToRight, f)), selm3(ifRobotToRight, ifInNest, fl)), probm3(probm2(probm3(ifInNest, ifInNest, ifInNest), rl), probm4(probm3(rr, rr, rl), probm4(ifInNest, r, stop, ifInNest), fr, ifInNest), probm2(probm4(ifInNest, ifInNest, r, ifInNest), probm4(rl, ifInNest, ifInNest, ifInNest))))",
			"fitness" : [0.5026199666666666, 9.055555555555554, -4.844444444444444, 0.7546594333333335]
		})

		self.tests.append({
			"bt" : "seqm2(seqm3(selm3(rl, f, r), seqm4(ifNestToLeft, f, stop, r), seqm2(ifFoodToRight, ifOnFood)), selm4(seqm2(ifRobotToLeft, rl), probm2(rl, ifNestToLeft), probm3(ifInNest, f, f), selm4(ifInNest, f, stop, ifNestToRight)))",
			"trimmed" : "seqm2(seqm3(rl, seqm4(ifNestToLeft, f, stop, r), seqm2(ifFoodToRight, ifOnFood)), selm4(seqm2(ifRobotToLeft, rl), probm2(rl, ifNestToLeft), probm3(ifInNest, f, f), selm2(ifInNest, f)))",
			"fitness" : [0.49275450000000004, -4.6, -21.133333333333333, 0.41426747777777767]
		})

		self.tests.append({
			"bt" : "seqm3(ifFoodToRight, rr, ifFoodToLeft)",
			"trimmed" : "seqm2(ifFoodToRight, rr)",
			"fitness" : [0.5052457777777778, 0.0, 3.7777777777777777, 0.9589260555555559]
		})

		self.tests.append({
			"bt" : "seqm4(rr, ifFoodToLeft, ifInNest, r)",
			"trimmed" : "seqm4(rr, ifFoodToLeft, ifInNest, r)",
			"fitness" : [0.5076742333333332, -3.6444444444444444, 36.355555555555554, 0.5469761111111111]
		})

		self.tests.append({
			"bt" : "seqm3(ifOnFood, f, fl)",
			"trimmed" : "seqm3(ifOnFood, f, fl)",
			"fitness" : [0.5001877222222223, 1.6888888888888889, 3.3111111111111113, 0.9174721777777778]
		})

		self.tests.append({
			"bt" : "seqm2(ifRobotToLeft, ifInNest)",
			"trimmed" : "ifRobotToLeft",
			"fitness" : [0.499769988888889, 0.0, 0.0, 1.0]
		})

		self.tests.append({
			"bt" : "selm3(ifNestToRight, r, f)",
			"trimmed" : "selm2(ifNestToRight, r)",
			"fitness" : [0.5040090555555556, -24.011111111111113, 0.0, 0.699696711111111]
		})

		self.tests.append({
			"bt" : "probm2(seqm2(seqm4(probm2(fl, ifNestToRight), probm2(fr, rl), seqm2(ifRobotToLeft, rr), selm4(r, stop, rr, rl)), seqm3(probm4(ifFoodToLeft, fr, ifRobotToRight, ifFoodToRight), seqm2(ifNestToRight, fl), probm3(ifOnFood, ifOnFood, ifOnFood))), seqm3(probm3(seqm4(ifRobotToLeft, ifFoodToRight, ifRobotToLeft, ifInNest), seqm2(rr, ifFoodToRight), seqm4(ifInNest, ifFoodToLeft, ifNestToRight, r)), probm4(seqm4(fl, ifFoodToRight, ifFoodToLeft, ifNestToLeft), probm4(ifNestToRight, ifFoodToLeft, ifNestToRight, ifNestToRight), probm3(ifInNest, rl, ifFoodToLeft), seqm2(r, ifRobotToRight)), seqm2(probm3(ifNestToRight, ifRobotToLeft, ifFoodToLeft), selm2(ifFoodToRight, ifNestToLeft))))",
			"trimmed" : "probm2(seqm2(seqm4(probm2(fl, ifNestToRight), probm2(fr, rl), seqm2(ifRobotToLeft, rr), r), seqm3(probm4(ifFoodToLeft, fr, ifRobotToRight, ifFoodToRight), seqm2(ifNestToRight, fl), probm3(ifInNest, ifInNest, ifInNest))), seqm3(probm3(seqm4(ifRobotToLeft, ifFoodToRight, ifRobotToLeft, ifInNest), seqm2(rr, ifFoodToRight), seqm4(ifInNest, ifFoodToLeft, ifNestToRight, r)), probm4(seqm4(fl, ifFoodToRight, ifFoodToLeft, ifNestToLeft), probm4(ifNestToRight, ifFoodToLeft, ifNestToRight, ifNestToRight), probm3(ifInNest, rl, ifFoodToLeft), seqm2(r, ifRobotToRight)), probm3(ifInNest, ifInNest, ifInNest)))",
			"fitness" : [0.4935315888888889, -5.2444444444444445, 3.9333333333333336, 0.560297711111111]
		})

		self.tests.append({
			"bt" : "seqm3(selm3(probm3(ifInNest, stop, f), seqm2(ifNestToRight, ifNestToRight), selm2(r, ifNestToRight)), selm4(seqm2(ifFoodToLeft, stop), seqm2(fr, ifInNest), selm2(fl, ifOnFood), seqm3(r, r, ifFoodToRight)), seqm4(seqm4(rl, rl, ifNestToLeft, ifInNest), probm4(r, r, ifFoodToRight, ifInNest), probm4(fl, ifNestToLeft, ifNestToLeft, r), probm2(ifNestToLeft, rl)))",
			"trimmed" : "seqm3(selm3(probm3(ifInNest, stop, f), seqm2(ifNestToRight, ifNestToRight), r), selm3(seqm2(ifFoodToLeft, stop), seqm2(fr, ifInNest), fl), seqm4(seqm4(rl, rl, ifNestToLeft, ifInNest), probm4(r, r, ifFoodToRight, ifInNest), probm4(fl, ifNestToLeft, ifNestToLeft, r), probm2(ifInNest, rl)))",
			"fitness" : [0.5010917333333333, 1.2444444444444445, -23.9, 0.46221539999999994]
		})

		self.tests.append({
			"bt" : "seqm3(seqm2(probm4(rl, rr, f, ifFoodToLeft), probm2(rr, ifNestToRight)), probm2(probm4(rr, fr, ifOnFood, r), probm3(rl, rr, f)), probm4(selm3(ifNestToLeft, ifFoodToLeft, ifRobotToLeft), probm4(ifNestToLeft, ifOnFood, fr, rl), selm3(ifFoodToLeft, r, ifInNest), seqm4(r, ifRobotToLeft, stop, ifFoodToLeft)))",
			"trimmed" : "seqm3(seqm2(probm4(rl, rr, f, ifFoodToLeft), probm2(rr, ifNestToRight)), probm2(probm4(rr, fr, ifOnFood, r), probm3(rl, rr, f)), probm4(ifInNest, probm4(ifInNest, ifInNest, fr, rl), selm2(ifFoodToLeft, r), seqm3(r, ifRobotToLeft, stop)))",
			"fitness" : [0.49671955555555575, 0.611111111111111, 5.133333333333333, 0.40983121111111115]
		})

		self.tests.append({
			"bt" : "probm4(seqm4(selm2(selm4(rl, ifFoodToRight, ifNestToLeft, ifFoodToLeft), seqm4(ifOnFood, r, fl, rr)), selm4(selm2(ifOnFood, fr), probm3(f, ifNestToLeft, f), probm2(ifNestToLeft, ifFoodToLeft), seqm3(ifRobotToLeft, f, ifRobotToLeft)), probm2(seqm2(ifNestToRight, ifRobotToRight), selm2(ifNestToLeft, stop)), probm3(probm4(rr, fl, rr, ifRobotToRight), selm3(ifNestToRight, ifFoodToRight, ifRobotToRight), seqm4(ifNestToRight, fr, ifRobotToLeft, ifFoodToRight))), probm4(seqm3(selm3(ifOnFood, rr, ifInNest), probm4(fl, rr, ifFoodToRight, ifNestToLeft), probm4(r, r, rr, ifNestToRight)), seqm3(seqm3(fr, ifFoodToLeft, rl), probm4(ifFoodToRight, ifNestToLeft, fr, fr), seqm4(f, ifInNest, rl, ifInNest)), probm4(selm4(ifNestToLeft, ifNestToLeft, ifFoodToLeft, ifRobotToLeft), selm3(f, fr, r), selm2(ifRobotToRight, fl), selm4(fr, fl, ifFoodToRight, ifRobotToLeft)), probm4(probm2(stop, fr), selm2(stop, ifInNest), seqm3(fl, ifInNest, ifFoodToLeft), seqm2(ifNestToLeft, r))), seqm2(seqm4(selm3(rl, ifRobotToLeft, r), selm4(ifRobotToLeft, ifNestToLeft, rr, ifFoodToRight), seqm4(ifNestToLeft, f, rr, ifRobotToRight), selm3(ifInNest, ifRobotToLeft, f)), probm4(selm4(rr, ifInNest, fl, ifFoodToLeft), seqm3(ifNestToRight, ifRobotToLeft, fr), probm4(ifOnFood, ifNestToRight, stop, ifRobotToRight), selm2(ifOnFood, fl))), selm3(seqm3(selm3(ifNestToLeft, ifFoodToLeft, ifNestToLeft), probm4(ifNestToRight, ifFoodToLeft, ifFoodToLeft, f), seqm3(rl, fl, ifRobotToRight)), probm2(probm4(ifFoodToRight, ifRobotToRight, ifRobotToLeft, rl), seqm2(r, ifNestToRight)), selm4(selm3(ifFoodToLeft, r, ifInNest), selm2(ifInNest, f), selm2(stop, ifFoodToLeft), probm2(ifInNest, stop))))",
			"trimmed" : "probm4(seqm4(rl, selm2(ifOnFood, fr), probm2(seqm2(ifNestToRight, ifRobotToRight), selm2(ifNestToLeft, stop)), probm3(probm4(rr, fl, rr, ifInNest), ifInNest, seqm2(ifNestToRight, fr))), probm4(seqm3(selm2(ifOnFood, rr), probm4(fl, rr, ifFoodToRight, ifNestToLeft), probm4(r, r, rr, ifInNest)), seqm3(seqm3(fr, ifFoodToLeft, rl), probm4(ifFoodToRight, ifNestToLeft, fr, fr), seqm3(f, ifInNest, rl)), probm4(ifInNest, f, selm2(ifRobotToRight, fl), fr), probm4(probm2(stop, fr), stop, fl, seqm2(ifNestToLeft, r))), seqm2(seqm4(rl, selm3(ifRobotToLeft, ifNestToLeft, rr), seqm4(ifNestToLeft, f, rr, ifRobotToRight), selm3(ifInNest, ifRobotToLeft, f)), probm4(rr, seqm3(ifNestToRight, ifRobotToLeft, fr), probm4(ifInNest, ifInNest, stop, ifInNest), selm2(ifOnFood, fl))), selm3(seqm3(selm3(ifNestToLeft, ifFoodToLeft, ifNestToLeft), probm4(ifNestToRight, ifFoodToLeft, ifFoodToLeft, f), seqm3(rl, fl, ifRobotToRight)), probm2(probm4(ifFoodToRight, ifRobotToRight, ifRobotToLeft, rl), seqm2(r, ifNestToRight)), selm2(ifFoodToLeft, r)))",
			"fitness" : [0.5043377333333333, -3.6888888888888887, -6.7, 0.5962667888888887]
		})

		self.tests.append({
			"bt" : "seqm3(selm4(probm4(fl, ifFoodToRight, r, stop), probm3(ifOnFood, ifInNest, ifRobotToRight), seqm4(ifFoodToRight, ifFoodToLeft, stop, ifRobotToLeft), probm3(r, fr, fl)), seqm4(seqm2(fl, rr), selm4(ifRobotToLeft, ifNestToRight, stop, ifOnFood), seqm3(fl, f, fr), probm4(ifNestToRight, rr, ifRobotToRight, f)), probm4(selm4(rr, fr, fr, ifFoodToLeft), probm2(ifRobotToRight, f), probm4(ifNestToRight, ifFoodToRight, stop, ifOnFood), selm4(f, ifRobotToLeft, ifRobotToLeft, ifFoodToRight)))",
			"trimmed" : "seqm3(selm4(probm4(fl, ifFoodToRight, r, stop), probm3(ifOnFood, ifInNest, ifRobotToRight), seqm4(ifFoodToRight, ifFoodToLeft, stop, ifRobotToLeft), probm3(r, fr, fl)), seqm4(seqm2(fl, rr), selm3(ifRobotToLeft, ifNestToRight, stop), seqm3(fl, f, fr), probm4(ifNestToRight, rr, ifRobotToRight, f)), probm4(rr, probm2(ifInNest, f), probm4(ifInNest, ifInNest, stop, ifInNest), f))",
			"fitness" : [0.49779737777777777, 7.166666666666666, 13.266666666666666, 0.2802874222222222]
		})

		self.tests.append({
			"bt" : "seqm4(fr, ifNestToRight, fl, fl)",
			"trimmed" : "seqm4(fr, ifNestToRight, fl, fl)",
			"fitness" : [0.47654929999999995, 0.0, -9.311111111111112, 0.37224841111111096]
		})

		self.tests.append({
			"bt" : "selm2(selm4(probm2(fl, r), selm4(r, ifFoodToLeft, rl, ifNestToLeft), seqm2(rl, r), selm2(ifFoodToRight, rr)), seqm3(selm4(rl, fl, stop, ifFoodToLeft), probm2(ifRobotToRight, rl), seqm3(ifRobotToRight, ifNestToLeft, ifRobotToRight)))",
			"trimmed" : "probm2(fl, r)",
			"fitness" : [0.4986953111111111, -18.93333333333333, 21.06666666666667, 0.0]
		})

		self.tests.append({
			"bt" : "seqm3(stop, ifInNest, fr)",
			"trimmed" : "seqm3(stop, ifInNest, fr)",
			"fitness" : [0.4989186111111111, 0.0, -5.833333333333334, 0.4623368333333332]
		})

		self.tests.append({
			"bt" : "seqm2(probm3(seqm2(seqm4(ifOnFood, ifNestToLeft, stop, fr), probm2(fr, ifInNest)), selm4(seqm3(f, ifFoodToLeft, ifNestToRight), probm4(ifNestToRight, ifNestToRight, rr, ifFoodToRight), seqm3(ifInNest, ifInNest, fr), probm4(fl, ifFoodToRight, ifRobotToRight, stop)), probm4(selm2(ifNestToLeft, ifFoodToLeft), probm4(ifFoodToLeft, ifFoodToRight, f, fr), selm3(ifRobotToLeft, stop, ifRobotToLeft), probm2(ifRobotToRight, r))), seqm3(probm3(selm3(ifFoodToLeft, f, fr), selm3(rl, fl, ifOnFood), selm4(ifFoodToRight, rr, ifRobotToLeft, rr)), selm3(seqm3(ifNestToRight, ifInNest, fl), probm2(rl, f), seqm4(f, rr, rr, fr)), probm2(seqm3(ifRobotToRight, stop, ifNestToLeft), probm2(r, ifNestToLeft))))",
			"trimmed" : "seqm2(probm3(seqm2(seqm4(ifOnFood, ifNestToLeft, stop, fr), probm2(fr, ifInNest)), selm4(seqm3(f, ifFoodToLeft, ifNestToRight), probm4(ifNestToRight, ifNestToRight, rr, ifFoodToRight), seqm3(ifInNest, ifInNest, fr), probm4(fl, ifFoodToRight, ifRobotToRight, stop)), probm4(selm2(ifNestToLeft, ifFoodToLeft), probm4(ifFoodToLeft, ifFoodToRight, f, fr), selm2(ifRobotToLeft, stop), probm2(ifRobotToRight, r))), seqm3(probm3(selm2(ifFoodToLeft, f), rl, selm2(ifFoodToRight, rr)), selm2(seqm3(ifNestToRight, ifInNest, fl), probm2(rl, f)), probm2(seqm2(ifRobotToRight, stop), probm2(r, ifInNest))))",
			"fitness" : [0.4991778, 7.777777777777777, -6.311111111111112, 0.6280080222222223]
		})

		self.tests.append({
			"bt" : "probm3(seqm3(selm4(selm3(ifInNest, fr, ifNestToRight), seqm3(ifInNest, ifInNest, ifNestToRight), selm4(ifFoodToRight, ifRobotToRight, rr, ifInNest), probm2(ifOnFood, ifOnFood)), selm2(selm3(fl, ifOnFood, ifRobotToRight), probm4(rl, fr, rr, f)), seqm4(probm3(fl, rl, ifFoodToLeft), seqm2(f, fr), probm2(ifInNest, ifNestToRight), selm4(ifNestToRight, ifRobotToRight, ifRobotToRight, ifRobotToLeft))), probm2(selm3(selm3(rl, ifFoodToLeft, ifRobotToRight), probm4(f, ifRobotToLeft, ifNestToRight, ifRobotToRight), seqm3(ifFoodToRight, ifRobotToRight, f)), seqm2(selm3(ifInNest, ifOnFood, ifOnFood), selm2(rl, ifRobotToRight))), probm3(selm4(seqm3(rr, ifNestToRight, ifRobotToLeft), probm2(rr, rl), probm2(r, rr), selm2(ifOnFood, ifRobotToLeft)), probm2(probm4(ifOnFood, f, ifRobotToLeft, ifFoodToLeft), probm2(ifInNest, ifRobotToRight)), seqm3(selm2(ifOnFood, stop), selm2(stop, rl), probm2(ifOnFood, rr))))",
			"trimmed" : "probm3(seqm3(selm2(ifInNest, fr), fl, seqm3(probm3(fl, rl, ifFoodToLeft), seqm2(f, fr), probm2(ifInNest, ifInNest))), probm2(rl, seqm2(selm3(ifInNest, ifOnFood, ifOnFood), rl)), probm3(selm2(seqm3(rr, ifNestToRight, ifRobotToLeft), probm2(rr, rl)), probm2(probm4(ifInNest, f, ifInNest, ifInNest), probm2(ifInNest, ifInNest)), seqm3(selm2(ifOnFood, stop), stop, probm2(ifInNest, rr))))",
			"fitness" : [0.4995142111111113, 3.5666666666666673, -6.988888888888889, 0.4406734]
		})

		self.tests.append({
			"bt" : "seqm2(selm4(seqm2(ifNestToRight, ifOnFood), seqm4(fl, ifNestToLeft, fr, ifFoodToLeft), selm3(fl, ifRobotToRight, ifRobotToLeft), probm3(fl, ifFoodToLeft, ifFoodToLeft)), selm3(selm3(ifOnFood, f, rr), probm2(ifFoodToRight, ifRobotToLeft), probm4(fl, stop, ifOnFood, rr)))",
			"trimmed" : "seqm2(selm3(seqm2(ifNestToRight, ifOnFood), seqm4(fl, ifNestToLeft, fr, ifFoodToLeft), fl), selm2(ifOnFood, f))",
			"fitness" : [0.4857958555555556, 13.355555555555554, 14.455555555555554, 0.6060275555555555]
		})

		self.tests.append({
			"bt" : "probm4(selm4(probm4(ifNestToRight, fr, rr, stop), selm4(rr, fl, ifInNest, fr), seqm3(fr, f, fr), seqm2(ifFoodToLeft, ifNestToLeft)), seqm2(probm2(ifOnFood, rr), selm3(rl, ifRobotToLeft, rl)), selm2(selm2(fl, ifInNest), probm4(ifRobotToRight, stop, ifFoodToRight, ifInNest)), probm3(selm2(ifNestToLeft, stop), selm2(ifRobotToRight, fl), probm2(rr, ifRobotToLeft)))",
			"trimmed" : "probm4(selm2(probm4(ifNestToRight, fr, rr, stop), rr), seqm2(probm2(ifOnFood, rr), rl), fl, probm3(selm2(ifNestToLeft, stop), selm2(ifRobotToRight, fl), probm2(rr, ifInNest)))",
			"fitness" : [0.496704, 0.0, 12.522222222222222, 0.3050153555555556]
		})

		self.tests.append({
			"bt" : "selm2(probm4(seqm3(seqm2(ifFoodToLeft, r), probm3(ifInNest, ifFoodToLeft, ifOnFood), selm4(ifOnFood, fr, ifFoodToLeft, ifFoodToRight)), probm2(seqm3(r, ifRobotToLeft, r), seqm2(rl, fl)), seqm3(seqm2(ifRobotToLeft, rl), selm3(stop, stop, ifNestToRight), probm3(rr, ifFoodToRight, stop)), selm4(seqm4(ifInNest, ifNestToLeft, fl, rl), seqm4(stop, stop, fr, rl), probm4(stop, ifOnFood, rr, rl), seqm3(fr, ifNestToLeft, ifNestToRight))), probm3(selm4(probm4(ifFoodToRight, ifInNest, ifRobotToLeft, ifFoodToRight), probm2(f, ifInNest), selm2(ifFoodToLeft, rl), probm4(ifFoodToRight, ifRobotToLeft, ifFoodToLeft, ifFoodToRight)), probm3(seqm3(ifFoodToRight, fr, fr), probm4(stop, ifOnFood, stop, ifInNest), probm2(ifFoodToRight, rr)), probm3(probm3(f, ifInNest, ifRobotToRight), seqm3(ifRobotToRight, ifRobotToRight, rr), probm3(rr, fr, ifRobotToLeft))))",
			"trimmed" : "selm2(probm4(seqm3(seqm2(ifFoodToLeft, r), probm3(ifInNest, ifFoodToLeft, ifOnFood), selm2(ifOnFood, fr)), probm2(seqm3(r, ifRobotToLeft, r), seqm2(rl, fl)), seqm3(seqm2(ifRobotToLeft, rl), stop, probm3(rr, ifFoodToRight, stop)), selm2(seqm4(ifInNest, ifNestToLeft, fl, rl), seqm4(stop, stop, fr, rl))), probm3(selm3(probm4(ifFoodToRight, ifInNest, ifRobotToLeft, ifFoodToRight), probm2(f, ifInNest), selm2(ifFoodToLeft, rl)), probm3(seqm3(ifFoodToRight, fr, fr), probm4(stop, ifInNest, stop, ifInNest), probm2(ifInNest, rr)), probm3(probm3(f, ifInNest, ifInNest), seqm3(ifRobotToRight, ifRobotToRight, rr), probm3(rr, fr, ifInNest))))",
			"fitness" : [0.49960057777777767, -3.0, -9.466666666666667, 0.41140192222222216]
		})

		self.tests.append({
			"bt" : "selm2(ifNestToLeft, ifOnFood)",
			"trimmed" : "ifNestToLeft",
			"fitness" : [0.499769988888889, 0.0, 0.0, 1.0]
		})

		self.tests.append({
			"bt" : "seqm3(selm3(probm3(probm3(r, fl, ifFoodToRight), selm4(ifFoodToLeft, ifRobotToRight, f, ifFoodToRight), probm4(stop, ifNestToLeft, ifOnFood, ifNestToLeft)), seqm3(selm3(f, ifNestToLeft, rr), seqm2(ifNestToLeft, r), selm4(fr, f, ifOnFood, r)), seqm2(probm4(fl, ifFoodToLeft, fr, ifInNest), selm3(ifFoodToLeft, ifInNest, fl))), probm4(seqm2(seqm2(r, rl), selm3(fl, rl, ifNestToLeft)), probm4(selm4(ifOnFood, f, ifFoodToRight, rr), seqm4(fr, r, ifFoodToLeft, ifNestToRight), selm3(f, ifRobotToRight, rl), selm3(ifRobotToLeft, ifRobotToRight, fl)), probm3(probm4(rr, ifNestToRight, r, ifRobotToRight), seqm2(rl, rl), seqm3(ifRobotToLeft, ifNestToRight, ifOnFood)), probm4(selm4(stop, rr, ifRobotToRight, ifInNest), selm4(f, rr, stop, r), selm4(ifOnFood, ifFoodToRight, rl, ifRobotToRight), selm2(ifNestToRight, ifFoodToLeft))), selm2(probm4(seqm2(rl, ifFoodToLeft), probm4(rr, fr, ifFoodToRight, r), probm4(fl, f, stop, ifFoodToLeft), probm4(ifRobotToLeft, stop, rl, rr)), probm4(selm4(f, fl, f, ifFoodToLeft), seqm4(ifFoodToLeft, ifNestToLeft, stop, ifRobotToRight), probm2(stop, r), probm2(ifFoodToLeft, fl))))",
			"trimmed" : "seqm3(selm3(probm3(probm3(r, fl, ifFoodToRight), selm3(ifFoodToLeft, ifRobotToRight, f), probm4(stop, ifNestToLeft, ifOnFood, ifNestToLeft)), seqm3(f, seqm2(ifNestToLeft, r), fr), seqm2(probm4(fl, ifFoodToLeft, fr, ifInNest), selm3(ifFoodToLeft, ifInNest, fl))), probm4(seqm2(seqm2(r, rl), fl), probm4(selm2(ifOnFood, f), seqm4(fr, r, ifFoodToLeft, ifNestToRight), f, selm3(ifRobotToLeft, ifRobotToRight, fl)), probm3(probm4(rr, ifNestToRight, r, ifRobotToRight), seqm2(rl, rl), seqm3(ifRobotToLeft, ifNestToRight, ifOnFood)), probm4(stop, f, selm3(ifOnFood, ifFoodToRight, rl), selm2(ifNestToRight, ifFoodToLeft))), selm2(probm4(seqm2(rl, ifFoodToLeft), probm4(rr, fr, ifFoodToRight, r), probm4(fl, f, stop, ifFoodToLeft), probm4(ifRobotToLeft, stop, rl, rr)), probm4(f, seqm3(ifFoodToLeft, ifNestToLeft, stop), probm2(stop, r), probm2(ifInNest, fl))))",
			"fitness" : [0.49557831111111106, 1.4666666666666668, -0.9444444444444443, 0.43520301111111126]
		})

		self.tests.append({
			"bt" : "selm4(fr, fl, f, ifOnFood)",
			"trimmed" : "fr",
			"fitness" : [0.4975353333333333, 0.0, -40.0, 0.0]
		})

		self.tests.append({
			"bt" : "selm4(selm4(seqm3(rr, fl, rr), selm2(rr, ifInNest), seqm2(rl, ifOnFood), selm4(ifFoodToLeft, ifRobotToRight, ifFoodToLeft, r)), probm3(seqm4(r, ifFoodToRight, ifRobotToLeft, ifRobotToRight), seqm2(ifRobotToRight, ifFoodToRight), probm2(ifRobotToLeft, ifNestToLeft)), selm2(probm2(rl, ifFoodToLeft), probm3(rl, ifNestToLeft, f)), seqm3(selm4(ifFoodToLeft, stop, ifFoodToLeft, fr), selm4(fr, ifFoodToLeft, ifRobotToLeft, ifFoodToRight), seqm4(ifNestToRight, fr, rl, ifRobotToRight)))",
			"trimmed" : "seqm3(rr, fl, rr)",
			"fitness" : [0.49847988888888894, 0.0, 40.0, 0.0]
		})

		self.tests.append({
			"bt" : "selm4(seqm2(seqm2(probm2(ifNestToRight, ifNestToLeft), selm3(fr, ifOnFood, ifInNest)), seqm3(probm2(ifRobotToRight, r), seqm2(ifRobotToLeft, fl), probm2(rl, ifOnFood))), seqm2(selm4(selm2(stop, ifNestToRight), probm4(ifRobotToLeft, ifFoodToRight, ifOnFood, fl), seqm2(fr, stop), selm4(rl, fl, fr, ifInNest)), seqm3(seqm3(ifNestToLeft, ifRobotToRight, r), selm2(r, ifNestToRight), seqm2(rl, ifRobotToLeft))), seqm2(seqm4(seqm3(fl, stop, ifRobotToRight), selm4(ifInNest, f, rl, ifRobotToRight), seqm2(ifNestToLeft, ifRobotToLeft), selm3(ifNestToLeft, stop, ifFoodToLeft)), selm4(probm4(ifFoodToLeft, rl, ifRobotToRight, fl), probm4(rr, ifNestToRight, r, r), probm3(rl, ifRobotToRight, ifInNest), selm2(r, fr))), probm3(seqm3(selm2(stop, fl), seqm4(ifFoodToLeft, r, rr, rl), seqm2(ifNestToRight, stop)), seqm3(seqm3(fr, ifNestToRight, ifRobotToLeft), probm2(ifNestToLeft, ifFoodToLeft), selm3(ifRobotToLeft, stop, fl)), selm2(probm4(rl, f, stop, ifNestToLeft), selm4(ifFoodToLeft, ifFoodToLeft, ifRobotToRight, fr))))",
			"trimmed" : "selm4(seqm2(seqm2(probm2(ifNestToRight, ifNestToLeft), fr), seqm3(probm2(ifRobotToRight, r), seqm2(ifRobotToLeft, fl), probm2(rl, ifOnFood))), seqm2(stop, seqm3(seqm3(ifNestToLeft, ifRobotToRight, r), r, seqm2(rl, ifRobotToLeft))), seqm2(seqm4(seqm3(fl, stop, ifRobotToRight), selm2(ifInNest, f), seqm2(ifNestToLeft, ifRobotToLeft), selm2(ifNestToLeft, stop)), selm4(probm4(ifFoodToLeft, rl, ifRobotToRight, fl), probm4(rr, ifNestToRight, r, r), probm3(rl, ifRobotToRight, ifInNest), r)), probm3(seqm3(stop, seqm4(ifFoodToLeft, r, rr, rl), seqm2(ifNestToRight, stop)), seqm3(seqm3(fr, ifNestToRight, ifRobotToLeft), probm2(ifNestToLeft, ifFoodToLeft), selm2(ifRobotToLeft, stop)), selm2(probm4(rl, f, stop, ifNestToLeft), selm4(ifFoodToLeft, ifFoodToLeft, ifRobotToRight, fr))))",
			"fitness" : [0.5015679333333333, 0.8666666666666666, -2.3666666666666663, 0.5215017222222222]
		})

		self.tests.append({
			"bt" : "seqm3(seqm4(selm3(ifRobotToRight, ifFoodToRight, f), seqm4(ifNestToRight, ifFoodToRight, ifNestToLeft, f), probm2(fr, rr), seqm4(stop, ifNestToLeft, ifOnFood, stop)), probm3(probm4(fr, ifNestToLeft, fl, r), selm3(ifFoodToRight, f, ifRobotToRight), seqm4(ifFoodToRight, ifInNest, ifNestToLeft, rr)), probm2(seqm3(ifNestToRight, ifInNest, fl), probm4(rl, fr, ifOnFood, f)))",
			"trimmed" : "seqm3(seqm4(selm3(ifRobotToRight, ifFoodToRight, f), seqm4(ifNestToRight, ifFoodToRight, ifNestToLeft, f), probm2(fr, rr), seqm4(stop, ifNestToLeft, ifOnFood, stop)), probm3(probm4(fr, ifNestToLeft, fl, r), selm2(ifFoodToRight, f), seqm4(ifFoodToRight, ifInNest, ifNestToLeft, rr)), probm2(seqm3(ifNestToRight, ifInNest, fl), probm4(rl, fr, ifInNest, f)))",
			"fitness" : [0.4938748111111112, 16.6, 0.0, 0.9035388999999998]
		})

		self.tests.append({
			"bt" : "seqm2(selm3(f, ifNestToRight, stop), seqm3(ifRobotToLeft, ifFoodToRight, ifOnFood))",
			"trimmed" : "f",
			"fitness" : [0.5018956222222222, 40.0, 0.0, 0.6017875333333333]
		})

		self.tests.append({
			"bt" : "seqm3(rl, f, ifNestToRight)",
			"trimmed" : "seqm2(rl, f)",
			"fitness" : [0.4962454444444443, 26.6, -13.4, 0.32999999999999974]
		})

		self.tests.append({
			"bt" : "selm3(ifFoodToLeft, fl, fl)",
			"trimmed" : "selm2(ifFoodToLeft, fl)",
			"fitness" : [0.49618741111111114, 0.0, 17.322222222222223, 0.7830550444444443]
		})

		self.tests.append({
			"bt" : "seqm3(probm4(selm4(ifOnFood, ifInNest, ifFoodToRight, ifFoodToRight), probm2(ifInNest, ifFoodToLeft), probm2(fl, f), selm2(ifFoodToRight, ifInNest)), seqm2(seqm2(ifFoodToLeft, ifFoodToRight), selm3(ifFoodToLeft, stop, ifOnFood)), probm3(selm2(ifInNest, ifNestToLeft), selm4(ifFoodToRight, rr, fr, fl), selm3(ifInNest, fl, ifFoodToRight)))",
			"trimmed" : "seqm3(probm4(selm4(ifOnFood, ifInNest, ifFoodToRight, ifFoodToRight), probm2(ifInNest, ifFoodToLeft), probm2(fl, f), selm2(ifFoodToRight, ifInNest)), seqm2(seqm2(ifFoodToLeft, ifFoodToRight), selm2(ifFoodToLeft, stop)), probm3(ifInNest, selm2(ifFoodToRight, rr), selm2(ifInNest, fl)))",
			"fitness" : [0.5032461444444444, 7.655555555555554, 7.9, 0.8967146222222222]
		})

		self.tests.append({
			"bt" : "selm2(probm4(probm3(ifInNest, ifFoodToRight, rr), probm2(f, rr), seqm3(ifRobotToLeft, ifInNest, fl), probm4(ifRobotToRight, f, ifRobotToLeft, stop)), selm4(seqm3(rr, ifNestToRight, fl), seqm3(stop, ifNestToLeft, ifOnFood), probm4(ifInNest, ifNestToLeft, ifNestToRight, ifNestToRight), selm4(ifFoodToLeft, stop, ifOnFood, ifFoodToLeft)))",
			"trimmed" : "selm2(probm4(probm3(ifInNest, ifFoodToRight, rr), probm2(f, rr), seqm3(ifRobotToLeft, ifInNest, fl), probm4(ifRobotToRight, f, ifRobotToLeft, stop)), selm4(seqm3(rr, ifNestToRight, fl), seqm3(stop, ifNestToLeft, ifOnFood), probm4(ifInNest, ifNestToLeft, ifNestToRight, ifNestToRight), selm2(ifFoodToLeft, stop)))",
			"fitness" : [0.502556811111111, 6.611111111111112, 18.27777777777778, 0.5804157]
		})

		self.tests.append({
			"bt" : "probm4(seqm3(seqm4(ifNestToLeft, ifRobotToLeft, fr, ifInNest), probm3(ifInNest, fl, stop), probm3(stop, stop, rl)), probm4(selm2(f, ifFoodToLeft), seqm4(fl, ifNestToLeft, ifNestToLeft, ifInNest), probm2(fl, rr), selm3(ifRobotToRight, rl, r)), probm3(probm3(rr, ifFoodToLeft, ifNestToLeft), probm2(rl, r), selm4(rl, ifRobotToRight, ifRobotToLeft, ifInNest)), probm2(seqm3(ifFoodToLeft, fl, fl), selm2(stop, ifOnFood)))",
			"trimmed" : "probm4(seqm3(seqm4(ifNestToLeft, ifRobotToLeft, fr, ifInNest), probm3(ifInNest, fl, stop), probm3(stop, stop, rl)), probm4(f, fl, probm2(fl, rr), selm2(ifRobotToRight, rl)), probm3(probm3(rr, ifInNest, ifInNest), probm2(rl, r), rl), probm2(seqm3(ifFoodToLeft, fl, fl), stop))",
			"fitness" : [0.49576707777777773, 1.7666666666666668, -0.7444444444444445, 0.5256523222222222]
		})

		self.tests.append({
			"bt" : "selm4(probm4(rr, ifInNest, ifRobotToRight, ifOnFood), selm4(f, fl, ifRobotToLeft, ifFoodToLeft), probm3(ifRobotToLeft, ifRobotToLeft, f), seqm4(ifOnFood, ifInNest, ifRobotToRight, r))",
			"trimmed" : "selm2(probm4(rr, ifInNest, ifRobotToRight, ifOnFood), f)",
			"fitness" : [0.48965547777777785, 22.133333333333333, 11.822222222222223, 0.4995699000000001]
		})

		self.tests.append({
			"bt" : "selm2(r, ifOnFood)",
			"trimmed" : "r",
			"fitness" : [0.4926536555555555, -40.0, 0.0, 0.0]
		})

		self.tests.append({
			"bt" : "probm2(stop, stop)",
			"trimmed" : "probm2(stop, stop)",
			"fitness" : [0.500907288888889, 0.0, 0.0, 0.0]
		})

		self.tests.append({
			"bt" : "probm4(seqm3(probm3(r, ifRobotToRight, rl), selm3(rr, r, f), selm3(ifInNest, stop, ifFoodToRight)), probm2(seqm2(r, ifOnFood), probm3(ifRobotToLeft, rr, fr)), probm3(seqm3(fl, fl, rr), selm2(f, ifRobotToLeft), selm4(ifRobotToLeft, ifFoodToRight, ifFoodToLeft, r)), probm3(seqm4(r, fr, ifNestToRight, fl), probm4(ifNestToLeft, ifOnFood, ifFoodToRight, fl), seqm2(rr, stop)))",
			"trimmed" : "probm4(seqm3(probm3(r, ifRobotToRight, rl), rr, selm2(ifInNest, stop)), probm2(r, probm3(ifInNest, rr, fr)), probm3(seqm3(fl, fl, rr), f, selm4(ifRobotToLeft, ifFoodToRight, ifFoodToLeft, r)), probm3(seqm4(r, fr, ifNestToRight, fl), probm4(ifInNest, ifInNest, ifInNest, fl), seqm2(rr, stop)))",
			"fitness" : [0.49216060000000006, -5.555555555555555, 8.933333333333334, 0.3284888666666667]
		})

		self.tests.append({
			"bt" : "probm4(seqm4(rr, ifFoodToRight, r, fr), seqm2(f, ifOnFood), seqm4(rr, ifNestToRight, ifRobotToLeft, fl), probm2(ifRobotToLeft, fr))",
			"trimmed" : "probm4(seqm4(rr, ifFoodToRight, r, fr), f, seqm4(rr, ifNestToRight, ifRobotToLeft, fl), probm2(ifInNest, fr))",
			"fitness" : [0.49888018888888885, 7.544444444444444, 12.511111111111111, 0.48246385555555554]
		})

		self.tests.append({
			"bt" : "seqm2(selm3(ifFoodToRight, ifFoodToRight, fl), selm3(r, fl, ifRobotToRight))",
			"trimmed" : "seqm2(selm3(ifFoodToRight, ifFoodToRight, fl), r)",
			"fitness" : [0.49848188888888895, -30.53333333333333, 9.466666666666665, 0.5003415333333333]
		})

		self.tests.append({
			"bt" : "probm3(seqm4(selm3(selm4(ifRobotToRight, ifRobotToLeft, stop, ifInNest), seqm4(rr, ifFoodToLeft, rl, ifNestToLeft), probm2(ifOnFood, ifRobotToLeft)), selm4(seqm2(r, ifOnFood), seqm2(ifNestToLeft, ifRobotToRight), selm4(fl, stop, r, rl), seqm3(rr, ifNestToLeft, ifNestToLeft)), probm4(seqm2(ifFoodToLeft, ifOnFood), seqm4(ifRobotToLeft, r, fl, fr), selm3(stop, fr, ifRobotToLeft), selm2(stop, r)), selm3(selm4(rr, ifNestToLeft, fl, ifNestToLeft), probm3(fl, ifNestToRight, ifInNest), probm4(rr, stop, ifNestToLeft, ifNestToLeft))), selm4(selm2(probm4(ifNestToRight, ifRobotToLeft, ifNestToRight, r), selm2(rr, stop)), selm3(probm4(fr, f, fl, stop), seqm2(ifNestToRight, ifRobotToLeft), seqm4(ifInNest, f, fl, ifOnFood)), selm4(seqm2(stop, ifInNest), seqm4(ifOnFood, stop, ifNestToRight, r), selm2(ifOnFood, rl), seqm3(ifRobotToRight, ifFoodToLeft, fr)), selm4(probm2(f, ifNestToLeft), probm4(fr, rl, ifFoodToRight, r), probm4(fl, ifRobotToRight, stop, r), selm4(stop, ifNestToLeft, fr, ifRobotToLeft))), selm4(selm3(seqm4(rl, ifFoodToLeft, ifFoodToRight, rr), probm2(ifFoodToLeft, f), seqm3(rl, ifNestToLeft, r)), seqm2(probm3(ifFoodToRight, rr, ifNestToLeft), seqm3(ifFoodToLeft, ifFoodToLeft, ifFoodToRight)), selm4(seqm3(f, ifRobotToRight, ifOnFood), probm2(ifNestToLeft, ifFoodToLeft), selm3(ifNestToRight, ifInNest, r), probm4(f, ifNestToRight, stop, ifRobotToLeft)), selm3(probm2(stop, ifRobotToRight), selm4(fr, ifNestToRight, ifInNest, fl), seqm2(ifNestToLeft, r))))",
			"trimmed" : "probm3(seqm4(selm3(ifRobotToRight, ifRobotToLeft, stop), selm3(seqm2(r, ifOnFood), seqm2(ifNestToLeft, ifRobotToRight), fl), probm4(seqm2(ifFoodToLeft, ifOnFood), seqm4(ifRobotToLeft, r, fl, fr), stop, stop), rr), selm2(probm4(ifNestToRight, ifRobotToLeft, ifNestToRight, r), rr), selm3(selm3(seqm4(rl, ifFoodToLeft, ifFoodToRight, rr), probm2(ifFoodToLeft, f), seqm3(rl, ifNestToLeft, r)), seqm2(probm3(ifFoodToRight, rr, ifNestToLeft), seqm3(ifFoodToLeft, ifFoodToLeft, ifFoodToRight)), selm3(seqm3(f, ifRobotToRight, ifOnFood), probm2(ifNestToLeft, ifFoodToLeft), selm3(ifNestToRight, ifInNest, r))))",
			"fitness" : [0.5012275777777777, -2.055555555555556, 6.988888888888889, 0.5617828333333333]
		})

		self.tests.append({
			"bt" : "selm2(fr, ifRobotToLeft)",
			"trimmed" : "fr",
			"fitness" : [0.4975353333333333, 0.0, -40.0, 0.0]
		})

		self.tests.append({
			"bt" : "selm4(probm2(probm2(probm4(stop, ifInNest, rr, ifNestToRight), selm4(ifNestToLeft, ifFoodToLeft, ifNestToRight, fl)), selm4(probm3(fr, rl, ifNestToLeft), selm3(ifFoodToLeft, fr, ifNestToLeft), probm3(ifRobotToRight, stop, ifFoodToLeft), seqm2(stop, rl))), seqm3(selm3(seqm4(ifOnFood, ifFoodToLeft, r, r), seqm2(f, ifFoodToRight), seqm4(ifFoodToLeft, f, ifOnFood, ifOnFood)), probm3(probm2(r, ifNestToLeft), seqm2(ifInNest, rl), selm4(fl, f, ifNestToRight, fr)), selm3(probm4(stop, ifRobotToLeft, ifInNest, rr), selm3(rl, ifRobotToLeft, fl), probm4(ifNestToLeft, rl, fr, f))), seqm3(selm2(seqm2(r, ifNestToRight), selm4(fl, ifRobotToRight, stop, f)), selm3(seqm3(ifOnFood, fl, ifNestToLeft), probm4(stop, ifNestToRight, rl, ifRobotToLeft), seqm3(r, fl, ifRobotToLeft)), selm4(seqm3(ifRobotToRight, ifInNest, fl), probm2(ifNestToLeft, stop), selm2(ifRobotToRight, r), selm2(ifRobotToRight, ifNestToRight))), selm4(probm4(probm3(rr, ifNestToRight, ifInNest), seqm2(fl, fr), selm2(rl, ifRobotToLeft), seqm4(ifNestToRight, ifNestToLeft, f, stop)), selm3(probm4(ifRobotToLeft, stop, ifFoodToRight, ifNestToRight), selm3(ifFoodToRight, fl, rr), seqm2(ifFoodToRight, rr)), selm2(seqm4(ifOnFood, rl, f, ifNestToLeft), probm2(rl, rr)), seqm3(seqm4(ifOnFood, f, stop, ifInNest), selm4(ifInNest, ifRobotToLeft, r, stop), seqm3(ifRobotToLeft, ifFoodToLeft, rr))))",
			"trimmed" : "selm4(probm2(probm2(probm4(stop, ifInNest, rr, ifNestToRight), selm4(ifNestToLeft, ifFoodToLeft, ifNestToRight, fl)), selm2(probm3(fr, rl, ifNestToLeft), selm2(ifFoodToLeft, fr))), seqm3(selm3(seqm4(ifOnFood, ifFoodToLeft, r, r), seqm2(f, ifFoodToRight), seqm4(ifFoodToLeft, f, ifOnFood, ifOnFood)), probm3(probm2(r, ifNestToLeft), seqm2(ifInNest, rl), fl), selm2(probm4(stop, ifRobotToLeft, ifInNest, rr), rl)), seqm3(selm2(seqm2(r, ifNestToRight), fl), selm3(seqm3(ifOnFood, fl, ifNestToLeft), probm4(stop, ifNestToRight, rl, ifRobotToLeft), seqm3(r, fl, ifRobotToLeft)), selm3(seqm3(ifRobotToRight, ifInNest, fl), probm2(ifNestToLeft, stop), selm2(ifRobotToRight, r))), selm2(probm4(probm3(rr, ifNestToRight, ifInNest), seqm2(fl, fr), rl, seqm4(ifNestToRight, ifNestToLeft, f, stop)), selm2(probm4(ifRobotToLeft, stop, ifFoodToRight, ifNestToRight), selm2(ifFoodToRight, fl))))",
			"fitness" : [0.501142411111111, -0.3555555555555555, -7.622222222222223, 0.5990815333333332]
		})

		self.tests.append({
			"bt" : "seqm4(selm2(probm4(rr, rl, ifRobotToRight, ifOnFood), selm4(ifFoodToLeft, f, fr, ifFoodToRight)), probm2(probm4(rl, ifFoodToLeft, ifInNest, rl), probm3(ifRobotToLeft, ifRobotToLeft, stop)), selm2(seqm2(ifOnFood, f), probm4(ifOnFood, ifInNest, rr, ifFoodToRight)), probm3(probm3(r, stop, ifOnFood), probm3(f, ifInNest, ifRobotToRight), seqm2(rl, stop)))",
			"trimmed" : "seqm4(selm2(probm4(rr, rl, ifRobotToRight, ifOnFood), selm2(ifFoodToLeft, f)), probm2(probm4(rl, ifFoodToLeft, ifInNest, rl), probm3(ifRobotToLeft, ifRobotToLeft, stop)), selm2(seqm2(ifOnFood, f), probm4(ifOnFood, ifInNest, rr, ifFoodToRight)), probm3(probm3(r, stop, ifInNest), probm3(f, ifInNest, ifInNest), seqm2(rl, stop)))",
			"fitness" : [0.500964, 5.7, -5.366666666666666, 0.5891685444444444]
		})

		self.tests.append({
			"bt" : "probm3(probm4(probm4(selm2(rr, ifNestToLeft), probm3(ifFoodToRight, ifNestToRight, ifNestToLeft), probm2(f, ifInNest), selm4(ifFoodToRight, rl, stop, ifRobotToLeft)), probm3(probm3(rl, ifFoodToLeft, f), probm3(ifOnFood, fr, ifInNest), selm3(rl, r, ifFoodToLeft)), selm4(probm4(ifFoodToLeft, f, r, f), seqm2(ifInNest, fr), probm2(rr, rr), seqm3(ifRobotToLeft, ifInNest, ifNestToLeft)), seqm3(probm4(fr, fl, ifFoodToLeft, ifNestToRight), selm3(ifInNest, ifFoodToLeft, fr), seqm4(ifOnFood, fr, stop, ifFoodToLeft))), selm3(probm4(seqm2(stop, ifFoodToRight), probm3(rr, ifFoodToLeft, rl), probm4(ifNestToLeft, ifOnFood, ifRobotToRight, rl), probm3(r, fr, ifOnFood)), selm2(probm3(ifRobotToLeft, fr, ifNestToLeft), probm4(ifOnFood, fr, f, fr)), probm4(selm4(ifNestToLeft, rr, ifNestToRight, ifNestToRight), seqm2(f, ifNestToLeft), probm4(ifInNest, fr, ifFoodToLeft, ifRobotToRight), selm3(r, ifOnFood, ifFoodToRight))), seqm4(probm3(probm3(ifNestToRight, rr, rr), selm2(ifOnFood, ifRobotToRight), selm2(ifNestToLeft, ifFoodToLeft)), probm4(selm2(ifOnFood, ifNestToRight), seqm2(stop, rl), probm2(ifOnFood, stop), selm3(ifNestToRight, ifRobotToRight, ifFoodToLeft)), selm3(seqm4(stop, ifFoodToRight, ifFoodToRight, ifRobotToLeft), seqm2(ifNestToRight, f), probm2(ifNestToRight, fl)), seqm3(selm4(f, ifRobotToRight, ifFoodToRight, ifOnFood), seqm4(ifOnFood, rr, ifInNest, fl), selm4(rl, fr, f, ifFoodToRight))))",
			"trimmed" : "probm3(probm4(probm4(rr, probm3(ifInNest, ifInNest, ifInNest), probm2(f, ifInNest), selm2(ifFoodToRight, rl)), probm3(probm3(rl, ifInNest, f), probm3(ifInNest, fr, ifInNest), rl), selm3(probm4(ifFoodToLeft, f, r, f), seqm2(ifInNest, fr), probm2(rr, rr)), seqm3(probm4(fr, fl, ifFoodToLeft, ifNestToRight), selm3(ifInNest, ifFoodToLeft, fr), seqm3(ifOnFood, fr, stop))), selm3(probm4(seqm2(stop, ifFoodToRight), probm3(rr, ifFoodToLeft, rl), probm4(ifNestToLeft, ifOnFood, ifRobotToRight, rl), probm3(r, fr, ifOnFood)), selm2(probm3(ifRobotToLeft, fr, ifNestToLeft), probm4(ifOnFood, fr, f, fr)), probm4(selm2(ifNestToLeft, rr), f, probm4(ifInNest, fr, ifInNest, ifInNest), r)), seqm4(probm3(probm3(ifNestToRight, rr, rr), selm2(ifOnFood, ifRobotToRight), selm2(ifNestToLeft, ifFoodToLeft)), probm4(selm2(ifOnFood, ifNestToRight), seqm2(stop, rl), probm2(ifOnFood, stop), selm3(ifNestToRight, ifRobotToRight, ifFoodToLeft)), selm3(seqm4(stop, ifFoodToRight, ifFoodToRight, ifRobotToLeft), seqm2(ifNestToRight, f), probm2(ifNestToRight, fl)), seqm3(f, seqm4(ifOnFood, rr, ifInNest, fl), rl)))",
			"fitness" : [0.503947322222222, 5.311111111111112, -2.888888888888889, 0.6155488222222223]
		})

		self.tests.append({
			"bt" : "seqm2(selm4(selm3(fr, stop, r), seqm4(rl, rl, f, f), probm4(stop, rl, ifRobotToRight, f), seqm4(f, ifRobotToRight, ifNestToLeft, rl)), seqm3(probm4(ifFoodToLeft, f, r, r), selm4(f, stop, ifFoodToLeft, ifFoodToLeft), seqm3(ifOnFood, f, r)))",
			"trimmed" : "seqm2(fr, seqm3(probm4(ifFoodToLeft, f, r, r), f, seqm3(ifOnFood, f, r)))",
			"fitness" : [0.5000831444444446, 11.455555555555556, -12.788888888888888, 0.2741719666666667]
		})

		self.tests.append({
			"bt" : "seqm4(ifRobotToRight, rr, ifFoodToRight, ifNestToRight)",
			"trimmed" : "seqm2(ifRobotToRight, rr)",
			"fitness" : [0.5140899666666667, 0.0, 8.044444444444444, 0.9218408222222223]
		})

		self.tests.append({
			"bt" : "selm3(seqm4(probm3(probm2(ifRobotToLeft, rl), selm4(ifOnFood, fl, ifInNest, ifFoodToRight), selm2(ifFoodToLeft, r)), probm4(selm2(ifFoodToLeft, ifRobotToLeft), selm2(ifFoodToRight, ifFoodToRight), seqm3(f, rr, r), selm2(ifNestToRight, fr)), seqm2(probm3(ifInNest, fl, rl), seqm2(ifNestToLeft, r)), seqm3(selm4(f, ifFoodToRight, ifNestToRight, ifOnFood), probm2(r, r), probm4(fr, f, fl, ifFoodToRight))), seqm3(seqm3(selm4(ifRobotToLeft, rr, stop, ifRobotToRight), seqm2(ifNestToRight, ifRobotToLeft), selm3(f, ifOnFood, f)), selm3(selm3(ifNestToRight, fr, ifRobotToLeft), selm4(ifNestToRight, f, ifNestToLeft, fr), seqm3(fr, fr, rr)), probm3(selm2(fr, fr), seqm3(ifRobotToRight, ifRobotToRight, ifNestToLeft), probm2(ifOnFood, ifFoodToRight))), selm4(probm4(probm3(rl, r, stop), seqm4(ifFoodToRight, f, ifInNest, f), seqm3(r, stop, fl), seqm3(ifRobotToLeft, ifOnFood, rl)), seqm3(seqm2(fl, ifRobotToRight), seqm2(stop, ifNestToRight), seqm3(ifRobotToLeft, ifFoodToRight, r)), selm3(selm2(ifInNest, f), probm4(stop, stop, ifNestToLeft, ifNestToLeft), seqm3(rr, ifOnFood, rr)), seqm2(selm3(ifOnFood, fl, ifOnFood), selm4(fr, fr, rl, ifOnFood))))",
			"trimmed" : "selm3(seqm4(probm3(probm2(ifRobotToLeft, rl), selm2(ifOnFood, fl), selm2(ifFoodToLeft, r)), probm4(selm2(ifFoodToLeft, ifRobotToLeft), selm2(ifFoodToRight, ifFoodToRight), seqm3(f, rr, r), selm2(ifNestToRight, fr)), seqm2(probm3(ifInNest, fl, rl), seqm2(ifNestToLeft, r)), seqm3(f, probm2(r, r), probm4(fr, f, fl, ifFoodToRight))), seqm3(seqm3(selm2(ifRobotToLeft, rr), seqm2(ifNestToRight, ifRobotToLeft), f), selm2(ifNestToRight, fr), probm3(fr, seqm3(ifRobotToRight, ifRobotToRight, ifNestToLeft), probm2(ifOnFood, ifFoodToRight))), selm3(probm4(probm3(rl, r, stop), seqm4(ifFoodToRight, f, ifInNest, f), seqm3(r, stop, fl), seqm3(ifRobotToLeft, ifOnFood, rl)), seqm3(seqm2(fl, ifRobotToRight), seqm2(stop, ifNestToRight), seqm3(ifRobotToLeft, ifFoodToRight, r)), selm2(ifInNest, f)))",
			"fitness" : [0.5030740333333334, -0.4444444444444445, 7.7333333333333325, 0.5587245444444443]
		})

		self.tests.append({
			"bt" : "selm2(ifOnFood, ifOnFood)",
			"trimmed" : "ifOnFood",
			"fitness" : [0.499769988888889, 0.0, 0.0, 1.0]
		})

		self.tests.append({
			"bt" : "probm3(selm2(selm2(stop, ifNestToRight), seqm4(ifNestToRight, ifFoodToLeft, ifFoodToLeft, f)), probm4(probm4(ifFoodToLeft, rr, ifNestToRight, ifNestToLeft), selm3(ifRobotToLeft, rr, ifOnFood), selm3(stop, fr, ifRobotToRight), selm2(ifFoodToRight, ifFoodToRight)), selm4(seqm2(ifOnFood, f), probm2(stop, fl), seqm2(r, ifNestToLeft), selm3(ifNestToRight, ifNestToLeft, ifFoodToLeft)))",
			"trimmed" : "probm3(stop, probm4(probm4(ifInNest, rr, ifInNest, ifInNest), selm2(ifRobotToLeft, rr), stop, ifInNest), selm2(seqm2(ifOnFood, f), probm2(stop, fl)))",
			"fitness" : [0.49811613333333343, 2.5444444444444443, 8.422222222222222, 0.4380880666666666]
		})

		self.tests.append({
			"bt" : "selm2(r, ifFoodToRight)",
			"trimmed" : "r",
			"fitness" : [0.4926536555555555, -40.0, 0.0, 0.0]
		})

		self.tests.append({
			"bt" : "seqm2(seqm4(ifNestToLeft, ifNestToRight, ifOnFood, fr), seqm3(ifFoodToRight, ifOnFood, f))",
			"trimmed" : "seqm2(seqm4(ifNestToLeft, ifNestToRight, ifOnFood, fr), seqm3(ifFoodToRight, ifOnFood, f))",
			"fitness" : [0.499769988888889, 0.0, 0.0, 1.0]
		})

		self.tests.append({
			"bt" : "seqm4(ifNestToRight, r, ifNestToRight, fl)",
			"trimmed" : "seqm4(ifNestToRight, r, ifNestToRight, fl)",
			"fitness" : [0.5023293333333334, -2.7222222222222223, 3.8888888888888884, 0.9067629555555555]
		})

		self.tests.append({
			"bt" : "seqm2(selm2(ifNestToRight, ifOnFood), seqm2(ifInNest, r))",
			"trimmed" : "seqm2(selm2(ifNestToRight, ifOnFood), seqm2(ifInNest, r))",
			"fitness" : [0.499769988888889, 0.0, 0.0, 1.0]
		})

		self.tests.append({
			"bt" : "seqm3(seqm3(stop, ifRobotToLeft, rl), selm3(fr, ifOnFood, fr), seqm3(r, ifNestToRight, ifFoodToRight))",
			"trimmed" : "seqm3(seqm3(stop, ifRobotToLeft, rl), fr, r)",
			"fitness" : [0.5132440333333332, -6.888888888888888, -6.9, 0.4343606555555555]
		})

		self.tests.append({
			"bt" : "probm3(seqm4(selm4(rl, fl, ifRobotToLeft, ifInNest), selm4(rr, ifNestToRight, rl, rl), seqm4(rr, ifFoodToRight, rr, ifNestToLeft), seqm2(ifNestToRight, ifInNest)), selm4(seqm3(stop, ifFoodToLeft, rr), probm3(r, rl, ifFoodToRight), selm4(ifRobotToRight, ifFoodToRight, ifFoodToRight, ifFoodToRight), selm4(ifRobotToRight, stop, ifOnFood, ifFoodToRight)), probm2(seqm3(ifNestToLeft, ifFoodToLeft, f), probm2(rl, stop)))",
			"trimmed" : "probm3(seqm3(rl, rr, seqm3(rr, ifFoodToRight, rr)), selm4(seqm3(stop, ifFoodToLeft, rr), probm3(r, rl, ifFoodToRight), selm4(ifRobotToRight, ifFoodToRight, ifFoodToRight, ifFoodToRight), selm2(ifRobotToRight, stop)), probm2(seqm3(ifNestToLeft, ifFoodToLeft, f), probm2(rl, stop)))",
			"fitness" : [0.4952239777777777, -1.7333333333333336, 8.977777777777778, 0.392768711111111]
		})

		self.tests.append({
			"bt" : "probm2(seqm4(fl, fl, ifNestToLeft, ifNestToLeft), probm2(ifInNest, rl))",
			"trimmed" : "probm2(seqm2(fl, fl), probm2(ifInNest, rl))",
			"fitness" : [0.4999561666666665, 0.0, 17.555555555555554, 0.4240691444444444]
		})

		self.tests.append({
			"bt" : "selm3(probm3(probm3(ifNestToLeft, ifFoodToLeft, rl), seqm4(ifFoodToLeft, ifInNest, ifRobotToLeft, ifNestToLeft), probm4(ifFoodToRight, rr, ifRobotToRight, rr)), seqm2(probm2(fl, ifFoodToRight), seqm2(fl, ifNestToLeft)), seqm4(probm4(ifOnFood, ifOnFood, fr, ifNestToRight), probm3(fr, ifFoodToRight, stop), probm3(rl, rl, r), probm4(fl, r, fl, ifFoodToRight)))",
			"trimmed" : "selm3(probm3(probm3(ifNestToLeft, ifFoodToLeft, rl), seqm4(ifFoodToLeft, ifInNest, ifRobotToLeft, ifNestToLeft), probm4(ifFoodToRight, rr, ifRobotToRight, rr)), seqm2(probm2(fl, ifFoodToRight), seqm2(fl, ifNestToLeft)), seqm4(probm4(ifOnFood, ifOnFood, fr, ifNestToRight), probm3(fr, ifFoodToRight, stop), probm3(rl, rl, r), probm4(fl, r, fl, ifInNest)))",
			"fitness" : [0.49575576666666654, -2.3333333333333335, 13.444444444444446, 0.5698342000000001]
		})

		self.tests.append({
			"bt" : "seqm2(probm2(selm4(ifOnFood, ifFoodToLeft, rr, f), selm3(ifOnFood, ifNestToRight, rl)), seqm3(probm3(f, ifRobotToLeft, ifNestToRight), probm3(r, ifOnFood, ifNestToRight), seqm3(fr, f, ifOnFood)))",
			"trimmed" : "seqm2(probm2(selm3(ifOnFood, ifFoodToLeft, rr), selm3(ifOnFood, ifNestToRight, rl)), seqm3(probm3(f, ifRobotToLeft, ifNestToRight), probm3(r, ifOnFood, ifNestToRight), seqm2(fr, f)))",
			"fitness" : [0.4870002555555556, 15.377777777777776, -6.277777777777777, 0.6362289666666665]
		})

		self.tests.append({
			"bt" : "seqm2(probm2(ifNestToRight, ifFoodToRight), probm4(rr, ifFoodToLeft, ifNestToLeft, ifNestToLeft))",
			"trimmed" : "seqm2(probm2(ifNestToRight, ifFoodToRight), probm4(rr, ifInNest, ifInNest, ifInNest))",
			"fitness" : [0.5056744777777779, 0.0, 4.4222222222222225, 0.9566915333333332]
		})

		self.tests.append({
			"bt" : "seqm2(seqm3(f, stop, stop), probm4(f, rr, rl, stop))",
			"trimmed" : "seqm2(seqm3(f, stop, stop), probm4(f, rr, rl, stop))",
			"fitness" : [0.5048984333333332, 12.133333333333335, 0.22222222222222224, 0.0]
		})

		self.tests.append({
			"bt" : "seqm4(probm4(seqm4(probm2(stop, rl), probm3(ifNestToRight, ifRobotToLeft, r), seqm2(ifFoodToLeft, ifNestToRight), selm3(r, ifNestToLeft, ifNestToLeft)), selm3(selm2(ifNestToLeft, ifRobotToRight), probm3(ifNestToLeft, ifOnFood, r), probm3(ifInNest, f, ifNestToRight)), selm3(seqm2(ifRobotToRight, fl), selm3(f, ifFoodToRight, ifNestToLeft), selm2(ifNestToRight, ifFoodToRight)), seqm4(probm4(ifOnFood, rr, ifOnFood, rl), probm3(ifRobotToRight, stop, ifFoodToRight), probm2(ifRobotToRight, ifInNest), probm4(ifFoodToRight, fl, fr, rr))), seqm3(probm3(seqm2(ifRobotToRight, ifFoodToRight), selm4(rl, ifInNest, ifFoodToLeft, ifInNest), probm3(ifOnFood, ifNestToLeft, rr)), probm3(selm3(ifFoodToRight, ifFoodToLeft, rl), seqm3(rl, ifFoodToLeft, ifRobotToRight), selm4(ifOnFood, ifFoodToLeft, ifNestToLeft, fl)), seqm3(selm2(ifInNest, ifRobotToLeft), selm4(rr, f, ifNestToRight, ifFoodToLeft), probm3(r, fl, fr))), seqm4(seqm3(seqm3(fl, ifNestToLeft, ifFoodToRight), probm2(ifFoodToRight, ifInNest), selm4(ifFoodToRight, stop, fr, f)), selm3(selm4(ifRobotToRight, ifNestToLeft, rl, ifRobotToRight), selm3(ifOnFood, fr, fl), selm3(ifInNest, fr, ifInNest)), selm2(probm4(stop, ifRobotToRight, f, ifRobotToRight), probm3(rr, stop, r)), probm2(seqm4(ifRobotToLeft, ifOnFood, ifRobotToLeft, stop), probm4(rl, fr, ifRobotToRight, ifNestToLeft))), probm3(selm2(probm3(rl, ifFoodToRight, ifRobotToRight), selm3(fr, fl, fl)), probm4(seqm3(rl, ifInNest, ifRobotToRight), probm3(ifNestToRight, ifNestToLeft, ifNestToLeft), seqm4(rr, rl, ifOnFood, ifFoodToRight), probm3(r, ifNestToLeft, f)), seqm4(seqm4(ifOnFood, f, ifNestToRight, rr), selm2(ifRobotToRight, fl), probm2(stop, ifNestToRight), selm4(ifRobotToRight, ifInNest, ifFoodToRight, ifFoodToLeft))))",
			"trimmed" : "seqm4(probm4(seqm4(probm2(stop, rl), probm3(ifNestToRight, ifRobotToLeft, r), seqm2(ifFoodToLeft, ifNestToRight), r), selm3(selm2(ifNestToLeft, ifRobotToRight), probm3(ifNestToLeft, ifOnFood, r), probm3(ifInNest, f, ifNestToRight)), selm2(seqm2(ifRobotToRight, fl), f), seqm4(probm4(ifOnFood, rr, ifOnFood, rl), probm3(ifRobotToRight, stop, ifFoodToRight), probm2(ifRobotToRight, ifInNest), probm4(ifFoodToRight, fl, fr, rr))), seqm3(probm3(seqm2(ifRobotToRight, ifFoodToRight), rl, probm3(ifOnFood, ifNestToLeft, rr)), probm3(selm3(ifFoodToRight, ifFoodToLeft, rl), seqm3(rl, ifFoodToLeft, ifRobotToRight), selm4(ifOnFood, ifFoodToLeft, ifNestToLeft, fl)), seqm3(selm2(ifInNest, ifRobotToLeft), rr, probm3(r, fl, fr))), seqm4(seqm3(seqm3(fl, ifNestToLeft, ifFoodToRight), probm2(ifFoodToRight, ifInNest), selm2(ifFoodToRight, stop)), selm3(ifRobotToRight, ifNestToLeft, rl), selm2(probm4(stop, ifRobotToRight, f, ifRobotToRight), probm3(rr, stop, r)), probm2(seqm4(ifRobotToLeft, ifOnFood, ifRobotToLeft, stop), probm4(rl, fr, ifRobotToRight, ifNestToLeft))), probm3(selm2(probm3(rl, ifFoodToRight, ifRobotToRight), fr), probm4(rl, probm3(ifInNest, ifInNest, ifInNest), seqm2(rr, rl), probm3(r, ifInNest, f)), seqm3(seqm4(ifOnFood, f, ifNestToRight, rr), selm2(ifRobotToRight, fl), probm2(stop, ifInNest))))",
			"fitness" : [0.5056337888888889, -0.7333333333333334, -0.14444444444444446, 0.6359443333333333]
		})

		self.tests.append({
			"bt" : "probm2(probm3(ifNestToLeft, ifNestToLeft, r), probm4(ifFoodToLeft, ifNestToRight, stop, fr))",
			"trimmed" : "probm2(probm3(ifInNest, ifInNest, r), probm4(ifInNest, ifInNest, stop, fr))",
			"fitness" : [0.49691431111111106, -9.233333333333334, -6.988888888888889, 0.5871197444444445]
		})

		self.tests.append({
			"bt" : "seqm4(seqm4(probm4(probm4(ifFoodToLeft, ifNestToLeft, stop, f), probm4(ifFoodToLeft, f, rl, r), selm3(ifFoodToLeft, fl, ifNestToLeft), selm2(rl, ifFoodToRight)), seqm2(selm4(ifRobotToLeft, fr, fl, stop), probm2(f, rr)), seqm4(seqm4(rl, stop, ifRobotToRight, ifFoodToRight), selm3(ifOnFood, ifInNest, fr), seqm2(ifInNest, stop), selm4(ifNestToLeft, ifRobotToRight, ifRobotToLeft, ifNestToLeft)), seqm4(seqm4(stop, rl, f, ifOnFood), selm3(f, ifRobotToRight, ifRobotToRight), selm4(ifFoodToLeft, rr, ifFoodToRight, r), probm2(rl, f))), seqm3(probm2(selm2(stop, ifOnFood), seqm2(rr, stop)), selm3(seqm4(rl, ifFoodToRight, ifRobotToRight, ifFoodToRight), seqm2(ifRobotToLeft, ifOnFood), seqm4(ifFoodToLeft, rr, ifRobotToLeft, ifRobotToRight)), probm3(probm4(ifInNest, ifNestToLeft, ifRobotToLeft, stop), selm4(rr, rr, f, fr), seqm4(stop, ifNestToLeft, ifFoodToRight, ifNestToLeft))), probm3(probm2(selm3(ifNestToRight, r, r), selm3(rr, ifRobotToRight, fl)), probm2(seqm2(fr, ifInNest), selm4(ifOnFood, ifRobotToRight, ifNestToLeft, ifFoodToRight)), probm4(probm3(ifFoodToLeft, ifRobotToLeft, ifOnFood), selm4(ifRobotToRight, fr, ifRobotToRight, ifFoodToLeft), seqm3(fl, f, ifRobotToLeft), probm3(rl, r, ifFoodToLeft))), probm2(seqm2(seqm4(ifNestToLeft, ifRobotToRight, ifNestToLeft, ifRobotToRight), seqm2(stop, ifInNest)), probm4(probm3(ifFoodToRight, rl, ifRobotToRight), probm4(rr, fl, ifFoodToRight, fr), probm3(stop, f, r), seqm4(ifFoodToRight, ifRobotToRight, fr, ifRobotToLeft))))",
			"trimmed" : "seqm4(seqm4(probm4(probm4(ifFoodToLeft, ifNestToLeft, stop, f), probm4(ifFoodToLeft, f, rl, r), selm2(ifFoodToLeft, fl), rl), seqm2(selm2(ifRobotToLeft, fr), probm2(f, rr)), seqm4(seqm4(rl, stop, ifRobotToRight, ifFoodToRight), selm3(ifOnFood, ifInNest, fr), seqm2(ifInNest, stop), selm4(ifNestToLeft, ifRobotToRight, ifRobotToLeft, ifNestToLeft)), seqm4(seqm4(stop, rl, f, ifOnFood), f, selm2(ifFoodToLeft, rr), probm2(rl, f))), seqm3(probm2(stop, seqm2(rr, stop)), selm3(seqm4(rl, ifFoodToRight, ifRobotToRight, ifFoodToRight), seqm2(ifRobotToLeft, ifOnFood), seqm4(ifFoodToLeft, rr, ifRobotToLeft, ifRobotToRight)), probm3(probm4(ifInNest, ifNestToLeft, ifRobotToLeft, stop), rr, seqm4(stop, ifNestToLeft, ifFoodToRight, ifNestToLeft))), probm3(probm2(selm2(ifNestToRight, r), rr), probm2(seqm2(fr, ifInNest), selm4(ifOnFood, ifRobotToRight, ifNestToLeft, ifFoodToRight)), probm4(probm3(ifFoodToLeft, ifRobotToLeft, ifOnFood), selm2(ifRobotToRight, fr), seqm3(fl, f, ifRobotToLeft), probm3(rl, r, ifFoodToLeft))), probm2(seqm2(seqm4(ifNestToLeft, ifRobotToRight, ifNestToLeft, ifRobotToRight), stop), probm4(probm3(ifInNest, rl, ifInNest), probm4(rr, fl, ifInNest, fr), probm3(stop, f, r), seqm3(ifFoodToRight, ifRobotToRight, fr))))",
			"fitness" : [0.5007200555555555, 4.2666666666666675, -8.3, 0.4233559222222222]
		})

		self.tests.append({
			"bt" : "probm2(selm3(stop, ifNestToRight, rl), selm3(ifOnFood, r, ifFoodToRight))",
			"trimmed" : "probm2(stop, selm2(ifOnFood, r))",
			"fitness" : [0.5179937444444445, -15.233333333333334, 0.0, 0.36266136666666665]
		})

		self.tests.append({
			"bt" : "probm3(ifRobotToLeft, ifOnFood, ifFoodToRight)",
			"trimmed" : "probm3(ifInNest, ifInNest, ifInNest)",
			"fitness" : [0.4999273888888888, 0.0, 0.0, 1.0]
		})

		self.tests.append({
			"bt" : "probm3(selm4(selm3(r, rr, rl), seqm3(rr, ifNestToRight, ifFoodToRight), selm4(fr, ifRobotToLeft, fl, r), probm2(ifOnFood, ifRobotToLeft)), probm3(selm3(ifNestToRight, ifInNest, rl), probm3(ifRobotToLeft, ifNestToRight, fr), seqm3(ifInNest, ifRobotToLeft, ifOnFood)), probm3(seqm2(r, ifRobotToLeft), probm2(ifInNest, stop), probm2(r, ifFoodToRight)))",
			"trimmed" : "probm3(r, probm3(selm3(ifNestToRight, ifInNest, rl), probm3(ifInNest, ifInNest, fr), ifInNest), probm3(r, probm2(ifInNest, stop), probm2(r, ifInNest)))",
			"fitness" : [0.5024005111111111, -24.7, -4.0777777777777775, 0.47864466666666666]
		})

		self.tests.append({
			"bt" : "selm4(selm4(ifFoodToRight, stop, rl, fl), probm4(ifFoodToLeft, ifNestToRight, ifNestToRight, ifNestToLeft), probm2(stop, ifNestToLeft), probm2(ifInNest, ifRobotToRight))",
			"trimmed" : "selm2(ifFoodToRight, stop)",
			"fitness" : [0.499769988888889, 0.0, 0.0, 0.625892211111111]
		})

		self.tests.append({
			"bt" : "selm4(probm2(rl, ifFoodToRight), probm3(f, ifNestToLeft, ifOnFood), probm3(r, ifNestToLeft, ifNestToRight), selm3(fr, ifRobotToRight, f))",
			"trimmed" : "selm4(probm2(rl, ifFoodToRight), probm3(f, ifNestToLeft, ifOnFood), probm3(r, ifNestToLeft, ifNestToRight), fr)",
			"fitness" : [0.49804723333333334, 3.9555555555555557, -26.577777777777776, 0.49493853333333326]
		})

		self.tests.append({
			"bt" : "selm2(seqm2(probm2(probm4(ifRobotToRight, f, ifNestToLeft, ifNestToRight), probm3(fr, ifNestToLeft, ifFoodToLeft)), probm3(seqm2(ifRobotToLeft, ifRobotToRight), selm2(stop, ifRobotToRight), selm3(fr, ifNestToRight, ifNestToRight))), selm2(seqm3(selm2(ifFoodToLeft, rl), probm4(ifNestToRight, ifInNest, r, ifInNest), seqm2(rl, ifRobotToLeft)), probm3(seqm2(ifRobotToRight, fr), probm4(fr, fl, ifRobotToRight, fl), seqm3(ifNestToLeft, ifRobotToLeft, ifFoodToRight))))",
			"trimmed" : "selm2(seqm2(probm2(probm4(ifRobotToRight, f, ifNestToLeft, ifNestToRight), probm3(fr, ifNestToLeft, ifFoodToLeft)), probm3(seqm2(ifRobotToLeft, ifRobotToRight), stop, fr)), selm2(seqm3(selm2(ifFoodToLeft, rl), probm4(ifNestToRight, ifInNest, r, ifInNest), seqm2(rl, ifRobotToLeft)), probm3(seqm2(ifRobotToRight, fr), probm4(fr, fl, ifInNest, fl), ifInNest)))",
			"fitness" : [0.5021536222222223, -0.5, -25.555555555555554, 0.6116803222222222]
		})

		self.tests.append({
			"bt" : "selm4(selm4(selm4(ifFoodToRight, stop, rr, ifNestToRight), selm3(ifInNest, ifNestToLeft, ifNestToRight), selm3(ifOnFood, ifNestToRight, fl), selm4(ifRobotToRight, r, f, ifRobotToRight)), seqm2(selm2(ifNestToLeft, rl), probm4(ifOnFood, ifOnFood, ifRobotToLeft, rl)), seqm3(selm4(ifNestToLeft, rl, ifNestToRight, fr), probm3(rr, ifRobotToLeft, r), probm3(f, fr, ifOnFood)), probm4(seqm4(ifNestToLeft, fr, rr, stop), probm3(f, ifOnFood, ifFoodToRight), seqm2(rl, rl), selm3(fl, fl, ifInNest)))",
			"trimmed" : "selm2(ifFoodToRight, stop)",
			"fitness" : [0.499769988888889, 0.0, 0.0, 0.625892211111111]
		})

		self.tests.append({
			"bt" : "probm2(selm2(probm3(probm2(ifNestToLeft, ifFoodToLeft), selm2(ifRobotToRight, fl), selm2(ifRobotToRight, ifInNest)), selm4(seqm2(ifRobotToRight, stop), probm4(ifInNest, ifNestToLeft, stop, rl), selm4(fl, f, stop, ifRobotToLeft), selm3(rr, stop, ifRobotToLeft))), seqm4(probm3(seqm4(ifInNest, ifInNest, ifNestToRight, f), probm3(ifInNest, ifInNest, ifFoodToRight), seqm2(rr, rr)), selm3(seqm2(fr, fl), seqm2(ifOnFood, stop), selm4(rr, ifNestToRight, ifInNest, ifFoodToLeft)), seqm4(selm2(f, ifRobotToLeft), probm4(ifFoodToLeft, ifRobotToLeft, fl, ifOnFood), selm2(ifFoodToLeft, rr), seqm4(ifRobotToRight, ifNestToRight, ifFoodToLeft, rr)), probm3(seqm4(ifRobotToRight, stop, ifOnFood, ifFoodToLeft), probm4(ifNestToLeft, fr, fr, ifRobotToRight), seqm4(ifFoodToLeft, f, f, ifNestToLeft))))",
			"trimmed" : "probm2(selm2(probm3(probm2(ifNestToLeft, ifFoodToLeft), selm2(ifRobotToRight, fl), selm2(ifRobotToRight, ifInNest)), selm3(seqm2(ifRobotToRight, stop), probm4(ifInNest, ifNestToLeft, stop, rl), fl)), seqm4(probm3(seqm4(ifInNest, ifInNest, ifNestToRight, f), probm3(ifInNest, ifInNest, ifFoodToRight), seqm2(rr, rr)), seqm2(fr, fl), seqm4(f, probm4(ifFoodToLeft, ifRobotToLeft, fl, ifOnFood), selm2(ifFoodToLeft, rr), seqm4(ifRobotToRight, ifNestToRight, ifFoodToLeft, rr)), probm3(seqm2(ifRobotToRight, stop), probm4(ifInNest, fr, fr, ifInNest), seqm3(ifFoodToLeft, f, f))))",
			"fitness" : [0.5061101333333333, 5.933333333333333, 11.344444444444445, 0.5632822]
		})

		self.tests.append({
			"bt" : "probm4(selm4(selm4(fl, stop, f, ifRobotToLeft), seqm4(r, fl, ifNestToRight, ifFoodToLeft), selm2(ifInNest, ifNestToLeft), seqm4(rl, rr, ifInNest, rl)), probm3(seqm3(rl, rl, ifFoodToLeft), probm4(rr, ifFoodToLeft, ifNestToLeft, ifInNest), probm4(ifNestToLeft, ifRobotToRight, rl, ifOnFood)), seqm4(seqm4(fr, f, rr, ifFoodToRight), probm4(ifFoodToRight, ifNestToLeft, fr, ifOnFood), probm4(ifNestToRight, r, ifFoodToLeft, f), seqm2(r, ifRobotToRight)), seqm3(selm2(fl, ifFoodToLeft), probm4(fr, ifOnFood, f, ifRobotToLeft), seqm2(ifInNest, fl)))",
			"trimmed" : "probm4(fl, probm3(seqm2(rl, rl), probm4(rr, ifInNest, ifInNest, ifInNest), probm4(ifInNest, ifInNest, rl, ifInNest)), seqm4(seqm4(fr, f, rr, ifFoodToRight), probm4(ifFoodToRight, ifNestToLeft, fr, ifOnFood), probm4(ifNestToRight, r, ifFoodToLeft, f), r), seqm3(fl, probm4(fr, ifOnFood, f, ifRobotToLeft), seqm2(ifInNest, fl)))",
			"fitness" : [0.5011519777777778, 4.211111111111111, 10.977777777777778, 0.3269735444444444]
		})

		self.tests.append({
			"bt" : "seqm4(seqm2(seqm4(stop, ifFoodToRight, f, rl), selm2(ifNestToRight, ifNestToLeft)), selm2(seqm2(r, ifOnFood), seqm2(stop, stop)), seqm3(selm3(ifNestToLeft, stop, ifNestToLeft), selm3(rl, ifNestToRight, ifInNest), probm4(ifFoodToRight, rr, fr, rl)), selm4(seqm3(f, ifNestToLeft, ifFoodToLeft), selm3(ifInNest, rl, f), seqm3(ifOnFood, rr, ifOnFood), selm4(f, ifFoodToLeft, rl, ifRobotToRight)))",
			"trimmed" : "seqm4(seqm2(seqm4(stop, ifFoodToRight, f, rl), selm2(ifNestToRight, ifNestToLeft)), selm2(seqm2(r, ifOnFood), seqm2(stop, stop)), seqm3(selm2(ifNestToLeft, stop), rl, probm4(ifFoodToRight, rr, fr, rl)), selm2(seqm3(f, ifNestToLeft, ifFoodToLeft), selm2(ifInNest, rl)))",
			"fitness" : [0.49889852222222214, 1.1111111111111112, -3.2888888888888888, 0.48310413333333335]
		})

		self.tests.append({
			"bt" : "selm4(seqm2(probm2(selm3(r, fl, ifOnFood), selm4(rl, ifRobotToLeft, ifFoodToRight, ifFoodToRight)), probm4(probm2(ifNestToLeft, r), selm3(ifNestToRight, r, ifOnFood), probm3(ifInNest, rl, ifRobotToRight), probm3(rl, ifNestToRight, ifNestToRight))), seqm3(probm2(probm4(ifRobotToLeft, ifInNest, ifRobotToRight, fl), selm2(ifRobotToRight, ifFoodToLeft)), seqm3(seqm3(rr, ifNestToRight, r), probm2(fr, fl), selm4(fl, ifOnFood, r, r)), selm4(seqm4(stop, rl, ifOnFood, ifNestToLeft), selm3(rl, ifRobotToRight, fl), seqm2(rr, ifFoodToLeft), selm4(ifNestToRight, stop, ifFoodToRight, ifInNest))), selm3(selm3(seqm4(f, ifInNest, ifNestToLeft, ifRobotToRight), probm3(fr, fl, f), selm4(ifRobotToLeft, stop, ifRobotToLeft, rl)), selm2(selm4(rl, ifNestToLeft, ifRobotToLeft, ifNestToLeft), selm2(ifFoodToLeft, ifRobotToLeft)), selm4(seqm2(ifNestToRight, f), seqm3(ifRobotToRight, f, ifRobotToLeft), seqm3(stop, rl, r), seqm2(ifFoodToRight, r))), probm2(probm4(probm4(r, ifFoodToLeft, fl, rr), selm2(stop, fl), seqm2(r, ifFoodToRight), seqm4(ifFoodToLeft, r, ifInNest, ifFoodToLeft)), probm2(seqm2(ifRobotToLeft, fr), selm4(ifOnFood, ifRobotToRight, f, fr))))",
			"trimmed" : "selm3(seqm2(probm2(r, rl), probm4(probm2(ifNestToLeft, r), selm2(ifNestToRight, r), probm3(ifInNest, rl, ifRobotToRight), probm3(rl, ifNestToRight, ifNestToRight))), seqm3(probm2(probm4(ifRobotToLeft, ifInNest, ifRobotToRight, fl), selm2(ifRobotToRight, ifFoodToLeft)), seqm3(seqm3(rr, ifNestToRight, r), probm2(fr, fl), fl), selm2(seqm4(stop, rl, ifOnFood, ifNestToLeft), rl)), selm2(seqm4(f, ifInNest, ifNestToLeft, ifRobotToRight), probm3(fr, fl, f)))",
			"fitness" : [0.49700163333333325, -9.933333333333334, -10.755555555555556, 0.38935016666666666]
		})

		self.tests.append({
			"bt" : "probm4(selm4(ifRobotToRight, r, rl, r), selm3(stop, ifOnFood, ifRobotToLeft), selm2(ifRobotToLeft, f), seqm2(ifNestToRight, fl))",
			"trimmed" : "probm4(selm2(ifRobotToRight, r), stop, selm2(ifRobotToLeft, f), seqm2(ifNestToRight, fl))",
			"fitness" : [0.4928344333333333, -0.3666666666666667, 4.288888888888889, 0.5651985222222222]
		})

		self.tests.append({
			"bt" : "seqm4(ifInNest, ifFoodToLeft, f, ifOnFood)",
			"trimmed" : "seqm3(ifInNest, ifFoodToLeft, f)",
			"fitness" : [0.5030937555555557, 1.8, 0.0, 0.9865415777777777]
		})

		self.tests.append({
			"bt" : "selm2(seqm2(seqm2(rl, ifOnFood), seqm3(ifFoodToRight, ifFoodToLeft, ifInNest)), probm4(seqm4(f, ifFoodToRight, rl, ifFoodToRight), probm2(rr, fl), probm3(rr, stop, ifNestToRight), probm3(f, ifNestToRight, ifNestToRight)))",
			"trimmed" : "selm2(seqm2(seqm2(rl, ifOnFood), seqm3(ifFoodToRight, ifFoodToLeft, ifInNest)), probm4(seqm3(f, ifFoodToRight, rl), probm2(rr, fl), probm3(rr, stop, ifInNest), probm3(f, ifInNest, ifInNest)))",
			"fitness" : [0.49730439999999987, 8.833333333333332, -9.833333333333332, 0.4821928999999999]
		})

		self.tests.append({
			"bt" : "seqm3(seqm3(rl, stop, ifFoodToRight), seqm3(f, ifOnFood, fl), seqm4(ifFoodToLeft, rl, fl, r))",
			"trimmed" : "seqm3(seqm3(rl, stop, ifFoodToRight), seqm3(f, ifOnFood, fl), seqm4(ifFoodToLeft, rl, fl, r))",
			"fitness" : [0.49624728888888897, 5.488888888888889, -12.188888888888888, 0.3528010333333332]
		})

		self.tests.append({
			"bt" : "probm2(selm3(rl, ifNestToLeft, ifInNest), seqm3(ifRobotToLeft, ifNestToRight, ifNestToLeft))",
			"trimmed" : "probm2(rl, ifInNest)",
			"fitness" : [0.4986800777777779, 0.0, -26.722222222222218, 0.5996047555555556]
		})

		self.tests.append({
			"bt" : "probm4(seqm2(ifFoodToRight, ifRobotToLeft), selm3(ifNestToLeft, ifOnFood, ifRobotToRight), selm3(ifRobotToLeft, r, ifInNest), seqm3(r, ifNestToRight, fr))",
			"trimmed" : "probm4(ifInNest, ifInNest, selm2(ifRobotToLeft, r), seqm3(r, ifNestToRight, fr))",
			"fitness" : [0.49758616666666666, -17.266666666666666, -3.677777777777778, 0.7603626444444445]
		})

		self.tests.append({
			"bt" : "probm4(seqm4(probm3(ifInNest, ifInNest, ifInNest), selm3(ifInNest, stop, ifRobotToRight), probm4(ifRobotToRight, ifOnFood, f, ifNestToLeft), seqm4(ifRobotToLeft, stop, ifInNest, ifNestToRight)), selm2(selm3(ifFoodToLeft, ifNestToRight, stop), seqm3(rr, ifFoodToLeft, ifFoodToLeft)), probm3(seqm3(ifFoodToLeft, ifOnFood, ifOnFood), selm2(fl, r), seqm4(ifOnFood, ifNestToRight, ifInNest, ifFoodToRight)), seqm4(seqm3(ifInNest, ifNestToRight, fl), seqm2(ifNestToRight, ifOnFood), selm3(fl, rr, ifNestToLeft), selm2(ifRobotToRight, fr)))",
			"trimmed" : "probm4(seqm4(probm3(ifInNest, ifInNest, ifInNest), selm2(ifInNest, stop), probm4(ifRobotToRight, ifOnFood, f, ifNestToLeft), seqm2(ifRobotToLeft, stop)), selm3(ifFoodToLeft, ifNestToRight, stop), probm3(ifInNest, fl, ifInNest), seqm4(seqm3(ifInNest, ifNestToRight, fl), seqm2(ifNestToRight, ifOnFood), fl, selm2(ifRobotToRight, fr)))",
			"fitness" : [0.5013806444444444, 0.7333333333333333, 5.5, 0.869712188888889]
		})

		self.tests.append({
			"bt" : "probm4(ifNestToRight, rl, ifRobotToRight, ifNestToLeft)",
			"trimmed" : "probm4(ifInNest, rl, ifInNest, ifInNest)",
			"fitness" : [0.4993715222222222, 0.0, -15.811111111111112, 0.7493805666666666]
		})

		self.tests.append({
			"bt" : "selm3(ifNestToLeft, ifInNest, ifOnFood)",
			"trimmed" : "ifNestToLeft",
			"fitness" : [0.499769988888889, 0.0, 0.0, 1.0]
		})

		self.tests.append({
			"bt" : "probm3(seqm2(stop, stop), seqm3(ifNestToRight, ifRobotToLeft, ifOnFood), probm4(ifFoodToLeft, ifFoodToRight, ifFoodToLeft, stop))",
			"trimmed" : "probm3(seqm2(stop, stop), ifInNest, probm4(ifInNest, ifInNest, ifInNest, stop))",
			"fitness" : [0.4997527444444444, 0.0, 0.0, 0.4610597444444444]
		})

		self.tests.append({
			"bt" : "selm4(probm4(probm4(probm4(ifRobotToRight, ifFoodToLeft, ifInNest, ifNestToLeft), seqm4(f, ifRobotToLeft, ifNestToLeft, rr), selm3(stop, ifOnFood, stop), selm2(rl, ifFoodToRight)), probm2(selm3(ifFoodToRight, ifRobotToLeft, ifOnFood), selm4(fr, rl, f, ifRobotToRight)), probm4(seqm2(r, fr), selm2(ifNestToLeft, stop), selm4(stop, ifRobotToLeft, stop, ifFoodToLeft), selm2(ifNestToRight, ifNestToRight)), seqm3(selm4(ifFoodToLeft, rr, stop, ifOnFood), seqm3(ifNestToRight, stop, stop), probm4(rr, ifNestToLeft, ifNestToRight, ifInNest))), selm3(seqm4(probm2(ifOnFood, fl), selm4(rr, ifFoodToLeft, ifOnFood, ifNestToLeft), seqm2(rl, ifOnFood), selm4(ifRobotToRight, ifNestToLeft, rl, ifNestToRight)), seqm4(seqm2(rl, fl), selm4(rl, ifNestToRight, ifInNest, ifNestToLeft), probm3(stop, ifRobotToRight, ifRobotToRight), probm4(fl, ifFoodToRight, ifRobotToLeft, rl)), selm3(seqm4(ifFoodToLeft, ifRobotToLeft, ifFoodToRight, ifRobotToLeft), selm3(ifRobotToLeft, rr, f), seqm2(ifNestToLeft, fl))), probm3(seqm2(selm2(ifRobotToLeft, rr), seqm4(ifOnFood, r, ifRobotToRight, rr)), seqm2(selm3(ifRobotToRight, ifFoodToRight, stop), seqm2(rr, ifFoodToRight)), selm2(seqm3(rl, f, stop), probm3(ifNestToLeft, f, ifNestToLeft))), selm4(seqm3(seqm4(fr, ifNestToRight, ifRobotToRight, fr), selm4(ifOnFood, stop, ifFoodToLeft, ifInNest), seqm3(ifFoodToLeft, ifOnFood, f)), seqm2(probm3(fl, stop, fl), probm2(ifNestToRight, ifFoodToLeft)), seqm2(probm2(ifRobotToRight, ifFoodToRight), selm4(fl, rl, r, ifRobotToRight)), seqm4(seqm2(f, ifRobotToRight), seqm2(rr, fl), selm2(ifOnFood, ifOnFood), seqm3(ifOnFood, ifFoodToLeft, ifFoodToLeft))))",
			"trimmed" : "selm2(probm4(probm4(probm4(ifRobotToRight, ifFoodToLeft, ifInNest, ifNestToLeft), seqm4(f, ifRobotToLeft, ifNestToLeft, rr), stop, rl), probm2(selm3(ifFoodToRight, ifRobotToLeft, ifOnFood), fr), probm4(seqm2(r, fr), selm2(ifNestToLeft, stop), stop, selm2(ifNestToRight, ifNestToRight)), seqm3(selm2(ifFoodToLeft, rr), seqm3(ifNestToRight, stop, stop), probm4(rr, ifNestToLeft, ifNestToRight, ifInNest))), selm3(seqm4(probm2(ifOnFood, fl), rr, seqm2(rl, ifOnFood), selm3(ifRobotToRight, ifNestToLeft, rl)), seqm4(seqm2(rl, fl), rl, probm3(stop, ifRobotToRight, ifRobotToRight), probm4(fl, ifFoodToRight, ifRobotToLeft, rl)), selm2(seqm4(ifFoodToLeft, ifRobotToLeft, ifFoodToRight, ifRobotToLeft), selm2(ifRobotToLeft, rr))))",
			"fitness" : [0.5024352, -0.13333333333333336, -3.6888888888888887, 0.4488305444444444]
		})

		self.tests.append({
			"bt" : "probm4(seqm4(f, fr, fl, ifFoodToRight), selm2(ifRobotToRight, rl), probm3(ifNestToRight, rl, ifNestToRight), probm3(fr, rl, rr))",
			"trimmed" : "probm4(seqm3(f, fr, fl), selm2(ifRobotToRight, rl), probm3(ifInNest, rl, ifInNest), probm3(fr, rl, rr))",
			"fitness" : [0.49505672222222225, 4.7666666666666675, -6.122222222222222, 0.3495109444444444]
		})

		self.tests.append({
			"bt" : "selm2(ifRobotToRight, stop)",
			"trimmed" : "selm2(ifRobotToRight, stop)",
			"fitness" : [0.499769988888889, 0.0, 0.0, 0.7147884]
		})

		self.tests.append({
			"bt" : "selm4(probm2(ifNestToLeft, ifNestToRight), seqm2(ifRobotToLeft, ifOnFood), probm2(ifFoodToRight, ifOnFood), seqm4(stop, rl, f, stop))",
			"trimmed" : "selm4(probm2(ifNestToLeft, ifNestToRight), seqm2(ifRobotToLeft, ifOnFood), probm2(ifFoodToRight, ifOnFood), seqm4(stop, rl, f, stop))",
			"fitness" : [0.5022110111111111, 5.6, -5.6, 0.6358402555555557]
		})

		self.tests.append({
			"bt" : "selm2(selm4(ifNestToRight, rl, rr, ifFoodToLeft), probm4(ifRobotToRight, ifNestToRight, rl, ifOnFood))",
			"trimmed" : "selm2(ifNestToRight, rl)",
			"fitness" : [0.5060438000000002, 0.0, -15.066666666666668, 0.8116855999999999]
		})

		self.tests.append({
			"bt" : "selm4(selm4(probm4(selm4(ifFoodToLeft, ifRobotToRight, ifFoodToRight, f), selm2(ifInNest, ifRobotToRight), selm4(ifNestToLeft, rr, ifRobotToLeft, ifNestToLeft), probm4(stop, r, stop, fr)), probm4(probm2(ifFoodToLeft, ifRobotToLeft), seqm4(ifFoodToLeft, ifFoodToRight, rr, fr), seqm4(rl, ifRobotToLeft, stop, ifRobotToLeft), seqm3(ifNestToRight, ifFoodToRight, stop)), probm4(probm4(ifNestToRight, ifFoodToLeft, ifOnFood, rl), seqm2(ifFoodToLeft, fr), selm4(ifNestToLeft, ifFoodToLeft, r, r), seqm3(ifRobotToRight, ifOnFood, ifNestToLeft)), seqm4(seqm2(ifNestToRight, ifNestToLeft), seqm2(ifRobotToLeft, ifOnFood), probm2(ifInNest, ifInNest), seqm4(stop, fr, fl, ifRobotToRight))), selm2(selm2(seqm3(ifOnFood, stop, ifRobotToRight), selm3(ifFoodToRight, f, ifRobotToRight)), seqm2(probm3(rr, ifFoodToRight, rl), selm4(rr, fl, ifRobotToLeft, ifFoodToLeft))), seqm2(selm3(seqm4(stop, ifFoodToRight, ifRobotToLeft, ifRobotToLeft), selm4(f, ifFoodToLeft, ifNestToLeft, ifNestToLeft), selm2(ifFoodToRight, ifFoodToRight)), selm4(seqm2(fl, f), probm3(f, rr, ifNestToLeft), probm2(r, fr), seqm2(stop, ifNestToRight))), seqm4(selm3(probm3(f, stop, rr), probm2(r, ifNestToRight), seqm3(ifNestToLeft, rl, fr)), probm2(selm4(ifRobotToLeft, ifRobotToRight, ifFoodToRight, fr), selm2(stop, ifInNest)), selm2(probm3(ifNestToRight, ifNestToLeft, ifNestToRight), selm4(ifRobotToRight, stop, f, ifFoodToLeft)), selm4(probm3(rr, ifRobotToRight, rr), probm3(ifInNest, f, f), selm2(r, ifNestToLeft), probm4(fr, ifRobotToRight, ifNestToLeft, ifInNest))))",
			"trimmed" : "selm2(selm4(probm4(selm4(ifFoodToLeft, ifRobotToRight, ifFoodToRight, f), selm2(ifInNest, ifRobotToRight), selm2(ifNestToLeft, rr), probm4(stop, r, stop, fr)), probm4(probm2(ifFoodToLeft, ifRobotToLeft), seqm4(ifFoodToLeft, ifFoodToRight, rr, fr), seqm4(rl, ifRobotToLeft, stop, ifRobotToLeft), seqm3(ifNestToRight, ifFoodToRight, stop)), probm4(probm4(ifNestToRight, ifFoodToLeft, ifOnFood, rl), seqm2(ifFoodToLeft, fr), selm3(ifNestToLeft, ifFoodToLeft, r), seqm3(ifRobotToRight, ifOnFood, ifNestToLeft)), seqm4(seqm2(ifNestToRight, ifNestToLeft), seqm2(ifRobotToLeft, ifOnFood), probm2(ifInNest, ifInNest), seqm4(stop, fr, fl, ifRobotToRight))), selm2(seqm3(ifOnFood, stop, ifRobotToRight), selm2(ifFoodToRight, f)))",
			"fitness" : [0.5092489444444446, 1.0333333333333334, 4.355555555555556, 0.7110633888888888]
		})

		self.tests.append({
			"bt" : "seqm2(ifOnFood, ifNestToLeft)",
			"trimmed" : "ifOnFood",
			"fitness" : [0.499769988888889, 0.0, 0.0, 1.0]
		})

		self.tests.append({
			"bt" : "selm3(seqm4(selm4(fr, stop, stop, ifFoodToLeft), seqm3(stop, ifRobotToLeft, rl), seqm2(fr, ifRobotToLeft), seqm4(ifNestToRight, ifInNest, fr, fr)), probm3(probm2(fl, f), selm2(fl, fr), selm4(fl, ifOnFood, ifFoodToLeft, ifFoodToRight)), selm2(seqm4(ifFoodToRight, f, ifOnFood, r), probm4(ifFoodToRight, rr, rr, fr)))",
			"trimmed" : "selm2(seqm4(fr, seqm3(stop, ifRobotToLeft, rl), seqm2(fr, ifRobotToLeft), seqm4(ifNestToRight, ifInNest, fr, fr)), probm3(probm2(fl, f), fl, fl))",
			"fitness" : [0.48528598888888885, 2.4, -1.3555555555555556, 0.3101767222222223]
		})

		self.tests.append({
			"bt" : "selm2(seqm4(seqm2(selm4(ifRobotToLeft, fr, ifInNest, rl), selm2(ifOnFood, rr)), probm4(selm4(r, ifFoodToRight, ifNestToLeft, ifRobotToLeft), selm2(ifNestToLeft, rr), seqm3(stop, fr, f), selm4(rl, fl, ifNestToLeft, r)), seqm4(seqm3(f, r, f), seqm3(fr, fl, ifOnFood), selm4(stop, f, ifRobotToLeft, rr), probm2(ifFoodToRight, ifNestToLeft)), seqm4(selm4(f, rr, rr, stop), probm2(stop, rr), seqm2(f, f), selm4(ifFoodToLeft, ifRobotToLeft, ifRobotToRight, fr))), selm2(seqm3(probm2(rl, fl), seqm3(ifRobotToLeft, ifFoodToLeft, ifInNest), seqm3(ifOnFood, ifInNest, rl)), seqm2(seqm4(ifNestToLeft, ifRobotToRight, ifNestToRight, r), selm3(ifOnFood, ifNestToRight, ifInNest))))",
			"trimmed" : "selm2(seqm4(seqm2(selm2(ifRobotToLeft, fr), selm2(ifOnFood, rr)), probm4(r, selm2(ifNestToLeft, rr), seqm3(stop, fr, f), rl), seqm4(seqm3(f, r, f), seqm3(fr, fl, ifOnFood), stop, probm2(ifFoodToRight, ifNestToLeft)), seqm4(f, probm2(stop, rr), seqm2(f, f), selm4(ifFoodToLeft, ifRobotToLeft, ifRobotToRight, fr))), selm2(seqm3(probm2(rl, fl), seqm3(ifRobotToLeft, ifFoodToLeft, ifInNest), seqm3(ifOnFood, ifInNest, rl)), seqm4(ifNestToLeft, ifRobotToRight, ifNestToRight, r)))",
			"fitness" : [0.5040548444444444, 4.088888888888889, -0.31111111111111106, 0.41418302222222214]
		})

		self.tests.append({
			"bt" : "seqm2(fr, ifOnFood)",
			"trimmed" : "fr",
			"fitness" : [0.4975353333333333, 0.0, -40.0, 0.5]
		})

		self.tests.append({
			"bt" : "selm2(ifFoodToLeft, ifRobotToLeft)",
			"trimmed" : "ifFoodToLeft",
			"fitness" : [0.499769988888889, 0.0, 0.0, 1.0]
		})

		self.tests.append({
			"bt" : "probm3(seqm2(ifOnFood, rl), selm4(r, f, f, rl), selm3(ifNestToLeft, stop, f))",
			"trimmed" : "probm3(seqm2(ifOnFood, rl), r, selm2(ifNestToLeft, stop))",
			"fitness" : [0.5116282111111111, -17.133333333333333, -3.1333333333333337, 0.5218883111111111]
		})

		self.tests.append({
			"bt" : "probm2(probm3(selm4(probm4(r, r, f, fl), probm2(ifFoodToRight, stop), seqm2(rr, fl), selm2(ifOnFood, r)), seqm3(seqm2(ifRobotToRight, ifInNest), selm2(rl, fl), selm2(fr, ifFoodToLeft)), probm4(seqm3(f, rr, f), seqm3(ifRobotToRight, ifRobotToLeft, ifInNest), selm3(ifFoodToLeft, fl, fl), probm2(stop, stop))), selm2(probm3(seqm4(ifInNest, ifRobotToLeft, r, fl), probm2(ifFoodToLeft, ifInNest), probm3(ifFoodToLeft, r, rl)), selm3(probm3(rr, f, ifNestToLeft), probm4(ifNestToRight, f, ifOnFood, ifNestToRight), seqm4(ifFoodToRight, fl, ifNestToLeft, ifRobotToLeft))))",
			"trimmed" : "probm2(probm3(probm4(r, r, f, fl), seqm3(seqm2(ifRobotToRight, ifInNest), rl, fr), probm4(seqm3(f, rr, f), ifInNest, selm2(ifFoodToLeft, fl), probm2(stop, stop))), selm2(probm3(seqm4(ifInNest, ifRobotToLeft, r, fl), probm2(ifFoodToLeft, ifInNest), probm3(ifFoodToLeft, r, rl)), selm3(probm3(rr, f, ifNestToLeft), probm4(ifNestToRight, f, ifOnFood, ifNestToRight), seqm2(ifFoodToRight, fl))))",
			"fitness" : [0.5042947, 2.488888888888889, 6.122222222222222, 0.5424714777777778]
		})

		self.tests.append({
			"bt" : "selm2(r, probm4(rl, ifRobotToLeft, ifNestToLeft, ifNestToRight))",
			"trimmed" : "r",
			"fitness" : [0.4926536555555555, 0.3453122333333333, 0.7390745444444444, 0.5073463444444445]
		})

