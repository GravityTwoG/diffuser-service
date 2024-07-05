import { Injectable } from '@nestjs/common';
import { AmqpConnection, RabbitSubscribe } from '@golevelup/nestjs-rabbitmq';
import { GenerationStatus } from '@prisma/client';

import { PrismaService } from 'src/prisma/prisma.service';

import { GenerationRequestDTO } from './dto/generation-request.dto';
import { ConfigService } from '@nestjs/config';

type GenerationRequest = {
  generationId: string;
  prompt: string;
  imagesCount: number;
};

type GenerationResponse = {
  generationId: string;
  status: GenerationStatus;
  prompt: string;
  imageNames: string[];
};

@Injectable()
export class ImagesService {
  private readonly generationRequestQueue: string;

  constructor(
    private readonly prismaService: PrismaService,
    private readonly amqpConnection: AmqpConnection,
    configService: ConfigService,
  ) {
    this.generationRequestQueue = configService.get('GENERATION_REQUEST_QUEUE');
  }

  async generateImage(dto: GenerationRequestDTO) {
    const request = await this.prismaService.generationRequest.create({
      data: {
        status: GenerationStatus.PENDING,
        prompt: dto.prompt,
      },
    });

    this.addRequestToQueue(request.id, dto);

    return request;
  }

  private addRequestToQueue(
    generationId: string,
    request: GenerationRequestDTO,
  ) {
    const queueElement: GenerationRequest = {
      generationId: generationId,
      prompt: request.prompt,
      imagesCount: request.imagesCount,
    };

    this.amqpConnection.publish('', this.generationRequestQueue, queueElement);
  }

  @RabbitSubscribe({
    exchange: '',
    routingKey: process.env.IMAGE_GENERATED_QUEUE,
    queue: process.env.IMAGE_GENERATED_QUEUE,
  })
  async onGenerationEnd(msg: unknown) {
    const generationResponse: GenerationResponse = JSON.parse(
      JSON.stringify(msg),
    );

    if (generationResponse.status !== GenerationStatus.GENERATED) {
      console.log('Generation failed', generationResponse);
      await this.prismaService.generationRequest.update({
        where: {
          id: generationResponse.generationId,
        },
        data: {
          status: GenerationStatus.FAILED,
        },
      });
      return;
    }

    console.log('Generation succeeded', generationResponse);
    await this.prismaService.generationRequest.update({
      where: {
        id: generationResponse.generationId,
      },
      data: {
        status: GenerationStatus.GENERATED,
        images: {
          createMany: {
            data: generationResponse.imageNames.map((imageName) => ({
              imageName: imageName,
            })),
          },
        },
      },
    });
  }

  async getGenerationStatus(id: string) {
    return this.prismaService.generationRequest.findUnique({
      where: {
        id: id,
      },
      include: {
        images: true,
      },
    });
  }
}
