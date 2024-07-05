import { Body, Controller, Get, Param, Post } from '@nestjs/common';
import { ApiTags } from '@nestjs/swagger';

import { GenerationRequestDTO } from './dto/generation-request.dto';
import { GeneratedImagesDTO } from './dto/generated-images.dto';

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
  async getGenerationRequest(
    @Param('id') id: string,
  ): Promise<GeneratedImagesDTO> {
    const result = await this.imagesService.getGeneratedImages(id);

    return {
      id: result.id,
      status: result.status,
      prompt: result.prompt,
      images: result.images.map(
        (image) => `${image.imagePath}/${image.imageName}`,
      ),
    };
  }
}
