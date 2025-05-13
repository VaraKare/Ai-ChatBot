# To run Jarvis
import multiprocessing


def startJarvis():
        # Code for process 1
        print("Process 1 is running.")
        from main import start
        start()

# To run hotword
def listenHotword():
        # Code for process 2
        print("Process 2 is running.")
        from engine.features import hotword
        hotword()

    # Start both processes
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=startJarvis)
        p2 = multiprocessing.Process(target=listenHotword)
        p1.start()
        p2.start()
        # p1.join() # if we stoped p1 ,p2 should also stop so we use join

        # if p2.is_alive(): #p1 task got finished and p2 is still alive then terminate
        #     p2.terminate()
        #     p2.join()
        # Allow process 2 to continue running
        try:
            p1.join()  # Wait for process 1 to finish
        except KeyboardInterrupt:
            print("Terminating processes...")
            p1.terminate()
            p2.terminate()
        finally:
            p1.join()
            p2.join()
            print("System stopped.")

