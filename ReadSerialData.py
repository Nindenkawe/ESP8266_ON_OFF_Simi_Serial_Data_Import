#Require modules,
import json, serial, time
 
#json doc file
doc = []

doc = json.dumps(doc)

file = open ('on_street_doc.json', 'a')
file.write(doc)
file.close()

doc = serial.Serial('COM5' ,115200)
time.sleep(1)


while True:
    while (doc.inWaiting() == 0):
        pass
    doc_packet = doc.readline()
    doc_packet = str(doc_packet, 'utf8')
    print(doc_packet)