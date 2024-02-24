This project is deprecated.

# Durable Serverless
Build serverless stateful applications in python with zero complexity.

Usually, building stateful applications comes with many challenges:
- Data persistence
- Serialization and deserialization
- Spawning background jobs
- Handling failure and retry policies
- Scaling resources

Many of these challanges arise from the fact that we don't trust in-memory state for more than a few seconds, and rightly so. Processes may be closed for many reasons which results in the lose of all the state that was not persisted to disk. But what if we had a solution which enabled us to write simple python code with built-in data structures and trust the state to persist? Combine that with serverless compute which allows to run code in the cloud without taking care of servers. This is Durable.

## Features
- **Stateful** - Use in-memory data structures and simple python functions instead of queues, databases and schedulers to handle complex stateful applications.
- **Durable Execution** - Achive reliability with [Temporal](https://temporal.io/)'s built-in event sourcing and function replay capabilities.
- **Serverless** - Deploy faster without the need to maintain servers.
- **Cost** - Pay-per-use model. Idle long-running functions incur no compute costs.

## Getting Started
- Checkout the [Gettings Started](./GETTING_STARTED.md) guide for a more in-depth explanation.
- Checkout the [Starter Project](https://github.com/danzilberdan/Durable-Serverless-Starter) to see an actual code example.
- Checkout the [Setup Guide](https://github.com/danzilberdan/Durable-Serverless-Starter/blob/main/SETUP.md).

## Stack
The current stack is based on:
- AWS Lambda
- Python for definition of workflows and activities
- Temporal as durable execution engine of choice
