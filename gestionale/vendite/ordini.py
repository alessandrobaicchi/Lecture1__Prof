from dataclasses import dataclass

from gestionale.core.cliente import ClienteRecord
from gestionale.core.prodotto import ProdottoRecord


@dataclass
class RigaOrdine:
    prodotto: ProdottoRecord
    quantita: int

    def totale_riga(self):
        return self.prodotto.prezzo_unitario * self.quantita

@dataclass
class Ordine:
    righe: list[RigaOrdine]
    cliente: ClienteRecord

    def totale_netto(self):
        return sum(r.totale_riga() for r in self.righe)

    def totale_lordo(self, aliquota_iva):
        return self.totale_netto()*(1+aliquota_iva)

    def numero_righe(self):
        return len(self.righe)

    def riepilogo(self) -> str:
        """Restituisce un riepilogo testuale dell'ordine."""
        linee = [
            f"Ordine per: {self.cliente.nome} ({self.cliente.mail})",
            f"Categoria cliente: {self.cliente.categoria}",
            "-" * 50
        ]

        for i, riga in enumerate(self.righe, 1):
            linee.append(
                f"{i}. {riga.prodotto.name} - "
                f"Q.tà {riga.quantita} x {riga.prodotto.prezzo_unitario}€ = "
                f"{riga.totale_riga()}€"
            )

        linee.append("-" * 50)
        linee.append(f"Totale netto: {self.totale_netto():.2f}€")
        linee.append(f"Totale lordo (IVA 22%): {self.totale_lordo(0.22):.2f}€")

        return "\n".join(linee)


@dataclass
class OrdineConSconto(Ordine):
    sconto_percentuale: float

    def totale_scontato(self):
        self.totale_lordo()*(1-self.sconto_percentuale)

    def totale_netto(self):
        netto_base = super().totale_netto()
        return netto_base*(1-self.sconto_percentuale)
