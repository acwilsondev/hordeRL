# Systems

## Income and Spending

- Peasants, crops, and other items grant income.
- Some abilities cost gold to activate.
- Some constructs cost gold to maintain each season.

## Taxes and Failure States

- The king collects taxes at the end of each year.
- Failing to pay taxes can end the game.
- If all peasants die, the game ends.

## (Aspirational) Difficulty Modifier

- A single metric Difficulty *D* is used to determine how many and which types of hordelings appear in raids.
- Difficulty is used to determine the Raid Class, which includes which types of monsters and the number of monster spawners of each type created during a raid.

- Difficulty is proportional to the following:
  - *s* = The season index (spring=1, summer=2...)
  - *y* = The year after start
  - *g* = The projected amount of gold generation (e.g. peasants, crops, cows)

`D = as + by + c(g)^2`

This means that by keeping your gold generation low, you can reduce the difficulty of raids. However see *Tax Modifier*

## Tax Modifier

- A single metric Taxes *T* is used to determine how much taxes the king expects you to pay at the end of each year.
- Taxes is proportal to the following:
  - *y* = the year after start
  - *o* = how much left over you had after last year's taxes (rubber-banding)

`T = FLOOR(ay + bo, tens)`

## Seasonal Cadence

- The horde arrives at the end of each season.
- Seasons are tracked as Spring, Summer, Fall, and Winter.
