import { Injectable } from '@nestjs/common';
import { GenerationStatus } from '@prisma/client';

import { PrismaService } from 'src/prisma/prisma.service';

import { GenerationRequestDTO } from './dto/generation-request.dto';

@Injectable()
export class ImagesService {
  constructor(private readonly prismaService: PrismaService) {}

  async generateImage(dto: GenerationRequestDTO) {
    const request = await this.prismaService.generationRequest.create({
      data: {
        status: GenerationStatus.PENDING,
        prompt: dto.prompt,
      },
    });

    // TODO: add request to queue
    // {
    //   generationId: request.id,
    //   prompt: request.prompt,
    //   numImages: dto.imagesCount,
    // }

    return request;
  }
}
