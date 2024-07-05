import sys
import os
import json

import pika
from dotenv import load_dotenv

from generate_image import generate_image


load_dotenv()

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')

RABBITMQ_USERNAME = os.getenv('RABBITMQ_USERNAME')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')

GENERATION_REQUEST_QUEUE = os.getenv('GENERATION_REQUEST_QUEUE')
IMAGE_GENERATED_QUEUE = os.getenv('IMAGE_GENERATED_QUEUE')

def send_image_generated(
  ch: pika.adapters.blocking_connection.BlockingChannel, 
  generation_id: str, 
  num_images: int,
  image_names: list[str]
):
  # send a message to queue "image_generated"
  image_generated = {
    'generationId': generation_id,
    "status": "GENERATED",
    'imageCount': num_images,
    "imageNames": image_names
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
  generation_request = json.loads(body)

  image_names = generate_image(
    generation_request['prompt'],
    generation_request['generationId'],
    generation_request['imagesCount']
  )
  ch.basic_ack(delivery_tag = method.delivery_tag)
  print(f" [x] Image generated: {generation_request['generationId']}")

  send_image_generated(
    ch, 
    generation_request['generationId'],
    generation_request['imagesCount'],
    image_names
  )
  print(" [x] Sent 'image_generated'")
  

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

