# The Joy of Draw

## Description

My best friend Joy Shah is an incredible chess player. We always used to look back at one specific match from July 2016 where he managed to force a brilliant draw. At the time, I never understood why he was so proud of a tie instead of a victory. Especially considering his opponent was highly rated at 1900! As time goes on, my memories of that tournament are beginning to decay. I know it took place at the 30th National Under-13 Boys Chess Championship in Ahmedabad, but the fine details are slipping away.

Find the following information about that match:

- Tournament Round (Format: digits only)
- Name of the Opponent (Format: First_Last)
- Last Traded Piece (Format: Capitalized singular noun)
- Name of the Opening Defence (Format: Capitalized_Words)
Flag Format: dalctf{Round_First_Last_Piece_Opening_Defence}

## Solution Walkthrough

Look up the [30th National Under-13 Boys Chess Championship](https://chess-results.com/Test/tnr228504.aspx?lan=1) on chess-results. Since the prompt states the opponent's rating is 1900, a quick check reveals the player is Panda Sambit.

![alt text](image.png)

Clicking on his name (you need to click "show tournament details" first) brings up his match history, which shows that his opponent in round 5 was Joy Shah.

![alt text](image-1.png)

By analyzing the chess notation, it can be determined that the last piece captured was a rook, and the opening played was the King's Indian Defence.

## Flag

```text
dalctf{5_Sambit_Panda_Rook_Kings_Indian_Defence}
```
