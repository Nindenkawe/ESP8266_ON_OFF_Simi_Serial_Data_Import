#Required modules,
import json, serial, time
 
#json doc file

def readCOM3():
    doc = []

    doc = json.dumps(doc)
    file = open ('on_street_doc.json', 'a')
    file.write(doc)
    file.close()

    doc = serial.Serial('COM3' ,115200)
    time.sleep(1)


    if True:
        while (doc.inWaiting() == 0):
            pass
        doc_packet = doc.readline()
        doc_packet = str(doc_packet, 'utf8')
        return(doc_packet)
print(readCOM3())