from collections import deque
import math

# ────────────────────────────────────────────────────────────
# HELPER: Print a simple Gantt Chart
# ────────────────────────────────────────────────────────────
def print_gantt(gantt):
    print("\nGantt Chart:")
    for p in gantt:
        print(f"| {p[0]} ", end="")
    print("|")
    print(gantt[0][1], end="")
    for p in gantt:
        print(f"    {p[2]}", end="")
    print()

# ════════════════════════════════════════════════════════════
#   MODULE 1A — FCFS (First Come First Served)
# ════════════════════════════════════════════════════════════
def fcfs():
    print("\n========== CPU SCHEDULING: FCFS ==========")

    # --- Input ---
    n = int(input("Enter number of processes: "))
    processes = []
    for i in range(n):
        pid = input(f"  Process ID [{i+1}]: ")
        at  = int(input("  Arrival Time: "))
        bt  = int(input("  Burst Time : "))
        processes.append([pid, at, bt])

    # --- Algorithm ---
    processes.sort(key=lambda x: x[1])   # sort by arrival time
    time   = 0
    gantt  = []
    wt_list  = []
    tat_list = []

    print("\nPID\tAT\tBT\tWT\tTAT")
    print("-" * 40)
    for pid, at, bt in processes:
        if time < at:
            time = at           # CPU was idle, jump to arrival
        wt  = time - at
        tat = wt + bt
        gantt.append((pid, time, time + bt))
        wt_list.append(wt)
        tat_list.append(tat)
        print(f"{pid}\t{at}\t{bt}\t{wt}\t{tat}")
        time += bt

    print("-" * 40)
    print(f"Average Waiting Time    : {sum(wt_list)/len(wt_list):.2f}")
    print(f"Average Turnaround Time : {sum(tat_list)/len(tat_list):.2f}")
    print_gantt(gantt)


# ════════════════════════════════════════════════════════════
#   MODULE 1B — SJF (Shortest Job First)
# ════════════════════════════════════════════════════════════
def sjf():
    print("\n========== CPU SCHEDULING: SJF ==========")

    # --- Input ---
    n = int(input("Enter number of processes: "))
    processes = []
    for i in range(n):
        pid = input(f"  Process ID [{i+1}]: ")
        at  = int(input("  Arrival Time: "))
        bt  = int(input("  Burst Time : "))
        processes.append([pid, at, bt])

    # --- Algorithm ---
    time   = 0
    done   = []
    gantt  = []
    remaining = processes[:]

    while remaining:
        # Find all processes that have arrived
        ready = [p for p in remaining if p[1] <= time]
        if not ready:
            time += 1
            continue
        # Pick the one with shortest burst time
        p = min(ready, key=lambda x: x[2])
        remaining.remove(p)
        pid, at, bt = p
        wt  = time - at
        tat = wt + bt
        gantt.append((pid, time, time + bt))
        done.append([pid, at, bt, wt, tat])
        time += bt

    print("\nPID\tAT\tBT\tWT\tTAT")
    print("-" * 40)
    for row in done:
        print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}")
    print("-" * 40)
    print(f"Average Waiting Time    : {sum(r[3] for r in done)/len(done):.2f}")
    print(f"Average Turnaround Time : {sum(r[4] for r in done)/len(done):.2f}")
    print_gantt(gantt)


# ════════════════════════════════════════════════════════════
#   MODULE 1C — Round Robin
# ════════════════════════════════════════════════════════════
def round_robin():
    print("\n========== CPU SCHEDULING: ROUND ROBIN ==========")

    # --- Input ---
    n  = int(input("Enter number of processes: "))
    TQ = int(input("Enter Time Quantum: "))
    processes = []
    for i in range(n):
        pid = input(f"  Process ID [{i+1}]: ")
        at  = int(input("  Arrival Time: "))
        bt  = int(input("  Burst Time : "))
        processes.append({"id": pid, "at": at, "bt": bt})

    # --- Algorithm ---
    processes.sort(key=lambda x: x["at"])
    time         = 0
    queue        = deque()
    remaining_bt = {p["id"]: p["bt"] for p in processes}
    completed    = {}
    gantt        = []
    i            = 0

    while i < len(processes) or queue:
        # Add all processes that have arrived
        while i < len(processes) and processes[i]["at"] <= time:
            queue.append(processes[i]["id"])
            i += 1

        if not queue:
            time += 1
            continue

        current   = queue.popleft()
        start     = time
        exec_time = min(TQ, remaining_bt[current])
        time     += exec_time
        remaining_bt[current] -= exec_time
        gantt.append((current, start, time))

        # Add processes that arrived during execution
        while i < len(processes) and processes[i]["at"] <= time:
            queue.append(processes[i]["id"])
            i += 1

        if remaining_bt[current] > 0:
            queue.append(current)       # not finished, go back in queue
        else:
            completed[current] = time   # finished!

    print("\nPID\tAT\tBT\tCT\tTAT\tWT")
    print("-" * 50)
    total_tat = total_wt = 0
    for p in processes:
        pid = p["id"]; at = p["at"]; bt = p["bt"]
        ct  = completed[pid]
        tat = ct - at
        wt  = tat - bt
        total_tat += tat; total_wt += wt
        print(f"{pid}\t{at}\t{bt}\t{ct}\t{tat}\t{wt}")
    print("-" * 50)
    print(f"Average Turnaround Time : {total_tat/n:.2f}")
    print(f"Average Waiting Time    : {total_wt/n:.2f}")
    print_gantt(gantt)


# ════════════════════════════════════════════════════════════
#   MODULE 1D — Priority Scheduling
# ════════════════════════════════════════════════════════════
def priority_scheduling():
    print("\n========== CPU SCHEDULING: PRIORITY ==========")
    print("(Lower priority number = Higher priority)")

    # --- Input ---
    n = int(input("Enter number of processes: "))
    processes = []
    for i in range(n):
        pid = input(f"  Process ID [{i+1}]: ")
        at  = int(input("  Arrival Time: "))
        bt  = int(input("  Burst Time : "))
        pr  = int(input("  Priority   : "))
        processes.append([pid, at, bt, pr])

    # --- Algorithm ---
    time      = 0
    done      = []
    gantt     = []
    remaining = processes[:]

    while remaining:
        ready = [p for p in remaining if p[1] <= time]
        if not ready:
            time += 1
            continue
        # Pick process with highest priority (lowest number)
        p = min(ready, key=lambda x: x[3])
        remaining.remove(p)
        pid, at, bt, pr = p
        wt  = time - at
        tat = wt + bt
        gantt.append((pid, time, time + bt))
        done.append([pid, at, bt, pr, wt, tat])
        time += bt

    print("\nPID\tAT\tBT\tPR\tWT\tTAT")
    print("-" * 48)
    for r in done:
        print(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\t{r[5]}")
    print("-" * 48)
    print(f"Average Waiting Time    : {sum(r[4] for r in done)/len(done):.2f}")
    print(f"Average Turnaround Time : {sum(r[5] for r in done)/len(done):.2f}")
    print_gantt(gantt)


# ════════════════════════════════════════════════════════════
#   MODULE 2 — MEMORY PAGING
# ════════════════════════════════════════════════════════════
def memory_paging():
    print("\n========== MEMORY MANAGEMENT: PAGING ==========")

    # --- Input ---
    page_size  = int(input("Enter Page Size (KB): "))
    phys_mem   = int(input("Enter Physical Memory Size (KB): "))
    total_frames = phys_mem // page_size
    print(f"  → Total Frames Available: {total_frames}")

    n = int(input("Enter number of processes: "))
    processes = []
    for i in range(n):
        pid  = input(f"  Process ID [{i+1}]: ")
        size = int(input("  Process Size (KB): "))
        processes.append([pid, size])

    # --- Allocation ---
    frame_counter = 0
    print("\n--- Page Tables ---")
    print(f"{'Process':<10}{'Pages':<8}{'Frames Allocated'}")
    print("-" * 40)

    total_used = 0
    for pid, size in processes:
        pages_needed = math.ceil(size / page_size)
        if frame_counter + pages_needed > total_frames:
            print(f"{pid:<10}  --> NOT ENOUGH FRAMES!")
            continue
        frames = list(range(frame_counter, frame_counter + pages_needed))
        frame_counter += pages_needed
        total_used    += pages_needed
        mapping = "  ".join(f"P{j}->F{frames[j]}" for j in range(len(frames)))
        print(f"{pid:<10}{pages_needed:<8}{mapping}")

    free_frames = total_frames - total_used
    print("-" * 40)
    print(f"Total Frames : {total_frames}")
    print(f"Used Frames  : {total_used}")
    print(f"Free Frames  : {free_frames}")
    print(f"Internal Fragmentation ≈ {free_frames * page_size} KB")


# ════════════════════════════════════════════════════════════
#   MODULE 3 — PAGE REPLACEMENT
# ════════════════════════════════════════════════════════════
def page_replacement():
    print("\n========== PAGE REPLACEMENT ==========")

    # --- Input ---
    n_frames = int(input("Enter number of frames: "))
    ref_str  = input("Enter reference string (space-separated): ")
    ref      = list(map(int, ref_str.split()))

    print("\nChoose Algorithm:")
    print("  1. FIFO")
    print("  2. LRU")
    print("  3. Optimal")
    choice = input("Enter choice (1/2/3): ")

    frames = []
    faults = 0
    history = []

    # ── FIFO ──
    if choice == "1":
        print("\n--- FIFO Page Replacement ---")
        for page in ref:
            fault = page not in frames
            if fault:
                faults += 1
                if len(frames) < n_frames:
                    frames.append(page)
                else:
                    frames.pop(0)         # remove oldest page
                    frames.append(page)
            history.append((page, frames[:], fault))

    # ── LRU ──
    elif choice == "2":
        print("\n--- LRU Page Replacement ---")
        for i, page in enumerate(ref):
            fault = page not in frames
            if fault:
                faults += 1
                if len(frames) < n_frames:
                    frames.append(page)
                else:
                    # Find least recently used page
                    lru = min(frames,
                              key=lambda p: max((j for j, r in enumerate(ref[:i]) if r == p), default=-1))
                    frames[frames.index(lru)] = page
            history.append((page, frames[:], fault))

    # ── Optimal ──
    elif choice == "3":
        print("\n--- Optimal Page Replacement ---")
        for i, page in enumerate(ref):
            fault = page not in frames
            if fault:
                faults += 1
                if len(frames) < n_frames:
                    frames.append(page)
                else:
                    # Replace page used farthest in the future
                    future = []
                    for f in frames:
                        try:    future.append(ref[i+1:].index(f))
                        except: future.append(float('inf'))   # never used again
                    frames[future.index(max(future))] = page
            history.append((page, frames[:], fault))

    else:
        print("Invalid choice!"); return

    # --- Display Table ---
    print(f"\n{'Page':<6}", end="")
    for i in range(n_frames):
        print(f"F{i:<5}", end="")
    print("Fault?")
    print("-" * (6 + n_frames*6 + 7))

    for page, state, fault in history:
        print(f"{page:<6}", end="")
        for i in range(n_frames):
            val = state[i] if i < len(state) else "-"
            print(f"{str(val):<6}", end="")
        print("FAULT" if fault else "  hit")

    hits = len(ref) - faults
    print("-" * (6 + n_frames*6 + 7))
    print(f"Total References : {len(ref)}")
    print(f"Page Faults      : {faults}")
    print(f"Page Hits        : {hits}")
    print(f"Hit Rate         : {hits/len(ref)*100:.2f}%")
    print(f"Fault Rate       : {faults/len(ref)*100:.2f}%")


# ════════════════════════════════════════════════════════════
#   MODULE 4 — PROCESS SYNCHRONIZATION (Dining Philosophers)
# ════════════════════════════════════════════════════════════
def dining_philosophers():
    print("\n========== PROCESS SYNCHRONIZATION: DINING PHILOSOPHERS ==========")

    n      = int(input("Enter number of philosophers (e.g. 5): "))
    rounds = int(input("Enter number of simulation rounds: "))

    # State: 0=Thinking, 1=Hungry, 2=Eating
    states = ["Thinking"] * n
    forks  = [True] * n     # True = fork available
    log    = []

    import random

    # --- Semaphore simulation ---
    # A semaphore controls access to shared resources (forks).
    # wait(s)  = acquire the resource (decrement). Blocks if 0.
    # signal(s) = release the resource (increment).
    # Here each fork is a binary semaphore: 1=available, 0=in-use.

    semaphore = [1] * n   # 1 fork semaphore per philosopher position

    def wait(fork_id):
        """Acquire fork (semaphore wait/P operation)"""
        if semaphore[fork_id] == 1:
            semaphore[fork_id] = 0    # lock the fork
            return True
        return False    # fork not available, must wait

    def signal(fork_id):
        """Release fork (semaphore signal/V operation)"""
        semaphore[fork_id] = 1        # unlock the fork

    print("\n--- Semaphore State: 1=Available, 0=In Use ---")
    print(f"Initial: {semaphore}")
    print("\n--- Simulation Log ---")

    for _ in range(rounds):
        i     = random.randint(0, n - 1)
        left  = i
        right = (i + 1) % n

        if states[i] == "Thinking":
            states[i] = "Hungry"
            msg = f"P{i+1} is now Hungry"

        elif states[i] == "Hungry":
            # Try to acquire both forks using semaphore wait()
            got_left  = wait(left)
            got_right = wait(right) if got_left else False
            if got_left and got_right:
                states[i] = "Eating"
                forks[left] = forks[right] = False
                msg = f"P{i+1} wait(Fork{left}) ✓  wait(Fork{right}) ✓  →  Now Eating"
            else:
                # Could not get both — release any acquired (avoid deadlock)
                if got_left: signal(left)
                msg = f"P{i+1} Hungry but Fork{right} busy → waiting (blocked)"

        elif states[i] == "Eating":
            # Release both forks using semaphore signal()
            signal(left); signal(right)
            forks[left] = forks[right] = True
            states[i]   = "Thinking"
            msg = f"P{i+1} signal(Fork{left}) ✓  signal(Fork{right}) ✓  →  Now Thinking"

        else:
            msg = f"P{i+1} waiting..."

        print(f"  {msg}")
        print(f"  Semaphores: {semaphore}")
        log.append(msg)

    print("\n--- Final States ---")
    print(f"{'Philosopher':<14}{'State'}")
    print("-" * 28)
    for i in range(n):
        print(f"P{i+1:<13}{states[i]}")

    print("\n--- Fork Status ---")
    for i in range(n):
        status = "Available" if forks[i] else "In Use"
        print(f"Fork {i}: {status}")


# ════════════════════════════════════════════════════════════
#   MODULE 5 — DEADLOCK: BANKER'S ALGORITHM
# ════════════════════════════════════════════════════════════
def bankers_algorithm():
    print("\n========== DEADLOCK HANDLING: BANKER'S ALGORITHM ==========")

    # --- Input ---
    n = int(input("Enter number of processes  : "))
    r = int(input("Enter number of resource types: "))

    print(f"\nEnter Available resources ({r} values): ", end="")
    available = list(map(int, input().split()))

    print(f"\nEnter MAX matrix ({n} rows, {r} values each):")
    max_mat = []
    for i in range(n):
        print(f"  P{i} Max  : ", end="")
        max_mat.append(list(map(int, input().split())))

    print(f"\nEnter ALLOCATION matrix ({n} rows, {r} values each):")
    alloc_mat = []
    for i in range(n):
        print(f"  P{i} Alloc: ", end="")
        alloc_mat.append(list(map(int, input().split())))

    # --- Compute Need = Max - Allocation ---
    need = [[max_mat[i][j] - alloc_mat[i][j] for j in range(r)] for i in range(n)]

    print("\n--- Need Matrix (Max - Allocation) ---")
    header = "Proc  " + "  ".join(f"R{j}" for j in range(r))
    print(header)
    print("-" * len(header))
    for i in range(n):
        row = "  ".join(str(need[i][j]) for j in range(r))
        print(f"P{i}    {row}")

    # --- Safety Algorithm ---
    work   = list(available)
    finish = [False] * n
    safe_seq = []

    for _ in range(n):
        for i in range(n):
            # Can P(i) complete with current available resources?
            if not finish[i] and all(need[i][j] <= work[j] for j in range(r)):
                finish[i] = True
                safe_seq.append(f"P{i}")
                # Release resources back to work
                work = [work[j] + alloc_mat[i][j] for j in range(r)]
                break

    # --- Resource Allocation Table (required output) ---
    print("\n--- Resource Allocation Table ---")
    col_h = "  ".join(f"R{j}" for j in range(r))
    print(f"{'Proc':<7}{'Allocation':<{r*4+4}}{'Max':<{r*4+4}}{'Need':<{r*4+4}}{'Available'}")
    print("-" * (7 + (r*4+4)*3 + r*4))
    for i in range(n):
        a_str = "  ".join(str(alloc_mat[i][j]) for j in range(r))
        m_str = "  ".join(str(max_mat[i][j])   for j in range(r))
        n_str = "  ".join(str(need[i][j])       for j in range(r))
        av_str = ("  ".join(str(available[j]) for j in range(r))) if i == 0 else ""
        print(f"P{i:<6}{a_str:<{r*4+4}}{m_str:<{r*4+4}}{n_str:<{r*4+4}}{av_str}")

    print("\n--- Need Matrix (Max - Allocation) ---")
    print(f"{'Proc':<7}" + "  ".join(f"R{j}" for j in range(r)))
    print("-" * (7 + r*4))
    for i in range(n):
        row = "  ".join(str(need[i][j]) for j in range(r))
        print(f"P{i:<6}{row}")

    # --- Result ---
    print("\n--- Result ---")
    if len(safe_seq) == n:
        print("✅  SYSTEM IS IN SAFE STATE")
        print("Safe Sequence: " + " → ".join(safe_seq))
    else:
        print("❌  DEADLOCK DETECTED! No safe sequence found.")
        unfinished = [f"P{i}" for i in range(n) if not finish[i]]
        print("Deadlocked Processes:", ", ".join(unfinished))


# ════════════════════════════════════════════════════════════
#   MODULE 6 — FILE MANAGEMENT
# ════════════════════════════════════════════════════════════
def file_management():
    print("\n========== FILE MANAGEMENT ==========")
    print("Choose Allocation Method:")
    print("  1. Sequential (Contiguous)")
    print("  2. Linked")
    print("  3. Indexed")
    choice = input("Enter choice (1/2/3): ")

    total_blocks = int(input("Enter total number of disk blocks: "))
    n = int(input("Enter number of files: "))

    files = []
    for i in range(n):
        name  = input(f"  File {i+1} name : ")
        size  = int(input("  File size (blocks): "))
        files.append([name, size])

    # --- Allocate blocks ---
    used   = 0
    alloc  = {}
    for name, size in files:
        if used + size > total_blocks:
            print(f"  ⚠ Not enough blocks for {name}!")
            break
        alloc[name] = list(range(used, used + size))
        used += size

    # --- Display based on method ---
    print(f"\n--- Disk Block Map (0 to {total_blocks-1}) ---")
    # Show a simple text map
    block_owner = {}
    for name, blocks in alloc.items():
        for b in blocks: block_owner[b] = name[0]   # first char as label
    line = ""
    for b in range(total_blocks):
        label = block_owner.get(b, ".")
        line += f"[{label}]"
    print(line)
    print("(. = Free)")

    print(f"\n--- Allocation Table ({['Sequential','Linked','Indexed'][int(choice)-1]}) ---")
    print(f"{'File':<14}{'Start':<8}{'Size':<8}{'Details'}")
    print("-" * 55)

    for name, blocks in alloc.items():
        if choice == "1":
            # Sequential: contiguous blocks
            detail = f"Blocks {blocks[0]} to {blocks[-1]} (contiguous)"

        elif choice == "2":
            # Linked: chain of blocks with pointers
            chain = " → ".join(str(b) for b in blocks) + " → NULL"
            detail = f"Chain: {chain}"

        elif choice == "3":
            # Indexed: first block is index block
            index_block = blocks[0]
            data_blocks = blocks[1:]
            detail = f"Index Block: {index_block}  |  Data: {data_blocks}"

        else:
            detail = "Invalid method"

        print(f"{name:<14}{blocks[0]:<8}{len(blocks):<8}{detail}")

    print("-" * 55)
    print(f"Total Blocks: {total_blocks}   Used: {used}   Free: {total_blocks - used}")


# ════════════════════════════════════════════════════════════
#   MAIN MENU
# ════════════════════════════════════════════════════════════
def main():
    while True:
        print("\n" + "=" * 55)
        print("       MINI OS SIMULATOR. Choose a module to run:")
        print("=" * 55)
        print("  1.  CPU Scheduling — FCFS")
        print("  2.  CPU Scheduling — SJF")
        print("  3.  CPU Scheduling — Round Robin")
        print("  4.  CPU Scheduling — Priority")
        print("  5.  Memory Management — Paging")
        print("  6.  Memory Management — First Fit / Best Fit / Worst Fit")
        print("  7.  Page Replacement (FIFO / LRU / Optimal)")
        print("  8.  Process Synchronization — Dining Philosophers (with Semaphore)")
        print("  9.  Deadlock — Banker's Algorithm")
        print("  10. File Management — Disk Allocation")
        print("  0.  Exit")
        print("=" * 55)

        choice = input("Enter your choice: ").strip()

        if   choice == "1":  fcfs()
        elif choice == "2":  sjf()
        elif choice == "3":  round_robin()
        elif choice == "4":  priority_scheduling()
        elif choice == "5":  memory_paging()
        elif choice == "6":  memory_fit()
        elif choice == "7":  page_replacement()
        elif choice == "8":  dining_philosophers()
        elif choice == "9":  bankers_algorithm()
        elif choice == "10": file_management()
        elif choice == "0":
            print("\nGoodbye!"); break
        else:
            print("Invalid choice. Please try again.")




# ════════════════════════════════════════════════════════════
#   BONUS: MEMORY MANAGEMENT — FIRST FIT / BEST FIT / WORST FIT
#   (2nd memory method)
# ════════════════════════════════════════════════════════════
def memory_fit():
    print("\n========== MEMORY MANAGEMENT: FIT ALGORITHMS ==========")
    print("Choose Method:")
    print("  1. First Fit")
    print("  2. Best Fit")
    print("  3. Worst Fit")
    choice = input("Enter choice (1/2/3): ")

    n_blocks = int(input("Enter number of memory blocks: "))
    blocks = []
    for i in range(n_blocks):
        size = int(input(f"  Block {i} size (KB): "))
        blocks.append(size)

    n_procs = int(input("Enter number of processes: "))
    processes = []
    for i in range(n_procs):
        pid  = input(f"  Process ID [{i+1}]: ")
        size = int(input("  Process size (KB): "))
        processes.append([pid, size])

    # allocation[i] = block index assigned to process i (-1 = not allocated)
    allocation = [-1] * n_procs
    remaining  = blocks[:]      # remaining space in each block

    for i, (pid, psize) in enumerate(processes):
        chosen = -1

        if choice == "1":   # First Fit — pick first block that fits
            for j in range(len(remaining)):
                if remaining[j] >= psize:
                    chosen = j; break

        elif choice == "2": # Best Fit — pick smallest block that fits
            best = -1
            for j in range(len(remaining)):
                if remaining[j] >= psize:
                    if best == -1 or remaining[j] < remaining[best]:
                        best = j
            chosen = best

        elif choice == "3": # Worst Fit — pick largest block
            worst = -1
            for j in range(len(remaining)):
                if remaining[j] >= psize:
                    if worst == -1 or remaining[j] > remaining[worst]:
                        worst = j
            chosen = worst

        if chosen != -1:
            allocation[i] = chosen
            remaining[chosen] -= psize

    # --- Output ---
    methods = {"1": "First Fit", "2": "Best Fit", "3": "Worst Fit"}
    print(f"\n--- {methods.get(choice,'?')} Allocation Result ---")
    print(f"{'Process':<10}{'Size':<10}{'Block':<10}{'Status'}")
    print("-" * 44)
    for i, (pid, psize) in enumerate(processes):
        if allocation[i] == -1:
            print(f"{pid:<10}{psize:<10}{'None':<10}NOT ALLOCATED")
        else:
            print(f"{pid:<10}{psize:<10}{allocation[i]:<10}Allocated")

    print(f"\n--- Memory Block Status After Allocation ---")
    print(f"{'Block':<8}{'Original':<12}{'Used':<10}{'Remaining':<12}{'Fragmentation'}")
    print("-" * 56)
    for j in range(len(blocks)):
        used = blocks[j] - remaining[j]
        print(f"{j:<8}{blocks[j]:<12}{used:<10}{remaining[j]:<12}{remaining[j]} KB wasted")

    total_frag = sum(remaining)
    print(f"\nTotal Internal Fragmentation: {total_frag} KB")

# ── Start ──
if __name__ == "__main__":
    main()
