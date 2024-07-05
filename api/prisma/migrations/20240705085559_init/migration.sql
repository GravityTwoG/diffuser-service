-- CreateEnum
CREATE TYPE "GenerationStatus" AS ENUM ('PENDING', 'GENERATED', 'FAILED');

-- CreateTable
CREATE TABLE "GenerationRequest" (
    "id" TEXT NOT NULL,
    "status" "GenerationStatus" NOT NULL,
    "prompt" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "GenerationRequest_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Image" (
    "id" TEXT NOT NULL,
    "generationRequestId" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Image_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Image" ADD CONSTRAINT "Image_generationRequestId_fkey" FOREIGN KEY ("generationRequestId") REFERENCES "GenerationRequest"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
