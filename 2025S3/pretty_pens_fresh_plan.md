# Pretty Pens: ELI5 Solution Plan

## The Idea

Pick the prettiest pen for each color. Add them up.

BUT: try moving ONE pen to a different color. Does it make the total bigger? Keep the best score.

## How It Works

1. **Normal score**: Pick the #1 prettiest pen per color, add them up.
2. **Try a move**: Move one pen to a different color. What's the new score?
3. **Compare**: Keep whichever is bigger.

Example:
```
Normal: Red (10) + Blue (8) + Green (5) = 23
Move blue-9 to red: Red (10+9) + Blue (8→6) + Green (5) = 28 ✓
```

## When Pens Change

If a pen gets a new color or becomes prettier/uglier, recalculate and try again.

After each change, output the best score.
