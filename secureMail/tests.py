from django.test import TestCase
from secureMail import functions

class CensorTestCase(TestCase):
    def testCensorTextLive(self):
        self.assertEqual(functions.censorTextLive('durch',0,5),
            '<strike>durch</strike>')

    def testCensorTextLiveFinal(self):
        x = unichr(9611)
        self.assertEqual(functions.censorTextFinal(''),
            '')
        self.assertEqual(functions.censorTextFinal('<strike>durch</strike>'),
            x+x+x+x+x)
        self.assertEqual(functions.censorTextFinal('streiche <strike>durch</strike>'),
            'streiche '+x+x+x+x+x)
        self.assertEqual(functions.censorTextFinal(
            '<strike>durch</strike> bla <strike>test</strike>'),
            x+x+x+x+x+' bla '+x+x+x+x)
        self.assertEqual(functions.censorTextFinal('Ein ganz normaler Text'),
            'Ein ganz normaler Text')

    def testHash(self):
        self.assertEqual(functions.hash('blablablablabl'), '93f3a974cfd916f7fe35783d7e3e3cbaa8401588194c4d80a7b32bdb562a30bc')

    def testCipher(self):
        cipher = functions.AESCipher('key')
        self.assertEqual(cipher.decrypt(cipher.encrypt('Dies ist ein Test')), u'Dies ist ein Test')
