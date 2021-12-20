#Required modules,
import json, serial, time
 
#json doc file

def readCOM3():
    doc = []

    doc = json.dumps(doc)
    file = open ('on_street_doc.json', 'a')
    file.write(doc)
    file.close()

    doc = serial.Serial('COM3' ,9600)
    time.sleep(1)

    while  True:
        if (doc.inWaiting() == 0):
            pass
        doc_packet = doc.readline()
        doc_packet = str(doc_packet, 'utf8')
        return(doc_packet)
while True:
    print(readCOM3())