'''
This is a pretty interesting find that I'm using as a reference for an
upcoming project.

Full credit goes to  Krlozanov (http://pguides.net/author/krlozanov/)
Original : http://pguides.net/python-tutorial/python-timeout-a-function/
'''

import sys
import signal


class TimeoutException(Exception):
    '''
    A custom exception we can throw, it doesn't need to do any work.
    It just has to be throwable to break a try-except block.
    '''
    pass


def timeout(timeout_duration, default_return):
    '''
    The timout decorator, this is where it gets good.
    @param timeout_duration:  Allowed runtime of decorated function
    @param default_return:  The value returned if decorated function's runtime
     exceeds timeout_duration
    '''
    def timeout_function(f):
        '''
        Returned by timeout(), takes a function as a parameter.
        @param f: Function automatically passed due to timeout() being used as
         a decorator.
        '''
        def function2(*args, **kwargs):
            '''
            Acts as a wrapper around function f() from timeout_function.
            Provides all of the setup and teardown required to effectively
            implement the desired timeout functionality.
            '''
            def timeout_handler(signum, frame):
                '''
                A function that only exists to raise TimeoutException.
                This function will be provided to signal later to invoke
                if a timeout occurs, thereby raising the TimeoutException
                '''
                raise TimeoutException()

            #Create an "original_handler", this will allow us to reset properly
            #after we are done with signal because signal
            #always returns the preivous handler
            original_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout_duration)  # Set signal to go off
            try:
                # Try to execute the decorated function
                return_value = f(*args, **kwargs)
            except TimeoutException:   # If signal goes off before it completes
                return default_return  # Return the default value
            finally:
                #Put signal back on the original handler we created earlier
                signal.signal(signal.SIGALRM, original_handler)
            signal.alarm(0)      # Deactivate the alarm
            return return_value  # Return the decorated function's return value
        return function2         # Invokes function2 from timeout_function
    return timeout_function      # Invokes timout_function from timeout

'''
Example dummy code below, the stuff up top is where the magic is.
'''


@timeout(3, 'super boring normal name')
def get_name():
    print "Please enter a name:  ",
    name = sys.stdin.readline()
    return name

if __name__ == '__main__':
    print "Got name:  %s" % get_name()
