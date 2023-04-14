import sys
import xml.etree.ElementTree as ET

tree = ET.parse(sys.argv[1])  # arquivo de codigo xml
root = tree.getroot() # evaml root node
script_node = root.find("script")
output = ""
gohashid = 0

# percorre os elementos xml mapeando-os nos respectivos no modelo Json do Eva
def mapping_xml_to_json():
    global output
    # conjunto de nodes abstratos que nao sao mapeados no Json do robô
    excluded_nodes = set(['script', 'switch', 'stop', 'goto'])
    for elem in script_node.iter():
        if not(elem.tag in excluded_nodes):

            if (elem.tag == 'audio'):
                output += ",\n"
                output += audio_process(elem)

            if (elem.tag == 'light'):
                output += ",\n"
                output += light_process(elem)

            if (elem.tag == 'wait'):
                output += ",\n"
                output += wait_process(elem)

            if (elem.tag == 'talk'):
                output += ",\n"
                output += talk_process(elem)

            if (elem.tag == 'random'):
                output += ",\n"
                output += random_process(elem)

            if (elem.tag == 'listen'):
                output += ",\n"
                output += listen_process(elem)

            if (elem.tag == 'counter'):
                output += ",\n"
                output += counter_process(elem)

            if (elem.tag == 'evaEmotion'):
                output += ",\n"
                output += eva_emotion_process(elem)

            if (elem.tag == 'userEmotion'):
                output += ",\n"
                output += user_emotion_process(elem)

            if (elem.tag == 'case'):
                output += ",\n"
                output += case_process(elem)

            # default é um caso especial do comando case, onde value = ""
            if (elem.tag == 'default'):
                output += ",\n"
                output += case_process(elem)


# head processing (generates the head of json file)
def head_process(node):
    node.attrib["key"] = str(0)
    init = """{
  "_id": """ + '"' + node.attrib["id"] + '",' + """
  "nombre": """ + '"' + node.attrib['name'] + '",' + """
  "data": {
    "node": [
"""
    return init

# processing the settings nodes
# always be the first node in the interaccion
def settings_process(node):
    return voice_process(node.find("voice"))
    # processar light-effects
    # processar sound-effects

# audio node processing
def audio_process(audio_command):
    global gohashid
    audio_node = """      {
        "key": """ + audio_command.attrib["key"] + """,
        "name": "Audio",
        "type": "sound",
        "color": "lightblue",
        "isGroup": false,
        "src": """ + '"' + audio_command.attrib['source'] + '",' + """
        "wait": """ + audio_command.attrib['block'] + ',' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return audio_node

# counter node processing #########################################################################
def counter_process(counter_command):
    global gohashid
    if counter_command.attrib['op'] == "=":
      op_eva = "assign"
    elif counter_command.attrib['op'] == "+":
      op_eva = "sum"
    elif counter_command.attrib['op'] == "*":
      op_eva = "mul"
    elif counter_command.attrib['op'] == "/":
      op_eva = "div"
    elif counter_command.attrib['op'] == "%":
      op_eva = "rest"

    counter_node = """      {
        "key": """ + counter_command.attrib["key"] + """,
        "name": "Counter",
        "type": "counter",
        "color": "lightblue",
        "isGroup": false,
        "group": "",
        "count": """ + '"' + counter_command.attrib['var'] + '",' + """
        "ops": """ + '"' + op_eva + '",' + """
        "value": """ + counter_command.attrib['value'] + ',' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return counter_node


# light node processing
def light_process(light_command):
    global gohashid
    if light_command.attrib['state'] == "off": # a ideia é admitir a ausencia do parametro color quando o estado da lampada for off
      light_command.attrib['color'] = "black" # mesmo se o atributo não tiver sido setado, ele será setado aqui
    color = light_command.attrib['color']
    color_map = {"white":"#ffffff", "black":"#000000", "red":"#ff0000", "pink":"#e6007e", "green":"#00ff00", "yellow":"#ffff00", "blue":"#0000ff"}
    if color_map.get(color) != None:
        color = color_map.get(color)
    light_node = """      {
        "key": """ + light_command.attrib["key"] + """,
        "name": "Light",
        "type": "light",
        "color": "#FFA500",
        "isGroup": false,
        "group": "",
        "lcolor": """ + '"' + color + '",' + """
        "state": """ + '"' + light_command.attrib['state'] + '",' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return light_node


# listen node processing 
####################################################################################### falta implementar os filtros
def listen_process(listen_command):
    global gohashid
    listen_node = """      {
        "key": """ + listen_command.attrib["key"] + """,
        "name": "Listen",
        "type": "listen",
        "color": "#ffff00",
        "isGroup": false,
        "opt": "",
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return listen_node


# talk node processing
def talk_process(talk_command):
    global gohashid
    talk_node = """      {
        "key": """ + talk_command.attrib["key"] + """,
        "name": "Talk",
        "type": "speak",
        "color": "#00ff00",
        "isGroup": false,
        "text": """ + '"' + talk_command.text + '",' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return talk_node


# voice node processing
def voice_process(voice_command):
  global gohashid
  voice_node = """      {
        "key": """ + voice_command.attrib["key"] + """,
        "name": "Voice",
        "type": "voice",
        "color": "#0020ff",
        "isGroup": false,
        "voice": """ + '"' + voice_command.attrib['tone'] + '",' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
  gohashid += 1
  return voice_node

# userEmotion node processing
def user_emotion_process(user_emotion_command):
  global gohashid
  user_emotion_node = """      {
        "key": """ + user_emotion_command.attrib["key"] + """,
        "name": "User_Emotion",
        "type": "user_emotion",
        "color": "lightgreen",
        "isGroup": false,
        "group": "",
        "vision": "capture",
        "__gohashid": """ + str(gohashid) + """
      }"""
  gohashid += 1
  return user_emotion_node


# eva_emotion node processing 
def eva_emotion_process(eva_emotion_command):
    global gohashid
    # speed 0 é o valor default. Não vejo necessidade de implementar isso

    if eva_emotion_command.attrib['emotion'] == "happy": # compatibiliza com o Eva. O Eva usa joy.
      eva_emotion_command.attrib['emotion'] = "joy"

    if eva_emotion_command.attrib['emotion'] == "angry": # compatibiliza com o Eva.
      eva_emotion_command.attrib['emotion'] = "anger"

    if eva_emotion_command.attrib['emotion'] == "neutral": # compatibiliza com o Eva.
      eva_emotion_command.attrib['emotion'] = "ini"

    eva_emotion_node = """      {
        "key": """ + eva_emotion_command.attrib["key"] + """,
        "name": "Eva_Emotion",
        "type": "emotion",
        "color": "lightcoral",
        "isGroup": false,
        "group": "",
        "emotion": """ + '"' + eva_emotion_command.attrib['emotion'] + '",' + """
        "level": 0,
        "speed": 0,
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return eva_emotion_node


# random node processing
def random_process(random_command):
    global gohashid
    random_node = """      {
        "key": """ + random_command.attrib["key"] + """,
        "name": "Random",
        "type": "random",
        "color": "pink",
        "isGroup": false,
        "group": "",
        "min": """ + random_command.attrib['min'] + ',' + """
        "max": """ + random_command.attrib['max'] + ',' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return random_node


# condition node (case and default) processing
def case_process(case_command):
  global gohashid
  # traducao dos operadores lógicos. Nós usamos o mesmo padrão que NCL
  if case_command.attrib['op'] == "lt":  op = "<"
  if case_command.attrib['op'] == "gt":  op = ">"
  if case_command.attrib['op'] == "eq":  op = "=="
  if case_command.attrib['op'] == "lte": op = "<="
  if case_command.attrib['op'] == "gte": op = ">="
  if case_command.attrib['op'] == "ne":  op = "!==" # preciso verificar este.parece que os mexicanos nao implementaram o not.
    
  # verifica qual o tipo de comparacao para $. Exact ou contain
  if case_command.attrib["op"] == "exact":
    case_node = """      {
        "key": """ + case_command.attrib["key"] + """,
        "name": "Condition",
        "type": "if",
        "color": "white",
        "isGroup": false,
        "text": """ + '"' + case_command.attrib['value'] + '",' + """
        "opt": 4,
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return case_node

  elif case_command.attrib["op"] == "contain": # se é "contain"
    case_node = """      {
        "key": """ + case_command.attrib["key"] + """,
        "name": "Condition",
        "type": "if",
        "color": "white",
        "isGroup": false,
        "text": """ + '"' + case_command.attrib['value'] + '",' + """
        "opt": 2,
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return case_node

  else: # testando um valor em relacao a outra variavel qualquer
    # é preciso que haja um espaço entre os operandos e o operador. ex #x == 1
    # opt": 5 é comparacao matematica, isto é, com operadores do tipo ==, >, <, >=, <= ou !=
    if case_command.attrib["var"] == "$":
      case_node = """      {
        "key": """ + case_command.attrib["key"] + """,
        "name": "Condition",
        "type": "if",
        "color": "white",
        "isGroup": false,
        "text": """ + '"' + case_command.attrib['var'] + ' ' + op + ' ' + case_command.attrib['value'] + '",' + """
        "opt": 5,
        "__gohashid": """ + str(gohashid) + """
      }"""
      gohashid += 1
      return case_node
    else:
      case_node = """      {
        "key": """ + case_command.attrib["key"] + """,
        "name": "Condition",
        "type": "if",
        "color": "white",
        "isGroup": false,
        "text": """ + '"#' + case_command.attrib['var'] + ' ' + op + ' ' + case_command.attrib['value'] + '",' + """
        "opt": 5,
        "__gohashid": """ + str(gohashid) + """
        }"""
      gohashid += 1
      return case_node


# wait node processing
def wait_process(wait_command):
    global gohashid
    wait_node = """      {
        "key": """ + wait_command.attrib["key"] + """,
        "name": "Wait",
        "type": "wait",
        "color": "lightblue",
        "isGroup": false,
        "time": """ + wait_command.attrib['duration'] + ',' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return wait_node
        

def saida_links():
    node_links = root.find("links")
    output ="""
    ],
    "link": [""" + """
      { 
        "from": """ + node_links[0].attrib["from"] + "," + """
        "to": """ + node_links[0].attrib["to"] + "," + """
        "__gohashid": 0
      }"""

    for i in range(len(node_links) - 1):
        output += """,
      { 
        "from": """ + node_links[i+1].attrib["from"] + "," + """
        "to": """ + node_links[i+1].attrib["to"] + "," + """
        "__gohashid": """ + str(i + 1) + """
      }"""

    output += """
    ]
  }
}"""
  
    return output

# gerando o cabeçalho do Json
# onde são inseridos o id e o nome da interação baseados nos dados xml
output += head_process(root) # usa os atributos id e name da tag <evaml>

# o proximo comando pega o parametro do elemento voice (timbre) e gera o primeiro elem. do script Json
output += settings_process(root.find("settings"))

# processamento da interação
mapping_xml_to_json() # nova versao

# mapeia os links xml para json
output += saida_links()

print("step 04 - Mapping XML nodes and links to a JSON file...")

# criação de um arquivo físico da interação em json
file_out = open(root.attrib['name'] + '.json', "w")
file_out.write(output)
# file_out.write(output.encode('utf-8')) para rodar no raspberry
file_out.close()

