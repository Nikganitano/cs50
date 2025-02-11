// Recover JPEGs from card.raw - Problem set 4 (3/3)

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Create a buffer for a block of data
    uint8_t buffer[512];
    int fileCount = 0;
    FILE *currentFile = NULL;
    char filename[8];

    // While there's still data left to read from the memory card
    while (fread(buffer, 1, 512, card) == 512)
    {
        // Check if the start of a new JPEG is found
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // Close the current file if it exists
            if (currentFile != NULL)
            {
                fclose(currentFile);
            }

            // Create a new JPEG file
            sprintf(filename, "%03i.jpg", fileCount++);
            currentFile = fopen(filename, "w");
            if (currentFile == NULL)
            {
                printf("Could not create output file.\n");
                return 1;
            }
        }

        // Write the buffer to the current file if it exists
        if (currentFile != NULL)
        {
            fwrite(buffer, 1, 512, currentFile);
        }
    }

    // Close any remaining files
    if (currentFile != NULL)
    {
        fclose(currentFile);
    }

    // Close the memory card file
    fclose(card);

    return 0;
}