import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    
    idx = 0
    n = int(data[idx]); idx += 1
    total = 1 << n  # 2^n участников
    
    # Читаем призовые
    prizes = []
    for i in range(total):
        row = []
        for j in range(n):
            row.append(int(data[idx])); idx += 1
        prizes.append(row)
    
    # dp: current[block_index][local_winner] = макс. сумма внутри блока
    # Изначально каждый участник — отдельный блок
    current = [[0] for _ in range(total)]
    
    for level in range(1, n + 1):
        block_size = 1 << level
        half = block_size >> 1
        next_dp = []
        
        for start in range(0, total, block_size):
            left = current[start // half]
            right = current[(start + half) // half]
            block = [0] * block_size
            
            for i in range(half):
                li = left[i]
                for j in range(half):
                    base = li + right[j]
                    
                    # Левый побеждает
                    if level == 1:
                        val = base
                    else:
                        val = base + prizes[start + half + j][level - 2]
                    if val > block[i]:
                        block[i] = val
                    
                    # Правый побеждает
                    if level == 1:
                        val = base
                    else:
                        val = base + prizes[start + i][level - 2]
                    if val > block[half + j]:
                        block[half + j] = val
            
            next_dp.append(block)
        
        current = next_dp
    
    # Финал: добавляем приз победителю за n побед
    ans = 0
    for i in range(total):
        total_money = current[0][i] + prizes[i][n - 1]
        if total_money > ans:
            ans = total_money
    
    print(ans)


if __name__ == "__main__":
    solve()