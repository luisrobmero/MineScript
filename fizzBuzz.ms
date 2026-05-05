Steve(20, 10, 5)

Steve.loot(i = 1, i <= 100, i++) {
    Steve.encounter((i % 15) == 0) {
        /chat "FizzBuzz"
    } otherwise {
        Steve.encounter((i % 3) == 0) {
            /chat "Fizz"
        } otherwise {
            Steve.encounter((i % 5) == 0) {
                /chat "Buzz"
            } otherwise {
                /chat i
            }
        }
    }
}