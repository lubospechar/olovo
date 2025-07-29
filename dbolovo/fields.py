from django.db import models  # Importujeme základní třídy pro tvorbu Django modelů
from django.core.exceptions import (
    ValidationError,
)  # Import pro vyvolání výjimky při neplatné hodnotě
from django.utils import timezone  # Import pro získání aktuálního data a času


class SpecialYearField(models.IntegerField):
    """
    Vlastní pole pro validaci roku. Rok musí být mezi 2011 a aktuálním rokem.
    Toto pole dědí od IntegerField, což znamená, že chování tohoto pole je velmi podobné číselnému poli,
    avšak přidáváme k němu vlastní logiku pro validaci.
    """

    def __init__(self, *args, **kwargs):
        """
        Konstruktor třídy, kde inicializujeme základní parametry pole.
        args a kwargs umožňují přístup k jakýmkoliv dalším argumentům, které mohou být
        předány do pole během jeho použití (např. max_length, verbose_name atd.).
        """
        self.min_year = 2011  # Definujeme minimální povolený rok (2011)
        self.max_year = (
            timezone.now().year
        )  # Dynamicky nastavíme maximální rok na aktuální rok
        super().__init__(
            *args, **kwargs
        )  # Zavoláme konstruktor předka (IntegerField) pro zajištění standardní funkčnosti

    def validate(self, value, model_instance):
        """
        Funkce validate kontroluje, zda hodnota zadaná v poli splňuje naše kritéria.
        value - hodnota, kterou chceme validovat
        model_instance - instance modelu, ke které se hodnota vztahuje
        """
        current_year = (
            timezone.now().year
        )  # Načteme aktuální rok pomocí timezone (zajistí podporu pro časové zóny)

        # Validace hodnoty - kontrolujeme, zda rok spadá mezi min_year a current_year
        if value < self.min_year or value > current_year:
            # Pokud hodnota není v rozmezí, vyhodíme výjimku ValidationError s chybovým hlášením
            raise ValidationError(
                f"Rok musí být mezi {self.min_year} a {current_year}."
            )

        # Pokud hodnota prošla validací, zavoláme validaci z předka (IntegerField), která provede ostatní standardní kontroly
        super().validate(value, model_instance)
