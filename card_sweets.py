#!/usr/bin/env python3
import math
import sys


def parse_tokens(tokens: list[str], n: int) -> list[int] | None:
    if not tokens:
        return []

    normalized = []
    for token in tokens:
        if token.lower() == "o" or token == "-1":
            normalized.append("0")
        elif token == "...":
            normalized.append("...")
        else:
            try:
                int(token)
                normalized.append(token)
            except ValueError:
                return None

    if normalized[-1] == "...":
        if len(normalized) < 2:
            return None
        fill_value = normalized[-2]
        values = []
        for token in normalized[:-1]:
            if token == "...":
                return None
            values.append(int(token))
        if len(values) > n:
            return None
        values.extend([int(fill_value)] * (n - len(values)))
        return values

    try:
        values = [int(token) for token in normalized]
    except ValueError:
        return None

    if len(values) > n:
        return None
    return values


def parse_input() -> tuple[int, list[int]] | None:
    raw = sys.stdin.read().strip()
    if not raw:
        return None

    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    if not lines:
        return None

    first_line = lines[0].split()
    try:
        n = int(first_line[0])
    except ValueError:
        return None

    if len(lines) == 1:
        cards = parse_tokens(first_line[1:], n)
        return (n, cards) if cards is not None else None

    cards = parse_tokens(lines[1].split(), n)
    return (n, cards) if cards is not None else None


SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def factor_small_primes(value: int, max_prime: int = 97) -> list[int]:
    factors = []
    remaining = value
    for p in SMALL_PRIMES:
        if p > max_prime or p * p > remaining:
            break
        if remaining % p == 0:
            factors.append(p)
            while remaining % p == 0:
                remaining //= p
    if remaining > 1 and remaining <= max_prime:
        factors.append(remaining)
    return factors


def find_card_pair_with_common_prime(cards: list[int]) -> tuple[int, int] | None:
    seen_values: dict[int, int] = {}
    seen_primes: dict[int, int] = {}

    for index, value in enumerate(cards):
        if value <= 1:
            continue
        if value in seen_values:
            return seen_values[value], index
        seen_values[value] = index

        for prime in factor_small_primes(value):
            if prime in seen_primes:
                return seen_primes[prime], index
            seen_primes[prime] = index
    return None


def find_zero_mod_subset(values: list[tuple[int, int]], p: int) -> list[int] | None:
    dp: list[tuple[int, int] | None] = [None] * p
    parent: list[tuple[int, int] | None] = [None] * p

    for idx, (value, orig_index) in enumerate(values):
        r = value % p
        if r == 0:
            return [orig_index]

        new_dp = dp.copy()
        new_parent = parent.copy()

        if new_dp[r] is None:
            new_dp[r] = (-1, idx)
            new_parent[r] = (None, idx)

        for rem, pointer in enumerate(dp):
            if pointer is None:
                continue
            new_rem = (rem + r) % p
            if new_dp[new_rem] is None:
                new_dp[new_rem] = (rem, idx)
                new_parent[new_rem] = (rem, idx)

        dp = new_dp
        parent = new_parent

        if dp[0] is not None:
            subset = []
            current = 0
            while True:
                prev_rem, idx = parent[current]
                subset.append(values[idx][1])
                if prev_rem is None:
                    break
                current = prev_rem
            return subset

    return None


def find_two_disjoint_subsets_mod_p(cards: list[int], p: int) -> tuple[list[int], list[int]] | None:
    divisible_indices = [i for i, value in enumerate(cards) if value % p == 0]
    if len(divisible_indices) >= 2:
        return [divisible_indices[0] + 1], [divisible_indices[1] + 1]

    values = [(value, i) for i, value in enumerate(cards)]
    subset_a = find_zero_mod_subset(values, p)
    if subset_a is None:
        return None

    remaining = [item for item in values if item[1] not in subset_a]
    if not remaining:
        return None

    subset_b = find_zero_mod_subset(remaining, p)
    if subset_b is not None:
        return [i + 1 for i in subset_a], [i + 1 for i in subset_b]

    if divisible_indices:
        single_divisible = divisible_indices[0]
        remaining = [item for item in values if item[1] != single_divisible]
        subset_b = find_zero_mod_subset(remaining, p)
        if subset_b is not None:
            return [single_divisible + 1], [i + 1 for i in subset_b]

    return None


def find_sweet_distribution(cards: list[int]) -> tuple[list[int], list[int]] | None:
    n = len(cards)
    if n < 2:
        return None

    if n <= 28:
        all_mask = (1 << n) - 1
        subset_sums = [0] * (1 << n)
        for mask in range(1, 1 << n):
            lowbit = mask & -mask
            prev_mask = mask ^ lowbit
            pos = lowbit.bit_length() - 1
            subset_sums[mask] = subset_sums[prev_mask] + cards[pos]

        subsets_by_size: list[list[int]] = [[] for _ in range(n + 1)]
        for mask in range(1, 1 << n):
            subsets_by_size[mask.bit_count()].append(mask)

        for total_size in range(n, 1, -1):
            sizes = list(range(1, total_size))
            sizes.sort(key=lambda x: (abs(x - total_size / 2), x))
            for size_a in sizes:
                size_b = total_size - size_a
                for mask_a in subsets_by_size[size_a]:
                    sum_a = subset_sums[mask_a]
                    if sum_a <= 1:
                        continue

                    remaining = all_mask ^ mask_a
                    for submask in subsets_by_size[size_b]:
                        if submask & remaining != submask:
                            continue
                        sum_b = subset_sums[submask]
                        if sum_b > 1 and math.gcd(sum_a, sum_b) > 1:
                            alice_indices = [i + 1 for i in range(n) if mask_a & (1 << i)]
                            bob_indices = [i + 1 for i in range(n) if submask & (1 << i)]
                            return alice_indices, bob_indices
        return None

    pair = find_card_pair_with_common_prime(cards)
    if pair is not None:
        return [pair[0] + 1], [pair[1] + 1]

    prime_candidates = set()
    for value in cards:
        for prime in factor_small_primes(value):
            prime_candidates.add(prime)
    prime_candidates.add(2)
    prime_candidates.add(3)
    prime_candidates = [p for p in sorted(prime_candidates) if p <= 97]

    for p in prime_candidates:
        solution = find_two_disjoint_subsets_mod_p(cards, p)
        if solution is not None:
            return solution

    return None


def main() -> None:
    parsed = parse_input()
    if parsed is None:
        return

    n, cards = parsed
    if len(cards) != n:
        print("no")
        print(0)
        print(0)
        print()
        print()
        return

    solution = find_sweet_distribution(cards)
    if solution is None:
        print("NO")
        print("0 0")
        print()
        print()
        return

    alice_indices, bob_indices = solution
    print("YES")
    print(f"{len(alice_indices)} {len(bob_indices)}")
    print(" ".join(str(index) for index in alice_indices))
    print(" ".join(str(index) for index in bob_indices))


if __name__ == "__main__":
    main()
