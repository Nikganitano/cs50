// Scores the words based on the Scrabble game rules and determines the winner - Problem set 2 (1/3)

#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Prompt the user for two words
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Compute the score of each word
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    // Keep track of score
    int score = 0;

    // Compute score for each character
    for (int i = 0, len = strlen(word); i < len; i++)
    {
        if (isupper(word[i]))
        {
            // If it is uppercase letter subtract the ASCII value of 'A' from the letter to get the index of the letter in the POINTS array
            score += POINTS[word[i] - 'A'];
        }
        else if (islower(word[i]))
        {
            // If it is lowercase letter subtract the ASCII value of 'a' from the letter to get the index of the letter in the POINTS array
            score += POINTS[word[i] - 'a'];
        }
        else
        {
            // If it's not a letter, it contributes zero points
            score += 0;
        }
    }

    return score;
}
