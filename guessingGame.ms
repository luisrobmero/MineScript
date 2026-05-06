// === Number Guessing Game ===
Steve(20, 10, 5)

/chat "Steve is trying to guess the secret number!"
/chat "The number is between 1 and 10."

/random secret
Steve.carry(guess, 0)
Steve.carry(attempts, 0)

Steve.mine(guess != secret) {
    /random guess
    Steve.carry(attempts, attempts + 1)
    /chat "Steve guesses:"
    /chat guess
    Steve.encounter(guess < secret) {
        /chat "Too low! Keep trying Steve!"
    } otherwise {
        Steve.encounter(guess > secret) {
            /chat "Too high! Guess again Steve!"
        } otherwise {
            /chat "Steve found the number!"
        }
    }
}

/chat "Steve guessed it in attempts:"
/chat attempts