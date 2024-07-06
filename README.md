# Text To Image

Web-UI for diffusers library.

Implemented with:

- Text To Image service: Python, diffusers, boto3, pika
- REST API: TypeScript, Nest.js, Prisma, PostgreSQL, @golevelup/nestjs-rabbitmq
- Client: TypeScript, Vue3

## RabbitMQ

- list messages statistics

```sh
rabbitmqctl list_queues name messages_ready messages_unacknowledged
```

## Demo

![alt text](image.png)
