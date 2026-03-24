import time
import hou

# Long process
def long_process():
    with hou.InterruptableOperation("Running My Function", open_interrupt_dialog=True) as operation:
        total_steps = 10
        for i in range(total_steps):
            # Simulate some work
            time.sleep(0.5)

            # Update progress
            operation.updateProgress(float(i+1)/total_steps)

            # Optional: update the text
            operation.updateLongProgress(i)

long_process()
