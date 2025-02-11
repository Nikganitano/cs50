// Determines the reading grade level of a text using the Coleman-Liau index - Problem set 2 (2/3)

#include <ctype.h>
#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Prompt the user for some text
    string text = get_string("Text: ");

    // Count the number of letters, words, and sentences in the text
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // Compute the Coleman-Liau index
    float L = (100.0 * letters) / words;
    float S = (100.0 * sentences) / words;
    int grade = round(0.0588 * L - 0.296 * S - 15.8);

    // Print the grade level
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

int count_letters(string text)
{
    // Return the number of letters in text
    int count = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        char lower = tolower(text[i]);
        if (isalpha(lower))
        {
            count++;
        }
    }
    return count;
}

int count_words(string text)
{
    int count = 1; // Start from 1 because a sentence will contain at least one word
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (text[i] == ' ')
        {
            count++;
        }
    }
    return count;
}

int count_sentences(string text)
{
    int count = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            count++;
        }
    }
    return count;
}
