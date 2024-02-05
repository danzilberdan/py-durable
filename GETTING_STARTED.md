# Getting Started
## Introduction to Durable Execution
Durable execution allows executing simple functions that use in-memory data structures in a way that persists the functions state automatically. The function's state is restored by replaying the history of recorded events. From that point on, the function can continue running as usual.

This abstraction, allows developers to define long-running functions that can run for weeks and months while holding internal state. The development of these long-running functions can be much simpler than writing the needed boilerplate in order to implement the same state preserving functionality with tools like databases, queues, schedulers, etc. These tools still have their place when they are needed for their specific benefits.

### Workflows
Workflows represent long-running functions.
For their state to be restorable, they need to be deterministic. This means that executing the workflow multiple times with the same order of events, will yield the same result.
Any functionality that uses randomnes, network or clock time is not deterministic thus replaying the history of events will yield a different state and shouldn't be used in workflows.

### Activities
Activities are pieces of non-deterministic functionality. For example, a call to a network endpoint can yield different results each time it is executed. When a workflow executes an activity, the activity's result is persisted to the workflow's event history. This way, when the workflow is restored and the events will be replayed, the activity will not actually execute. Instead, it's previous result will be injected back to the workflow function.

## Serverless
Serverless execution is an abstraction that enables developers to write and deploy functions to the cloud. Managing servers and scheduling the execution of those functions is done by the cloud provider

## Project Setup
- Checkout the [Starter Project](https://github.com/danzilberdan/Durable-Serverless-Starter) to see the an actual code example.
- Checkout the [Setup Guide](https://github.com/danzilberdan/Durable-Serverless-Starter/blob/main/SETUP.md).

## SDK docs
You can checkout more in-depth examples of durable function development in Temporal's python [sdk docs](https://docs.temporal.io/dev-guide/python).
