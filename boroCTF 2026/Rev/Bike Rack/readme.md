# Bike Rack

## Description

OH NO!!! You forgot the PIN for your bike lock. Analyze the lock and figure out how to break it.

## Solution Walkthrough

Opening it with IDA reveals the following logic, where `aAweqblpmnortyu` is `AweQbLpMnorTyUioZxcvbnmCQwertyuioTqwFer{TyUiopasRd@fghjknLzXcvbnmdQwerty0u0IopasdMFghjklzxc_VbnmqwerYCvbnZMqw4e2RtyuiopasuFghjklzx%SdfyGhjklzmNbmqwerty}` and `dest` is `1927591750185873109357128735:912357132509713257561029375701027357361:2179327561242142098:980985641877731:238`

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  size_t v3; // rax
  __int64 v5; // rax
  int v6; // [rsp+8h] [rbp-138h]
  __int64 v7; // [rsp+10h] [rbp-130h]
  size_t i; // [rsp+18h] [rbp-128h]
  size_t j; // [rsp+20h] [rbp-120h]
  char s[264]; // [rsp+30h] [rbp-110h] BYREF
  unsigned __int64 v11; // [rsp+138h] [rbp-8h]

  v11 = __readfsqword(0x28u);
  printf("Hey, uhm, why are there so many different inputs for this bike lock???\nPIN: ");
  v3 = strlen(dest);
  memmove(dest, &dest[8], v3 - 7);
  strncat(dest, "187773102385012356629012836224235219768597857", 0xBu);
  if ( !fgets(::s, 256, stdin) )
    return 0;
  ::s[strcspn(::s, "\r\n")] = 0;
  v7 = 0;
  for ( i = 0; i < strlen(::s); i += 4LL )
  {
    v5 = v7++;
    s[v5] = ::s[i];
  }
  s[v7] = 0;
  v6 = 0;
  strlen(aAweqblpmnortyu);
  for ( j = 0; j < strlen(s); ++j )
  {
    v6 += s[j] - 48;
    putchar(aAweqblpmnortyu[v6 - 1]);
  }
  putchar(10);
  return 0;
}
```

It can be observed that although the program requests a PIN input, it only actually takes the 0th, 4th, 8th, 12th, ... characters of the input; the remaining characters have no effect on the result. Next, observing the output portion, it treats the extracted characters as numbers. For every character read, it adds s[j] - '0' to v6, and then uses v6 - 1 as an index to look up `aAweqblpmnortyu`.

```c
v6 = 0;
for ( j = 0; j < strlen(s); ++j )
{
  v6 += s[j] - 48;
  putchar(aAweqblpmnortyu[v6 - 1]);
}
```

In other words, assuming the valid input is `55158:33`, the actual operations the program performs would be:

```text
v6 = 0

'5' -> v6 += 5  -> table[4]  = b
'5' -> v6 += 5  -> table[9]  = o
'1' -> v6 += 1  -> table[10] = r
'5' -> v6 += 5  -> table[15] = o
'8' -> v6 += 8  -> table[23] = C
':' -> v6 += 10 -> table[33] = T
'3' -> v6 += 3  -> table[36] = F
'3' -> v6 += 3  -> table[39] = {
```

## Flag

```text
boroCTF{R@nd00M_YZ42u%ym}
```
