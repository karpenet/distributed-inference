import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial

GPUS = [1, 3, 7]
TASKS = [1, 2, 3, 4, 5, 6]

# Simulate an async download
async def download(task_id):
    print(f"[Task {task_id}] Downloading model weights...")
    await asyncio.sleep(1)  # Simulate I/O
    print(f"[Task {task_id}] Download complete.")

# Inference is compute-bound, we run it in thread pool with exclusive access to a GPU
def infer_model(task_id, gpu_id):
    print(f"[Task {task_id}] Running inference on GPU {gpu_id}...")
    import time
    time.sleep(2)  # Simulate compute
    print(f"[Task {task_id}] Inference complete on GPU {gpu_id}.")

# Simulate an async upload
async def upload_output(task_id):
    print(f"[Task {task_id}] Uploading output...")
    await asyncio.sleep(1)  # Simulate I/O
    print(f"[Task {task_id}] Upload complete.")

async def infer_ondevice(task_id, gpu_queue, executor):
    await download(task_id)

    # Acquire a GPU
    gpu_id = await gpu_queue.get()
    try:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(executor, partial(infer_model, task_id, gpu_id))
    finally:
        gpu_queue.put_nowait(gpu_id)  # Release GPU back to queue

    await upload_output(task_id)

async def main():
    # Use ThreadPoolExecutor for inference
    executor = ThreadPoolExecutor(max_workers=len(GPUS))
    
    # Queue to manage available GPUs
    gpu_queue = asyncio.Queue()
    for gpu in GPUS:
        gpu_queue.put_nowait(gpu)

    # Launch all tasks concurrently
    await asyncio.gather(*(infer_ondevice(task_id, gpu_queue, executor) for task_id in TASKS))

if __name__ == "__main__":
    asyncio.run(main())


