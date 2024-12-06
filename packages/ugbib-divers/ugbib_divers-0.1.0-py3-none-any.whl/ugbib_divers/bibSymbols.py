#!/usr/bin/env python3

class Symbols():
    
    _SymbolDicts = {
        ###
        ###  Verschiedene Varianten
        ###
        # Variante Standard
        'Standard': {
            # Nach Namen/Aussehen (was sie zeigen)
            'copyright'     : chr(0xA9),
            'haus'          : chr(0x2302),      # Haus
            'lemniskate'    : chr(0x221E),      # Liegende 8
            'pfeil_dlx'     : chr(0x21CD),      # Pfeil doppelt links durchgestrichen
            'pfeil_drlx'    : chr(0x21CE),      # Pfeil doppelt links rechts durchgestrichen
            'pfeil_drx'     : chr(0x21CF),      # Pfeil doppelt rechts durchgestrichen
            'pfeil_dl'      : chr(0x21D0),      # Pfeil doppelt links
            'pfeil_do'      : chr(0x21D1),      # Pfeil doppelt oben
            'pfeil_dr'      : chr(0x21D2),      # Pfeil doppelt rechts
            'pfeil_du'      : chr(0x21D3),      # Pfeil doppelt unten
            'pfeil_drl'     : chr(0x21D4),      # Pfeil doppelt rechts links
            'pfeil_dou'     : chr(0x21D5),      # Pfeil doppelt oben unten
            'pfeil_dnw'     : chr(0x21D6),      # Pfeil doppelt nord-west
            'pfeil_dno'     : chr(0x21D7),      # Pfeil doppelt nord-ost
            'pfeil_dso'     : chr(0x21D8),      # Pfeil doppelt süd-ost
            'pfeil_dsw'     : chr(0x21D9),      # Pfeil doppelt süd-west
            'pfeil_l'       : chr(0x2190),      # Pfeil links
            'pfeil_o'       : chr(0x2191),      # Pfeil oben
            'pfeil_r'       : chr(0x2192),      # Pfeil rechts
            'pfeil_u'       : chr(0X2193),      # Pfeil unten
            'pfeil_lx'      : chr(0x219A),      # Pfeil links durchgestrichen
            'pfeil_rx'      : chr(0x219B),      # Pfeil rechts durchgestrichen
            'pfeil_kr'      : chr(0x21BB),      # Pfeil kreisförmig rechts
            'pfeil_kl'      : chr(0x21BA),      # Pfeil kreisförmig links
            'pfeil_rl'      : chr(0x21C4),      # Pfeil rechts Pfeil links
            'pfeil_lr'      : chr(0x21C6),      # Pfeil links Pfeil rechts
            'pfeil_ou'      : chr(0x21C5),      # Pfeil oben Pfeil unten
            'pfeil_ll'      : chr(0x21C7),      # Pfeil links Pfeil links
            'pfeil_oo'      : chr(0x21C8),      # Pfeil oben Pfeil oben
            'pfeil_rr'      : chr(0x21C9),      # Pfeil rechts Pfeil rechts
            'pfeil_uu'      : chr(0x21CA),      # Pfeil unten Pfeil unten
            'recycle'       : chr(0x267A),      # Dreieckiges und dreiteiliges Recycling Symbol
            'sanduhr'       : chr(0x231B),      # Sanduhr
            'sanduhr_l'     : chr(0x23F3),      # Sanduhr laufend
            'schluessel_q'  : chr(0x26BF),      # Schlüssel im Quadrat
            'telefon'       : chr(0x260F),      # Telefon
            'unendlich'     : chr(0x221E),      # Liegende 8
            'wecker'        : chr(0x23F0),      # Wecker
            # Fach Funktion (was sie symbolisieren)
            'alarm'         : chr(0x23F0),      # Roter Wecker
            'birth'         : '*',              # Geburtstag (Stern)
            'busy'          : chr(0x23F3),      # Sanduhr laufend
            'check'         : chr(0x2713),      # Haken
            'connect'       : chr(0x21C4),      # Pfeil rechts/links
            'copy'          : chr(0x2750),      # Original und Kopie
            'cut'           : chr(0x2700),      # Schere
            'death'         : chr(0x2020),      # Sterbedatum (Kreuz)
            'delete'        : chr(0x2BBD),      # Box mit Kreuz
            'disconnect'    : chr(0x21F9),      # Pfeil durchgestrichen rechts/links
            'down'          : chr(0x23F7),      # Dreieck Spitze unten
            'edit'          : chr(0x270E),      # Bleistift
            'emptyform'     : chr(0x1F5CB),     # Leeres Dukument
            'erase_l'       : chr(0x232B),      # Erase nach links
            'erase_r'       : chr(0x2326),      # Erase nach rechts
            'exit'          : chr(0x274C),      # Rotes liegendes Kreuz
            'haken'         : chr(0x2713),
            'home'          : chr(0x2302),      # Haus
            'next'          : chr(0x23F5),      # Dreieck Spitze rechts
            'night'         : chr(0x23FE),      # Mond
            'no_entry'      : chr(0x26D4),      # "Verkehrsschild": keine Einfahrt, Einbahnstraße
            'observe'       : chr(0x23FF),      # Auge beobachtend
            'power'         : chr(0x23FB),
            'previous'      : chr(0x23F4),      # Dreieck Spitze links
            'redo'          : chr(0x21BB),      # Kreisförmiger Pfeil rechtsrum
            'refresh'       : chr(0x21BA),      # Kreisförmiger Pfeil linksrum
            'save'          : chr(0x1F5AB),     # Floppy Disk
            'search'        : chr(0x1F50D),     # Lupe
            'sleep'         : chr(0x23FE),      # Mond
            'undo'          : chr(0x21BA),      # Kreisförmiger Pfeil linksrum
            'up'            : chr(0x23F6),      # Dreieck Spitze oben
            'warning'       : chr(0x26A0),      # Dreieckiges Warnschild
            },
        'Buchstaben': {
            'check'         : 'c',
            'copyright'     : 'C',
            'delete'        : 'd',
            'exit'          : 'x',
            'refresh'       : 'R',
            'save'          : 'S',
            'undo'          : 'u',
            },
        'WeissAufBlau': {
            # Nach Namen/Aussehen (was sie zeigen)
            'pfeil_rl'      : chr(0x2194),
            'pfeil_ou'      : chr(0x2195),
            'pfeil_nw'      : chr(0x2196),
            'pfeil_no'      : chr(0x2197),
            'pfeil_so'      : chr(0x2198),
            'pfeil_sw'      : chr(0x2199),
            # Nach Funktion (was sie symbolisieren)
            'fast_back'     : chr(0x23EA),
            'fast_down'     : chr(0x23EC),
            'fast_forward'  : chr(0x23E9),
            'fast_up'       : chr(0x23EB),
            'eject'         : chr(0x23CF),
            'first'         : chr(0x23EE),
            'last'          : chr(0x23ED),
            'pause'         : chr(0x23F8),
            'start'         : chr(0x23FA),
            'stop'          : chr(0x23F9),
            },
        }
    
    def __init__(self, Variante = 'Standard'):
        self._Variante = Variante
        for attr in self._SymbolDicts[Variante]:
            setattr(self, attr, self._SymbolDicts[Variante][attr])
    
    def __str__(self):
        return 'Variante: {}'.format(self._Variante)
    
    @classmethod
    def Varianten(cls):
        for variante in cls._SymbolDicts:
            yield variante
    
    @classmethod
    def Unterschiede(cls):
        logfilename = 'Symbols.log'
        print(f'\nUnterschiede siehe {logfilename}')
        with open('Symbols.log', 'w') as logfile:
            for variante_links in cls.Varianten():
                SymLinks = cls(variante_links)
                for variante_rechts in cls.Varianten():
                    # wir vergleichen eine Variante nicht mit sich selbst
                    if variante_rechts != variante_links:
                        SymRechts = cls(variante_rechts)
                        logfile.write('Wir vergleichen die Varianten {} und {}\n'.format(
                                  SymLinks, SymRechts))
                        for attribut in SymLinks.__dict__:
                            if not attribut in SymRechts.__dict__:
                                logfile.write('--> {} fehlt in {}\n'.format(attribut, SymRechts))

if __name__ == '__main__':
    for variante in Symbols.Varianten():
        print('###############################################################')
        print('###   Variante: {}'.format(variante))
        print('###############################################################')
        Sym = Symbols(variante)
        for attribut in Sym.__dict__:
            print('{} - {}'.format(getattr(Sym, attribut), attribut))
    print('###\n###   Vergleiche\n###')
    Symbols.Unterschiede()
