Steve(20, 10, 5)
Alex("Alex", 5)
Jordan("Jordan", 10)

/greet greeter receiver {
    /chat greeter.name
    /chat "greets"
    /chat receiver.name
    /chat "Welcome, traveler!"
}

Steve.encounter(Alex.level > Jordan.level) {
    /greet Alex Jordan
} otherwise {
    /greet Jordan Alex
}