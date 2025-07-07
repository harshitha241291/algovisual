import streamlit as st
import matplotlib.pyplot as plt
import random
import time

st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


st.set_page_config(layout="wide")

st.markdown("""
<style>

[data-testid="stSidebar"] {
    background-color: #d7dcd3;
}

html, body, [class*="css"] {
    color: #333333;
    font-family: 'Segoe UI', sans-serif;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 AlgoVisual - Animated Sorting Visualizer")

if "arr" not in st.session_state:
    st.session_state.arr = []
if "steps" not in st.session_state:
    st.session_state.steps = []
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "playing" not in st.session_state:
    st.session_state.playing = False
if "completed" not in st.session_state:
    st.session_state.completed = False
if "sort_type" not in st.session_state:
    st.session_state.sort_type = None


def generate_bubble_sort_steps(arr):
    steps = []
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(n - i - 1):
            steps.append((a.copy(), (j, j+1), False))
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                steps.append((a.copy(), (j, j+1), True))
    return steps

def generate_selection_sort_steps(arr):
    steps = []
    a = arr.copy()
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            steps.append((a.copy(), (min_idx, j), False))
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            steps.append((a.copy(), (i, min_idx), True))
    return steps

def generate_insertion_sort_steps(arr):
    steps = []
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            steps.append((a.copy(), (j, j+1), False))
            a[j + 1] = a[j]
            steps.append((a.copy(), (j, j+1), True))
            j -= 1
        a[j + 1] = key
        steps.append((a.copy(), (j+1,), True))
    return steps

def generate_merge_sort_steps(arr):
    steps = []
    def merge_sort(a, l, r):
        if l < r:
            m = (l + r) // 2
            merge_sort(a, l, m)
            merge_sort(a, m+1, r)
            merge(a, l, m, r)

    def merge(a, l, m, r):
        left = a[l:m+1]
        right = a[m+1:r+1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            steps.append((a.copy(), (k,), False))
            if left[i] <= right[j]:
                a[k] = left[i]
                i += 1
            else:
                a[k] = right[j]
                j += 1
            steps.append((a.copy(), (k,), True))
            k += 1
        while i < len(left):
            a[k] = left[i]
            steps.append((a.copy(), (k,), True))
            i += 1
            k += 1
        while j < len(right):
            a[k] = right[j]
            steps.append((a.copy(), (k,), True))
            j += 1
            k += 1

    a = arr.copy()
    merge_sort(a, 0, len(a)-1)
    return steps

def generate_heap_sort_steps(arr):
    steps = []
    a = arr.copy()

    def heapify(n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and a[l] > a[largest]:
            largest = l
        if r < n and a[r] > a[largest]:
            largest = r
        if largest != i:
            steps.append((a.copy(), (i, largest), False))
            a[i], a[largest] = a[largest], a[i]
            steps.append((a.copy(), (i, largest), True))
            heapify(n, largest)

    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    for i in range(n - 1, 0, -1):
        steps.append((a.copy(), (0, i), False))
        a[i], a[0] = a[0], a[i]
        steps.append((a.copy(), (0, i), True))
        heapify(i, 0)

    return steps

def generate_counting_sort_steps(arr):
    steps = []
    a = arr.copy()
    max_val = max(a)
    count = [0] * (max_val + 1)

    for num in a:
        count[num] += 1
        steps.append((a.copy(), (a.index(num),), False))

    index = 0
    for i in range(len(count)):
        while count[i] > 0:
            a[index] = i
            steps.append((a.copy(), (index,), True))
            index += 1
            count[i] -= 1
    return steps

def generate_radix_sort_steps(arr):
    steps = []
    a = arr.copy()
    max_num = max(a)
    exp = 1
    while max_num // exp > 0:
        counting_sort_exp(a, exp, steps)
        exp *= 10
    return steps

def counting_sort_exp(a, exp, steps):
    n = len(a)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = (a[i] // exp) % 10
        count[index] += 1
        steps.append((a.copy(), (i,), False))

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in reversed(range(n)):
        index = (a[i] // exp) % 10
        output[count[index] - 1] = a[i]
        count[index] -= 1

    for i in range(n):
        a[i] = output[i]
        steps.append((a.copy(), (i,), True))

def generate_bucket_sort_steps(arr):
    steps = []
    a = arr.copy()
    max_val = max(a)
    size = max_val / len(a)

    buckets = [[] for _ in range(len(a))]

    for i in range(len(a)):
        index = int(a[i] / size)
        if index != len(a):
            buckets[index].append(a[i])
        else:
            buckets[len(a) - 1].append(a[i])
        steps.append((a.copy(), (i,), False))

    k = 0
    for bucket in buckets:
        bucket.sort()
        for value in bucket:
            a[k] = value
            steps.append((a.copy(), (k,), True))
            k += 1

    return steps

def generate_quick_sort_steps(arr):
    steps = []
    def quick_sort(a, low, high):
        if low < high:
            pi = partition(a, low, high)
            quick_sort(a, low, pi - 1)
            quick_sort(a, pi + 1, high)

    def partition(a, low, high):
        pivot = a[high]
        i = low - 1
        for j in range(low, high):
            steps.append((a.copy(), (j, high), False))
            if a[j] < pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
                steps.append((a.copy(), (i, j), True))
        a[i+1], a[high] = a[high], a[i+1]
        steps.append((a.copy(), (i+1, high), True))
        return i + 1

    a = arr.copy()
    quick_sort(a, 0, len(a)-1)
    return steps


sort_options = {
    "Bubble Sort": generate_bubble_sort_steps,
    "Selection Sort": generate_selection_sort_steps,
    "Insertion Sort": generate_insertion_sort_steps,
    "Merge Sort": generate_merge_sort_steps,
    "Quick Sort": generate_quick_sort_steps,
    "Heap Sort": generate_heap_sort_steps,
    "Counting Sort": generate_counting_sort_steps,
    "Radix Sort": generate_radix_sort_steps,
    "Bucket Sort": generate_bucket_sort_steps,
}

sort_descriptions = {
    "Bubble Sort": "🔁 Bubble Sort compares adjacent elements and swaps them if they are in the wrong order. This process repeats until the list is sorted. It's simple but inefficient for large data.",
    "Selection Sort": "🔍 Selection Sort selects the smallest element from the unsorted part and places it at the beginning. It continues until all elements are sorted.",
    "Insertion Sort": "🧩 Insertion Sort builds the sorted list one element at a time by inserting each new element into its correct position in the already-sorted part.",
    "Merge Sort": "🧬 Merge Sort is a divide-and-conquer algorithm that splits the list into halves, recursively sorts them, and merges the sorted halves. It's very efficient for large data.",
    "Quick Sort": "⚡ Quick Sort picks a 'pivot' element, partitions the array around it, and recursively applies the same logic. It’s fast and commonly used in practice.",
    "Heap Sort": "🏔️ Heap Sort turns the array into a max heap and repeatedly extracts the maximum element, placing it at the end. It guarantees O(n log n) time.",
    "Counting Sort": "📊 Counting Sort counts the occurrences of each value and uses that to place elements in sorted order. Works only with non-negative integers.",
    "Radix Sort": "🔢 Radix Sort processes digits from least significant to most significant using Counting Sort as a subroutine. Efficient for numbers with many digits.",
    "Bucket Sort": "🪣 Bucket Sort distributes elements into buckets, sorts each bucket, and concatenates them. Works well when input is uniformly distributed."
}


selected_sort = st.sidebar.selectbox(
    "🧮 Choose Sorting Algorithm",
    ["-- Select an algorithm --"] + list(sort_options.keys())
)


if selected_sort != "-- Select an algorithm --":
    st.session_state.sort_type = selected_sort
else:
    st.session_state.sort_type = None



speed = st.sidebar.slider("⏱️ Speed (seconds per step)", 0.05, 1.0, 0.3)


mode = st.sidebar.radio("Input Mode", ["Random", "User Input"])

if mode == "Random":
    size = st.sidebar.slider("Array Size", 5, 30, 10)
    if st.sidebar.button("🔁 Generate Random Array"):
        if not st.session_state.sort_type:
            st.sidebar.warning("⚠️ Please select a sorting algorithm first.")
        else:
            st.session_state.arr = random.sample(range(10, 100), size)
            st.session_state.steps = sort_options[st.session_state.sort_type](st.session_state.arr)
            st.session_state.current_step = 0
            st.session_state.playing = False
            st.session_state.completed = False

elif mode == "User Input":
    user_input = st.sidebar.text_input("Enter comma-separated numbers", key="user_input")
    if st.sidebar.button("📥 Load Array"):
        if not st.session_state.sort_type:
            st.sidebar.warning("⚠️ Please select a sorting algorithm first.")
        else:
            try:
                arr = list(map(int, user_input.split(',')))
                st.session_state.arr = arr
                st.session_state.steps = sort_options[st.session_state.sort_type](arr)
                st.session_state.current_step = 0
                st.session_state.playing = False
                st.session_state.completed = False
            except:
                st.sidebar.error("❌ Invalid input. Please enter valid integers.")



def draw_bars(arr, highlight_idx=None, swap=False):
    fig, ax = plt.subplots(figsize=(10, 4))
    colors = ['#1f77b4'] * len(arr)
    if highlight_idx:
        for idx in highlight_idx:
            if idx < len(colors):
                colors[idx] = '#d62728' if swap else '#ff7f0e'
    bars = ax.bar(range(len(arr)), arr, color=colors)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, str(arr[i]),
                ha='center', va='bottom', fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])
    if arr:
        ax.set_ylim(0, max(arr) * 1.2)
    ax.set_title(f"{st.session_state.sort_type} Visualization", fontsize=14)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    st.pyplot(fig)


if st.session_state.sort_type:
    st.markdown("### ℹ️ About the Algorithm")
    st.info(sort_descriptions[st.session_state.sort_type])


if st.session_state.steps:
    step_idx = st.session_state.current_step
    arr_state, highlight, swapped = st.session_state.steps[step_idx]
    draw_bars(arr_state, highlight_idx=highlight, swap=swapped)
    st.markdown("### 🧾 Current Array State")
    st.code(str(arr_state), language='python')

if st.session_state.sort_type and st.session_state.steps:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if not st.session_state.playing and not st.session_state.completed:
            if st.button("▶ Start"):
                st.session_state.playing = True
                st.rerun()
        elif st.session_state.playing:
            if st.button("⏸ Pause"):
                st.session_state.playing = False
                st.rerun()
        elif not st.session_state.playing and not st.session_state.completed:
            if st.button("🔁 Resume"):
                st.session_state.playing = True
                st.rerun()
    with col2:
        if st.button("⏭ Step"):
            if st.session_state.current_step < len(st.session_state.steps) - 1:
                st.session_state.current_step += 1
            else:
                st.session_state.completed = True
    with col3:
        if st.button("🔄 Reset"):
            st.session_state.current_step = 0
            st.session_state.playing = False
            st.session_state.completed = False
    with col4:
        if st.session_state.completed:
            st.success("✅ Sorting complete!")
else:
    st.warning(" Please select a sorting algorithm and load an array to enable controls.")

if st.session_state.playing and not st.session_state.completed:
    if st.session_state.current_step < len(st.session_state.steps) - 1:
        time.sleep(speed)
        st.session_state.current_step += 1
        st.rerun()
    else:
        st.session_state.playing = False
        st.session_state.completed = True
        st.success("✅ Sorting complete!")
