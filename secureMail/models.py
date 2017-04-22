from django.db import models
import functions

class Message(models.Model):
    msg_hash = models.CharField(max_length = 255)
    cyphertext = models.TextField()
    pwd = models.CharField(max_length = 255)
    btrf = models.CharField(max_length = 255, default='Betreff')
    email = models.CharField(max_length=255, default='test@mail.de')

    #def generatePassword():
        #return functions.generatePassword()

    #def censorTextFinal(text):
       #return functions.censorTextFinal(text)

    #def saveMessage(message, pwd):
      #  return functions.saveMessage(message, pwd)

  #def retrieveMessage(messageHash, pwd):
    #    return functions.retrieveMessage(messageHash, pwd)

    #def deleteMessage(messageHash, pwd):
      #  return functions(messageHash, pwd)

    #def hash(text):
      #  return functions.hash(text)
