# Pretty Pens: ELI5 Solution Plan

## What's the problem? 🖍️

Imagine you have pens in different colors: red pens, blue pens, green pens, etc.

For each color, we pick the PRETTIEST pen of that color. Then we add up how pretty all the picked pens are.

**BUT** we can move ONE pen to a different color to make the total prettier. What's the best we can do?

## How to solve it 🎯

### Step 1: Pick the prettiest pen for each color

- Red pens: pick the nicest red pen
- Blue pens: pick the nicest blue pen
- Green pens: pick the nicest green pen
- Add up their prettiness = **Normal Score**

### Step 2: What if we move ONE pen?

For example, what if we take a really pretty blue pen and make it a red pen?

- Red pens lose one pretty pen (if we move it), BUT get the blue pen instead
- Blue pens lose the blue pen, BUT get their second-nicest pen instead
- All other colors stay the same

### Step 3: Is the move worth it?

Compare the new score with the normal score. Pick whichever is bigger.

```
Normal: Red (10) + Blue (8) + Green (5) = 23
After moving blue-9 to red: Red (10+9) + Blue (8→6) + Green (5) = 28
Better! Use 28.
```

## What about updates? 📝

Sometimes a pen changes:

- It gets a different color
- It becomes prettier/uglier

When that happens, just recalculate which pens are prettiest for each color, and try the best move again.

## Why does this work?

If we're only moving ONE pen, only the color it LEFT and the color it WENT TO can change their picked pen. Everything else stays the same. So we just need to check: "What's the best single move?" and compare it to "no move at all."

## Quick test ideas

- What if there's only 1 color? (Can't move anything useful)
- What if a color only has 1 pen? (Moving it removes that color's score)
- What if moving a pen makes things worse? (We don't do it)
