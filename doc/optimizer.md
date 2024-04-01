# Optimizer - AST patterns replacement

The optimizer is a module that takes an AST and applies a set of rules to simplify it.
This file describes the rules used by the optimizer to optimize both constant and non-constant expressions.
Constant expressions such as `2 + 3` are implicitly simplified to `5` by the optimizer.
Non-constant expressions such as `E + E` are simplified to `2 * E` by the optimizer.
Please note that `E` represents any algebraic expression.

## Binary operations

Binary operations are the most complex to simplify, as they can be applied to any two algebraic expressions.

### Rules for commutative operations

- `E + 0` → `E`
- `0 * E` → `0`
- `1 * E` → `E`
- `E + E` → `2 * E`
- `E * E` → `E ^ 2`

### Non-commutative operations

- `E - 0` → `E`
- `0 - E` → `- E`
- `E / 1` → `E`
- `E ^ 0` → `1`
- `E ^ 1` → `E`
- `E - E` → `0`
- `E / E` → `1`

## Unary operations

The unary operations are easy to simplify, as they are only applied to a single operand.

### Rules

- `+ E` → `E`
- `- - E` → `E`
