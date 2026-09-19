import sys
def solve():
    try:
        lines = sys.stdin.read().split()
        if not lines:
            return
        n = int(lines[0])
        a = int(int(x) for x in lines[1:n+1])
        return n, a
    except Exception:
        return None, None


def check_all_count(S, counts, num_groops):
    if num_groops == 1:
        return sum(counts) == S

    n = len(counts)
    for mask in range(1 << len(counts)):
        remaining = []
        subset_sum = 0

        for i in range(n):
            if mask & (1 << i):
                subset_sum += counts[i]
            else:
                remaining.append(counts[i])

        if subset_sum == S:
            if check_all_count(S, remaining, num_groops - 1):
                return True

    return False

def check_counts(n , counts):
    total_sum = 0
    for i in counts:
        total_sum += i

    if total_sum % (n - 1) == 0:
        S = total_sum // (n - 1)
        print(S)
        for i in counts:
            if i <= S:
                continue
            else:
                return "No"

        if check_all_count(S, counts, n-1):
            return "Yes"
        else:
            return "No"
    else:
        return "No"

n, counts = solve()

if n is not None and counts is not None:
    result = check_counts(n, counts)
    print(result)


