"""bibGlobal - Implementiert Klasse für globale Variablen u.ä.

    Zu Testzwecke ergänzt
"""

class glb():
    """glb - Klasse, deren Klassen-Attribute für globale Inhalte genutzt werden können
    
        Diese Klasse wird nicht instanziiert, die Attribute werden immer nur über die
        Klasse selbst referenziert.
        
        Typische Anwendung ist eine Datenbank-Konnektor, also z.B.
            glb.DB = sqlite3.connect('filename.db')
            Cur = glb.DB.cursor()
            Cur.execute('...')
            Cur.close
        
        Attribute von glb können direkt erzeugt werden:
            glb.hallo = 'Guten Tag'
        
        In diesem Fall wird nicht geprüft, ob es dieses Attribut bereits gibt, es wird
        ggf. einfach überschrieben.
        
        Sicherer ist es, ein Attribut mit der Staticmethod setup zu erzeugen, dabei kann
        optional der Wert des Attributes mitgegeben werden:
            glb.setup('hallo', 'Guten Tag')
        
        In diesem Fall wird, falls das Attribut schon existiert, ein ValueError geworfen.
        
        Ähnlich ist es mit dem neuen Sezten eines Wertes und mit dem Löschen von
        Attributen. Das kann unmittelbar oder mit den Staticmethods setvalue und delete
        erledigt werden.
        
        Static Methods
            setup     Einrichten eines neuen Klassen-Attributes
            setvalue  Setzen eines Wertes für ein Klassen-Attribut
            delete    Löschen eines Klassen-Attributes
    """
    
    @staticmethod
    def setup(attribut, value=None, force=False):
        """setup - Richtet ein neues Klassenattribut ein
            
            Richtet ein neues Klassenattribut ein.
            
            Falls force False (default), wird geprüft, ob das Attribut
            bereits vorhanden ist; in diesem Fall wird eine Exception (ValueError)
            geworfen. Diese Prüfung kann übergangen werden, indem force auf True
            gesetzt wird.
            
            Optional kann das Attribut einen Wert erhalten. Ansonsten erhält es None
            als Wert.
        
            Parameter
                attribut    Name des neuen Klassenattributes
                            Typ: str
                value       Wert, auf den das neue Klassenattribut gesetzt wird
                            Typ: beliebig
                            Optional
                            Default: None
                force       True: Das Klassenattribut wird auch dann neu
                                  eingerichtet (und damit auf value gesetzt),
                                  wenn es bereits vohanden ist.
            
            Exceptions
                ValueError    Wird geworfen, wenn das neue Attribut bereits
                              vorhanden ist und nicht force True ist.
        """
        if not force and attribut in dir(__class__):
            raise ValueError(f'bibGlobal.glb.setup: Attribut {attribut} existiert bereits.')
        else:
            setattr(__class__, attribut, value)
    
    @staticmethod
    def setvalue(attribut, value):
        """setvalue - Setzt den Wert eines Attributes neu
            
            Setzt den Wert eines Attributes neu. Dabei wird geprüft, ob es das Attribut
            gibt. Falls nicht, wird eine Exception (AttributeError) geworfen.
            
            Parameter
                attribut    Name des Attributes, dessen Wert neu gesetzt werden soll
                            Typ: str
                value       Wert, auf den das Attribut gesetzt werden soll
                            Typ: beliebig
            
            Exceptions
                AttributeError    Wird geworfen, wenn es das Attribut nicht gibt.
        """
        if attribut not in dir(__class__):
            raise AttributeError(f'bibGlobal.glb.setvalue: Attribut {attribut} existiert nicht.')
        else:
            setattr(__class__, attribut, value)
    
    @staticmethod
    def delete(attribut):
        """delete - Löscht ein vorhandenes Attribut
        
            Löscht ein vorhandenes Attribut. Ist das Attribut nicht vorhanden, wird
            eine Exception (AttributeError) geworfen.
            
            Parameter
                attribut    Zu löschendes Attribut
                            Typ: str
            
            Exception
                AttributeError    Wird geworfen, wenn es das Attribut nicht gibt.
        """
        if attribut not in dir(__class__):
            raise AttributeError(f'bibGlobal.glb.delete: Attribut {attribut} existiert nicht.')
        else:
            delattr(__class__, attribut)
