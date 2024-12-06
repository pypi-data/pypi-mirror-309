""" bibForm - Implementiert Formulare u.a. für TkInter

    
"""

#####################################################################
###   Logger herstellen
#####################################################################
import logging, logging.handlers
logger = logging.getLogger()

from ugbib_werkzeug.bibWerkzeug import checkPythonName

from decimal import Decimal
import datetime
from collections import OrderedDict
import os, sys

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

from PIL import Image, ImageTk

#
# Format Strings für Typumwandlung von date, datetime und time
#
FORMATS_TIME = ('%H:%M',)
FORMATS_DATE = ('%d.%m.%Y', '%Y-%m-%d')
FORMATS_DATETIME = ('%Y-%m-%d %H:%M',)

#
# TRUES, TRUES_SHORT, FALSE - Liste zulässiger String Werte für True.
#
    #         Kleinschreibung reicht, letztlich wird nur der erste Buchstabe
    #         in Kleinschreibung verglichen. Siehe getValue -> Entry -> bool
    #
    #         Wichtig: Das erste Element wird verwendet für die Typumwandlung
    #                  von value --> String
TRUES = [
    'ja',
    'x',
    'yes',
    'true',
    'wahr'
    ]
TRUES_SHORT = [s[0] for s in TRUES]
FALSE = 'nein'

ICONS_DIR = './icons/'

class ListboxValueLabel(tk.Listbox):
    """ListboxValueLabel - Erweitert Listbox um unabhängige Value/Label-Paare
    
        tk.Listbox hält immer eine Liste von String-Werten, aus denen ausgewählt
        werden kann. Wir möchten aber Value/Label-Paare bearbeiten, d.h. z.B.
        
            Value   Label
            =======+===============
            m      | männlich
            w      | weiblich
            d      | divers
            ?      | nicht angegeben
        
        In der ListboxValueLabel sollen die Label angezeigt werden, als Wert soll
        der zugehörige Value herausgegeben werden.
        
        Die Funktionalität von Listbox soll ansonsten erhalten bleiben.
        
        Über selectmode kann eingestellt werden, ob ein Wert oder mehrere
        Werte ausgewählt werden können. Zwei Methoden liefern entsprechend
        sinnvolle Ergebnisse:
            getValues   Liefert eine Liste der ausgewählten Werte
            getValue    Liefert den ersten ausgewählten Wert oder None,
                        wenn kein Wert ausgewählt ist.
                        Das ist v.a. (und wohl nur) dann sinnvoll,
                        wenn nur ein Wert ausgewählt werden darf.
        
        Parameter
            Wie tk.Listbox, wird ohne weitere Verarbeitung direkt weiter
            gereicht.
        
        Attribute
            _lv     Dict Label --> Value
                    Bildet Label auf Value ab. Das mag verwirrend erscheinen.
                    Wir können aber annehmen, dass die Label eindeutig sind.
                    Und über den Index ist später der Label leicht zugänglich,
                    s.d. über das Dict _lv der Value ermittel werden kann.
    """
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lv = OrderedDict()
    
    def clear(self):
        """clear - Löscht die Auswahlliste
        """
        self.delete(0, tk.END)
        while self._lv:
            self._lv.popitem()
    
    def append(self, value, label=None):
        """append - Hängt ein value/label Paar ans Ende der Auswahlliste an
        """
        if label:
            l = label
        else:
            l = str(value).capitalize()
        if l in self._lv:
            raise ValueError(f'Label {l} nicht eindeutig.')
        self.insert(tk.END, l)
        self._lv[l] = value
    
    def clearValue(self):
        """clearValue - Alle Elemente werden abgewählt
        """
        self.selection_clear(0, tk.END)
    
    def setValues(self, values):
        """setValues - Wählt genau die Werte aus values in der Liste aus
        
            setValues wählt genau die Werte aus values in der Liste aus.
        
            Parameter
                values    Tupel oder Liste von Werten
        """
        if not type(values) in (tuple, list):
            raise TypeError('values muss tuple oder list sein, ist aber {}'.type(values))
        self.clearValue()
        for value in values:
            self.setValue(value, exclusive=False)
    
    def setValue(self, value, exclusive=False):
        """setValue - Wählt value in der Liste aus (select)
        
            Parameter
                value       Dieser Wert wird ausgewählt
                            Typ: Typ des Widgets
                exclusive   Wenn True, werden alle anderen Auswahlen gelöscht.
                            Andernfalls bleiben alle anderen Auswahlen unverändert.
        """
        if value is None:
            self.clearValue()
            return
        if exclusive:
            self.clearValue()
        index = 0
        for label in self._lv.keys():
            if self._lv[label] == value:
                self.selection_set(index)
            index += 1
    
    def getValues(self):
        """getValues - Liefert Liste der ausgewählten Werte
        """
        return [self._lv[self.get(index)] for index in self.curselection()]
    
    def getValue(self):
        """getValue - Liefert den ersten der ausgewählten Werte
        
            Das ist v.a. dann hilfreich, wenn nur ein Wert ausgewählt werden
            darf.
        """
        values = self.getValues()
        if len(values) > 0:
            return values[0]
        else:
            return None

class FrameScrolledListbox(ttk.Frame):
    """FrameScrolledListbox - Frame mit enthaltener Listbox
    
        Frame, der eine einfache tk.Listbox enthält. Außerdem einen Scrollbalken.
        Als Werte kommen hier nur Strings infrage.
        
        Argumente
            wie tk.Listbox
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # build Control Variable
        self.listvariable = tk.StringVar()
        self.listvariable.set('')
        # build Listbox and Scrollbar
        self.Listbox = tk.Listbox(self, listvariable=self.listvariable)
        self.Scrollbar = ttk.Scrollbar(self)
        # configure these two
        self.Listbox.config(yscrollcommand=self.Scrollbar.set)
        self.Scrollbar.config(command=self.Listbox.yview)
        # pack them in Frame
        self.Listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.Scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
    
    def clear(self):
        """clear - Löscht die Auswahlliste
        """
        self.Listbox.delect(0, tk.END)
    
    def append(self, value):
        """append - Hängt einen Value ans Ende der Auswahlliste
        """
        if not type(value) == str:
            raise TypeError(f'Value muss Type str haben hat aber {type(value)}.')
        self.Listbox.insert(tk.END, value)
    
    def clearValue(self):
        """clearValue - Alle Elemente werden abgewählt
        """
        self.Listbox.selection_clear(0, tk.END)
    
    def setValues(self, values):
        """setValues - Wählt venau die Werte aus values in der Liste aus
        
            Parameter
                values    Tupel oder Liste von Werten (str)
        """
        if not type(values) in (tuple, list):
            raise TypeError('values muss tuple oder list sein, ist aber {}'.type(values))
        self.clearValue()
        for value in values:
            if not type(value) == str:
                raise TypeError(f'Value muss Type str haben hat aber {type(value)}.')
            self.setValue(value, exclusive=False)
    
    def setValue(self, value, exclusive=False):
        """setValue - Wählt value in der Liste aus (select)
        
            Parameter
                value       Dieser Wert wird ausgewählt
                            Typ: String oder None
                exclusive   Wenn True, werden alle anderen Auswahlen gelöscht.
                            Andernfalls bleiben alle anderen Auswahlen unverändert.
        """
        if type(value) in (list, tuple):
            self.setValues(value)
            return
        if value is None:
            self.clearValue()
            return
        if exclusive:
            self.clearValue()
        values = self.Listbox.get(0, tk.END)
        if not value in values:
            raise ValueError(f'{value=} ist nicht in der Auswahlliste.')
        index = values.index(value)
        self.Listbox.selection_set(index)
    
    def getValues(self):
        """getValues - Liefert Liste der ausgewählten Werte
        """
        return [self.Listbox.get(index) for index in self.Listbox.curselection()]
    
    def getValue(self):
        """getValue - Liefert den ersten der ausgewählten Werte
        
            Das ist v.a. dann hilfreich, wenn nur ein Wert ausgewählt werden
            darf.
        """
        values = self.getValues()
        if len(values) > 0:
            return values[0]
        else:
            return None

class FrameScrolledListboxValueLabel(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #
        # build Listbox and Scrollbar
        self.Listbox = ListboxValueLabel(self)
        self.Scrollbar = ttk.Scrollbar(self)
        #
        # configure these two
        self.Listbox.config(yscrollcommand=self.Scrollbar.set)
        self.Scrollbar.config(command=self.Listbox.yview)
        #
        # pack them in Frame
        self.Listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.Scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
    
    def clear(self):
        self.Listbox.clear()
    
    def append(self, value, label=None):
        self.Listbox.append(value=value, label=label)
    
    def clearValue(self):
        self.Listbox.clearValue()
    
    def setValues(self, values):
        if not type(values) in (tuple, list):
            raise TypeError('values muss tuple oder list sein, ist aber {}'.type(values))
        self.clearValue()
        for value in values:
            self.Listbox.setValue(value=value, exclusive=False)
    
    def setValue(self, value, exclusive=False):
        self.Listbox.setValue(value=value, exclusive=exclusive)
    
    def getValues(self):
        return self.Listbox.getValues()
    
    def getValue(self):
        return self.Listbox.getValue()

class Validator():
    """Validator - Implementiert Validatoren für TkInter und Factories für Validatoren
    
        Validator wird nicht instanziiert. Stattdessen werden die benötigten
        Klassenmethoden in der TkInter Anwendung als Validatoren registriert
        und über den dort zurückgegebenen Namen referenziert.
        
        Vgl. Doku von TkInter, z.B.
        https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/entry-validation.html
        
        Beachte insb., dass Validatoren immer an Entry bzw. Combobox Widgets
        gehängt werden. D.h. das Argument für die Validatoren ist immer str.
        Soll also z.B. eine Typenprüfung durchgeführt werden, wirt tatsächlich
        geprüft, ob sich der übergebene String in diesen Typen konvertieren
        lässt.
        
        Bsp.:
            import Validator as V
            valInt = widget.register(V.valInt)
            Entry(widget, validate='all', validatecommand=(valInt, '%P'))
        
        Alle Validatoren akzeptieren jeweils einen String Wert value,
        der geprüft wird.
        
        Alle Validatoren liefern True für value == ''. Wie letztlich ''
        interpretiert wird (None oder leerer String), und ob ggf. None
        zulässig ist, muss an anderer Stelle geklärt werden, i.d.R. beim
        Abspeichern in die DB.
        
        Factories für Validatoren
        =========================
        
        Neben den eigentlichen Validatoren werden auch drei Factories für
        Validatoren implementiert. Zwei davon verknüpfen beliebig viele Validatoren
        per and bzw. or. Die Dritte negiert einen Validator.
        So können z.B. die Validatoren valInt
        und valPositiv zu valPositivInt kombiniert werden.
        
        Diese Factories können nicht nur die hier bereitgestellten Validatoren
        kombinieren, sondern auch andere Funktionen, die z.B. von der Anwendung
        bereitgestellt werden. Denkbar wäre die Prüfung, ob ein value ein 
        Datum ist (valDate) und ob es innerhalb eines bestimmten Zeitraums liegt
    """
    def valInt(value):
        """valInt - True <-> int(value) erfolgreich oder value == ''
        """
        if value == '':
            return True
        try:
            int(value)
        except:
            return False
        return True
    
    def valFloat(value):
        """valFloat - True <-> float(value) erfolgreich oder value == ''
        """
        if value == '':
            return True
        try:
            float(value)
        except:
            return False
        return True

    def valDecimal(value):
        """valDecimal - True <-> Decimal(value) erfolgreich oder value == ''
        
            Anmerkung
                baut auf decimal.Decimal auf
        """
        if value == '':
            return True
        try:
            Decimal(value)
        except:
            return False
        return True
    
    def valBool(value):
        """valBool - True <--> value[0] in TRUES_SHORT
        """
        if value == '':
            return True
        else:
            return value[0].lower() in TRUES_SHORT
    
    def valDate(value):
        """valDate - True <--> value gültiges Datum oder leer
        """
        if value == '':
            return True
        for formatString in FORMATS_DATE:
            try:
                datetime.datetime.strptime(value, formatString)
                return True
            except:
                pass
        return False

    def valDatetime(value):
        """valDatetime - True <--> value gültiges Datum+Zeit oder leer
        """
        if value == '':
            return True
        for formatString in FORMATS_DATETIME:
            try:
                datetime.datetime.strptime(value, formatString)
                return True
            except:
                pass
        return False

    def valTime(value):
        """valTime - True <--> value gültige Zeit oder leer
        """
        if value == '':
            return True
        for formatString in FORMATS_TIME:
            try:
                datetime.datetime.strptime(value, formatString)
                return True
            except:
                pass
        return False
    
    def valFactoryAnd(*vals):
        """valFactoryAnd - Verknüpft Validatoren mit and
        
            ValFactoryAnd kombiniert eine Reihe von Validatoren und liefert
            einen neuen Validator, der genau dann True liefert, wenn alle
            übergebenen Validatoren True liefern.
            
            Dabei werden die übergebenen Validatoren in deren Reihenfolge
            aufgerufen. Diese Prüfung wird abgebrochen, nachdem die erste
            Prüfung False ergibt.
            
            Damit können Validatoren aufgebaut werden, die z.B. zuerst eine
            Typenprüfung vornehmen und anschließend noch Wertebereiche.
            Bsp.: valNumPositiv prüft erst, ob der Wert numerisch ist und
                  anschließend, ob er auch positiv ist.
        """
        
        def validator(x):
            for f in vals:
                if not f(x):
                    return False
            return True
        
        return validator
    
    def valFactoryOr(*vals):
        """valFactoryAnd - Verknüpft Validatoren mit aor
        
            ValFactoryAnd kombiniert eine Reihe von Validatoren und liefert
            einen neuen Validator, der genau dann True liefert, wenn mindestens
            einer der übergebenen Validatoren True liefert.
            
            Dabei werden die übergebenen Validatoren in deren Reihenfolge
            aufgerufen. Diese Prüfung wird abgebrochen, nachdem die erste
            Prüfung True ergibt.
        """
        
        def validator(x):
            for f in vals:
                if f(x):
                    return True
            return False
        
        return validator
    
    def valFactoryNot(val):
        """valFactoryNot - Liefert negierten Validator
        """
        
        def validator(x):
            return not val(x)
        
        return validator
    
    valNum = valFactoryOr(valInt, valFloat, valDecimal)
    valPositiv = valFactoryAnd(valNum, lambda x: float(x)>0)
    

class Form():
    """Form - Basisklasse für Formulare
    
    
        =======================================================================
        Grundsätzliches
        =======================================================================
        
        1. Formulare, also Instanzen von Ableitungen von Form, sind im
        Wesentlichen Sammlungen von TkInter Widgets oder selbst gebauten Widgets.
        Diese Sammlung von Widgets werden die Attribute der Instanz sein.
        Selbst gebaute Widgets können z.B. Listen von Checkbuttons innerhalb
        eines tk.Text Widgets, oder ein ergänztes tk.Listbox Widget.
        
        2. Jedes dieser Widgets gehört in aller Regel zu einer Spalte
        einer DB-Tabelle. Selbst wenn das nicht so ist, hat in aller Regel
        jedes Widget genau einen Wert, ist also kein zusammengesetztes Widget
        mit z.B. mehreren Entry Widgets.
        
        3. a) Zu jedem Widget wird ein passendes Label-Widget erzeugt. Optional
        kann dieses Label-Widget bereits beim Hinzufügen des Widgets
        fertig mitgegeben werden.
        
        
        =======================================================================
        Namenskonventionen
        =======================================================================
        
        Damit die Sachen am Ende auseinanderzuhalten sind, gilt folgende
        Namenskonvention für Attribute der Instanzen:
            
            Widtets             Wie Spalte in der DB-Tabelle
                                Falls unabhängig von einer DB-Tabelle, dann
                                frei wählbar, allerdings ohne Unterstrich
                                am Anfang.
                                In keinem Fall darf das Abbtribut mit
                                lbl_ beginnen (vgl. Label-Widgets)
                                Bsp.: self.id         Zu Spalte .. in DB-Tabelle
                                      self.name       "
                                      self.plz        "
                                      self.username   Ohne Bezug auf DB-Tabelle
            Label-Widgets       Beginnt immer mit lbl_, dann folgt das
                                Attribut des zugehörigen Widgets.
                                Bsp.: self.lbl_id
                                      self.lbl_name
                                      self.lbl_plz
                                Daher dürfen die Widget-Attribute nicht mit
                                lbl_ beginnen.
            Weitere Attribute   Alle weiteren Attribute beginnen mit
                                (mindestens) einem Unterstrich.
                                Bsp.: _id       ID des Formulars
                                      _typ      Dict für Typen der Widgets
                                      _navi     Navi für das Formular
        
        Die gleiche Namenskonvention soll ggf. für Properties gelten. Tatsächlich
        sollten alle Properties mit einem Unterstrich beginnen, da Properties
        nach den obigen Regeln weder Widgets noch Label-Widgets halten werden.
        
        Generell sollten Methoden mit einem Kleinbuchstaben beginnen und
        mindestens einen Großbuchstaben enthalten, z.B. addWidget, getWidgets usw.
        Da meine Datenbanken durchgehend Spaltenbezeichnungen aus Kleinbuchstaben
        und Unterstrichen enthalten (by the way: PostgreSQL keywords und namen sind
        case-insensitiv), werden so Namenskonflikte vermieden.
        
        Diese Namenskonvention ermöglicht es u.a.,
            1. die Liste der Widgets zu liefern,
            2. die Liste der Label-Widgets zu liefern,
            3. die Label-Widgets und Widgets
               eindeutig einander zuzuordnen.
        
        
        =======================================================================
        Bearbeitung der Widgets/Attribute
        =======================================================================
        
        Die Widgets und Label-Widgets, also die "normalen"
        Attribute, werden
        ausschließlich durch Methoden hinzugefügt. Späteres Überschreiben
        oder Hinzufügen eines Widgets mit einem schon verwendeten Namen
        ist nicht erlaubt.
        
        
        =======================================================================
        Label-Widgets zu den Widgets
        =======================================================================
        
        Zu jedem Widget, dass hinzugefügt wird, wird automatisch ein
        Label-Widget erzeugt und hinzugefügt. Dieses Label-Widget kann optional
        auch vorher erzeugt und beim Hinzufügen des Widgets mitgegeben werden.
        
        
        =======================================================================
        Schnittstelle zu den Widgets
        =======================================================================
        
        Eine einheitliche Schnittstelle für die Werte der Widgets
        wird über Methoden wie den folgenden hergestellt:
            getValue(colName)
            setValue(colName, value)
            clearValue(colName)
        Diese Methoden müssen
            1. selbst erkennen, um welche Art von Widget es sich handelt
               (TkInter Entry, Listbox usw.)
            2. je nach Typ (_typ) des Widgets/Feldes die Typenkonvertierung
               vornehmen.
        
        
        =======================================================================
        Implementierung als Kontext-Manager
        =======================================================================
        
        Wir implementieren Form als Kontext-Manager. Das machen wir
        eigentlich nur, um bei der Verwendung eine bessere Lesbarkeit zu
        erreichen. Der Aufruf kann so erfolgen:
            
            with Form(...) as Form_Person:
                ...
            with Form(...) as Form_Familie:
                ...
        
        Üblicherweise sind die Definitionen, die dann innerhalb des Kontextes
        auftauchen, sehr zahlreich. Dass das als Kontext möglich ist, erlaubt
        die Einrückung im Editor.
        
        Tatsächlich macht der Kontext-Manager nichts (vgl. __enter__ und
        __exit__). Das macht einen einfachen Aufruf möglich, ohne
        Funktionalität einzubüßen. Später könnten in __enter__ und/oder
        __exit__ relevante Dinge definiert werden.
        
        
        =======================================================================
        Auflistung der Eigenschaften
        =======================================================================
        
        Parameter
            bisher keine
        
        Klassen-Attribute
            TYPES           Liste der zulässigen Typen der Widget-Werte
                            z.B. ['text', 'int', ...]
        
        Attribute
            _navi           Ggf. Navi für das Formular (vgl. Klasse Navi)
            _types          Dict mit Zuordnungen colName: typ
            _colNames       List aller colName, also damit auch 
                            Widget-Namen (maßgebliche Reihenfolge)
            _getterAuswahl  Dict colName -> getterAuswahl
        
        Methoden
            __enter__           Für den Kontext-Manager
            __exit__            "
            addWidget           Fügt ein Widget hinzu
            colType             Liefert type vom einem Widget
            getValue            Liefert value des Widgets, aber mit konvertiertem Type
            setValue            Setzt value des Widgets, aber aus konvertiertem Type
            clearValue          Löscht value des Widgets, d.h. setzt value = ''
            getValues           Liefert Dict der Werte aller Widgets
            setValues           Setzt die Werte aller Widgets
            clearValues         Löscht values aller Widgets
            setGetterAuswahl    setzt GetterAuswahl für ein Widget. Diese Getter
                                sind dafür gedacht, später Auswahlen für
                                Select o.a. Widgets zu liefern.
    """
    #
    # Klassen-Attribute
    #
    
    # TYPES - Liste zulässiger Typen der Widgets
    TYPES = [
        'text',             # Einfacher Text (str)
        'int',              # Integer
        'float',            # Float (Fließkomma mit begrenzter Genauigkeit)
        'decimal',          # Decimal (Fließkomma mit ungebrenzter Genauigkeit)
                            # Python-Standardbibliothek decimal.Decimal
        'bool',             # Boolean, ggf. zuzgl. None ('Tristate')
        'datetime',         # datetime.datetime
        'date',             # datetime.date
        'time',             # datetime.time
        ]
        
    def __init__(self):
        self._navi = None
        self._types = {}
        self._colNames = []
        self._controlVars = {}
        self._getterAuswahl = {}
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass
    
    def __repr__(self):
        return f'Form mit Widgets für {self._colNames}'
    
    def getNavi(self):
        """getNavi - Gibt das Navi des Widgets zurück
        
            Ergebnis
                Das Navi des Widgets
                None, falls nicht gesetzt
        """
        return self._navi
    
    def getType(self, colName):
        """getType - Gibt den Typ des Widgets zu colName zurück
        
            Parameter
                colName   Name des Widgets bzw. der Spalte aus der DB
        """
        return self._types[colName]
    
    def getColNames(self):
        """getColNames - Gibt Liste der colNames zurück
        """
        return self._colNames
    
    def existsColName(self, colName):
        """existsColName - True, wenn zu colName ein Widget existiert
        
            Parameter
                colName   Name des Widgets bzw. der Spalte aus der DB
            
            Ergebnis
                True      Wenn es ein Widget zu colName gibt
                False     Sonst
        """
        return colName in self._colNames
    
    def getWidget(self, colName):
        """getWidget - Gibt Widget zu colName zurück
        
            Parameter
                colName   Name des Widgets bzw. der Spalte aus der DB
        """
        if self.existsColName(colName):
            return getattr(self, colName)
        else:
            raise ValueError(f'Col Name {colName} existiert nicht.')
    
    def getWidgets(self):
        """getWidgets - Gibt Liste aller Widgets zurück
        
            Ergebnis
                Liste aller "normalen" Widgets (also ohne die Label Widgets)
        """
        return [self.getWidget(colName) for colName in self.getColNames()]
    
    def getLabel(self, colName):
        """getLabel - Gibt Label Widget zu colName
        
            Parameter
                colName   Name des Widgets bzw. der Spalte aus der DB
        """
        if self.existsColName(colName):
            return getattr(self, f'lbl_{colName}')
        else:
            raise ValueError(f'Col Name {colName} existiert nicht.')

    def addWidget(self, colName, widget, typ, label=None):
        """addWidget - Fügt dem Formular ein Widget hinzu
        
            Fügt dem Formular ein Tk/Ttk Widget hinzu.
            
            Außerdem wird, je nach label, ein Label-Widget erzeugt und
            dem Formular hinzugefügt.
            
            Schließlich wird der LabelFrame erzeugt
            
            Es sind nur solche Widgets erlaubt, die einen Wert (value)
            haben bzw. die einen Wert (value) manipulieren können.
            Bsp.: Entry, Checkbutton, Selectbox, Text, oder entsprechende
                  selbst gebaute Widgets.
                  
            ACHTUNG:
            Das Widget muss mit einer Control Variable ausgestattet sein.
            Und zwar - vielleicht im Einzelfall anders als erwartet -
            mit den folgenden festgelegten Typen.
            
                    Hintergrund:
                    Sonst funktionieren die Methoden
                    getValue, setValue und clearValue nicht richtig.
                    Leider kann der Typ der Control Variable nicht festgestellt
                    werden. Folglich kann er auch nicht auf seine Richtigkeit
                    geprüft werden.
                
                Entry           tk.StringVar
                Checkbutton     tk.IntVar
            
            Besonderheiten für datetime, date und time Widgets
            
                Alle drei Typen können entweder None (d.h. '' im Widget)
                oder einen gültigen String enthalten. Als gültig betrachten wir
                im Wesentlichen die deutsche oder eine normierte internationale
                Schreibweise, d.h. z.B für...
                
                    time        23:54
                    date        23.05.2022 (23. Mai 2022) oder
                                23.04.22 (dto)
                                2022-05-23 (dto)
                    datetime    2022-05-23 23:54
                
                Vgl. dazu die Konstanten FORMATS_DATE, FORMATS_TIME, FORMATS_DATETIME
                Weitere Möglichkeiten können evt. über diese Konstanten ermöglicht
                werden.
                
                Alles darüber hinaus müsste ggf. über Validatoren implementiert
                werden.
            
            Parameter
                colName    i.d.R. Name der Spalte in der DB-Tabelle,
                            auf die sich das Widget bezieht.
                            Bezieht sich das Widget auf keine DB-Tabelle,
                            kann colName frei gewählt werden (im Rahmen
                            von checkPythonName)
                widget      Widget
                typ         Typ des Widgets, ein Wert aus TYPES
                label       Label für das Widget.
                            Optional. Im Fall von None wird ein
                            "leeres" Label Widget hergestellt
                            Typ: eine von Möglichkeiten:
                                str: Einfacher Text
                                Label Widget
                            Je nach dem Typ wird...
                                im ersten Label Widget hergestellt
                                im dritten Fall wird das Label Widget
                                einfach übernommen
        """
        #
        # Parameter prüfen
        #
        # colName erlaubt?
        # 1. muss eindeutig sein
        # 2. darf sich nicht mit irgendwelchen Attributen der
        #    Instanz überschneiden
        if colName in self._colNames:
            raise ValueError(f'colName {colName} bereits vergeben.')
        if colName in self.__dict__:
            raise ValueError(f'colName {colName} nicht erlaubt.')
        # colName muss ein zulässiger Python-Name sein
        checkPythonName(colName)
        # typ prüfen
        if typ not in __class__.TYPES:
            raise ValueError(f'{typ=} ungültig.')
        # Typ des Widgets prüfen
        if not (isinstance(widget, tk.Widget) or isinstance(widget, ttk.Widget)):
            raise TypeError('widget hat falschen Typ {type(widget)}.')
        #
        # Widget und typ kompatibel?
        #
        if isinstance(widget, ttk.Checkbutton):
            if typ != 'bool':
                raise ValueError(f'Checkbutton nur für bool, hat aber {typ=}')
        elif isinstance(widget, tk.Text) or isinstance(widget, scrolledtext.ScrolledText):
            if typ != 'text':
                raise ValueError(f'Text nur für text, hat aber {typ=}')
        #
        # Bei Bedarf Control Variable erzeugen und an Widget hängen
        #
        if isinstance(widget, ttk.Entry) or isinstance(widget, ttk.Combobox):
            self._controlVars[colName] = tk.StringVar()
            widget['textvariable'] = self._controlVars[colName]
        elif isinstance(widget, ttk.Checkbutton):
            self._controlVars[colName] = tk.IntVar()
            widget['variable'] = self._controlVars[colName]
        #
        # Widget merken
        #
        setattr(self, colName, widget)
        #
        # colName und typ behandeln
        #
        self._colNames.append(colName)
        self._types[colName] = typ
        #
        # label bearbeiten
        #
        parentWidgetName = widget.winfo_parent()
        parentWidget = widget._nametowidget(parentWidgetName)
        if label is None:
            # Kein label angegeben, Default-Label erzeugen
            lbl = ttk.Label(
                        parentWidget,
                        text=str(colName))
        elif type(label) == str:
            # label ist ein String
            lbl = ttk.Label(
                        parentWidget,
                        text=label)
        elif isinstance(label, ttk.Label):
            # label ist bereits ein Label
            lbl = label
        else:
            # Typ von label falsch
            raise TypeError('Falscher label Typ: {}'.format(type(label)))
        lbl_text = lbl['text']
        # label merken
        setattr(self, f'lbl_{colName}', lbl)
        
        return colName

    def setValue(self, colName, value):
        """setValue - Setzt den Wert des Widgets auf (ggf. String-Variante von) value
        
            setValue konvertiert value nötigenfalls in eine String-Variante und
            setzt den Wert des Widgets darauf.
            
            Durch die zweifache Fallunterscheidung (Art des Widgets und
            typ des Widgets) ist der Code entsprechend zweifach
            geschachtelt...
            
            Parameter
                colName   Name des Widgets bzw. der Spalte in der DB
                value     Wert, i.d.R. aus der DB, in Python Type konvertiert
        """
        # Gibt es colName überhaupt?
        if not self.existsColName(colName):
            raise ValueError(f'Col Name {colName} existiert nicht.')
        # Widget und Typ des Widgets merken
        widget = self.getWidget(colName)
        typ = self.getType(colName)
        #
        # Haupt-Fallunterscheidung
        #
        if isinstance(widget, ttk.Entry) or isinstance(widget, ttk.Combobox):
            # Entry Widget
            if typ == 'text':
                self._controlVars[colName].set('' if value is None else value.strip())
            elif typ == 'int':
                self._controlVars[colName].set('' if value is None else str(value))
            elif typ == 'float':
                self._controlVars[colName].set('' if value is None else float(value))
            elif typ == 'decimal':
                self._controlVars[colName].set('' if value is None else Decimal(value))
            elif typ == 'bool':
                if value is None:
                    self._controlVars[colName].set('')
                elif value:
                    self._controlVars[colName].set(TRUES[0])
                else:
                    self._controlVars[colName].set(__class__.FALSE)
            elif typ == 'date':
                if value is None:
                    self._controlVars[colName].set('')
                else:
                    self._controlVars[colName].set(value.strftime(FORMATS_DATE[0]))
            elif typ == 'time':
                if value is None:
                    self._controlVars[colName].set('')
                else:
                    self._controlVars[colName].set(value.strftime(FORMATS_TIME[0]))
            elif typ == 'datetime':
                if value is None:
                    self._controlVars[colName].set('')
                else:
                    self._controlVars[colName].set(value.strftime(FORMATS_DATETIME[0]))
            else:
                raise ValueError(f'Ungültiger Widget Typ: {typ=}')
        elif isinstance(widget, ttk.Checkbutton):
            # Checkbutton Widget
            if typ == 'bool':
                self._controlVars[colName].set(1 if value else 0)
            else:
                raise TypeError(f'Checkbutton nur für bool, hier aber {typ}.')
        elif isinstance(widget, tk.Text) or isinstance(widget, scrolledtext.ScrolledText):
            # Text (oder ScrolledText) Widget
            if typ == 'text':
                widget.delete('0.0', tk.END)
                if value is None:
                    widget.insert('0.0', '')
                else:
                    widget.insert('0.0', value.strip())
            else:
                raise ValueError(f'Text Widget nur für text, hat aber {typ=}')
        elif isinstance(widget, ListboxValueLabel):
            # ListboxValueLabel Widget, abgeleitet von Listbox
            if type(value) in (tuple, list):
                widget.setValues(value)
            else:
                widget.setValue(value, exclusive=True)
        elif isinstance(widget, FrameScrolledListbox) \
              or isinstance(widget, FrameScrolledListboxValueLabel):
            if type(value) in (tuple, list):
                widget.setValues(value)
            else:
                widget.setValue(value, exclusive=True)
        else:
            raise TypeError('Für {} Widget nicht implementiert.'.format(type(widget)))
    
    def getValue(self, colName):
        """getValue - Gibt den konvertierten Wert des Widgets
        
            getValue holt den Wert aus dem Widget und gibt ihn je nach typ in
            den entsprechenden Python Type konvertiert zurück.
            
            getValue nimmt stillschweigend kleine Korrekturen vor, so werden z.B.
            bei text Widgets führende und folgende Whitespaces entfernt.
            
            Im Übrigen gehen wir davon aus, dass (z.B. durch Validatoren)
            sichergestellt ist, dass gültige Werte im Widget
            stehen. Wir nehmen hier also keine weitere Prüfung vor und
            nehmen in Kauf, wenn andernfalls Exceptions geworfen werden.
            
            Durch die zweifache Fallunterscheidung (Art des Widgets und
            typ des Widgets) ist der Code entsprechend zweifach
            geschachtelt...
            
            Parameter
                colName   Name des Widgets bzw. der Spalte in der DB
            
            Ergebnis
                In Python Type konvertierter Wert des Widgets.
        """
        # Gibt es colName überhaupt?
        if not self.existsColName(colName):
            raise ValueError(f'Col Name {colName} existiert nicht.')
        # Widget und Typ des Widgets merken
        widget = self.getWidget(colName)
        typ = self.getType(colName)
        #
        # Haupt-Fallunterscheidung
        #
        if isinstance(widget, ttk.Entry) or isinstance(widget, ttk.Combobox):
            # Entry Widget
            #
            value = self._controlVars[colName].get().strip()
            if typ == 'text':
                return value.strip()
            elif typ == 'int':
                if value == '':
                    return None
                else:
                    return int(value)
            elif typ == 'float':
                if value == '':
                    return None
                else:
                    return float(value.replace(',', '.'))
            elif typ == 'decimal':
                if value == '':
                    return None
                else:
                    return Decimal(value)
            elif typ == 'bool':
                if value == '':
                    return None
                elif value.lower()[0] in TRUES_SHORT:
                    return True
                else:
                    return False
            elif typ == 'date':
                if value == '':
                    return None
                else:
                    for formatString in FORMATS_DATE:
                        try:
                            Ergebnis = datetime.datetime.strptime(value, formatString).date()
                            return Ergebnis
                        except Exception as e:
                            pass
                    raise RuntimeError('Datum ungültig - dürfte nicht vorkommen.')
            elif typ == 'time':
                if value == '':
                    return None
                else:
                    for formatString in FORMATS_TIME:
                        try:
                            Ergebnis = datetime.datetime.strptime(value, formatString).time()
                            return Ergebnis
                        except Exception as e:
                            pass
                    raise RuntimeError('Datum ungültig - dürfte nicht vorkommen.')
            elif typ == 'datetime':
                if value == '':
                    return None
                else:
                    for formatString in FORMATS_DATETIME:
                        try:
                            Ergebnis = datetime.datetime.strptime(value, formatString)
                            return Ergebnis
                        except Exception as e:
                            pass
                    raise RuntimeError('Datum ungültig - dürfte nicht vorkommen.')
            else:
                raise ValueError(f'Ungültiger Widget Typ: {typ=}')
        elif isinstance(widget, ttk.Checkbutton):
            # Checkbutton Widget
            value = self._controlVars[colName].get()
            if typ == 'bool':
                return value == 1
            else:
                raise TypeError(f'Checkbutton nur für bool, hier aber {typ}.')
        elif isinstance(widget, tk.Text) or isinstance(widget, scrolledtext.ScrolledText):
            # Text (oder ScrolledText) Widget
            if typ == 'text':
                return widget.get('0.0', tk.END).strip()
            else:
                raise ValueError(f'Text Widget nur für text, hat aber {typ=}')
        elif isinstance(widget, ListboxValueLabel):
            # ListboxValueLabel Widget, abgeleitet von Listbox
            liste = widget.getValues()
            laenge = len(liste)
            if laenge == 0:
                return None
            elif laenge == 1:
                return liste[0]
            else:
                return liste
        elif isinstance(widget, FrameScrolledListbox) \
                or isinstance(widget, FrameScrolledListboxValueLabel):
            liste = widget.getValues()
            laenge = len(liste)
            if laenge == 0:
                return None
            elif laenge == 1:
                return liste[0]
            else:
                return liste
        else:
            raise TypeError('Für {} Widget nicht implementiert.'.format(type(widget)))
    
    def setValues(self, values, check=False, keep=False):
        """setValues - Setzt die Werte der Widgets nach dem Dict values
        
            setValues setzt die Werte der Widgets nach dem Dict values. Dabei
            werden natürlich nur die Werte gesetzt, die in values vorkommen.
            
            Wenn keep False ist, werden vorher werden alle Werte gelöscht. Andernfalls
            werden die Werte überschrieben, folglich die nicht vorhandenen erhalten.
            
            Wenn check False ist, wird nicht geprüft, ob alle colNames von Form
            auch in values vorkommen. Dieser Check wird nur mit check = True
            vorgenommen und führt ggf. zu einer Exception.
        
            Parameter
                values    Dict von colName --> value
                check     Bool. 
                          True:   es wird geprüft, ob alle colNames von Form
                                  in values vorkommen. Andernfalls wird eine
                                  Exception geworfen.
                          False:  es wird nicht geprüft.
                keep      Bool
                          True:   Werte, die nicht in values vorkommen, werden
                                  erhalten
                          False:  Erst werden alle Werte in Form gelöscht.
        """
        # ggf. prüfen, ob alle colNames von Form in values vorkommen
        if check:
            for colName in self.getColNames():
                if not colName in values:
                    raise RuntimeError(f'values unvollständig: mindestens {colName=} fehlt.')
        # ggf. Werte vorher löschen
        if not keep:
            self.clearValues()
        # values durchgehen
        for colName in values.keys():
            self.setValue(colName, values[colName])
    
    def getValues(self):
        """getValues - Liefert die Werte aller Widgets als Dict
        
            Liefert die Werte aller Widgets als Dict. Die Werte kommen als Python
            Typen.
        """
        return {colName: self.getValue(colName) for colName in self.getColNames()}
    
    def clearValue(self, colName):
        """clearValue - Löscht den Wert in dem zugehörigen Widget
        
            clearValue setzt auf setValue auf und setzt den Wert auf None.
            In Zukunft könnte das anders implementiert werden.
        
            Parameter
                colName     Name des Widgets bzw. der Spalte in der DB
        """
        self.setValue(colName, None)
    
    def clearValues(self):
        """clearValues - Löscht die Werte aller Widgets
        """
        for colName in self.getColNames():
            self.clearValue(colName)
            
class NaviWidget(ttk.Frame):
    """NaviWidget - Stellt Widgets für Navi Funktionalität bereit
    
        In abgeleiteten Klassen wird das Navi um Schnittstellen zu Modell/DB
        erweitert. Je nach Art dieser Schnittstelle eignet sich das Navi dann
        für Hauptformulare (Form), Unterformulare (ListForm) oder für
        ListForm als Listenansicht (also nicht als Unterformular).
        
        Mit diesen Ergänzungen wir das Navi zur "Schaltzentrale" zwischen
        Formular, Datenbank/Modell und Benutzer.
        
        In NaviWidget werden ausschließlich die nötigen Widgets bereitgestellt,
        schön angeordnet in ttkFrame (von dem NaviWidget abgeleitet ist),
        das später als Navi in das Formular eingbaut (z.B. gepackt) werden kann.
        
        Für die abgeleiteten Klassen initialisieren wir Attribute/Methoden,
        eigentlich aber nur um der Klarheit willen.
        
        In NaviWidget bauen wir folglich ein ttk.Frame der folgenden Form:
        
        +---------------------------+
        | Filter, Buttons           |
        +---------------------------+
        | Auswahlliste              | 
        |                           |
        +---------------------------+
        
        Dabei ist:
            Filter
                Ein Eingabefeld (Entry) (mit Icon (Lupe)?). Eingaben hier
                führen zu einer Filterung der Auswahlliste
            Buttons
                Eine Reihe von Buttons, die der Navigation und Funktionalität
                auf der Datenbank bzw. auf dem Formular dienen. Z.B. Sichern, Löschen,
                Refresh
            Auswahlliste
                Variante von tk.Listbox (i.d.R. FrameScrolledListboxValueLabel), darin
                untereinander für jeden Datensatz in der DB eine Zeile. Wird eine
                Zeile ausgewählt, d.h. der zugehörige
                Datensatz ausgewählt, wird er in dem Formular angezeigt.
                Diese Zeilen verhalten sich letztlich wie ein Button.
        
        Achtung: Icons (Images) für Buttons können erst gebaut werden, wenn es
        ein root-Window gibt. Daher kann bei der Instanziierung von NaviWidget
        i.d.R. den Buttons noch kein Image zugeteilt werden.
        Workaround: Bei der Instanziierung merken wir uns ohnehin die eingebauten
        Widgets, also auch die Buttons. Wir definieren die
            Static Method
                imageInit(), die nachträglich die Images erzeugt und
        den Buttons zuordnet.
        
        Parameter
            parent        Eltern Widget, wird an ttk.Frame weiter gegeben
            elemente      Liste/Tupel der Elemente, die in dem Navi tatsächlich eingebaut
                          werden sollen.
                          Default: () (leeres Tupel), d.h. alle verfügbaren Elemente
                              werden eingebaut
                          Die Elemente werden mit str-Werten angegeben. Mögliche
                          Werte sind:
                              filter      Input-Feld zum Filtern
                              emptyform   Formular leeren für neue Eingabe
                              save        Datensatz in der DB sichern (INSERT/UPDATE)
                              save-clear  Datensatz in der DB sichren (INSERT/UPDATE)
                                          Beachte
                                          Die beiden save Varianten unterscheiden sich
                                          nur dadurch, dass bei save nach dem
                                          Speichern der gespeicherte Datensatz
                                          im Formular wieder gezeigt wird. save-clear
                                          hingegen leert das Formular nach dem
                                          Speichern.
                              delete      Datensatz in der DB löschen (DELETE)
                              refresh     Auswahlliste neu aufbauen
                              undo        Datensatz neu aus der DB lesen, d.h.
                                          eventuell im Formular vorgenommene
                                          Änderungen verwerfen.
                              copy        Doublette des angezeigten Datensatzes
                                          anlegen und im Formular zeigen.
                              list        Auswahlliste, ggf. gefiltert
                          Bsp.: ('filter', 'save', 'delete')
                          Ungültige Werte führen zu ValueError
        
        Klassen Attribute
            GUELTIGE_ELEMENTE     Tupel der gültigen Elemente, vgl. Parameter elemente
        
        Attribute
            elemente              elemente, vgl. entspr. Parameter
            form                  Formular, an dem das Navi hängt. Wird z.B. durch
                                  BasisForm.setNavi gesetzt
            naviElemente          Dict der Navi-Elemente
                                  Für die Elemente, die nicht vorhanden sind (weil nicht
                                  in elemente angegeben), wird der Wert auf None gesetzt.
        
        Static Methods
            imageInit     Baut die Icons (Images) für die Buttons und
                          versorgt die Buttons damit.
        
        Methods
            iconsInit         Versorg das Navi bzw. dessen Buttons mit Icons
            buildNaviWidget   Baut Navi Widget auf
            listAppend        Hängt value/label an Auswahlliste an
                              ruft append der Auswahlliste auf
            listClear         Löscht Auswahlliste
                              ruft clear der Auswahlliste auf
            
    """
    # Tupel der Elemente, die als Widgets o.ä. in das Navi eingebaut werden können.
    # GUELTIGE_ELEMENTE wird verwendet, um
        #   1.  Die übergebenen Elemente (elemente) auf ihre Gültigkeit zu überprüfen.
        #           Ungültigkeit wird einerseits mit einem DEBUG gelogged (nur einmal beim
        #           Instantiieren), andererseits später stillschweigend ignoriert.
        #   2.  Dict der Navi-Buttons zu initialisieren. GUELTIGE_ELEMENTE
        #           sollte also vollständig sein.
    GUELTIGE_ELEMENTE = (
        'filter',
        'emptyform',
        'save',
        'save-clear',
        'delete',
        'refresh',
        'undo',
        'copy',
        'list',
        )
    
    NAVI_ICONS = {
        'emptyform':    'actions/edit-clear-list',
        'save':         'actions/document-save-as',
        'save-clear':   'actions/document-save',
        'delete':       'actions/edit-delete',
        'refresh':      'actions/view-refresh',
        'undo':         'actions/edit-undo',
        'copy':         'actions/edit-copy',
        }
        
    navis = []
    
    def __init__(self, parent, elemente=()):
        #
        # __init__ von super() aufrufen, in diesem Fall also von Widget.
        super().__init__(parent)
        #
        # Merken der übergebenen Parameter
        if elemente:
            # Es wurden Elemente übergeben
            self.elemente = elemente
        else:
            # Default, es wurden keine Elemente übergeben, gemeint
            # sind also alle erlaubten Elemente
            self.elemente = __class__.GUELTIGE_ELEMENTE
        #
        # Gültigkeit der Elemente prüfen
        for element in elemente:
            if not element in __class__.GUELTIGE_ELEMENTE:
                raise ValueError(f'')
        #
        # Attribut: Dict für Navi-Elemente initialisieren
        self.naviElemente = {element: None for element in self.GUELTIGE_ELEMENTE}
        #
        # Attribut: Var für Filter-Input initialisieren
        self.naviFilterEntry = None
        # Navi Widget
        self.buildNaviWidget()
        # Navi in Klassenattribut merken
        __class__.navis.append(self)
    
    @staticmethod
    def imagesInit():
        """imagesInit - Sucht alle verfügbaren Icons zusammen und versorgt Navis damit
        
            Baut auf iconsInit auf. 
        """
        __class__.icons = {}
        counter = 0
        for pfad, untrordner, dateien in os.walk(ICONS_DIR):
            for datei in dateien:
                counter += 1
                iconName = pfad.replace(ICONS_DIR, '') + '/' + datei.replace('.png', '')
                pfadName = pfad + '/' + datei
                image = Image.open(pfadName)
                icon = image.resize((14,14))
                __class__.icons[iconName] = ImageTk.PhotoImage(icon)
        for navi in __class__.navis:
            navi.iconsInit()
    
    def iconsInit(self):
        """iconsInit - Versorgt das Widget mit einem Icon
        
            Wird von der Klassen-Methode imagesInit aufgerufen.
        """
        for element in ('emptyform', 'save', 'save-clear', 'delete',
                'refresh', 'undo', 'copy'):
            if btn := self.naviElemente[element]:
                btn.config(
                    image=__class__.icons[__class__.NAVI_ICONS[element]],
                    # compound=tk.TOP,
                    width=10)
    
    def buildNaviWidget(self):
        """buildNaviWidget - baut Widgets und packt sie in ttk.Frame
        """
        style = ttk.Style()
        style.configure('Navi.TButton',
            borderwidth=0,
            padding=0,
            padx=0,
            pady=0,
            width='100px')
        buttons = ttk.Frame(self)
        buttons.pack(side=tk.TOP)
        for element in self.elemente:
            if element == 'filter':
                self.naviElemente[element] = ttk.Entry(
                        buttons,
                        width=6)
                self.naviElemente[element].pack(side=tk.LEFT)
            if element == 'emptyform':
                self.naviElemente[element] = ttk.Button(
                        buttons,
                        text='Empty Form',
                        style='Navi.TButton'
                        )
                self.naviElemente[element].pack(side=tk.LEFT)
            if element == 'save':
                self.naviElemente[element] = ttk.Button(
                        buttons,
                        text='Save',
                        style='Navi.TButton')
                self.naviElemente[element].pack(side=tk.LEFT)
            if element == 'save-clear':
                self.naviElemente[element] = ttk.Button(
                        buttons,
                        text='Empty Form',
                        style='Navi.TButton')
                self.naviElemente[element].pack(side=tk.LEFT)
            if element == 'delete':
                self.naviElemente[element] = ttk.Button(
                        buttons,
                        text='Empty Form',
                        style='Navi.TButton')
                self.naviElemente[element].pack(side=tk.LEFT)
            if element == 'refresh':
                self.naviElemente[element] = ttk.Button(
                        buttons,
                        text='Empty Form',
                        style='Navi.TButton')
                self.naviElemente[element].pack(side=tk.LEFT)
            if element == 'undo':
                self.naviElemente[element] = ttk.Button(
                        buttons,
                        text='Empty Form',
                        style='Navi.TButton')
                self.naviElemente[element].pack(side=tk.LEFT)
            if element == 'copy':
                self.naviElemente[element] = ttk.Button(
                        buttons,
                        text='Empty Form',
                        style='Navi.TButton')
                self.naviElemente[element].pack(side=tk.LEFT)
        if 'list' in self.elemente:
            self.naviElemente['list'] = FrameScrolledListboxValueLabel(self)
            self.naviElemente['list'].pack(side=tk.TOP)
    
    def listClear(self):
        """listClear - Leert die Ausswahlliste
        """
        self.naviElemente['list'].clear()
    
    def listAppend(self, value, label=None):
        """listAppend - Hängt value/label an die Auswahlliste an
        """
        self.naviElemente['list'].append(value, label)
