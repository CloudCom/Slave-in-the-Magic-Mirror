import time
import drm
import sys
#import msvcrt

#msvcrt.setmode (sys.stdin.fileno(), os.O_BINARY)

class FairPlayREPL(object):
    def __init__(self, airtunesd_filename=None):
        self.airtunesd_filename = airtunesd_filename

    def run(self):
        self.init()

        run = True
        while run:
            if self.sap_stage == 0:
                expected_data_length = 16
            elif self.sap_stage == 1:
                expected_data_length = 164
            else:
                expected_data_length = 72

            data = sys.stdin.read(expected_data_length)

            if len(data) == 0:
        	    run = False
            else:
                if len(data) > 0 and data[0] == chr(27):
                    self.sap_stage = 0
                else:
                    if self.sap_stage <= 1:
                        print self.challenge(data)
                    else:
                        print self.decrypt(data)

    def init(self):
        #print "Initialising FairPlay SAP..."
        st = time.clock()
        self.sap = drm.FairPlaySAP(self.airtunesd_filename)
        et = time.clock()
        #print "Done! Took %.2f seconds." % (et-st)

        self.sap_stage = 0
        print "FPLYRDY"

    def challenge(self, chal_data):
        #print "Calculating AirPlay challenge stage %d..." % self.sap_stage
        st = time.clock()
        response = self.sap.challenge(ord(chal_data[4]), chal_data.rstrip("\n"), self.sap_stage)
        et = time.clock()
        #print "Done! Took %.2f seconds." % (et-st)
        self.sap_stage += 1
        return response

    def decrypt(self, encrypted_key):
        #print "Decrypting AirPlay key..."
        st = time.clock()
        key = self.sap.decrypt_key(encrypted_key)
        et = time.clock()
        #print "Done! Took %.2f seconds. AirPlay key: %s" % (et-st, key.encode("hex"))

        self.sap_stage = 0

        return key

if __name__ == "__main__":
    repl = FairPlayREPL("airtunesd")
    repl.run()

