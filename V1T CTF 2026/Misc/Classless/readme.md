# Classless

## Description

Ever learnt OOP? If yes? Good, now forget what a class is xD

## Solution Walkthrough

### Solution 1

I first ran `strings` on the entire file and found nothing. Then, I looked at `.rodata`. Since this `objectvm` doesn't have much in `.rodata`, I decided to look for the flag directly. I noticed something suspicious at the bottom:

![alt text](image.png)

```text
0x41, 0x06, 0x43, 0x4C, 0x43, 0x45, 0x5E, 0x5B, 0x5E, 0x59, 0x50, 0x42, 0x56, 0x5B, 0x68, 0x41, 0x43, 0x56, 0x55, 0x5B, 0x52, 0x68, 0x55, 0x56, 0x55, 0x52, 0x5B, 0x68, 0x01, 0x51, 0x07, 0x06, 0x56, 0x05, 0x54, 0x0E, 0x4A
```

Without further ado, I performed an XOR bruteforce and discovered that XORing with `0x37` reveals the flag.

![alt text](image-1.png)

### Solution 2

By putting the contents of the `.bbl` file into CyberChef and using the Magic tool, I discovered that it is actually JSON -> zlib compressed -> base64 encoded.

![alt text](image-2.png)

I found three main fields in the JSON:

```json
{
  "classes": [...],
  "objects": [...],
  "entry": 1
}
```

Among these, `classes` defines the class, method, slot, visibility, and body, while `objects` defines the actual object's `declared_class`, `runtime_class`, `fields`, and `vtable`. This means the program is essentially a simple object VM that simulates class dispatch, interfaces, MRO, and vtable behavior based on the classes/objects defined in the JSON.

The output for the sample is as follows:

```text
hello from objectvm
interface Greeter: yes
resolved class: Cat
dispatch slot 7: allow
Vault denied: verifier
```

`04_denied.bbl` looked more suspicious; it likely represents a vault. This suggests that there should be a hidden vault logic within the binary, but the sample hasn't passed the check yet. Looking closely, I found several verification steps:

![alt text](image-3.png)

```text
verifier -> resolver -> dispatcher
```

I noticed `sub_4760`, which is a function specifically designed to perform an XOR operation with `0x5A`.

![alt text](image-4.png)

![alt text](image-5.png)

Therefore, the first verifier stage is likely checking whether the current object can be considered a `TrustedPlugin`.

Next, looking at the resolver part, once the hidden vault passes the verifier, it calls:

```c
sub_51D0(v87, (_DWORD)v41, ...);
v61 = sub_10F50(v60, v108);
```

Here, `v108` is the `TrustedPlugin` decrypted earlier, so this part checks if the string returned by `sub_51D0` is equal to `TrustedPlugin`.

Entering `sub_51D0`, we can see:

```c
__int64 __fastcall sub_51D0(__int64 a1, __int64 a2)
{
  _QWORD v3[4];
  _QWORD v4[11];

  sub_4760(v4, byte_134F0, 9);
  sub_5170(v3, a2, v4);
  std::string::_M_dispose(v4);

  if ( v3[1] )
    std::string::basic_string(a1, v3);
  else
    std::string::basic_string(a1, a2 + 40);

  std::string::_M_dispose(v3);
  return a1;
}
```

`sub_4760` is called again here.

```c
sub_4760(v4, byte_134F0, 9);
```

XORing `byte_134F0` with `0x5A` gives `__class__`. Thus, `sub_51D0` actually first looks for the `__class__` field in the object's fields. If found, it returns `fields["__class__"]`; if not, it returns the object's original class, which is `a2 + 40`.

Then, `sub_10F50` is a string comparison function, so the resolver only needs the object's `fields` to contain:

```json
"fields": {
  "__class__": "TrustedPlugin"
}
```

Next, looking at the dispatcher part:

```c
sub_4760(v87, ";665-", 5);
sub_9910(&v109, &v95, v41, 7, 0);
v63 = sub_10F50(&v109, v87);
```

Here, `sub_4760(v87, ";665-", 5)` is again an XOR with `0x5A`. Decrypting `";665-"` yields `allow`. So, the dispatcher stage requires the result dispatched by `vtable[7]` to be `allow`.

If the verifier, resolver, and dispatcher all pass, it proceeds to the success path, which is where the flag is actually decrypted. Therefore, the overall logic of the hidden vault can be summarized as:

```c
if (obj.fields["__task__"].empty()) {
    trusted = xor_decode(byte_13500, 13, 0x5A); // "TrustedPlugin"

    if (!verifier(vm, obj, trusted)) {
        puts("Vault denied: verifier");
        return;
    }

    resolved = resolve_class(obj); // fields["__class__"] or runtime_class

    if (resolved != trusted) {
        puts("Vault denied: resolver");
        return;
    }

    expected = xor_decode(";665-", 5, 0x5A); // "allow"
    result = dispatch_slot(vm, obj, 7);

    if (result != expected) {
        puts("Vault denied: dispatcher");
        return;
    }

    flag = xor_decode(unk_134A0, 37, 0x37);
    puts(flag);
}
```

## Flag

```text
v1t{trilingual_vtable_babel_6f01a2c9}
```
