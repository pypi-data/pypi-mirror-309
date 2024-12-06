"""bibWerkzeug - Definiert nützlichen Kram
"""

import contextlib
import datetime
import json
import os, os.path
import string
import subprocess

def human_readable(num):
    """human_readable - liefert Menschen-lesbaren str für (Datei-)Größe
    
    Liefert 5K, 199M, 23G, 45T
    
    Parameter
        num     Ingeter
    """
    if type(num) != int:
        return 'Type ist nicht int.'
    if num < 0:
        return '-{}'.format(human_readable(-num))
    for unit in ('', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y', 'R', 'Q', 'ZuGross'):
        if num < 1024:
            break
        num /= 1024
    return f'{num:.0f}{unit}'

def getFileRclone(remote, filename, path='', local_path='./'):
    """getRclone - gets all files from remote:path and puts it to local_path
    """
    subprocess.run(
        f'rclone copyto {remote}:{path}{filename} {local_path}{filename}',
        shell=True
        )

def lsRclone(remote, path=''):
    """dirFiles - holt per rclone Verzeichnis der Dateien in path
    
    Holt per rclone lsjson Verzeichnis in path.
    
    Parameter
        remote    gültiger Remote von rclone
        path      Pfad, von dem das Verzeichnis geholt werden soll
                  Default: Grundverzeichnis des Remote
    
    Ergebnis
        List von Dicts mit den keys
            'Name'      : Name der Datei
            'Size'      : Größe der Datei (als Str)
            'Date'      : Mod Date der Datei (als Str)
            'Str'       : Anzeigbarer String: Size Date Name
    """
    ls = subprocess.run(
            f'rclone lsjson {remote}:{path}',
            capture_output=True,
            text=True,
            shell=True)
    if StdError := ls.stderr:
        logger.error(f'{StdError}')
        return []
    Ergebnis = []
    Zeilen = json.loads(ls.stdout)
    for Zeile in Zeilen:
        Name = Zeile['Name']
        Size = human_readable(Zeile['Size'])
        # Eleminiere T und Z aus DateTime-String
        DateTime = datetime.datetime.strptime(Zeile['ModTime'], '%Y-%m-%dT%H:%M:%SZ')
        Date = datetime.datetime.strftime(DateTime, '%Y-%m-%d %H:%M')
        Ergebnis.append({
            'Name': Name,
            'Size': Size,
            'Date': Date,
            'Str': f'{Size:>4} {Date} {Name}',
            })
    return Ergebnis

def _checkTypeOfKey(key):
    """_checkTypeOfKey - True, wenn key ein gültiger Python Name ist
        
        _checkTypeOfKey wird von getAttr und setAttr verwendet.
        _checkTypeOfKey prüft, ob key ein gültiger Python Name ist.
        Genauer: Es wird geprüft, ob
            1. key mit einem ascii-Zeichen beginnt
            2. alle übrigen Zeichen
                  ascii-Zeichen
                  oder Nummern ('0', .. '9')
                  oder Unterstrich ('_')
               sind.
        
        Falls die Prüfung besteht, wird True zurück gegeben.
        In allen anderen Fällen wird ValueError geworfen.
    
        Parameter
            key     Zu prüfender Name
                    Typ: str
    """
    
    BEGINS = string.ascii_letters
    CONTINUES = string.ascii_letters + string.digits + '_'
    E = 'bibWerkzeug: _checkTypeOfKey: '
    
    if type(key) != str:
        raise ValueError(E + f'key muss str sein, ist {type(str)}')
    
    if key[0] not in BEGINS:
        raise ValueError(E + f'{key=} muss mit einem ascii-char beginnen.')
    
    for i in range(1, len(key)):
        if key[i] not in CONTINUES:
            raise ValueError(E + f'falsches Zeichen in {key=}: {key[i]=}')
    
    return True

def checkPythonName(name):
    """checkPythonName - Alias für _checkTypeOfKey
    
        Aus historischen Gründen wird _checkTypeOfKey beibehalten und dieses
        Alias eingeführt.
    """
    return _checkTypeOfKey(name)

def getAttr(obj, key):
    """getAttr - erweitert getattr, holt Attribut auch von Dict
    
        Vgl. "Gegenstück" setAttr
    
        Primär sind getAttr und setAttr entstanden, um Daten aus einer DB
        von einem Modell an ein Formular zu übergeben oder umgekehrt.
        Vor allem für Testzwecke ist es hilfreich, wenn die Daten
        alternativ als Dictionary übergeben werden. Mit
            getAttr und
            setAttr
        werden je nach Typ der Objekte letztlich die Funktionen
        getattr/setattr oder dict.get/dict[key]=... verwendet.
        
        Parameter
            obj     dict oder Instanz einer Klasse
            key     key eines dict oder Attribut der Klasse
                    Typ: str. Der Benutzer verantwortet, dass es sich bei 
                    key um einen gültigen Namen für Attribute handelt
        
        Beachte:
            Falls obj kein Attribut key hat, wird None zurückgegeben.
    """
    # Typ von key überprüfen
    # _checkTypeOfKey wirft ValueError, falls die Prüfung nicht erfolgreiche ist.
    _checkTypeOfKey(key)
    
    if type(obj) == dict:
        return obj.get(key)       # None, wenn nicht key in obj (dict)
    elif hasattr(obj, key):
        return getattr(obj, key)
    else:
        return None

def setAttr(obj, key, value):
    """setAttr - erweitert setattr, setzt Attribut auch von Dict
    
        Vgl. "Gegenstück" getAttr
    
        Primär sind getAttr und setAttr entstanden, um Daten aus einer DB
        von einem Modell an ein Formular zu übergeben oder umgekehrt.
        Vor allem für Testzwecke ist es hilfreich, wenn die Daten
        alternativ als Dictionary übergeben werden. Mit
            getAttr und
            setAttr
        werden je nach Typ der Objekte letztlich die Funktionen
        getattr/setattr oder dict.get/dict[key]=... verwendet.
        
        Parameter
            obj     dict oder Instanz einer Klasse
            key     key eines dict oder Attribut der Klasse
                    Typ: str. Der Benutzer verantwortet, dass es sich bei 
                    key um einen gültigen Namen für Attribute handelt
            value   Wert, auf den das Attribut gesetzt werden soll
        
        Beachte:
            Falls obj kein Attribut key hat, wird nichts unternommen. Insb.
            wird dieses Attribut dann auch nicht neu angelegt.
        
        Ergebnis
            True    Falls das Attribut key vorhanden ist
                    und auf value gesetzt wurde
            False   Falls das Attribut key nicht vorhanden ist
                    und entsprechend auch nicht gesetzt wurde
    """
    # Typ von key überprüfen
    # _checkTypeOfKey wirft ValueError, falls die Prüfung nicht erfolgreiche ist.
    _checkTypeOfKey(key)
    
    if type(obj) == dict:
        if key in obj:
            obj[key] = value
            return True
        else:
            return False
    elif hasattr(obj, key):
        setattr(obj, key, value)
        return True
    else:
        return False

def copyAttrs(a, b):
    """copyAttrs - setzt alle Attribute von a in b, soweit es sie dort gibt
    
        copyAttrs setzt in b alle Attribute, die sowohl in a als auch in b
        vorkommen. Alle anderen Attribute werden ignoriert bzw. übergangen.
        
        Parameter
            a, b    dict Instanz einer Klasse
    """
    if type(a) == dict:
        for k in a:
            setAttr(b, k, getAttr(a, k))
    else:
        for k in a.__dict__:
            setAttr(b, k, getAttr(a, k))

class Attribute():
    """Attribute - Simple Lösung für Punkt-Notation (L.a...)
    
        Dicts sind über []-Notation erreichbar, wir suchen aber eine
        simple Möglichkeit für .-Notation.
        
        Die einfachste Anwendung von Attribute geht über direkte
        Zuweisung:
            A = Attribute()
            A.a = 1
            A.b = 2
        Entsprechend kann auf die so gesetzten Attribute zugegriffen werden:
            x = A.a     # x = 1
            y = A.b     # y = 2
        
        Darüber hinaus kann beim Instanziieren bereits eine Aufzählung
        von Attributen und Werten übergeben werden.
        Dabei müssen die Attribute vom Typ str sein.
        Übergeben werden können:
        
            Tupel/Listen von key/value-Tupeln/Listen
                Bsp.: (('a', 1), ('b', 2))
            
            Dict mit key/value-Einträgen. Auch hier muss key vom Typ str sein.
                Bsp.: {'a': 1, 'b': 2}
        
        Parameter
            atts    Vorgabe für die Attribute, vgl. Erklärung, was übergeben
                    werden kann.
        
        Operatoren
            in      True, wenn ein Attribut (str) vorhanden ist.
                    Bsp.:
                    A = Attribut({'a', 1})
                    'a' in A   -->   True
                    Wird über __contains__ implementiert
        
        Methoden
            addAttribut
                    Anstatt A.a = 1 kann auch
                    A.addAttribut('a', 1) verwendet werden.
            atts    Liefert alle keys, d.h. alle Attribute als str
                    Type: Liste
            values  Liefert alle values als Liste
            dict    Liefert alle Attribute mit ihren Values als
                    Dict zurück.
    """
    
    def __init__(self, atts=None):
        if type(atts) == dict:
            # Es wurde ein Dict übergeben
            for key in atts:
                if type(key) == str:
                    setattr(self, key, atts[key])
                else:
                    raise TypeError(f'Attribute: {key=} muss str sein.')
        elif atts is not None:
            # Es wurde kein Dict übergeben, aber es wurde etwas übergeben.
            # Wir unterstellen, dass atts in diesem Fall ein iterable von
            # key/value Tupeln/Listen ist, die jeweils genau zwei Werte enthalten,
            # nämlich key und value.
            for (key, value) in atts:
                if type(key) == str:
                    self.addAttribut(key, value)
                else:
                    raise TypeError(f'Liste: {key=} muss str sein.')
        else:
            # Es wurde nichts übergeben. Wir machen auch nichts.
            pass
    
    def __contains__(self, key):
        return key in self.__dict__
    
    def addAttribut(self, key, value):
        """addAttribut - Fügt ein neues Attribut hinzu
        
            Ist A = Attribut(), kann
                A.a = 1
            oder
                A.addAttribut('a', 1)
            verwendet werden.
            A.addAttribut erlaubt nur neue Attribute, A.a ersetzt ggf. den Wert,
            falls das Attribut bereits vorhanden ist. A.addAttribut wirft
            eine Exception (ValueError), falls das Attribut bereits vorhanden ist.
            A.addAttribut wirft ein Exception (Type Error), falls key kein str ist.
            
            Parameter
                key     Schlüssel des Attributs
                value   Wert des Attributs
        """
        if key in self.__dict__:
            raise ValueError(f'Attribute.addAttribut: {key=} bereits vohanden.')
        if type(key) == str:
            setattr(self, key, value)
        else:
            raise TypeError(f'Attribute.addAttribut: {key=} muss str sein.')
        
    def atts(self):
        """atts - Liefert eine Liste der Schlüssel (keys) der Attribute
        """
        Ergebnis = [k for k in self.__dict__]
        return Ergebnis
    
    def values(self):
        """values - Liefert eine Liste der Werte (values) der Attribute
        """
        return [v for v in self.__dict__.values()]
    
    def dict(self):
        """dict - Liefert die key/value-Paare als Dict
        """
        return self.__dict__

import logging, logging.handlers
logger = logging.getLogger()
def log_init(LogBaseName):
    ###   LogLevelDatei
      #       Dateiname der LogLevelDatei für das logging Modul
      #       Die letzte nicht leere und nicht auskommentierte Zeile bestimmt den LogLevel
      #       Erlaubt sind folgende Werte:
      #         CRITICAL
      #         ERROR
      #         WARNING
      #         INFO
      #         DEBUG
      #       Alle anderen Werte werden ignoriert
      #       Wenn die Datei nicht existiert oder ungültig ist, wird
      #       DEBUG als Default verwendet.
    LogLevelDatei = f'{LogBaseName}Logging.conf'
    ###   Log-Datei
    LogDatei = f'{LogBaseName}.log'
    ###   Log Formatter
    LogFormatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(module)s %(funcName)s Line: %(lineno)s %(message)s')
    ###   LogHandler
    # Erzeuge Handler
    LogHandler = logging.handlers.RotatingFileHandler(
        LogDatei,
        maxBytes = 10000000,
        backupCount = 3)
    # Formatter aktivieren
    LogHandler.setFormatter(LogFormatter)
    # Handler hinzufügen
    logger.addHandler(LogHandler)
    # LogLevelDatei suchen und auslesen, Ergebnis ggf. in LogLevel
        # Beachte: Der Eintrag in LogLevelDatei bzw. der in LogLevel gesetzte
        # Default wird ggf. durch die Kommandozeile überschrieben.
        # Vgl. ArgParse/start_aufgaben weiter unten.
    LogLevel = logging.DEBUG
    try:
        with open(LogLevelDatei, 'r') as Datei:
            LogText = 'LogLevel aus LogLevelDatei {} ist {}'
            for Zeile in Datei.readlines():
                ZS = Zeile.strip()
                logger.debug(LogText.format(LogLevelDatei, ZS))
                if ZS == 'CRITICAL':
                    LogLevel = logging.CRITICAL
                elif ZS == 'ERROR':
                    LogLevel = logging.ERROR
                elif ZS == 'WARNING':
                    LogLevel = logging.WARNING
                elif ZS == 'INFO':
                    LogLevel = logging.INFO
                elif ZS == 'DEBUG':
                    LogLevel = logging.DEBUG
    except FileNotFoundError:
        logger.info(
            'LogLevelDatei {} nicht gefunden. Setze LogLevel auf {}'.format(
                LogLevelDatei, LogLevel
        ))
    except Exception as e:
        logger.warning(
            'LogLevelDatei Fehler: {}. Setze LogLevel auf {}'.format(e, LogLevel))
    logger.setLevel(LogLevel)

@contextlib.contextmanager
def tempDir(path):
    """tempDir - Contextmanager: wechselt vorübergehend in anderes Verzeichnis
    
    Parameter
        path    Pfad, in das vorübergehend gewechselt wird.
                absolut oder relativ
    """
    AktVerz = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(AktVerz)

class FilePublisher():
    """FilePublisher - Baut Klasse zum Veröffentlichen von Dateien
    
        FilePublisher soll später über verschiedene Kanäle veröffentlichen können.
        Das kann sein:
            cp        Ganz normales cp innerhalb des Dateisystems
            rclone    Alles, was mit rclone möglich ist, insb. auf Cloud Speicher
            rsync     Könnte später noch implementiert werden
        
        FilePublisher wird instanziiert, anschließend werden nach Bedarf
        einzelne Publisher in der Instanz angelegt.
        
        Publisher sind später einfache Dicts, die die nötigen Parameter enthalten:
            'name'        Frei wählbarer Name
            'art'         String, der die Art des Publishers verrät, also
                          'cp'
                          'rclone'
                          'rsync'
                          usw.
            'command'     Auszuführendes Kommando mit zwei {} für Quelle und Ziel
            weitere       Können zu Debugging Zwecken gespeichert werden
        
        Die Methode publish löst dann die tatsächliche Veröffentlichung aus.
        Dabei werden alle Publisher der Liste self._publisher abgearbeitet.
        
        Aufgerufen wird das Ganze am Ende mit:
            fp.publish(file_name, target_rel_path, target_name)
            
            Dabei ist
                file_name         Datei, die veröffentlicht werden soll.
                                  Einfacher Dateiname oder relativer oder absoluter
                                  Pfad sind als Angaben möglich.
                target_rel_path   Relativer Pfad, der an den target_base_path des
                                  jeweiligen Publishers gehängt wird
                                  Bsp.: gem_maerchenland/DB/
                target_name       Optional, falls die Zieldatei einen anderen Namen
                                  haben soll als die Quelldatei.
                                  Hier ist kein Pfad erlaubt (also darf target_name
                                  kein / enthalten)
        
        Mehtoden
            add_cp        Fügt cp-Publisher hinzu
            add_rclone    Fügt rclone-Publisher hinzu
            
            publish       Geht alle vorhandenen Publisher durch
    """
    def __init__(self):
        self._publisher = []
    
    def __str__(self):
        return ' - '.join([p['command'] for p in self._publisher])
    
    def add_cp(self, name, target_base_path='./'):
        """add_cp - fügt einen cp-Publisher hinzu
        
            Parameter
                name                Frei wählbarer Name für diesen Publisher
                target_base_path    Pfad am Ziel, an den später der relative Pfad
                                    angehängt wird.
                                    Bsp.: /somewhere/at/the/target/
                                          ../Download/
                                    Default: ./ (aktuelles Verzeichnis)
        """
        # Sicherstellen, dass target_base_path mit / endet:
        if target_base_path.endswith('/'):
            tbp = target_base_path
        else:
            tbp = target_base_path + '/'
        # Späteres System Kommando zusammenstellen
        cmd = 'cp {} ' + tbp + '{}'
        # Publisher herstellen
        cp_publisher = {
            'name': name,
            'art': 'cp',
            'target_base_path': tbp,
            'command': cmd,
            }
        # Publisher an Liste anhängen
        self._publisher.append(cp_publisher)
    
    def add_rclone(self, name, rclone_target):
        """add_rclone - fügt einen rclone-Publisher hinzu
        
            Parameter
                name            Frei wählbarer Name für diesen Publisher
                rclone_target   Name der rclone Konfiguration (vergeben bei rclone config)
                                Bsp.: nc_cg
        """
        # Späteres Kommando zusammenstellen
        cmd = 'rclone -q copyto {} ' + rclone_target + ':{}'
        # Publisher herstellen
        rclone_publisher = {
            'name': name,
            'art': 'rclone',
            'rclone_target': rclone_target,
            'command': cmd,
            }
        # Publisher an Liste anhängen
        self._publisher.append(rclone_publisher)
    
    def publish(self, file_name, target_rel_path='./', target_name=''):
        """publish -
        """
        # Sicherstellen, dass target_rel_path mit / endet:
        if target_rel_path.endswith('/'):
            trp = target_rel_path
        else:
            trp = target_rel_path + '/'
        # Sicherstellen, dass trp nicht mit / beginnt
        trp = trp.lstrip('/')
        # Ziel je nach target_name zusammensetzen
        if target_name:
            target = trp + target_name
        else:
            target = trp + os.path.basename(file_name)
        # tatsächlich ausführen
        for publisher in self._publisher:
            if publisher['art'] == 'cp':
                # Kommando zusammensetzen
                cmd = publisher['command'].format(file_name, target)
                # tatsächlich ausführen
                logger.debug(f'Kommando für subprocess: {cmd}')
                Ergebnis = subprocess.run(cmd.split())
                logger.debug(f'Returncode: {Ergebnis.returncode}')
            elif publisher['art'] == 'rclone':
                # Kommando zusammensetzen
                cmd = publisher['command'].format(file_name, target)
                # tatsächlich ausführen
                logger.debug(f'Kommando für subprocess: {cmd}')
                Ergebnis = subprocess.run(cmd.split())
                logger.debug(f'Returncode: {Ergebnis.returncode}')
    
  