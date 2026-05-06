Steve(20, 10, 5)

/mine count {
    Steve.carry(total, 0)
    Steve.loot(i = 1, i <= count, i++) {
        Steve.carry(total, total + 1)
    }
    /return total
}

/random itemCount
Steve.carry(result, /mine itemCount)
/chat "Steve mined this many items:"
/chat result
/chat "Direct chat result:"
/chat /mine itemCount