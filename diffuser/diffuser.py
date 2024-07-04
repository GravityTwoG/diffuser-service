from generate_image import generate_image
import json

import pika
import sys
import os

RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672

RABBITMQ_USERNAME = 'admin'
RABBITMQ_PASSWORD = '12121212'

GENERATION_REQUEST_QUEUE = 'image_generation_requests'
IMAGE_GENERATED_QUEUE = 'image_generation_responses'

def send_image_generated(
  ch: pika.adapters.blocking_connection.BlockingChannel, 
  generation_id: str, 
  num_images: int,
):
  # send a message to queue "image_generated"
  image_generated = {
    "status": "done",
    'generation_id': generation_id,
    'image_count': num_images
  }
  ch.basic_publish(
    exchange='',
    routing_key=IMAGE_GENERATED_QUEUE,
    body=json.dumps(image_generated),
  )


def handle_generation_request(
  ch: pika.adapters.blocking_connection.BlockingChannel, 
  method: pika.spec.Basic.Deliver, 
  properties: pika.spec.BasicProperties, 
  body: str,
):
  print(f" [x] Received {body}")
  generate_request = json.loads(body)
  
  generate_image(
    generate_request['prompt'],
    generate_request['generation_id'],
    generate_request['num_images']
  )
  ch.basic_ack(delivery_tag = method.delivery_tag)
  print(f" [x] Image generated: {generate_request['generation_id']}")

  send_image_generated(
    ch, 
    generate_request['generation_id'], 
    generate_request['num_images'],
  )
  print(" [x] Sent 'image_generated'")
  

def send_generation_request(
  ch: pika.adapters.blocking_connection.BlockingChannel,
):
  # send a message to queue "generate_image"
  generate_image_request = {
    "prompt": "A black and white image",
    "generation_id": "1234",
    "num_images": 1
  }
  ch.basic_publish(
    exchange='',
    routing_key=GENERATION_REQUEST_QUEUE,
    body=json.dumps(generate_image_request),
    properties=pika.BasicProperties(
      delivery_mode=pika.DeliveryMode.Persistent
    )
  )


def main():

  credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)

  connection = pika.BlockingConnection(pika.ConnectionParameters(
    RABBITMQ_HOST, RABBITMQ_PORT, 
    credentials=credentials,
  ))

  channel = connection.channel()
  print("Connected to RabbitMQ")
  # don't dispatch a new message to a worker until it has processed and acknowledged the previous one
  channel.basic_qos(prefetch_count=1)

  # create a queue (idempotent operation)
  channel.queue_declare(queue=GENERATION_REQUEST_QUEUE, durable=True)
  channel.queue_declare(queue=IMAGE_GENERATED_QUEUE, durable=True)

  send_generation_request(channel)

  # receive messages
  channel.basic_consume(
    queue=GENERATION_REQUEST_QUEUE,
    auto_ack=False,
    on_message_callback=handle_generation_request,
  )

  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()

  # flush all buffers and close connection
  connection.close()


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print('Interrupted')
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)

'''
Generate image message:
{
  "prompt": string,
  "generation_id": uuid,
  "num_images": int
}
'''