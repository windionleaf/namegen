"""
Created on 24. 5. 2019
Modul se třídami (funktory) pro filtrování.

:author:     Martin Dočekal
:contact:    xdocek09@stud.fit.vubtr.cz
"""

from abc import ABC, abstractmethod
from typing import Any, Set

import re
class Filter(ABC):
    """
    Základni funktor pro filtrování
    """

    @abstractmethod
    def __call__(self, o:Any) -> bool:
        """
        Volání filtru
        
        :param o: objekt pro filtrování
        :type o: Any
        :return: True pokud má být objekt o propuštěn filtrem. False pokud má být odfiltrován.
        :rtype: bool
        """
        pass
        

class NameLanguagesFilter(Filter):
    """
    Filtruje jména na základě vybraných jazyků.
    """
    
    def __init__(self, languages:Set[str]):
        """
        Inicializace filtru.
        
        :param languages: Povolené jazyky.
        :type languages: Set[str]
        """
        
        self._languages=languages
        
    def __call__(self, o) -> bool:
        """
        Volání filtru
        
        :param o: jméno pro filtrování
        :type o: Name
        :return: True pokud má být jméno o propuštěno filtrem. False pokud má být odfiltrováno.
        :rtype: bool
        """
        
        return  o.language in self._languages
   
class NameRegexFilter(Filter):
    """
    Filtruje jména dle podoby samotného jména.
    """
    
    def __init__(self, nameRegex:Set[str]):
        """
        Inicializace filtru.
        
        :param nameRegex: Regulární výraz určující množinu všech povolených jmen.
        :type nameRegex: re
        """
        
        self._nameRegex=nameRegex
        
    def __call__(self, o) -> bool:
        """
        Volání filtru
        
        :param o: jméno pro filtrování
        :type o: Name
        :return: True pokud má být jméno o propuštěno filtrem. False pokud má být odfiltrováno.
        :rtype: bool
        """
        
        return  self._nameRegex.match(str(o))

class NameAlfaFilter(Filter):
    """
    Filtruje jména na základě povolených alfa znaků.
    Propouští pouze jména jejichž alfa znaky jsou v dané množině alfa znaků. Nehledí na jiné druhy znaků.
    """
    
    def __init__(self, alfas:Set[str], caseInsensitive:bool=True):
        """
        Inicializace filtru.
        
        :param alfas: Povolené alfa znaky.
        :type alfas: Set[str]
        :param caseInsensitive: Defaultné nezaleží na velikosti písmen. Pokud je false, tak na velikosit
            písmen záleží.
        :type caseInsensitive: bool
        """
        
        self._alfas=alfas
        
        if caseInsensitive:
            self._alfas=set(c.upper() for c in self._alfas)

    def __call__(self, o) -> bool:
        """
        Volání filtru
        
        :param o: jméno pro filtrování
        :type o: Name
        :return: True pokud má být jméno o propuštěno filtrem. False pokud má být odfiltrováno.
        :rtype: bool
        """
        
        return  all( not c.isalpha() or c.upper() in self._alfas for c in str(o))
        
        
    
class NamesFilter(Filter):
    """
    Filtruje jména na základě vybraných jazyků a podoby samotného jména.
    """
    
    
    def __init__(self, languages:Set[str], nameRegex:re, alfas:Set[str]):
        """
        Inicializace filtru.
        
        :param languages: Povolené jazyky.
        :type languages: Set[str]
        :param nameRegex: Regulární výraz určující množinu všech povolených jmen.
        :type nameRegex: re
        :param alfas: Povolené alfa znaky.
        :type alfas: Set[str]
        """
        
        alwaysTrueFunc=lambda x:True
        
        self._languages=alwaysTrueFunc if languages is None else NameLanguagesFilter(languages)
        self._nameRegex=alwaysTrueFunc if nameRegex is None else NameRegexFilter(nameRegex)
        self._alfaFilter=alwaysTrueFunc if alfas is None else NameAlfaFilter(alfas)
        
    def __call__(self, o) -> bool:
        """
        Volání filtru
        
        :param o: jméno pro filtrování
        :type o: Name
        :return: True pokud má být jméno o propuštěno filtrem. False pokud má být odfiltrováno.
        :rtype: bool
        """
        
        return self._languages(o) and self._nameRegex(o) and self._alfaFilter(o)
                
                


        
        