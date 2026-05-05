Steve(20, 10, 5)
Creeper(15, 8)

Steve.mine(Creeper.hp > 0) {
    /attack Steve Creeper
    /attack Creeper Steve
    /chat Creeper.hp
    /chat Steve.hp
}

Steve.encounter(Creeper.hp <= 0) {
    /chat "Steve wins!"
} otherwise {
    /chat "Creeper wins!"
}