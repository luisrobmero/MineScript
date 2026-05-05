// ==========================================
// MineScript: A Minecraft Story
// ==========================================

Steve(20, 1, 0)

// === Act 1: Spawn ===
/chat "=========================================="
/chat "A MINECRAFT STORY"
/chat "=========================================="
/chat ""
/chat "=== Act 1: Spawn ==="
/chat "Steve has spawned into a new world."
/chat "He must gather resources to survive."

Steve.carry(wood, 0)
Steve.carry(stone, 0)
Steve.carry(food, 0)

Steve.loot(i = 1, i <= 5, i++) {
    Steve.carry(wood, wood + 2)
    Steve.carry(stone, stone + 3)
    Steve.carry(food, food + 1)
}

/chat "Steve gathered some resources."
/chat "Wood collected:"
/chat wood
/chat "Stone collected:"
/chat stone
/chat "Food collected:"
/chat food

// Night is falling, time to sleep
/chat ""
/chat "Night is falling..."
/chat "Steve finds shelter and sleeps."
/sleep

// === Act 2: First Night ===
/chat ""
/chat "=== Act 2: First Night ==="
/chat "A Zombie has spotted Steve!"
/chat "Steve equipped his stone sword."

Steve.carry(attack, 3)
Zombie(20, 3)

Steve.mine(Zombie.hp > 0) {
    /attack Steve Zombie
    /attack Zombie Steve
}

Steve.encounter(Zombie.hp <= 0) {
    /chat "Steve defeated the Zombie!"
    /chat "Steve gained some leather armor."
    Steve.carry(armor, 2)
} otherwise {
    /chat "Steve was defeated by the Zombie!"
}
/eat 5

// === Act 3: Mining ===
/chat ""
/chat "=== Act 3: Mining ==="
/chat "Steve ventures underground to mine for diamonds."
/chat "He upgrades to iron gear before descending."

Steve.carry(attack, 5)
Steve.carry(armor, 3)
/eat 10

Steve.carry(diamonds, 0)
Steve.carry(depth, 0)

Steve.mine(diamonds < 5) {
    Steve.carry(depth, depth + 1)
    Steve.carry(diamonds, diamonds + 1)
    /chat "Mining at depth:"
    /chat depth
    /chat "Diamonds found:"
    /chat diamonds
}

Steve.encounter(diamonds >= 5) {
    /chat "Steve found enough diamonds!"
    /chat "Steve crafts diamond armor and sword."
    Steve.carry(attack, 7)
    Steve.carry(armor, 5)
} otherwise {
    /chat "Steve could not find enough diamonds."
}

/chat "Steve's attack is now:"
/chat attack
/chat "Steve's armor is now:"
/chat armor

// === Act 4: The Nether ===
/chat ""
/chat "=== Act 4: The Nether ==="
/chat "Steve builds a Nether portal and steps through."
/chat "The heat is overwhelming..."
/chat "WARNING: Steve cannot sleep in the Nether!"

Blaze(20, 8)

/chat "A Blaze appears!"
Steve.mine(Blaze.hp > 0) {
    /attack Steve Blaze
    /attack Blaze Steve
}

Steve.encounter(Blaze.hp <= 0) {
    /chat "Steve defeated the Blaze!"
    /chat "Steve collected Blaze Rods."
} otherwise {
    /chat "Steve was defeated by the Blaze!"
}

ZombiePigman(20, 7)

/chat ""
/chat "A Zombie Pigman approaches!"
Steve.mine(ZombiePigman.hp > 0) {
    /attack Steve ZombiePigman
    /attack ZombiePigman Steve
}

Steve.encounter(ZombiePigman.hp <= 0) {
    /chat "Steve defeated the Zombie Pigman!"
    /chat "Steve collected Gold Nuggets."
} otherwise {
    /chat "Steve was defeated by the Zombie Pigman!"
}

/chat ""
/chat "Steve returns from the Nether."
/eat 10
/chat "Steve upgrades to full diamond gear!"
Steve.carry(attack, 9)
Steve.carry(armor, 7)

// === Act 5: The Stronghold ===
/chat ""
/chat "=== Act 5: The Stronghold ==="
/chat "Steve uses the Blaze Rods to craft Eyes of Ender."
/chat "He follows them to find the Stronghold."

Steve.carry(eyes, 12)
Steve.carry(roomsSearched, 0)
Steve.nametag(location, "Unknown")

Steve.mine(roomsSearched < 5) {
    Steve.carry(roomsSearched, roomsSearched + 1)
    /chat "Searching room:"
    /chat roomsSearched
}

/chat "Steve found the portal room!"
Steve.nametag(location, "Stronghold Portal Room")
/chat "Location marked:"
/chat location

// Random Silverfish encounter
/random chance
/chat "Checking for Silverfish..."
Steve.encounter(chance < 4) {
    /chat "Silverfish ambush!"
    Silverfish(8, 2)
    Steve.mine(Silverfish.hp > 0) {
        /attack Steve Silverfish
        /chat "Steve crushed the Silverfish in one hit!"
        /chat "Silverfish HP:"
        /chat Silverfish.hp
    }
    Steve.encounter(Silverfish_hp <= 0) {
        /chat "Steve crushed the Silverfish!"
    } otherwise {
        /chat "The Silverfish escaped!"
    }
} otherwise {
    /chat "No Silverfish this time. Steve is safe."
}

/chat ""
/chat "Steve activates the End Portal."
/chat "Eyes of Ender remaining:"
/chat eyes
/chat "Steve leaps into the portal..."

// === Act 6: The End ===
/chat ""
/chat "=== Act 6: The End ==="
/chat "Steve emerges in The End."
/chat "The Ender Dragon circles overhead..."
/chat "This is it. The final battle!"
/chat ""

EnderDragon(200, 10)
Steve.carry(destroyedCrystals, 0)

// Destroy End Crystals first
/chat "Steve must destroy the End Crystals!"
Steve.loot(crystal = 1, crystal <= 4, crystal++) {
    Steve.carry(destroyedCrystals, destroyedCrystals + 1)
    /chat "End Crystal destroyed:"
    /chat destroyedCrystals
    /eat 3
}

/chat "All End Crystals destroyed!"
/chat "The Ender Dragon is vulnerable!"
/chat ""

// Final battle
/chat "=== FINAL BATTLE ==="
Steve.mine(EnderDragon.hp > 0) {
    /eat 4
    /attack Steve EnderDragon
    /attack EnderDragon Steve
}

Steve.encounter(EnderDragon.hp <= 0) {
    /chat ""
    /chat "=========================================="
    /chat "THE ENDER DRAGON HAS BEEN DEFEATED!"
    /chat "Steve has beaten Minecraft!"
    /chat "=========================================="
    /chat ""
    /chat "Steve collected the Dragon Egg."
    /chat "A portal home appeared."
    /chat "THE END."
} otherwise {
    /chat "Steve was defeated by the Ender Dragon!"
    /chat "But Steve never gives up..."
}