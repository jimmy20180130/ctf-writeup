# One Small (13 Year Old Edit) for Mankind

## Description

"So, here we are and here I am. Exactly what I'm going to do here is a mystery, although editing wikipedia is addicting." - my friend, a genius predictor

Baltimore, Maryland
Pomona, California
Grand Rapids, Michigan
London, Ontario, Canada
Find the username of the author and the date of the edit.

Format: boroCTF{SolarityPy_April_20_1967}

## Solution Walkthrough

Searching for `Baltimore Maryland Pomona California Grand Rapids Michigan London Ontario` on Google, which are the four locations mentioned above, reveals that these are the birthplaces of the Artemis II crew members.

Since the problem states that his friend loves editing Wikipedia, I checked the edit history. Based on the prompt, I went back 13 years to 2013, where I discovered that a user named Ericl had edited the Wikipedia page for Artemis II.

![alt text](image.png)

Clicking on Ericl's profile page, I found the text: `So, here we are and here I am. Exactly what I'm going to do here is a mystery, although editing wikipedia is addicting.`, which is exactly the same as the description in the challenge.

## Flag

```text
boroCTF{Ericl_December_17_2013}
```
