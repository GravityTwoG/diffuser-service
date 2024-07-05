import { Body, Controller, Get, Param, Post } from '@nestjs/common';
import { ApiTags } from '@nestjs/swagger';

import { GenerationRequestDTO } from './dto/generation-request.dto';

import { ImagesService } from './images.service';

@ApiTags('images')
@Controller('/images')
export class ImagesController {
  constructor(private readonly imagesService: ImagesService) {}

  @Post('generate')
  generateImage(@Body() dto: GenerationRequestDTO) {
    return this.imagesService.generateImage(dto);
  }

  @Get('generation/:id')
  getGenerationRequest(@Param('id') id: string) {
    return this.imagesService.getGenerationStatus(id);
  }
}
