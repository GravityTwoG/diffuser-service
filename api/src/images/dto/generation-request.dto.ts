import { IsInt, IsString } from 'class-validator';

export class GenerationRequestDTO {
  @IsString()
  prompt: string;

  @IsInt()
  imagesCount: number;
}
