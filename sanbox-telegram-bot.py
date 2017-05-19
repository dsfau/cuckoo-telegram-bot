import re
import telepot
import ast
import subprocess
#print bot.getUpdates()
class Message:
	def __init__(self, raw_message):
		self.raw_message=raw_message
		self.date=self.raw_message["message"]["date"]
		try:
			self.text=self.raw_message["message"]["text"]
		except:
			pass
		try:
			self.document_id = self.raw_message["message"]["document"]['file_id']
			self.document_name =  self.raw_message["message"]["document"]['file_name']
		except:
			pass
		self.id_from=self.raw_message["message"]["from"]["id"]
		self.message_id=self.raw_message["message"]["message_id"]
		self.update_id=self.raw_message["update_id"]
	def getMessage(self):
		return self.raw_message
	def getDate(self):
		return self.date
	def getMessageId(self):
		return self.message_id
	def getText(self):
		try:
			return self.text
		except:
			return None
	def getUpdateId(self):
		return self.update_id
	def getIdFrom(self):
		return self.id_from
	def getDocumentId(self):
		try:
			return self.document_id
		except:
			return None
	def getDocumentName(self):
		try:
			return self.document_name
		except:
			return None
class boot:
	def __init__(self,api):
		self.__api_key=api
		self.bot=telepot.Bot(self.__api_key)
		self.list_ids_ban=[]
#		self.list_ids_permit=[]
		self.list_ids_permit=[ID_PERMITS]
	def updates(self,func):
		last_id=0
		while True:
			try:
				last_msg=self.bot.getUpdates()[-1]
#				if last_msg["update_id"] <> last_id and last_msg["message"]["from"]["id"] not in self.list_ids_ban:
				if last_msg["update_id"] <> last_id and last_msg["message"]["from"]["id"] in self.list_ids_permit and last_msg["message"]["from"]["id"] not in self.list_ids_ban:
					func(self.bot.getUpdates()[-1])
					last_id=last_msg["update_id"]
				else:
					pass
			except Exception as e:
				print e
				break
	def setInsertIdBan(self,new_id):
		self.list_ids_ban.append(new_id)
		print "Se a baneado a {0}".format(new_id)
	def sendMessage(self,msg,id):
		self.bot.sendMessage(id, msg)
	def listener(self, raw_msg):
		msg=Message(raw_msg)
		print msg		
	def download_file(self, id, file):
		self.bot.download_file(id, file)
class Listenner:
	def __init__(self, bot):
		self.bot=bot
		self.id=0
		self.dic_trys={}
		self.dic_users_autenticated=bot.list_ids_permit
	def listen(self,raw_msg):
		self.msg=Message(raw_msg)
		print self.msg.getText()
		if self.msg.getIdFrom() in self.dic_users_autenticated:
			if self.msg.getDocumentId() is not None:
				documentName = self.msg.getDocumentName()
				f=open("./documents/"+documentName, "wr")
				self.bot.download_file(self.msg.getDocumentId(),f)
				f.close()
				pipe = subprocess.Popen(["/usr/local/bin/cuckoo",'submit', './documents/'+documentName],stdout=subprocess.PIPE)
				st, so = pipe.communicate()
				self.bot.sendMessage(documentName + " " + st.split('"')[2], self.msg.getIdFrom())
				
p=boot("API_KEY_BOT")
l=Listenner(p)
p.updates(l.listen)
