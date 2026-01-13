# Systems

## Economy

### Gold Flow

**Income**: Peasants, crops, and other items generate gold.
**Costs**: Some abilities cost gold to activate.
**Upkeep**: Some advanced constructs cost gold each season.

---

## Time

### Seasons

- Spring → Summer → Fall → Winter
- A raid happens at the end of each season.

### Year End

- Taxes are collected at the end of each year.

---

## Loss Conditions

- If all peasants die, you lose.
- If you can’t pay taxes, you lose.

---

## Raids & Difficulty (Aspirational)

### Difficulty Metric (D)

Difficulty determines the **Raid Class**, which controls:

- which hordeling types can appear
- how many spawners of each type spawn

Inputs:

- `s` = season index (Spring=1, Summer=2, Fall=3, Winter=4)
- `y` = years since start
- `i` = projected income generation rate

**Formula**
`D = a*s + b*y + c*(i)^2`

Design Note

- Higher income rate increases raid difficulty.
- This is balanced against taxes (below).

---

## Taxes

### Taxes Metric (T)

Taxes determine how much gold is owed at year end.

Inputs:

- `y` = years since start
- `o` = leftover gold after last year’s taxes (rubber-banding)

**Formula**
`T = FLOOR(a*y + b*o, tens)`
