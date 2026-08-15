import unittest
import Method as M
#This file tests the main functions to make sure they all work correctly.
#The numbers are all confirmed by other calculators and then compared to the calculations done in the previous code (with some tolerance for extra decimals).
class MyTestCase(unittest.TestCase):
    #Tests European Option formula
    def test_european_option(self):
        assert abs(M.european_option_formula(100, 100, 1, .2, .05, 0, "yes")-10.4506) <.001, f"European 1 (Call) wrong {M.european_option_formula(100, 100, 1, .2, .05, 0, "yes")}"
        #Tests the function, call and all.
        assert abs(M.european_option_formula(100, 100, 1, .2, .05, 0, "no")-5.5735) <.001, f"European 2 with put wrong {M.european_option_formula(100, 100, 1, .2, .05, 0, "no")}"
        #Tests put.
        assert abs(M.european_option_formula(120, 100, .5, .25, .04, .01, "yes") - 22.6491) < .0001, f"European different numbers wrong {M.european_option_formula(120, 100, .5, .25, .04, .01, "yes")}"
        assert abs(M.european_option_formula(100, 110, .25, .3, .05, .02, "no") -11.8217) < .0001, f"European different numbers wrong {M.european_option_formula(100, 110, .25, .3, .05, .02, "no")}"
        #These last two make sure it is not just a fluke and add dividend yield.
        print("European test clear!")


    #Tests the Greeks
    def test_greek(self):
        agreektuple = M.Greeks(100, 100, 1, .2, .05, 0, "yes", 0)
        agreektuple2 = M.Greeks(100, 100, 1, .2, .05, 0, "no", 0)
        assert abs(agreektuple[0] -.6368) < .0001, f"Greeks wrong (Call delta) {agreektuple[0]}"
        assert abs(agreektuple[1] -.01876) < .0001, f'Greeks wrong (Call gamma) {agreektuple[1]}'
        assert abs(agreektuple[2] - .37524) < .001, f'Greeks wrong (Call Vega) {agreektuple[2]}'
        assert abs(agreektuple[3] - .53232) < .001, f"Greeks wrong (Call rho) {agreektuple[3]}"
        assert abs(agreektuple[4]+ 6.414) < .001, f"Greeks wrong (Call theta) {agreektuple[4]}"
        assert abs(agreektuple2[0] + .3632) < .0001, f"Greeks wrong (Put delta) {agreektuple2[0]}"
        assert abs(agreektuple2[1] - agreektuple[1]) < .0001, f"Greeks wrong (put Gamma) {agreektuple2[1]}"
        assert abs(agreektuple2[2] - agreektuple[2]) < .001, f"Greeks wrong (put Vega) {agreektuple2[2]}"
        assert abs(agreektuple2[3] + .41891) < .001, f"Greeks wrong (put Rho) {agreektuple2[3]}"
        assert abs(agreektuple2[4] + 1.657) < .001, f"Greeks wrong (put theta) {agreektuple2[4]}"
        #This simply makes sure every single one of them are close as they pretty much all have similar formulas.
        print("Greek test clear!")

    #Tests CRR/american_option_main.
    def test_CRR(selfself):
        crr = M.american_option_main(100, 100, 1, .2, .05, 0, "yes", 10000)
        assert abs(crr - 10.4506) < .01, f"CRR failed first test {crr}"
        #calculates crr for 10000 timesteps for accuracy and then lets you know if wrong and what it would be. CRR approx european option here.

        crr = M.american_option_main(100, 100, 1, .2, .05, 0, "no", 10000)
        assert abs(crr - 6.0903) < .01, f"CRR failed put {crr}"
        # Calculates CRR when it is not similar to european option by put method

        crr = M.american_option_main(120, 100, .5, .25, .04, .01, "yes", 10000)
        assert abs(crr- 22.6491) < .01, f"CRR failed with dividend call {crr}"
        crr = M.american_option_main(100, 110, .25, .3, .05, .02, "no", 10000)
        assert abs(crr - 12.0035) < .001, f"CRR failed with dividend put {crr}"
        #Makes sure the others were not a fluke.
        print("CRR test clear!")
if __name__ == '__main__':
    unittest.main()
    print("done")
