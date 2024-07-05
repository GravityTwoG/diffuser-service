import { Body, Controller, Post } from '@nestjs/common';

import { GenerationRequestDTO } from './dto/generation-request.dto';

import { ImagesService } from './images.service';
import { ApiTags } from '@nestjs/swagger';

@ApiTags('images')
@Controller('/images')
export class ImagesController {
  constructor(private readonly imagesService: ImagesService) {}

  @Post('generate')
  generateImage(@Body() dto: GenerationRequestDTO) {
    return this.imagesService.generateImage(dto);
  }
}
