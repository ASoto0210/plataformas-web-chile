#!/usr/bin/env python3
"""Cambia el sitio del dominio de GitHub Pages al dominio propio.

    python cambiar-dominio.py            # solo revisa, no toca nada
    python cambiar-dominio.py --aplicar  # hace el cambio

Por que un script y no ocho reemplazos a mano: el archivo CNAME NO se puede crear
antes de que el DNS resuelva. Apenas existe, GitHub redirige la URL de github.io al
dominio nuevo; si ese dominio todavia no apunta a ninguna parte, el sitio queda
inalcanzable — incluido el enlace del credito en el pie de stom.cl. Por eso lo
primero que hace el script es comprobar el DNS y abortar si no esta listo.
"""
import argparse
import pathlib
import re
import socket
import sys

DOMINIO = "plataformasweb.cl"
VIEJO = "https://asoto0210.github.io/plataformas-web-chile/"
NUEVO = f"https://{DOMINIO}/"

# Las cuatro IP de GitHub Pages para dominios apex.
IPS_PAGES = {"185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153"}

RAIZ = pathlib.Path(__file__).resolve().parent
ARCHIVOS = ["index.html"]


def resuelve(nombre):
    """IPs a las que resuelve el nombre, o conjunto vacio si no resuelve."""
    try:
        return {info[4][0] for info in socket.getaddrinfo(nombre, None, socket.AF_INET)}
    except socket.gaierror:
        return set()


def revisar_dns():
    apex = resuelve(DOMINIO)
    if not apex:
        return False, f"{DOMINIO} todavia no resuelve. Falta cargar los nameservers de Cloudflare en NIC."
    faltan = IPS_PAGES - apex
    sobran = apex - IPS_PAGES
    if faltan or sobran:
        detalle = f"responde {sorted(apex)}"
        if faltan:
            detalle += f"; faltan {sorted(faltan)}"
        if sobran:
            detalle += f"; sobran {sorted(sobran)} (¿el proxy naranja de Cloudflare encendido?)"
        return False, f"{DOMINIO} resuelve, pero no a las IP de GitHub Pages: {detalle}"
    return True, f"{DOMINIO} apunta a las cuatro IP de GitHub Pages."


def ocurrencias():
    total = {}
    for nombre in ARCHIVOS:
        texto = (RAIZ / nombre).read_text(encoding="utf-8")
        total[nombre] = texto.count(VIEJO)
    return total


def aplicar():
    for nombre, n in ocurrencias().items():
        ruta = RAIZ / nombre
        texto = ruta.read_text(encoding="utf-8")
        ruta.write_text(texto.replace(VIEJO, NUEVO), encoding="utf-8")
        print(f"  {nombre}: {n} referencias actualizadas")
    (RAIZ / "CNAME").write_text(DOMINIO + "\n", encoding="utf-8")
    print(f"  CNAME creado con {DOMINIO}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true", help="escribe los cambios")
    ap.add_argument("--forzar", action="store_true",
                    help="omite la comprobacion de DNS (no usar salvo que sepas por que)")
    args = ap.parse_args()

    listo, mensaje = revisar_dns()
    print(("OK   " if listo else "ALTO ") + mensaje)

    print("\nReferencias al dominio viejo:")
    for nombre, n in ocurrencias().items():
        print(f"  {nombre}: {n}")
    if (RAIZ / "CNAME").exists():
        print("  CNAME: ya existe")

    if not args.aplicar:
        print("\n(Solo revision. Agrega --aplicar para hacer el cambio.)")
        return 0

    if not listo and not args.forzar:
        print("\nNo se cambia nada: crear el CNAME ahora dejaria el sitio inalcanzable.")
        return 1

    print("\nAplicando:")
    aplicar()
    print("\nFalta hacer a mano, en GitHub:")
    print("  Settings -> Pages -> Custom domain -> " + DOMINIO)
    print("  Esperar el certificado y marcar 'Enforce HTTPS'.")
    print("\nY despues, commitear y pushear.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
