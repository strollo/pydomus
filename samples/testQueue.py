from context import *
import time
import random

def consumer(queue):
    print 'Received queue'
    for i in range(1000):
        queue.push('Elem %d' % i)

def producer(queue):
    print 'Received queue'
    while(True):
        time.sleep(random.randint(0,2))
        print 'Found: %s' % queue.pop()
    pass

def main():
    print 'starting'
    queue = SyncQueue()
    tc = threading.Thread(target=consumer, args=(queue,))
    tc.daemon = True
    tc.start()
    tp = threading.Thread(target=producer, args=(queue,))
    tp.daemon = True
    tp.start()

    try:
        while True:
            # print 'still here'
            tc.join(600)
            tp.join(600)
            if not tc.isAlive():
                break
            if not tp.isAlive():
                break
    except KeyboardInterrupt:
        print "Ctrl-c pressed ..."
        print "Closing connections"
        sys.exit(1)

if __name__ == '__main__':
    main()