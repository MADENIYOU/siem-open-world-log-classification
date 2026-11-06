"""Ajoute une transition « fondu » entre les diapositives (sobre) et un léger fondu d'entrée du titre. Idempotent.
Usage : .venv/bin/python post_process.py Soutenance_SIEM_monde_ouvert.pptx"""
import re, shutil, sys, zipfile, tempfile, os
src = sys.argv[1]; tmp = tempfile.mktemp(suffix=".pptx"); n = 0
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        if item.filename.endswith('/'): continue                      # pas d'entrées de dossier (échecs d'ouverture via certains services)
        data = zin.read(item.filename)
        if re.match(r"ppt/slides/slide\d+\.xml$", item.filename):
            xml = data.decode("utf-8")
            if "<p:transition" not in xml:
                tr = '<p:transition spd="med"><p:fade/></p:transition>'
                xml = xml.replace("</p:clrMapOvr>", "</p:clrMapOvr>" + tr, 1) if "</p:clrMapOvr>" in xml else xml.replace("</p:cSld>", "</p:cSld>" + tr, 1)
                n += 1
            data = xml.encode("utf-8")
        zout.writestr(item, data)
shutil.move(tmp, src); print("transitions ajoutées :", n)
