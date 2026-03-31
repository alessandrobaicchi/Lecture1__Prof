from dataclasses import dataclass

@dataclass
class ClienteRecord:
    nome: str
    mail: str
    categoria: str

    def __hash__(self):
        return hash(self.mail)

    def __eq__(self, other):
        return self.mail == other.mail

    def __str__(self):
        # Rappresentazione leggibile del cliente per stampe e logging
        return f" Cliente {self.nome} -- {self.mail} ({self.categoria})"
