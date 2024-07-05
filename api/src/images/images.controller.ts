import { Controller, Post } from '@nestjs/common';

import { GenerationRequestDTO } from './dto/generation-request.dto';

import { ImagesService } from './images.service';

@Controller('/images')
export class ImagesController {
  constructor(private readonly imagesService: ImagesService) {}

  @Post('generate')
  generateImage(dto: GenerationRequestDTO) {
    return this.imagesService.generateImage(dto);
  }
}
