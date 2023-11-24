import datetime
import pytz

from gtt.extra import api_data_json


def next_pass(pas):
    hours, minutes = map(int, pas.split(' ')[0].split(':'))
    rome_timezone = pytz.timezone('Europe/Rome')  # Set the time zone to Rome
    now = datetime.datetime.now(rome_timezone)
    nextpass = (hours * 60 + minutes) - (now.hour * 60 + now.minute)
    return nextpass


def printout(data):
    var = ""
    if data == "Errore: Fermata non trovata o sito non raggiungibile":
        return data
    for bus_line, pas, direction, nextpass in data:
        var += "Linea: " + str(bus_line) + " (" + str(direction) + ")<br>"
        var += "Passaggi: " + str(pas) + "<br>"
        if nextpass == "Non disponibile":
            var += "Prossimo passaggio: Non disponibile <br>"
        elif int(nextpass) <= 1:
            var += "Prossimo passaggio: In arrivo" + "<br>"
        else:
            var += "Prossimo passaggio: " + str(nextpass) + " minuti" + "<br>"
    return var


def gttorari_stop(stop):
    url = f" https://www.gtt.to.it/cms/index.php?option=com_gtt&task=palina.getTransitiOld&palina={stop}&bacino=U&realtime=true&get_param=value"
    data = api_data_json(url)
    if data == "Errore: Fermata non trovata o sito non raggiungibile":
        return data, stop
    stops = []
    if str(data) == "[{'PassaggiRT': [], 'PassaggiPR': []}]":
        return "Fermata non trovata o sito non raggiungibile", stop
    pas = ""
    print(data)
    for i in data:
        if not i['PassaggiRT']:
            for passaggi in i["PassaggiPR"]:
                pas = pas + str(passaggi) + " "
            nextpass = next_pass(i["PassaggiPR"][0])
        else:
            for passaggi in i['PassaggiRT']:
                pas = pas + str(passaggi) + "* "
            nextpass = next_pass(i['PassaggiRT'][0])
        stops.append((i['Linea'], pas, i['Direzione'], nextpass))
        pas = ""
    return stops, stop


def gttorari_stop_line(stop, line):
    line = str(line)
    data, stop = gttorari_stop(stop)
    if data == "Errore: Fermata non trovata o sito non raggiungibile":
        return data
    else:
        data = [x for x in data if x[0] == line]
        return data, stop