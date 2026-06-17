from pypdf import PdfReader
from pypdf.generic import IndirectObject

r = PdfReader("financial_report")

objs = set()

for generation, entries in r.xref.items():
    for obj_id in entries:
        objs.add((obj_id, generation, "normal"))

for obj_id, (stream_obj_id, index) in r.xref_objStm.items():
    objs.add((obj_id, 0, f"ObjStm {stream_obj_id}, index {index}"))

for obj_id, generation, source in sorted(objs):
    obj = IndirectObject(obj_id, generation, r).get_object()
    print(f"\n--- {obj_id} {generation} obj ({source}) ---")
    print(obj)