from dataclasses import dataclass

@dataclass
class ProdottoRecord:
    name: str
    prezzo_unitario: float

    # Rendo l'oggetto hashable calcolando l'hash di una tupla
    # contenente gli attributi che identificano univocamente l'istanza.
    # Necessario per usare l'oggetto come chiave di dizionario o in un set.
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    # Creo un metodo per una stampa "più bella"
    def __str__(self):
        return f"{self.name} -- {self.prezzo_unitario}"