# nameko-atomicity
This is a dependency that guarantees that nameko's rpc calls are atomic operations.


# Background
This dependency solves two main problems: 
1. If the execution of the main logic fails, 
the saved data or operations need to be rolled back;
2. Ensure that after the main logic is executed successfully, 
other logic is executed or events are thrown.


In response to question (1) how to ensure the integrity of transactions 
between multiple services. As a separate RPC logic can guarantee the transaction, 
but multiple RPC inter-call, there is no way to guarantee the transaction, 
so there is a possibility that the data has been committed, 
the data is modified, and the execution of the later RPC data fails, 
in such a case, it is necessary to roll back the previous data. 
In the call to an RPC (RPC name A), 
you need to call two other service in the RPC (RPC name B and C), 
after the call A, B execution is successful (data has been saved), 
but in C to execute an error, you need to ensure the integrity of the data, 
so you need to roll back the data saved in RPC A (or delete 
or restore the data before the change data).


# Usage

- Solving Problem 1), for example:
```
>>> from nameko.rpc import rpc
... from nameko_atomicity import RollbackCommands
...
... def rollback_function():
...     pass
...
... class ConversionService(object):
...    name = "conversions"
...
...    rollback_commands = RollbackCommands()
...
...    @rpc
...    @rollback_once_failed
...    def inches_to_cm(self, inches):
...        self.rollback_commands.append(
...            func=rollback_function,
...            args=(),
...            kwargs={},
...        )

```

- Solving Problem 2), for example:

```
>>> from nameko.rpc import rpc
>>> from nameko.events import EventDispatcher
>>> from nameko_atomicity import DispatchCommands
...
>>> class ConversionService(object):
...    name = "conversions"
...    dispatch_commands = DispatchCommands()
...
...    @rpc
...    @dispatch_after_commit
...    def inches_to_cm(self, inches):
...        event_name = "booking_updated"
...        dispatch_data = {}
...        self.dispatch_commands.append(
...            func=self.event_dispatcher,
...            args=(event_name, dispatch_data),
...            kwargs={},
...        )
```
